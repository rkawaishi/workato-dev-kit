#!/bin/bash
# Pre-push validation hook
# Validates JSON syntax and checks for common issues before workato push

INPUT=$(cat)

# Fast exit: skip if not a workato push command (avoids python3 overhead)
case "$INPUT" in
  *"workato push"*) ;;
  *) exit 0 ;;
esac

CWD=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('cwd',''))")

# Detect project directory
PROJECT_DIR=""
if [ -f "$CWD/.workatoenv" ]; then
  PROJECT_DIR="$CWD"
else
  PROJECT_DIR=$(find "$CWD/projects" -name ".workatoenv" -maxdepth 2 -exec dirname {} \; 2>/dev/null | head -1)
fi

if [ -z "$PROJECT_DIR" ] || [ ! -d "$PROJECT_DIR" ]; then
  exit 0  # Can't determine project, allow push
fi

ERRORS=()
WARNINGS=()

# 1. Validate JSON syntax (blocking)
while IFS= read -r -d '' file; do
  if ! VALIDATE_FILE="$file" python3 -c "import json,os; json.load(open(os.environ['VALIDATE_FILE']))" 2>/dev/null; then
    ERRORS+=("JSON syntax error: $(basename "$file")")
  fi
done < <(find "$PROJECT_DIR" -type f \( -name "*.recipe.json" -o -name "*.lcap_app.json" -o -name "*.lcap_page.json" -o -name "*.workato_db_table.json" -o -name "*.agentic_skill.json" -o -name "*.agentic_genie.json" -o -name "*.mcp_server.json" -o -name "*.connection.json" \) -print0 2>/dev/null)

# 2. Check for missing extended_output_schema on triggers (warning only)
while IFS= read -r -d '' file; do
  HAS_EOS=$(VALIDATE_FILE="$file" python3 -c "
import json,os
with open(os.environ['VALIDATE_FILE']) as f:
    d = json.load(f)
print('yes' if d.get('code',{}).get('extended_output_schema') else 'no')
" 2>/dev/null)
  if [ "$HAS_EOS" = "no" ]; then
    WARNINGS+=("Missing extended_output_schema on trigger: $(basename "$file")")
  fi
done < <(find "$PROJECT_DIR" -type f -name "*.recipe.json" -print0 2>/dev/null)

# 3. Check for dropdown with null dataSource in pages (warning only)
while IFS= read -r -d '' file; do
  NULL_DS=$(VALIDATE_FILE="$file" python3 -c "
import json,os
def find_dropdowns(obj):
    if isinstance(obj, dict):
        if obj.get('type') == 'dropdown' and obj.get('dataSource') is None:
            print(obj.get('name', 'unknown'))
        for v in obj.values():
            find_dropdowns(v)
    elif isinstance(obj, list):
        for item in obj:
            find_dropdowns(item)
with open(os.environ['VALIDATE_FILE']) as f:
    find_dropdowns(json.load(f))
" 2>/dev/null)
  if [ -n "$NULL_DS" ]; then
    while IFS= read -r name; do
      WARNINGS+=("Dropdown \"$name\" has null dataSource (value won't be saved): $(basename "$file")")
    done <<< "$NULL_DS"
  fi
done < <(find "$PROJECT_DIR" -type f -name "*.lcap_page.json" -print0 2>/dev/null)

# Show warnings (non-blocking)
if [ ${#WARNINGS[@]} -gt 0 ]; then
  echo "" >&2
  echo "=== Pre-push warnings ===" >&2
  for warn in "${WARNINGS[@]}"; do
    echo "  ⚠️  $warn" >&2
  done
fi

# Block on errors
if [ ${#ERRORS[@]} -gt 0 ]; then
  echo "" >&2
  echo "=== Pre-push validation FAILED ===" >&2
  for err in "${ERRORS[@]}"; do
    echo "  ❌ $err" >&2
  done
  echo "" >&2
  echo "Fix errors above before pushing." >&2
  exit 2
fi

exit 0
