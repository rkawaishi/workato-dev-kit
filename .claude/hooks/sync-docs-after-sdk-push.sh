#!/bin/bash
# PostToolUse hook: after sdk push, remind AI to sync connector docs
#
# Compatible with both Claude Code and Cursor:
#   Claude Code: tool_name="Bash", tool_response={exitCode,stdout,stderr}
#   Cursor:      tool_name="Shell", tool_output="{\"exitCode\":0,...}" (JSON string)
#
# When `sdk push` completes successfully, this hook detects the connector path
# from the command and outputs a message to update connectors/docs/.

INPUT=$(cat)

# Fast exit: skip if not an sdk push command
case "$INPUT" in
  *"sdk push"*) ;;
  *) exit 0 ;;
esac

# Parse tool input and check exit code (handles both Claude Code and Cursor formats)
RESULT=$(echo "$INPUT" | python3 -c "
import sys, json, re

data = json.load(sys.stdin)
command = data.get('tool_input', {}).get('command', '')

# Verify it's an sdk push command
if 'workato-api.py sdk push' not in command:
    sys.exit(0)

# Get exit code: Claude Code uses tool_response (dict), Cursor uses tool_output (JSON string)
exit_code = 1
resp = data.get('tool_response')
if isinstance(resp, dict):
    exit_code = resp.get('exitCode', 1)
else:
    raw = data.get('tool_output', '')
    if isinstance(raw, str) and raw:
        try:
            exit_code = json.loads(raw).get('exitCode', 1)
        except (json.JSONDecodeError, AttributeError):
            pass

if exit_code != 0:
    sys.exit(0)

# Extract connector path from --connector argument
q = chr(39)  # single quote (avoids bash escaping issues)
m = re.search(r'--connector\s+[\"' + q + r'](.*?)[\"' + q + r']', command) or re.search(r'--connector\s+(\S+)', command)
if not m:
    sys.exit(0)

from pathlib import Path
p = Path(m.group(1))
name = p.parent.name if p.name == 'connector.rb' else p.stem
print(name)
" 2>/dev/null)

if [ -z "$RESULT" ]; then
  exit 0
fi

CONNECTOR_NAME="$RESULT"

# Output feedback (stdout is shown to the AI as hook feedback)
echo "sdk push completed. Please update connector docs: read connectors/${CONNECTOR_NAME}/connector.rb and generate/update connectors/docs/${CONNECTOR_NAME}.md following the custom connector doc format defined in the /sync-connectors skill."

exit 0
