#!/bin/bash
# block-credential-read.sh — PreToolUse hook (Claude Code).
#
# Blocks every tool call that would read or shell-access a credential file
# (patterns in framework/credential-patterns.txt). Covers Read / Edit / Write /
# NotebookEdit / Grep / Glob via tool_input paths, and Bash via command-string
# scanning.
#
# The Bash layer uses a surfacing model: it blocks only commands that would
# emit a credential file's CONTENT into the agent context, not every command
# that merely names one. See framework/credential-patterns.txt for the model.
#
# Defense-in-depth: the .claude/settings.json permissions.deny list also
# blocks these tools, but that list has known enforcement bugs in some Claude
# Code versions. This hook is the reliable enforcement layer.
#
# The embedded Python decides AND emits the user-facing message itself, then
# exits 2 (block) or 0 (allow). The wrapper deliberately does NOT capture the
# output via $(...): a quoted heredoc inside command substitution makes bash
# scan the body for quote/paren balance, so a stray ' " or ( in a comment
# breaks the whole script. Running the heredoc directly avoids that entirely.

INPUT=$(cat)

# Resolve framework/credential-patterns.txt relative to this script — works
# even when invoked through the .claude/hooks/ symlink (realpath strips it).
SCRIPT_PATH="$(python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$0" 2>/dev/null || echo "$0")"
PATTERNS_FILE="$(dirname "$SCRIPT_PATH")/../../credential-patterns.txt"

if [ ! -f "$PATTERNS_FILE" ]; then
  # Fail open — without patterns we cannot decide, so allow.
  exit 0
fi

INPUT="$INPUT" PATTERNS_FILE="$PATTERNS_FILE" python3 <<'PY'
import fnmatch, json, os, re, sys

def deny(reason):
    sys.stderr.write(f"Blocked by workato-dev-kit credential guard: {reason}\n")
    sys.stderr.write("  Credential files (see kit/framework/credential-patterns.txt) must not be\n")
    sys.stderr.write("  read by the agent. If this is intentional, edit that file or temporarily\n")
    sys.stderr.write("  remove this hook from .claude/settings.json.\n")
    sys.exit(2)

raw = os.environ.get("INPUT", "")
try:
    data = json.loads(raw)
except Exception:
    sys.exit(0)  # fail open on malformed input

patterns = []
with open(os.environ["PATTERNS_FILE"]) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)

def path_hit(p):
    """Return the matching pattern, or None. Checks the basename and each
    path segment so .workatoignore-style globs apply at any depth."""
    parts = p.replace("\\", "/").split("/")
    candidates = [p, parts[-1]] + parts
    for pat in patterns:
        for cand in candidates:
            if cand and fnmatch.fnmatchcase(cand, pat):
                return pat
    return None

def pat_to_bash_re(p):
    """Glob to regex that matches the pattern as a whole token inside a shell
    command (preceded and followed by non-word characters or boundaries)."""
    body = re.escape(p).replace(r"\*", r"\S*")
    return re.compile(rf"(?<!\w){body}(?!\w)")

# Surfacing model: a Bash segment is blocked only when it would emit a
# credential file's CONTENT to stdout/stderr — i.e. into the agent/LLM context.
# Passing a credential to a program as an argument or input (workato exec,
# git-staging, cp, a deploy script, curl --key) is allowed: the bytes never
# reach the agent, so it cannot reuse them at a lower layer.
#
# This is an accident / bypass guard, NOT a sandbox. Out of scope: deliberate
# multi-step evasion (copy to a non-credential name, then read it), shell
# function redefinition, connector code that prints a secret, and network
# exfiltration (feeding a credential to a program is explicitly allowed).
SAFE_GIT_SUBCMDS = {"add", "rm", "mv", "status", "commit", "stash",
                    "restore", "checkout", "switch", "reset"}

