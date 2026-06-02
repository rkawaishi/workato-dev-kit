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
    sys.stderr.write(f"Blocked by workato-dev-kit credential guard: bash command references {pat}\n")
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

# Only the workato CLI (no print-file mode) and git used for staging are
# allowlisted alongside a credential filename. The kit helper script is NOT
# allowlisted: its normal commands never name a credential file, while its
# sdk-decrypt subcommand prints plaintext to stdout and must stay blocked.
# This is an accident-guard, not a sandbox: shell-function redefinition,
# connector code that prints secrets, and dumps that do not name the file
# are out of scope. git is safe only for non-reading subcommands with no
# global options and no -p / --patch flag.
SAFE_PROGS = {"workato"}
SAFE_GIT_SUBCMDS = {"add", "rm", "mv", "status", "commit", "stash",
                    "restore", "checkout", "switch", "reset"}

def pat_re(p):
    body = re.escape(p).replace(r"\*", r"\S*")
    return re.compile(rf"(?<!\w){body}(?!\w)")

def git_segment_safe(rest):
    if not rest or rest[0].startswith("-"):
        return False
    if rest[0] not in SAFE_GIT_SUBCMDS:
        return False
    for t in rest[1:]:
        if t in ("-p", "--patch") or t.startswith("--patch"):
            return False
    return True

def segment_safe(seg):
    toks = seg.split()
    i = 0
    while i < len(toks) and re.match(r"^\w+=", toks[i]):
        i += 1
    if i >= len(toks):
        return False
    prog = os.path.basename(toks[i])
    if prog == "git":
        return git_segment_safe(toks[i + 1:])
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
    deny(hit)

sys.exit(0)
PY
rc=$?
# Only an explicit deny (exit 2) blocks; anything else falls through to allow.
[ "$rc" -eq 2 ] && exit 2
exit 0
