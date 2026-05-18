#!/usr/bin/env bash
# ensure-workatoignore.sh — give a project a .workatoignore matching the kit's
# base template (templates/workatoignore.template).
#
# Usage: bash scripts/ensure-workatoignore.sh <project-dir>
#
# Idempotent and non-destructive — it never removes or reorders existing lines:
#   - No .workatoignore       → created from the template.
#   - .workatoignore present  → missing CORE entries are appended.
#   - The ">>> opt-out <<<" custom-connector block is appended ONCE, only if
#     the file has never carried it. Once the block markers are present the
#     block is left untouched, so a project that deletes the connector lines
#     to manage a connector as code keeps that opt-out across future runs.
set -euo pipefail

PROJ="${1:-}"
if [ -z "$PROJ" ]; then
  echo "usage: ensure-workatoignore.sh <project-dir>" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TPL="$SCRIPT_DIR/../templates/workatoignore.template"
DST="$PROJ/.workatoignore"

if [ ! -f "$TPL" ]; then
  echo "ensure-workatoignore: template not found: $TPL" >&2
  exit 1
fi
if [ ! -d "$PROJ" ]; then
  echo "ensure-workatoignore: project directory not found: $PROJ" >&2
  exit 1
fi

if [ ! -f "$DST" ]; then
  cp "$TPL" "$DST"
  echo "created $DST"
  exit 0
fi

# Make sure the file ends with a newline — otherwise the first appended
# entry would concatenate onto the last existing line (specs/ + DESIGN.md
# -> specs/DESIGN.md). Command substitution strips a trailing newline, so a
# non-empty result means the last byte was not a newline.
if [ -s "$DST" ] && [ -n "$(tail -c1 "$DST")" ]; then
  printf '\n' >> "$DST"
fi

# Append missing CORE entries (lines outside the opt-out block).
added=0
skip=0
while IFS= read -r line; do
  case "$line" in
    *'>>> opt-out'*) skip=1; continue ;;
    *'<<< opt-out'*) skip=0; continue ;;
  esac
  if [ "$skip" = "1" ]; then continue; fi
  case "$line" in ''|\#*) continue ;; esac
  if ! grep -qxF "$line" "$DST"; then
    printf '%s\n' "$line" >> "$DST"
    added=$((added + 1))
  fi
done < "$TPL"

# Append the opt-out block once, only if this file has never carried it.
if grep -qF '>>> opt-out' "$DST"; then
  echo "topped up $DST (+${added} core entries; opt-out block left as-is)"
else
  printf '\n' >> "$DST"
  sed -n '/>>> opt-out/,/<<< opt-out/p' "$TPL" >> "$DST"
  echo "topped up $DST (+${added} core entries; connector opt-out block added)"
fi