# Programs that read a named FILE argument (or stdin) and print its content to
# stdout — so a credential appearing anywhere in the segment surfaces it.
EMITTERS = {
    "cat", "tac", "nl", "head", "tail", "less", "more", "bat", "view",
    "strings", "xxd", "od", "hexdump", "base64", "base32",
    "grep", "egrep", "fgrep", "rg", "ag", "ack",
    "sed", "awk", "gawk", "cut", "sort", "uniq", "column", "jq", "yq",
    "paste", "fold", "rev", "diff", "comm", "dd",
    "iconv", "pr", "expand", "unexpand", "fmt",
}
# Programs that echo STDIN to stdout but do NOT read a named file argument, so
# they surface a credential only when it is the stdin redirect source
# (`tr ... < cred`, `tee f < cred`) — not when a credential is a positional or
# output argument (`tr a b cred`, `tee cred`, which read/​write nothing of it).
STDIN_ECHOERS = {"tr", "tee"}
# Interpreters that surface content only when given inline code (-c / -e) that
# reads the credential. Running a *script* file with a credential argument is a
# consumer, not an emitter.
INTERPRETERS = {"python", "python3", "ruby", "node", "nodejs", "perl", "php"}
# An interpreter that reads its SCRIPT from stdin (`python -`), a heredoc
# (`python <<EOF`), or an input redirect (`python < file`) can print a
# credential named anywhere in the command — but the name lands in a
# program-less split segment, so this is caught at the whole-command level.
INTERP_STDIN_RE = re.compile(
    r"(?<!\w)(?:python3?|ruby|node|nodejs|perl|php)\b[^|;&\n]*?(?:\s-(?=\s|$)|<)"
)
# Command-runner prefixes that do not themselves read files; unwrap to find the
# real program. NOTE: value-taking wrapper flags (e.g. `nice -n 5`) are not
# parsed, so a contrived `nice -n 5 cat secret` may slip — acceptable for an
# accident guard (the path-based Read/Grep/Glob hooks are the primary defense).
RUNNERS = {"env", "command", "exec", "nice", "time", "nohup", "stdbuf"}

def git_segment_safe(rest):
    """rest = tokens after git. Safe only when the first token is a non-reading
    subcommand, there are no global options before it (a global option like
    -c alias or --no-pager can turn git into an arbitrary reader), and no flag
    that prints file contents to stdout follows: -p/--patch (hunks) and
    -v/--verbose (e.g. `git status -v` emits the staged diff). Bundled short
    flags such as -vp are caught too."""
    if not rest or rest[0].startswith("-"):
        return False
    if rest[0] not in SAFE_GIT_SUBCMDS:
        return False
    for t in rest[1:]:
        if t == "--":
            continue  # pathspec separator, not an option
        if t.startswith("--"):
            # git accepts any unambiguous prefix, so reject every abbreviation
            # of --patch / --verbose (--ver, --patc, …), both of which print
            # file contents to stdout.
            stem = t[2:].split("=", 1)[0]
            if stem and ("verbose".startswith(stem) or "patch".startswith(stem)):
                return False
        elif t.startswith("-") and len(t) > 1:
            if "p" in t[1:] or "v" in t[1:]:  # patch / verbose short flag (incl. -vp)
                return False
    return True

def resolve_prog_index(toks):
    """Index of the real program token after skipping VAR=value env assignments
    and unwrapping `bundle exec` / RUNNER prefixes. Returns len(toks) if no
    program token remains (e.g. a bare redirect)."""
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
    """True if a single shell token names a credential pattern."""
    return any(pat_to_bash_re(p).search(t) for p in patterns)

def _reads_cred_via_stdin(args):
    """True if an input redirect feeds a credential as stdin: `< cred`, `<cred`,
    or an fd-prefixed form like `0< cred` / `0<cred`."""
    for i, t in enumerate(args):
        if re.fullmatch(r"\d*<", t) and i + 1 < len(args) and _cred_token(args[i + 1]):
            return True
        m = re.match(r"^\d*<(.+)$", t)
        if m and _cred_token(m.group(1)):
            return True
    return False

def surfaces(seg):
    """True if this segment would emit a credential's CONTENT to stdout/stderr.
    The segment is already known to reference a credential pattern."""
    stripped = seg.strip()
    # Bare read-redirect with no consuming program: `$(< master.key)` splits to
    # a `< master.key` segment; bash reads the file straight into the
    # substitution (→ stdout → agent).
    if re.match(r"^<\s*\S", stripped):
        return True
    toks = seg.split()
    pi = resolve_prog_index(toks)
    if pi >= len(toks):
        return False
    prog = os.path.basename(toks[pi])
    args = toks[pi + 1:]
    # git: defer to the vetted oracle — "not git-safe" means it would print
    # file content (show <rev>:<path>, diff, log -p, -c alias=!cat, --no-index).
    if prog == "git":
        return not git_segment_safe(args)
    if prog in EMITTERS:
        return True
    if prog in STDIN_ECHOERS:
        return _reads_cred_via_stdin(args)
    if prog in INTERPRETERS:
        for a in args:
            if a == "-c" or a == "-e" or a.startswith("-c") or a.startswith("-e"):
                return True  # inline code in a segment that names a credential
        # Credential used AS the interpreter's script (first positional), e.g.
        # `python3 master.key` — parse errors echo its lines to stderr. `-m`
        # runs a module, so any later credential is a data arg, not the script.
        # Only the first positional is the script; otherwise fall through to the
        # remaining checks (e.g. the `sdk decrypt` helper run via python3).
        for a in args:
            if a == "-m":
                break
            if a.startswith("-"):
                continue
            if _cred_token(a):
                return True
            break  # first positional is not a credential; keep checking below
    if prog == "openssl":
        for i, a in enumerate(args):
            if a == "-in" and i + 1 < len(args) and _cred_token(args[i + 1]):
                return True  # only the `-in` operand is read; `-out cred` writes
    if prog == "gpg" and any(a in ("-d", "--decrypt") for a in args):
        return True
    # Generic decrypt subcommand: the kit helper `sdk decrypt`, gpg-style, etc.
    if "decrypt" in args:
        return True
    return False

