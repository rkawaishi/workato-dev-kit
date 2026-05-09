#!/usr/bin/env bash
# setup.sh — workato-dev-kit を submodule として消費するためのセットアップスクリプト
#
# 利用者のリポジトリで実行すると、kit 内のスキル・ルール・ドキュメント等への
# シンボリックリンクを作成し、Claude Code / Cursor がフレームワークを認識できるようにする。
#
# Usage:
#   git submodule add https://github.com/<org>/workato-dev-kit.git kit
#   bash kit/setup.sh
#
# 冪等: 何度実行しても同じ結果になる。既存のシンボリックリンクは更新され、
# 利用者が追加した独自ファイルは保持される。

set -euo pipefail

# ── 位置の検出 ──────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KIT_DIR="$SCRIPT_DIR"

# kit/ の親ディレクトリ = 利用者のワークスペースルート
WORKSPACE_ROOT="$(cd "$KIT_DIR/.." && pwd)"

# kit ディレクトリ名（通常 "kit" だが別名もサポート）
KIT_NAME="$(basename "$KIT_DIR")"

# ワークスペースルートからの相対パス（symlink に使用）
KIT_REL="$KIT_NAME"

echo "=== workato-dev-kit setup ==="
echo "  Kit:       $KIT_DIR"
echo "  Workspace: $WORKSPACE_ROOT"
echo ""

cd "$WORKSPACE_ROOT"

# ── ヘルパー関数 ────────────────────────────────────────────

