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

def bash_hit(cmd):
    for pat in patterns:
        if pat_to_bash_re(pat).search(cmd):
            return pat
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
