#!/bin/bash
# Pre-push validation hook
# Validates JSON syntax and checks for common issues before workato push

INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

# Detect project directory from the push command or cwd
# workato push runs from the project dir or uses "workato projects use" first
PROJECT_DIR=""
if [[ "$COMMAND" == *"cd "* ]]; then
  PROJECT_DIR=$(echo "$COMMAND" | grep -oP 'cd "([^"]+)"' | sed 's/cd "//;s/"//')
fi
if [ -z "$PROJECT_DIR" ]; then
  # Find .workatoenv in cwd or parent
  if [ -f "$CWD/.workatoenv" ]; then
    PROJECT_DIR="$CWD"
  else
    # Search in projects/ subdirectories
    PROJECT_DIR=$(find "$CWD/projects" -name ".workatoenv" -maxdepth 2 -exec dirname {} \; 2>/dev/null | head -1)
  fi
fi

if [ -z "$PROJECT_DIR" ] || [ ! -d "$PROJECT_DIR" ]; then
  exit 0  # Can't determine project, allow push
fi

ERRORS=()

# 1. Validate JSON syntax
while IFS= read -r -d '' file; do
  if ! jq empty "$file" 2>/dev/null; then
    ERRORS+=("JSON syntax error: $(basename "$file")")
  fi
done < <(find "$PROJECT_DIR" -type f \( -name "*.recipe.json" -o -name "*.lcap_app.json" -o -name "*.lcap_page.json" -o -name "*.workato_db_table.json" -o -name "*.agentic_skill.json" -o -name "*.agentic_genie.json" -o -name "*.mcp_server.json" -o -name "*.connection.json" \) -print0 2>/dev/null)

# 2. Check for missing extended_output_schema on triggers
while IFS= read -r -d '' file; do
  # Check if trigger (number: 0) has extended_output_schema
  TRIGGER_HAS_EOS=$(jq '.code.extended_output_schema // empty' "$file" 2>/dev/null)
  if [ -z "$TRIGGER_HAS_EOS" ]; then
    ERRORS+=("Missing extended_output_schema on trigger: $(basename "$file")")
  fi
done < <(find "$PROJECT_DIR" -type f -name "*.recipe.json" -print0 2>/dev/null)

# 3. Check for dropdown with null dataSource in pages
while IFS= read -r -d '' file; do
  NULL_DS=$(jq -r '.. | objects | select(.type == "dropdown" and .dataSource == null) | .name' "$file" 2>/dev/null)
  if [ -n "$NULL_DS" ]; then
    while IFS= read -r name; do
      ERRORS+=("Dropdown \"$name\" has null dataSource (value won't be saved): $(basename "$file")")
    done <<< "$NULL_DS"
  fi
done < <(find "$PROJECT_DIR" -type f -name "*.lcap_page.json" -print0 2>/dev/null)

if [ ${#ERRORS[@]} -gt 0 ]; then
  echo "" >&2
  echo "=== Pre-push validation failed ===" >&2
  for err in "${ERRORS[@]}"; do
    echo "  - $err" >&2
  done
  echo "" >&2
  echo "Fix errors above before pushing." >&2
  exit 2
fi

exit 0