# ファイル単位のシンボリックリンクを作成（ディレクトリ内の各ファイルに対して）
# 利用者が同じディレクトリに独自ファイルを追加できるようにする
link_files_in_dir() {
  local src_dir="$1"   # kit 内のソースディレクトリ（絶対パス）
  local dst_dir="$2"   # ワークスペース内のリンク先ディレクトリ（絶対パス）
  local rel_prefix="$3" # ワークスペースルートからの相対パス

  mkdir -p "$dst_dir"

  for src_file in "$src_dir"/*; do
    [ -e "$src_file" ] || continue
    local name
    name="$(basename "$src_file")"

    local dst_file="$dst_dir/$name"
    local rel_target="$rel_prefix/$name"

    if [ -L "$dst_file" ]; then
      rm "$dst_file"
    elif [ -e "$dst_file" ]; then
      echo "  SKIP $dst_file (not a symlink, preserving user file)"
      continue
    fi

    ln -s "$rel_target" "$dst_file"
    echo "  ✓ $(basename "$dst_dir")/$name → $rel_target"
  done
}

# 利用者ディレクトリ内の壊れた kit-managed symlink を削除する
# ・symlink 以外（利用者の実ファイル/ディレクトリ）には触れない
# ・kit を指している symlink のみ対象（target 文字列に kit_marker を含むもの）
# ・target が解決できないもの（kit 側で削除/リネームされたもの）だけ削除
prune_stale_links() {
  local dst_dir="$1"      # 利用者側のディレクトリ（絶対パス）
  local kit_marker="$2"   # symlink target に含まれているはずの kit 側パス断片

  [ -d "$dst_dir" ] || return 0

  for entry in "$dst_dir"/* "$dst_dir"/.[!.]*; do
    [ -L "$entry" ] || continue
    local target
    target="$(readlink "$entry")"
    case "$target" in
      *"$kit_marker"*) ;;
      *) continue ;;
    esac
    if [ ! -e "$entry" ]; then
      rm "$entry"
      echo "  PRUNED $(basename "$dst_dir")/$(basename "$entry") (kit no longer provides this)"
    fi
  done
}

# ディレクトリ単位のシンボリックリンクを作成
link_dir() {
  local src_dir="$1"
  local dst_name="$2"
  local rel_target="$KIT_REL/$3"

  local dst_path="$WORKSPACE_ROOT/$dst_name"

  if [ -L "$dst_path" ]; then
    rm "$dst_path"
  elif [ -e "$dst_path" ]; then
    echo "  SKIP $dst_name (exists and is not a symlink)"
    return
  fi

  ln -s "$rel_target" "$dst_path"
  echo "  ✓ $dst_name → $rel_target"
}

# ── 1. .claude/rules/ （ファイル単位 symlink）──────────────
echo "--- Setting up .claude/rules/ ---"
prune_stale_links "$WORKSPACE_ROOT/.claude/rules" "framework/claude/rules/"
link_files_in_dir \
  "$KIT_DIR/framework/claude/rules" \
  "$WORKSPACE_ROOT/.claude/rules" \
  "../../$KIT_REL/framework/claude/rules"

# ── 2. .claude/skills/ （ディレクトリ単位 symlink: 各スキルフォルダ）─
echo ""
echo "--- Setting up .claude/skills/ ---"
mkdir -p "$WORKSPACE_ROOT/.claude/skills"
prune_stale_links "$WORKSPACE_ROOT/.claude/skills" "framework/claude/skills/"

for skill_dir in "$KIT_DIR/framework/claude/skills"/*/; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"

  dst="$WORKSPACE_ROOT/.claude/skills/$skill_name"
  rel_target="../../$KIT_REL/framework/claude/skills/$skill_name"

  if [ -L "$dst" ]; then
    rm "$dst"
  elif [ -e "$dst" ]; then
    echo "  SKIP skills/$skill_name (not a symlink, preserving user skill)"
    continue
  fi

  ln -s "$rel_target" "$dst"
  echo "  ✓ skills/$skill_name → $rel_target"
done

# ── 3. .claude/hooks/ （ファイル単位 symlink）─────────────
echo ""
echo "--- Setting up .claude/hooks/ ---"
prune_stale_links "$WORKSPACE_ROOT/.claude/hooks" "framework/claude/hooks/"
link_files_in_dir \
  "$KIT_DIR/framework/claude/hooks" \
  "$WORKSPACE_ROOT/.claude/hooks" \
  "../../$KIT_REL/framework/claude/hooks"

# ── 4. docs/ guides/ scripts/ templates/ （ディレクトリ symlink）─
echo ""
echo "--- Setting up top-level directories ---"
link_dir "$KIT_DIR/docs"      "docs"      "docs"
link_dir "$KIT_DIR/guides"    "guides"    "guides"
link_dir "$KIT_DIR/scripts"   "scripts"   "scripts"
link_dir "$KIT_DIR/templates" "templates" "templates"

# ── 5. .claude/settings.json のマージ ────────────────────
echo ""
echo "--- Setting up .claude/settings.json ---"

KIT_SETTINGS="$KIT_DIR/framework/claude/settings.json"
USER_SETTINGS="$WORKSPACE_ROOT/.claude/settings.json"

if [ ! -f "$USER_SETTINGS" ]; then
  # 初回: kit の settings.json をコピー（hook パスを書き換え）
  python3 -c "
import json, sys

with open('$KIT_SETTINGS') as f:
    s = json.load(f)

# Hook のコマンドパスを kit/framework/claude/ 配下に書き換え
# テンプレート上は \".claude/hooks/<name>\" と書かれているが、実体は
# kit/framework/claude/hooks/<name>。利用者の \".claude/settings.json\" には
# 実体パスを直接埋め込む（symlink を経由しない）。
for event in s.get('hooks', {}).values():
    for group in event:
        for hook in group.get('hooks', []):
            cmd = hook.get('command', '')
            if cmd.startswith('.claude/hooks/'):
                hook['command'] = '$KIT_REL/framework/claude/hooks/' + cmd[len('.claude/hooks/'):]

with open('$USER_SETTINGS', 'w') as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
    f.write('\n')
  "
  echo "  ✓ Created .claude/settings.json (from kit template)"
else
  # 既存設定: 旧版 setup.sh が書いた hook パスを framework/claude/ 配下に書き換える。
  # 利用者が追加した hook（kit 由来でないもの）には手を付けない。
  python3 -c "
import json

old_prefix = '$KIT_REL/.claude/hooks/'
new_prefix = '$KIT_REL/framework/claude/hooks/'

with open('$USER_SETTINGS') as f:
    s = json.load(f)

migrated = 0
for event in s.get('hooks', {}).values():
    for group in event:
        for hook in group.get('hooks', []):
            cmd = hook.get('command', '')
            if cmd.startswith(old_prefix):
                hook['command'] = new_prefix + cmd[len(old_prefix):]
                migrated += 1

if migrated:
    with open('$USER_SETTINGS', 'w') as f:
        json.dump(s, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f'  ✓ Migrated {migrated} kit hook path(s) in .claude/settings.json (.claude/hooks/ → framework/claude/hooks/)')
else:
    print('  EXISTS .claude/settings.json (no kit hook paths needed migrating — merge manually if other changes are needed)')
  "
fi

# ── 6. CLAUDE.md の生成 ──────────────────────────────────
echo ""
echo "--- Setting up CLAUDE.md ---"

CLAUDE_MD="$WORKSPACE_ROOT/.claude/CLAUDE.md"
KIT_CLAUDE_MD="$KIT_DIR/framework/claude/CLAUDE.md"

if [ ! -f "$CLAUDE_MD" ]; then
  cat > "$CLAUDE_MD" << 'HEREDOC'
# Workato Workspace

このワークスペースは [workato-dev-kit](kit/) をフレームワークとして使用しています。

## フレームワーク

HEREDOC

  # kit の CLAUDE.md の内容を取り込み（最初の見出し行を除く）
  tail -n +2 "$KIT_CLAUDE_MD" >> "$CLAUDE_MD"

  echo "  ✓ Created .claude/CLAUDE.md"
else
  echo "  EXISTS .claude/CLAUDE.md (not overwritten)"
fi

# ── 7. .gitignore の更新 ─────────────────────────────────
echo ""
echo "--- Updating .gitignore ---"

GITIGNORE="$WORKSPACE_ROOT/.gitignore"
touch "$GITIGNORE"

ENTRIES=(
  "# Workato Dev Kit (managed by kit/setup.sh)"
  ".workatoenv"
  "master.key"
  "settings.yaml"
  "settings.yaml.enc"
  ".resource-providers.yml"
  ".env"
  ".env.*"
  "*.key"
  "*.pem"
  "*.secret"
  "*.credential*"
)

added=0
for entry in "${ENTRIES[@]}"; do
  if ! grep -qxF "$entry" "$GITIGNORE" 2>/dev/null; then
    echo "$entry" >> "$GITIGNORE"
    added=$((added + 1))
  fi
done

if [ $added -gt 0 ]; then
  echo "  ✓ Added $added entries to .gitignore"
else
  echo "  ✓ .gitignore already up to date"
fi

# ── 8. Cursor 配布 ──────────────────────────────────────
# framework/cursor/ は kit 側で生成済み（python3 scripts/sync_agents.py）。
# 利用者の Cursor 環境に届けるため symlink を張る。
if [ -d "$KIT_DIR/framework/cursor" ]; then
  echo ""
  echo "--- Setting up .cursor/rules/ ---"
  prune_stale_links "$WORKSPACE_ROOT/.cursor/rules" "framework/cursor/rules/"
  link_files_in_dir \
    "$KIT_DIR/framework/cursor/rules" \
    "$WORKSPACE_ROOT/.cursor/rules" \
    "../../$KIT_REL/framework/cursor/rules"

  echo ""
  echo "--- Setting up .cursor/skills/ ---"
  mkdir -p "$WORKSPACE_ROOT/.cursor/skills"
  prune_stale_links "$WORKSPACE_ROOT/.cursor/skills" "framework/cursor/skills/"

  for skill_dir in "$KIT_DIR/framework/cursor/skills"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"

    dst="$WORKSPACE_ROOT/.cursor/skills/$skill_name"
    rel_target="../../$KIT_REL/framework/cursor/skills/$skill_name"

    if [ -L "$dst" ]; then
      rm "$dst"
    elif [ -e "$dst" ]; then
      echo "  SKIP skills/$skill_name (not a symlink, preserving user skill)"
      continue
    fi

    ln -s "$rel_target" "$dst"
    echo "  ✓ skills/$skill_name → $rel_target"
  done

  echo ""
  echo "--- Setting up .cursor/hooks.json ---"
  HOOKS_DST="$WORKSPACE_ROOT/.cursor/hooks.json"
  HOOKS_REL="../$KIT_REL/framework/cursor/hooks.json"
  if [ -L "$HOOKS_DST" ]; then
    rm "$HOOKS_DST"
    ln -s "$HOOKS_REL" "$HOOKS_DST"
    echo "  ✓ .cursor/hooks.json → $HOOKS_REL"
  elif [ -e "$HOOKS_DST" ]; then
    echo "  SKIP .cursor/hooks.json (not a symlink, preserving user file)"
  else
    ln -s "$HOOKS_REL" "$HOOKS_DST"
    echo "  ✓ .cursor/hooks.json → $HOOKS_REL"
  fi
fi

# ── 9. Codex CLI 配布 ────────────────────────────────────
# Codex CLI（skills モード）は ``.agents/skills/<name>/SKILL.md`` を読む。
if [ -d "$KIT_DIR/framework/codex" ]; then
  echo ""
  echo "--- Setting up .agents/skills/ ---"
  mkdir -p "$WORKSPACE_ROOT/.agents/skills"
  prune_stale_links "$WORKSPACE_ROOT/.agents/skills" "framework/codex/skills/"

  for skill_dir in "$KIT_DIR/framework/codex/skills"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"

    dst="$WORKSPACE_ROOT/.agents/skills/$skill_name"
    rel_target="../../$KIT_REL/framework/codex/skills/$skill_name"

    if [ -L "$dst" ]; then
      rm "$dst"
    elif [ -e "$dst" ]; then
      echo "  SKIP skills/$skill_name (not a symlink, preserving user skill)"
      continue
    fi

    ln -s "$rel_target" "$dst"
    echo "  ✓ skills/$skill_name → $rel_target"
  done
fi

# ── 10. Gemini CLI 配布 ──────────────────────────────────
# Gemini CLI（skills モード）は ``.gemini/skills/<name>/SKILL.md`` を読む。
if [ -d "$KIT_DIR/framework/gemini" ]; then
  echo ""
  echo "--- Setting up .gemini/skills/ ---"
  mkdir -p "$WORKSPACE_ROOT/.gemini/skills"
  prune_stale_links "$WORKSPACE_ROOT/.gemini/skills" "framework/gemini/skills/"

  for skill_dir in "$KIT_DIR/framework/gemini/skills"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"

    dst="$WORKSPACE_ROOT/.gemini/skills/$skill_name"
    rel_target="../../$KIT_REL/framework/gemini/skills/$skill_name"

    if [ -L "$dst" ]; then
      rm "$dst"
    elif [ -e "$dst" ]; then
      echo "  SKIP skills/$skill_name (not a symlink, preserving user skill)"
      continue
    fi

    ln -s "$rel_target" "$dst"
    echo "  ✓ skills/$skill_name → $rel_target"
  done
fi

# ── 11. AGENTS.md / GEMINI.md（エージェント横断の規約）────
# Codex CLI / Gemini CLI / Aider 等が読むエージェント中立ドキュメント。
# 中身は CLAUDE.md + rules を集約したもので、kit 側で生成済み。
# Gemini は GEMINI.md を読むため、AGENTS.md と同じ実体を別名で symlink する。
if [ -f "$KIT_DIR/framework/AGENTS.md" ]; then
  echo ""
  echo "--- Setting up AGENTS.md / GEMINI.md ---"
  for name in AGENTS.md GEMINI.md; do
    dst="$WORKSPACE_ROOT/$name"
    rel="$KIT_REL/framework/AGENTS.md"
    if [ -L "$dst" ]; then
      rm "$dst"
      ln -s "$rel" "$dst"
      echo "  ✓ $name → $rel"
    elif [ -e "$dst" ]; then
      echo "  SKIP $name (not a symlink, preserving user file)"
    else
      ln -s "$rel" "$dst"
      echo "  ✓ $name → $rel"
    fi
  done
fi

# ── 完了 ────────────────────────────────────────────────
echo ""
echo "=== Setup complete ==="
echo ""
echo "Next steps:"
echo "  1. Review .claude/CLAUDE.md and customize for your organization"
echo "  2. Run 'workato init' to authenticate with Workato"
echo "  3. Run 'git add .claude/ .cursor/ .agents/ .gemini/ AGENTS.md GEMINI.md docs guides scripts templates .gitignore && git commit'"
echo ""
echo "To update the framework later:"
echo "  git submodule update --remote kit && bash kit/setup.sh"
