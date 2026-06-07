#!/bin/bash
# block-credential-read.sh — PreToolUse hook (Codex CLI, Bash-only).
#
# Codex CLI's PreToolUse hook only fires for the Bash tool — Read / Write /
# Edit / web fetch / MCP tool calls do not trigger it (documented limitation).
# So this hook can only block credential reads that happen through the shell
# (e.g. `cat master.key`, `grep token settings.yaml`).
#
# The Bash scan uses a surfacing model: it blocks only commands that would emit
# a credential file's CONTENT into the agent context, not every command that
# merely names one.
#
# The kit also ships `.codexignore` with the same patterns, but Codex
# currently ignores that file (openai/codex#6530); this hook is the best
# enforcement available today.
#
# The embedded Python decides AND emits the message itself, then exits 2
# (block) or 0 (allow). We deliberately do NOT capture via $(...): a quoted
# heredoc inside command substitution makes bash scan the body for quote/paren
# balance, so a stray ' " or ( in a comment breaks the script. Running the
# heredoc directly avoids that.

INPUT=$(cat)

SCRIPT_PATH="$(python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$0" 2>/dev/null || echo "$0")"
PATTERNS_FILE="$(dirname "$SCRIPT_PATH")/../../credential-patterns.txt"

if [ ! -f "$PATTERNS_FILE" ]; then
  exit 0   # fail open — without patterns we cannot decide.
fi

INPUT="$INPUT" PATTERNS_FILE="$PATTERNS_FILE" python3 <<'PY'
import json, os, re, sys

def deny(pat):
    sys.stderr.write(f"Blocked by workato-dev-kit credential guard: bash command would surface {pat} content to the agent\n")
    sys.stderr.write("  Credential files (see kit/framework/credential-patterns.txt) must not be\n")
    sys.stderr.write("  read through the shell. Edit that file or temporarily remove this hook\n")
    sys.stderr.write("  from .codex/hooks.json if this is intentional.\n")
    sys.exit(2)

raw = os.environ.get("INPUT", "")
try:
    data = json.loads(raw)
except Exception:
    sys.exit(0)

# Codex PreToolUse fires only for Bash, but be defensive.
if data.get("tool_name") != "Bash":
    sys.exit(0)

cmd = (data.get("tool_input") or {}).get("command", "") or ""

patterns = []
with open(os.environ["PATTERNS_FILE"]) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)

# Surfacing model: block a Bash command only when it would emit a credential
# file's CONTENT to stdout/stderr (the agent context). Passing a credential to
# a program as an argument/input (workato exec, git-staging, cp, deploy script,
# curl --key) is allowed. Accident/bypass guard, not a sandbox: deliberate
# multi-step evasion, shell-function redefinition, and network exfil are out of
# scope.
SAFE_GIT_SUBCMDS = {"add", "rm", "mv", "status", "commit", "stash",
                    "restore", "checkout", "switch", "reset"}
# Programs that read a named FILE argument (or stdin) and print its content to
# stdout — a credential anywhere in the segment surfaces it.
EMITTERS = {
    "cat", "tac", "nl", "head", "tail", "less", "more", "bat", "view",
    "strings", "xxd", "od", "hexdump", "base64", "base32",
    "grep", "egrep", "fgrep", "rg", "ag", "ack",
    "sed", "awk", "gawk", "cut", "sort", "uniq", "column", "jq", "yq",
    "paste", "fold", "rev", "diff", "comm", "dd",
    "iconv", "pr", "expand", "unexpand", "fmt",
}
# Echo stdin but read no file arg: surface only when the credential is the
# stdin redirect source (`tr ... < cred`, `tee f < cred`), not when it is a
# positional/output arg (`tr a b cred`, `tee cred`).
STDIN_ECHOERS = {"tr", "tee"}
INTERPRETERS = {"python", "python3", "ruby", "node", "nodejs", "perl", "php"}
RUNNERS = {"env", "command", "exec", "nice", "time", "nohup", "stdbuf"}
# An interpreter reading its SCRIPT from stdin (`python -`), a heredoc, or `<`
# can print a credential named anywhere in the command; the name otherwise
# lands in a program-less split segment. Caught at the whole-command level.
INTERP_STDIN_RE = re.compile(
    r"(?<!\w)(?:python3?|ruby|node|nodejs|perl|php)\b[^|;&\n]*?(?:\s-(?=\s|$)|<)"
)

def pat_re(p):
    body = re.escape(p).replace(r"\*", r"\S*")
    return re.compile(rf"(?<!\w){body}(?!\w)")