def bash_hit(cmd):
    """Return the first credential pattern whose segment would SURFACE its
    content, else None. Default-allow: naming a credential is fine unless the
    segment emits its content into the agent's tool output."""
    # Whole-command guard: an interpreter fed its script via stdin/heredoc/`<`
    # can print a credential named anywhere in the command, but the name lands
    # in a program-less split segment that surfaces() can't attribute to it.
    if INTERP_STDIN_RE.search(cmd):
        for pat in patterns:
            if pat_to_bash_re(pat).search(cmd):
                return pat
    sep = re.compile("|".join([r"\|\|", r"&&", r"[|;&\n]", r"\$\(", r"\)", re.escape(chr(96))]))
    for seg in sep.split(cmd):
        if not seg.strip():
            continue
        hit = None
        for pat in patterns:
            if pat_to_bash_re(pat).search(seg):
                hit = pat
                break
        if not hit:
            continue
        if surfaces(seg):
            return hit
    return None

def _decide():
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}

    paths = []
    if tool in ("Read", "Edit", "Write"):
        fp = ti.get("file_path")
        if fp:
            paths.append(fp)
    elif tool == "NotebookEdit":
        np = ti.get("notebook_path")
        if np:
            paths.append(np)
    elif tool in ("Grep", "Glob"):
        # Direct path match (e.g. Grep on master.key) — block immediately.
        pp = ti.get("path") or "."
        direct = path_hit(pp)
        if direct:
            deny(f"{direct}: {pp}")
        # Reachability check: if Grep/Glob points at a directory that contains
        # any credential file, its results would expose it. Walk the tree and
        # deny if a credential basename is found. Bounded by skipping known
        # heavy dirs so the hook stays interactive.
        try:
            target = pp if os.path.isabs(pp) else os.path.abspath(pp)
            if os.path.isdir(target):
                SKIP_DIRS = {".git", "node_modules", ".venv", "venv",
                             "dist", "build", "__pycache__", ".cache"}
                for root, dirs, files in os.walk(target, followlinks=False):
                    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                    for f in files:
                        for pat in patterns:
                            if fnmatch.fnmatchcase(f, pat):
                                rel = os.path.join(root, f)
                                deny(f"{pat}: {tool} on {pp} would expose {rel}")
        except SystemExit:
            raise
        except Exception:
            pass  # fail open on traversal errors; Read/Bash layers still apply
        sys.exit(0)
    elif tool == "Bash":
        hit = bash_hit(ti.get("command", "") or "")
        if hit:
            deny(f"{hit}: command would surface credential content to the agent")
        sys.exit(0)

    for p in paths:
        hit = path_hit(p)
        if hit:
            deny(f"{hit}: {p}")
    sys.exit(0)

# Run the decision. Malformed input and a missing patterns file already failed
# open earlier; but if OUR classification raises, fail CLOSED (deny) instead of
# letting the bash wrapper's non-2 fail-open silently allow a credential read.
try:
    _decide()
except SystemExit:
    raise  # deny()'s exit(2) and the normal exit(0) pass through unchanged
except Exception:
    sys.stderr.write("Blocked by workato-dev-kit credential guard: internal error during credential check (failing closed)\n")
    sys.exit(2)
PY
rc=$?
# exit 2 blocks. The embedded Python fails CLOSED (exits 2) if its own
# classification raises, so the only remaining fail-open here is the case where
# Python cannot start at all (missing interpreter) — which would brick every
# tool call if we failed closed, so we allow it.
[ "$rc" -eq 2 ] && exit 2
exit 0
