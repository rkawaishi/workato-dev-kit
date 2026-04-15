#!/bin/bash
# PostToolUse hook: after sdk push, remind Claude to sync connector docs
#
# When `sdk push` completes successfully, this hook detects the connector path
# from the command and outputs a message for Claude to update connectors/docs/.

INPUT=$(cat)

# Fast exit: skip if not an sdk push command
case "$INPUT" in
  *"sdk push"*) ;;
  *) exit 0 ;;
esac

# Extract the command string
COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)

# Verify it's actually an sdk push command
case "$COMMAND" in
  *"workato-api.py sdk push"*) ;;
  *) exit 0 ;;
esac

# Check exit code (success = 0)
EXIT_CODE=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_response',{}).get('exitCode',1))" 2>/dev/null)
if [ "$EXIT_CODE" != "0" ]; then
  exit 0
fi

# Extract connector path from --connector argument
CONNECTOR_PATH=$(echo "$COMMAND" | python3 -c "
import sys, re
cmd = sys.stdin.read()
m = re.search(r'--connector\s+[\"\\x27](.*?)[\"\\x27]', cmd) or re.search(r'--connector\s+(\S+)', cmd)
print(m.group(1) if m else '')
")

if [ -z "$CONNECTOR_PATH" ]; then
  exit 0
fi

# Derive connector name from path (parent directory of connector.rb)
CONNECTOR_NAME=$(echo "$CONNECTOR_PATH" | python3 -c "
from pathlib import Path
import sys
p = Path(sys.stdin.read().strip())
print(p.parent.name if p.name == 'connector.rb' else p.stem)
")

# Output feedback for Claude (stdout is shown to Claude as hook feedback)
echo "sdk push completed. Please update connector docs: read connectors/${CONNECTOR_NAME}/connector.rb and generate/update connectors/docs/${CONNECTOR_NAME}.md following the custom connector doc format defined in the /sync-connectors skill."

exit 0
