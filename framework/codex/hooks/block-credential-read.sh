#!/bin/bash
# block-credential-read.sh — PreToolUse hook (Codex CLI, Bash-only).
#
# Codex CLI's PreToolUse hook only fires for the Bash tool — Read / Write /
# Edit / web fetch / MCP tool calls do not trigger it (documented limitation).
# So this hook can only block credential reads that happen through the shell
# (e.g. `cat master.key`, `grep token settings.yaml`).
#
# The kit also ships `.codexignore` with the same patterns, but Codex
# currently ignores that file (openai/codex#6530); this hook is the best
# enforcement available today.

INPUT=$(cat)

SCRIPT_PATH="$(python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$0" 2>/dev/null || echo "$0")"
PATTERNS_FILE="$(dirname "$SCRIPT_PATH")/../../credential-patterns.txt"

if [ ! -f "$PATTERNS_FILE" ]; then
  exit 0   # fail open — without patterns we cannot decide.
fi

DECISION="$(INPUT="$INPUT" PATTERNS_FILE="$PATTERNS_FILE" python3 <<'PY'
import json, os, re, sys

raw = os.environ.get("INPUT", "")
try:
    data = json.loads(raw)
except Exception:
    print("OK")
    sys.exit(0)

# Codex PreToolUse fires only for Bash, but be defensive.
if data.get("tool_name") != "Bash":
    print("OK")
    sys.exit(0)

cmd = (data.get("tool_input") or {}).get("command", "") or ""

patterns = []
with open(os.environ["PATTERNS_FILE"]) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)

# Tools that legitimately operate ON credential files without dumping their
# contents: the workato CLI (no print-file mode), git for staging only, and the
# kit helper script. This is an accident-guard, not a sandbox against a
# deliberately hostile command. We close the cheap holes: the safe program is
# the REAL program (the script behind python, not a -c payload), and git is
# safe only for non-reading subcommands with no global options (so git -c,
# git show, git diff, git cat-file are NOT allowlisted).
SAFE_PROGS = {"workato", "workato-api.py"}
SAFE_GIT_SUBCMDS = {"add", "rm", "mv", "status", "commit", "stash",
                    "restore", "checkout", "switch", "reset"}

def pat_re(p):
    body = re.escape(p).replace(r"\*", r"\S*")
    return re.compile(rf"(?<!\w){body}(?!\w)")

def git_segment_safe(rest):
    for t in rest:
        if t.startswith("-"):
            return False
        return t in SAFE_GIT_SUBCMDS
    return False

def segment_safe(seg):
    toks = seg.split()
    i = 0
    while i < len(toks) and re.match(r"^\w+=", toks[i]):
        i += 1
    if i >= len(toks):
        return False
    prog = os.path.basename(toks[i])
    rest = toks[i + 1:]
    if re.match(r"^python[0-9.]*$", prog) and rest:
        prog = os.path.basename(rest[0])
        rest = rest[1:]
    if prog == "git":
        return git_segment_safe(rest)
    return prog in SAFE_PROGS

# Block only when credential file contents would be dumped to the agent.
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
    if segment_safe(seg):
        continue
    print(f"DENY:{hit}")
    sys.exit(0)

print("OK")
PY
)"

case "$DECISION" in
  DENY:*)
    PAT="${DECISION#DENY:}"
    echo "Blocked by workato-dev-kit credential guard: bash command references $PAT" >&2
    echo "  Credential files (see kit/framework/credential-patterns.txt) must not be" >&2
    echo "  read through the shell. Edit that file or temporarily remove this hook" >&2
    echo "  from .codex/hooks.json if this is intentional." >&2
    exit 2
    ;;
  *)
    exit 0
    ;;
esac
