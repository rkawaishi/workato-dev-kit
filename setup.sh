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
  #
  # 値は env 経由で Python に渡す。`python3 -c "..."` 内にシェル変数を直接展開すると、
  # パスにクォート・改行・バックスラッシュが含まれた場合に Python コードが破綻する
  # （あるいは任意コード実行に近い挙動になる）。ヒアドキュメントは <<'PY' でクォート
  # しておけば変数展開も完全に防げる。
  KIT_SETTINGS="$KIT_SETTINGS" USER_SETTINGS="$USER_SETTINGS" KIT_REL="$KIT_REL" \
    python3 <<'PY'
import json
import os

kit_settings = os.environ['KIT_SETTINGS']
user_settings = os.environ['USER_SETTINGS']
kit_rel = os.environ['KIT_REL']

with open(kit_settings) as f:
    s = json.load(f)

# Hook のコマンドパスを kit/framework/claude/ 配下に書き換え
# テンプレート上は ".claude/hooks/<name>" と書かれているが、実体は
# kit/framework/claude/hooks/<name>。利用者の ".claude/settings.json" には
# 実体パスを直接埋め込む（symlink を経由しない）。
for event in s.get('hooks', {}).values():
    for group in event:
        for hook in group.get('hooks', []):
            cmd = hook.get('command', '')
            if cmd.startswith('.claude/hooks/'):
                hook['command'] = kit_rel + '/framework/claude/hooks/' + cmd[len('.claude/hooks/'):]

with open(user_settings, 'w') as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
    f.write('\n')
PY
  echo "  ✓ Created .claude/settings.json (from kit template)"
else
  # 既存設定: 旧版 setup.sh が書いた hook パスを framework/claude/ 配下に書き換える。
  # 利用者が追加した hook（kit 由来でないもの）には手を付けない。
  USER_SETTINGS="$USER_SETTINGS" KIT_REL="$KIT_REL" \
    python3 <<'PY'
import json
import os

user_settings = os.environ['USER_SETTINGS']
kit_rel = os.environ['KIT_REL']
old_prefix = kit_rel + '/.claude/hooks/'
new_prefix = kit_rel + '/framework/claude/hooks/'

with open(user_settings) as f:
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
    with open(user_settings, 'w') as f:
        json.dump(s, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f'  ✓ Migrated {migrated} kit hook path(s) in .claude/settings.json (.claude/hooks/ → framework/claude/hooks/)')
else:
    print('  EXISTS .claude/settings.json (no kit hook paths needed migrating — merge manually if other changes are needed)')
PY
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
  ".cursor/.kit-manifest"
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

# ── 8. Cursor 配布（コピー方式）──────────────────────────
# framework/cursor/ は kit 側で生成済み（python3 scripts/sync_agents.py）。
#
# 他のエージェント（Claude / Codex / Gemini）は symlink で配布するが、Cursor は
# symlink を確実に解決できないため実ファイルとしてコピーする。
#   - .cursor/rules/*.mdc symlink は silent load failure する（forum.cursor.com）
#   - .cursor/skills/<name>/ ディレクトリ symlink は再起動後に検出されなくなる
#   - v2.5 で部分修正されたが再発報告あり
#
# kit-managed なファイルは .cursor/.kit-manifest で追跡し、kit から削除された
# ファイルは prune、利用者が独自に追加したファイル（manifest にない実ファイル）は
# 触らない。
if [ -d "$KIT_DIR/framework/cursor" ]; then
  echo ""
  echo "--- Setting up .cursor/ (copy mode — Cursor does not reliably follow symlinks) ---"

  CURSOR_DST="$WORKSPACE_ROOT/.cursor"
  MANIFEST="$CURSOR_DST/.kit-manifest"
  mkdir -p "$CURSOR_DST"

  # 旧 setup.sh が張った symlink を撤去（実ファイル/ディレクトリは利用者ファイルとして保持）
  if [ -d "$CURSOR_DST" ]; then
    while IFS= read -r -d '' link; do
      target="$(readlink "$link")"
      case "$target" in
        *"framework/cursor/"*)
          rm "$link"
          echo "  CLEANED legacy symlink: .cursor/${link#$CURSOR_DST/}"
          ;;
      esac
    done < <(find "$CURSOR_DST" -mindepth 1 -type l -print0 2>/dev/null)
  fi

  # 新しい kit-managed ファイル一覧を作成
  NEW_MANIFEST="$(mktemp)"
  (
    cd "$KIT_DIR/framework/cursor"
    find rules skills -type f 2>/dev/null | sort
    [ -f hooks.json ] && echo "hooks.json"
  ) > "$NEW_MANIFEST"

  # 旧 manifest にあって新 manifest に無いファイルを削除（kit が提供しなくなったもの）
  if [ -f "$MANIFEST" ]; then
    while IFS= read -r rel_path; do
      [ -z "$rel_path" ] && continue
      if ! grep -qxF "$rel_path" "$NEW_MANIFEST"; then
        target="$CURSOR_DST/$rel_path"
        if [ -f "$target" ] && [ ! -L "$target" ]; then
          rm "$target"
          echo "  PRUNED .cursor/$rel_path (kit no longer provides this)"
        fi
      fi
    done < "$MANIFEST"
    # 空ディレクトリを掃除（利用者ファイルがあるディレクトリは type d -empty に該当しないので安全）
    find "$CURSOR_DST" -mindepth 1 -type d -empty -delete 2>/dev/null || true
  fi

  # 各 kit ファイルをコピー
  copied=0
  skipped=0
  while IFS= read -r rel_path; do
    [ -z "$rel_path" ] && continue
    src="$KIT_DIR/framework/cursor/$rel_path"
    dst="$CURSOR_DST/$rel_path"

    # 利用者ファイル保護: dst が実ファイル かつ 旧 manifest に存在しない = 利用者が追加したもの
    if [ -f "$dst" ] && [ ! -L "$dst" ] && [ -f "$MANIFEST" ]; then
      if ! grep -qxF "$rel_path" "$MANIFEST"; then
        echo "  SKIP .cursor/$rel_path (user file, preserving)"
        skipped=$((skipped + 1))
        continue
      fi
    fi

    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    copied=$((copied + 1))
  done < "$NEW_MANIFEST"

  # manifest を更新
  mv "$NEW_MANIFEST" "$MANIFEST"

  echo "  ✓ Copied $copied kit-managed file(s) into .cursor/"
  if [ $skipped -gt 0 ]; then
    echo "  ✓ Preserved $skipped user file(s)"
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
