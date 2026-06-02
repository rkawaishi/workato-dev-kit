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
# contents (workato CLI encrypts/edits/runs; git stages/commits). Never block
# these. The kit helper script is matched by substring (its program is
# `python3`, which we cannot allowlist wholesale).
SAFE_PROGS = {"workato", "git"}
SAFE_MARKERS = ("workato-api.py",)

def pat_re(p):
    body = re.escape(p).replace(r"\*", r"\S*")
    return re.compile(rf"(?<!\w){body}(?!\w)")

def segment_program(seg):
    toks = seg.split()
    i = 0
    while i < len(toks) and re.match(r"^\w+=", toks[i]):
        i += 1
    return os.path.basename(toks[i]) if i < len(toks) else ""

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
    if any(m in seg for m in SAFE_MARKERS):
        continue
    if segment_program(seg) in SAFE_PROGS:
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
