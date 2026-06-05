#!/bin/bash
# block-credential-read.sh — PreToolUse hook (Claude Code).
#
# Blocks every tool call that would read or shell-access a credential file
# (patterns in framework/credential-patterns.txt). Covers Read / Edit / Write /
# NotebookEdit / Grep / Glob via tool_input paths, and Bash via command-string
# scanning.
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

# The only tools allowlisted to appear alongside a credential filename are the
# workato CLI (encrypt/edit/run; it has no print-file mode) and git used for
# staging only (add/rm/mv/commit/...). Everything else that names a credential
# is blocked. That is safe because the kit helper script's normal commands
# (profile/pull/diff/deploy) never name a credential file; only its sdk-decrypt
# (which prints plaintext to stdout) and sdk-edit subcommands do, and decrypt is
# exactly what we want blocked. The workato gem covers the edit case.
#
# NOTE: this is an accident-guard, not a sandbox against a deliberately hostile
# command. Out of scope: redefining a shell function, connector code that
# prints a secret, and commands that dump contents WITHOUT naming the file
# (a git patch view of a stash) -- the hook only fires when a credential
# pattern literally appears in the command.
SAFE_PROGS = {"workato"}
# git subcommands that never print file contents to stdout in their plain form.
# The -p / --patch variants DO print hunks, so they are rejected below.
SAFE_GIT_SUBCMDS = {"add", "rm", "mv", "status", "commit", "stash",
                    "restore", "checkout", "switch", "reset"}

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

def segment_safe(seg):
    """True if this segment's program is a known-safe tool. Skips leading
    VAR=value env assignments and unwraps `bundle exec` / bare `exec` runner
    prefixes so the wrapped program is what gets matched. The kit docs MANDATE
    `bundle exec workato` (the SDK gem's `workato` collides with the Platform
    CLI), so without this the allowlisted `workato edit/exec` is unreachable.
    Unwrapping is safe: the real program is still re-checked against the
    allowlist, so `bundle exec cat master.key` stays blocked."""
    toks = seg.split()
    i = 0
    while i < len(toks) and re.match(r"^\w+=", toks[i]):
        i += 1
    # Unwrap runner prefixes that don't themselves read files.
    while i < len(toks):
        base = os.path.basename(toks[i])
        if base == "bundle" and i + 1 < len(toks) and toks[i + 1] == "exec":
            i += 2
            while i < len(toks) and toks[i].startswith("-"):
                i += 1  # skip bundler options / `--` separator
        elif base == "exec":
            i += 1
        else:
            break
    if i >= len(toks):
        return False
    prog = os.path.basename(toks[i])
    if prog == "git":
        return git_segment_safe(toks[i + 1:])
    return prog in SAFE_PROGS

def bash_hit(cmd):
    """Block only when credential file contents would be dumped into the agent
    tool output. Split on shell separators and deny a segment that references a
    credential pattern unless its program is a known-safe tool."""
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
        if segment_safe(seg):
            continue
        return hit
    return None

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
    # Reachability check: if Grep/Glob points at a directory that contains any
    # credential file, its results would expose it. Walk the tree and deny if a
    # credential basename is found. Bounded by skipping known heavy dirs so the
    # hook stays interactive.
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
        pass  # fail open on traversal errors; Read/Bash hook layers still apply
    sys.exit(0)
elif tool == "Bash":
    hit = bash_hit(ti.get("command", "") or "")
    if hit:
        deny(f"{hit}: bash command references credential file")
    sys.exit(0)

for p in paths:
    hit = path_hit(p)
    if hit:
        deny(f"{hit}: {p}")

sys.exit(0)
PY
rc=$?
# Only an explicit deny (exit 2) blocks. Any other status — including an
# unexpected Python error — falls through to allow (fail open).
[ "$rc" -eq 2 ] && exit 2
exit 0