def git_segment_safe(rest):
    # Safe only for a non-reading subcommand with no leading global option and
    # no content-printing flag: -p/--patch (hunks) or -v/--verbose (e.g.
    # `git status -v` emits the staged diff). Bundled short flags (-vp) caught.
    if not rest or rest[0].startswith("-"):
        return False
    if rest[0] not in SAFE_GIT_SUBCMDS:
        return False
    for t in rest[1:]:
        if t == "--":
            continue  # pathspec separator, not an option
        if t.startswith("--"):
            # git accepts any unambiguous prefix, so reject every abbreviation
            # of --patch / --verbose (--ver, --patc, …).
            stem = t[2:].split("=", 1)[0]
            if stem and ("verbose".startswith(stem) or "patch".startswith(stem)):
                return False
        elif t.startswith("-") and len(t) > 1:
            if "p" in t[1:] or "v" in t[1:]:
                return False
    return True

def resolve_prog_index(toks):
    i = 0
    while i < len(toks):
        if re.match(r"^\w+=", toks[i]):
            i += 1
            continue
        base = os.path.basename(toks[i])
        if base == "bundle" and i + 1 < len(toks) and toks[i + 1] == "exec":
            i += 2
            while i < len(toks) and toks[i].startswith("-"):
                i += 1
            continue
        if base in RUNNERS:
            i += 1
            while i < len(toks) and toks[i].startswith("-"):
                i += 1
            continue
        break
    return i

def _cred_token(t):
    return any(pat_re(p).search(t) for p in patterns)

def _reads_cred_via_stdin(args):
    # `< cred`, `<cred`, or fd-prefixed `0< cred` / `0<cred`.
    for i, t in enumerate(args):
        if re.fullmatch(r"\d*<", t) and i + 1 < len(args) and _cred_token(args[i + 1]):
            return True
        m = re.match(r"^\d*<(.+)$", t)
        if m and _cred_token(m.group(1)):
            return True
    return False

def surfaces(seg):
    stripped = seg.strip()
    if re.match(r"^<\s*\S", stripped):
        return True
    toks = seg.split()
    pi = resolve_prog_index(toks)
    if pi >= len(toks):
        return False
    prog = os.path.basename(toks[pi])
    args = toks[pi + 1:]
    if prog == "git":
        return not git_segment_safe(args)
    if prog in EMITTERS:
        return True
    if prog in STDIN_ECHOERS:
        return _reads_cred_via_stdin(args)
    if prog in INTERPRETERS:
        for a in args:
            if a == "-c" or a == "-e" or a.startswith("-c") or a.startswith("-e"):
                return True
        # Credential used AS the interpreter's script (first positional), e.g.
        # `python3 master.key` — parse errors echo its lines. `-m` runs a
        # module, so a later credential is a data arg, not the script. Only the
        # first positional is the script; otherwise fall through (e.g. the
        # `sdk decrypt` helper run via python3).
        # Out of scope (deliberate): a value-taking flag before the script, e.g.
        # `python3 -W ignore master.key` (same class as `nice -n 5 cat`).
        for a in args:
            if a == "-m":
                break
            if a.startswith("-"):
                continue
            if _cred_token(a):
                return True
            break
    if prog == "openssl":
        for i, a in enumerate(args):
            if a == "-in" and i + 1 < len(args) and _cred_token(args[i + 1]):
                return True  # only the `-in` operand is read; `-out cred` writes
    if prog == "gpg" and any(a in ("-d", "--decrypt") for a in args):
        return True
    if "decrypt" in args:
        return True
    return False

def _decide():
    # Whole-command guard: an interpreter fed its script via stdin/heredoc/`<`
    # can print a credential named anywhere in the command, but the name lands
    # in a program-less split segment that surfaces() can't attribute to it.
    if INTERP_STDIN_RE.search(cmd):
        for pat in patterns:
            if pat_re(pat).search(cmd):
                deny(pat)

    # Block only when a segment would surface credential content to the agent.
    sep = re.compile("|".join([r"\|\|", r"&&", r"[|;&\n]", r"\$\(", r"\)", re.escape(chr(96))]))
    for seg in sep.split(cmd):
        if not seg.strip():
            continue
        hit = None
        for pat in patterns:
            if pat_re(pat).search(seg):
                hit = pat
                break
        if not hit:
            continue
        if surfaces(seg):
            deny(hit)
    sys.exit(0)

# If OUR classification raises, fail CLOSED (deny) rather than letting the bash
# wrapper's non-2 fail-open silently allow a credential read. Malformed input
# already failed open earlier.
try:
    _decide()
except SystemExit:
    raise
except Exception:
    sys.stderr.write("Blocked by workato-dev-kit credential guard: internal error during credential check (failing closed)\n")
    sys.exit(2)
PY
rc=$?
# exit 2 blocks. The embedded Python fails CLOSED on its own classification
# errors, so the only fail-open left here is Python failing to start at all
# (failing closed there would brick every tool call).
[ "$rc" -eq 2 ] && exit 2
exit 0
