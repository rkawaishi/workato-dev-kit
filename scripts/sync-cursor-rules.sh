#!/usr/bin/env bash
# sync-cursor-rules.sh
#
# .claude/rules/*.md  → .cursor/rules/*.mdc   へフロントマター変換＋内容コピー
# .claude/skills/*/SKILL.md → .cursor/skills/*/SKILL.md へスキル変換
#
# Usage: bash scripts/sync-cursor-rules.sh
#
# 注意:
#   - .cursor/rules/workato-project.mdc (alwaysApply) はこのスクリプトの対象外
#   - Cursor では symlink が不安定なため、実ファイルをコピーする

set -eo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_RULES="$REPO_ROOT/.claude/rules"
CURSOR_RULES="$REPO_ROOT/.cursor/rules"
CLAUDE_SKILLS="$REPO_ROOT/.claude/skills"
CURSOR_SKILLS="$REPO_ROOT/.cursor/skills"

mkdir -p "$CURSOR_RULES" "$CURSOR_SKILLS"

# --- ルール: description をファイルの最初の # 見出しから自動生成 ---
get_description() {
  awk '
    /^---$/ { fm++; next }
    fm >= 2 && /^# / {
      sub(/^# */, "")
      print
      exit
    }
  ' "$1"
}

# ============================================================
# Part 1: ルール変換 (.claude/rules/*.md → .cursor/rules/*.mdc)
# ============================================================
echo "=== Syncing rules ==="

for claude_file in "$CLAUDE_RULES"/*.md; do
  basename_no_ext="$(basename "$claude_file" .md)"
  cursor_file="$CURSOR_RULES/${basename_no_ext}.mdc"
  desc="$(get_description "$claude_file")"

  if [ -z "$desc" ]; then
    echo "WARN: No heading found in $basename_no_ext, skipping"
    continue
  fi

  # Claude フロントマターから paths を抽出してカンマ区切りに変換
  globs=$(awk '
    /^---$/ { fm++; next }
    fm == 1 && /^  - "/ {
      gsub(/^  - "/, "")
      gsub(/"$/, "")
      paths = (paths == "") ? $0 : paths "," $0
    }
    END { print paths }
  ' "$claude_file")

  # フロントマター以降の本文を抽出
  body=$(awk '
    /^---$/ { fm++; next }
    fm >= 2 { print }
  ' "$claude_file")

  # Cursor 形式で出力
  {
    echo "---"
    echo "description: ${desc}"
    echo "globs: \"${globs}\""
    echo "alwaysApply: false"
    echo "---"
    echo "$body"
  } > "$cursor_file"

  echo "  ✓ $basename_no_ext.mdc"
done

# ============================================================
# Part 2: スキル変換 (.claude/skills/*/SKILL.md → .cursor/skills/*/SKILL.md)
# ============================================================
echo ""
echo "=== Syncing skills ==="

for skill_dir in "$CLAUDE_SKILLS"/*/; do
  skill_file="$skill_dir/SKILL.md"
  [ -f "$skill_file" ] || continue

  skill_name="$(basename "$skill_dir")"
  cursor_skill_dir="$CURSOR_SKILLS/${skill_name}"
  cursor_file="$cursor_skill_dir/SKILL.md"
  mkdir -p "$cursor_skill_dir"

  # フロントマターのフィールドを抽出
  desc=$(awk '
    /^---$/ { fm++; next }
    fm == 1 && /^description:/ {
      sub(/^description: */, "")
      print
    }
  ' "$skill_file")

  disable_model=$(awk '
    /^---$/ { fm++; next }
    fm == 1 && /^disable-model-invocation:/ {
      sub(/^disable-model-invocation: */, "")
      print
    }
  ' "$skill_file")

  # フロントマター以降の本文を抽出し、ファイル参照パスを変換
  # Note: /skill-name は Cursor でも同じなので変換不要
  body=$(awk '
    /^---$/ { fm++; next }
    fm >= 2 { print }
  ' "$skill_file" | sed \
    -e 's|@docs/|docs/|g' \
    -e 's|@connectors/|connectors/|g' \
    -e 's|@\.claude/rules/\([^.]*\)\.md|.cursor/rules/\1.mdc|g' \
    -e 's|\.claude/rules/\([^.]*\)\.md|.cursor/rules/\1.mdc|g' \
  )

  # Cursor スキル形式で出力
  {
    echo "---"
    echo "name: ${skill_name}"
    echo "description: ${desc}"
    if [ -n "$disable_model" ]; then
      echo "disable-model-invocation: ${disable_model}"
    fi
    echo "---"
    echo "$body"
  } > "$cursor_file"

  echo "  ✓ skills/${skill_name}/SKILL.md"
done

echo ""
echo "Done. Manual step: update .cursor/rules/workato-project.mdc separately."
