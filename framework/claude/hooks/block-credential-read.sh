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

INPUT=$(cat)

# Resolve framework/credential-patterns.txt relative to this script — works
# even when invoked through the .claude/hooks/ symlink (realpath strips it).
SCRIPT_PATH="$(python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$0" 2>/dev/null || echo "$0")"
PATTERNS_FILE="$(dirname "$SCRIPT_PATH")/../../credential-patterns.txt"

if [ ! -f "$PATTERNS_FILE" ]; then
  # Fail open — without patterns we cannot decide, so allow.
  exit 0
fi

DECISION="$(INPUT="$INPUT" PATTERNS_FILE="$PATTERNS_FILE" python3 <<'PY'
import fnmatch, json, os, re, sys

raw = os.environ.get("INPUT", "")
try:
    data = json.loads(raw)
except Exception:
    print("OK")
    sys.exit(0)

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
    """Glob → regex that matches the pattern as a whole token inside a shell
    command (preceded and followed by non-word characters or boundaries)."""
    body = re.escape(p).replace(r"\*", r"\S*")
    return re.compile(rf"(?<!\w){body}(?!\w)")

# Tools that legitimately operate ON credential files without dumping their
# contents to the agent: the workato CLI (encrypt/edit/run — it has no "print
# file" mode), git for staging only (add/rm/mv/commit/…), and the kit helper
# script. These must never be blocked, or the hook would break normal
# workflows.
#
# NOTE: this is an accident-guard, not a sandbox against a deliberately hostile
# command. A determined caller can still exfiltrate by redefining a shell
# function (`git(){ cat "$1"; }; git add master.key`) or by authoring connector
# code that prints a secret; those are out of scope. We do close the cheap
# holes: the safe program is the REAL program (the script behind `python`, not
# a `-c` payload), and `git` is safe only for non-reading subcommands with no
# global options (so `git -c …`, `git show`, `git diff`, `git cat-file` — all of
# which can print file contents — are NOT allowlisted).
SAFE_PROGS = {"workato", "workato-api.py"}
# git subcommands that never print file contents to stdout.
SAFE_GIT_SUBCMDS = {"add", "rm", "mv", "status", "commit", "stash",
                    "restore", "checkout", "switch", "reset"}

def _git_segment_safe(rest):
    """rest = tokens after `git`. Safe only when the first token is a
    non-reading subcommand and there are no global options before it (a global
    option such as `-c alias…=!cat` or `-C` / `--no-pager` can turn git into an
    arbitrary file reader, so any leading `-…` disqualifies the segment)."""
    for t in rest:
        if t.startswith("-"):
            return False
        return t in SAFE_GIT_SUBCMDS
    return False  # bare `git` with no subcommand

def _segment_safe(seg):
    """True if this segment's program is a known-safe tool. Skips leading
    VAR=value env assignments and resolves `python[3] <script>` to <script>."""
    toks = seg.split()
    i = 0
    while i < len(toks) and re.match(r"^\w+=", toks[i]):
        i += 1
    if i >= len(toks):
        return False
    prog = os.path.basename(toks[i])
    rest = toks[i + 1:]
    if re.match(r"^python[0-9.]*$", prog) and rest:
        prog = os.path.basename(rest[0])   # the interpreted script is the real program
        rest = rest[1:]
    if prog == "git":
        return _git_segment_safe(rest)
    return prog in SAFE_PROGS

def bash_hit(cmd):
    """Block only when a credential file's CONTENTS would be dumped into the
    agent's tool output. We split on shell separators and deny a segment that
    references a credential pattern UNLESS its program is a known-safe tool.
    `cat master.key`, `grep token settings.yaml`, `git show …:settings.yaml`,
    `python3 -c "open('master.key')"` are still blocked; `workato edit
    settings.yaml.enc`, `git add settings.yaml.enc`, and
    `python3 scripts/workato-api.py …` are not."""
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
        if _segment_safe(seg):
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
    # Direct path match (e.g. Grep(path="master.key")) — block immediately.
    pp = ti.get("path") or "."
    direct = path_hit(pp)
    if direct:
        print(f"DENY:{direct}:{pp}")
        sys.exit(0)
    # Reachability check: if Grep/Glob points at a directory that contains
    # any credential file, its results would expose it. Walk the tree and
    # deny if a credential basename is found. Bounded by skipping known
    # heavy dirs (.git, node_modules, …) so the hook stays interactive.
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
                            print(f"DENY:{pat}:{tool} on '{pp}' would expose {rel}")
                            sys.exit(0)
    except Exception:
        pass  # fail open on traversal errors; Read/Bash hook layers still apply
    print("OK")
    sys.exit(0)
elif tool == "Bash":
    hit = bash_hit(ti.get("command", "") or "")
    if hit:
        print(f"DENY:{hit}:bash command references credential file")
        sys.exit(0)
    print("OK")
    sys.exit(0)

for p in paths:
    hit = path_hit(p)
    if hit:
        print(f"DENY:{hit}:{p}")
        sys.exit(0)

print("OK")
PY
)"

case "$DECISION" in
  DENY:*)
    REASON="${DECISION#DENY:}"
    echo "Blocked by workato-dev-kit credential guard: $REASON" >&2
    echo "  Credential files (see kit/framework/credential-patterns.txt) must not be" >&2
    echo "  read by the agent. If this is intentional, edit that file or temporarily" >&2
    echo "  remove this hook from .claude/settings.json." >&2
    exit 2
    ;;
  *)
    exit 0
    ;;
esac
