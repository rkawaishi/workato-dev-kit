#!/usr/bin/env bash
# setup.sh — bootstrap script for consuming workato-dev-kit as a submodule.
#
# Run this from your workspace repository to create symlinks into the
# kit's skills, rules, and docs so Claude Code / Cursor / Codex CLI /
# Gemini CLI can pick them up.
#
# Usage:
#   git submodule add https://github.com/<org>/workato-dev-kit.git kit
#   bash kit/setup.sh
#
# Idempotent: repeated runs produce the same result. Existing symlinks
# are refreshed, and user-added files are preserved.

set -euo pipefail

# ── Locate ourselves ─────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KIT_DIR="$SCRIPT_DIR"

# Parent of kit/ = consumer workspace root.
WORKSPACE_ROOT="$(cd "$KIT_DIR/.." && pwd)"

# Kit directory name (usually "kit"; we support other names too).
KIT_NAME="$(basename "$KIT_DIR")"

# Path from the workspace root to the kit (used in symlink targets).
KIT_REL="$KIT_NAME"

echo "=== workato-dev-kit setup ==="
echo "  Kit:       $KIT_DIR"
echo "  Workspace: $WORKSPACE_ROOT"
echo ""

cd "$WORKSPACE_ROOT"

# ── Detect git worktree context ──────────────────────────────
# `git worktree add` does NOT check out submodules into the new worktree,
# so in a linked worktree the kit submodule can be empty and every symlink
# created below would dangle. Detect a linked worktree (its --git-dir
# differs from the shared --git-common-dir) so we can warn precisely.
IS_WORKTREE=0
if git -C "$WORKSPACE_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  _git_dir="$(git -C "$WORKSPACE_ROOT" rev-parse --git-dir 2>/dev/null || true)"
  _common_dir="$(git -C "$WORKSPACE_ROOT" rev-parse --git-common-dir 2>/dev/null || true)"
  if [ -n "$_common_dir" ] && [ "$_git_dir" != "$_common_dir" ]; then
    IS_WORKTREE=1
  fi
fi

# ── Verify the kit submodule is checked out ──────────────────
# setup.sh running implies kit/setup.sh exists, but a partial checkout
# could still lack framework/. Fail fast with a precise remedy rather
# than building a tree of dangling symlinks.
if [ ! -d "$KIT_DIR/framework/claude/rules" ]; then
  echo "ERROR: the kit submodule is not fully checked out." >&2
  echo "  Missing: $KIT_DIR/framework/claude/rules" >&2
  echo "" >&2
  echo "  Submodules are not auto-populated in a new 'git worktree'." >&2
  echo "  Run this in the current working tree, then re-run setup.sh:" >&2
  echo "    git submodule update --init --recursive" >&2
  exit 1
fi

# ── Helpers ──────────────────────────────────────────────────

# Symlink each file inside src_dir into dst_dir so the user can add
# their own files alongside kit-managed ones.
link_files_in_dir() {
  local src_dir="$1"   # Absolute path of the kit-side source dir.
  local dst_dir="$2"   # Absolute path of the workspace-side dir.
  local rel_prefix="$3" # Relative path from the workspace root.

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

# Remove broken kit-managed symlinks from the consumer's directory.
# - Never touch non-symlinks (those are user files / dirs).
# - Only touch symlinks whose target contains the kit_marker path.
# - Only delete symlinks whose target no longer resolves (i.e. the
#   kit has removed or renamed the original file).
prune_stale_links() {
  local dst_dir="$1"      # Consumer-side directory (absolute path).
  local kit_marker="$2"   # Kit-side path fragment the symlink target should contain.

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

# Create a directory-level symlink.
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

# ── 1. .claude/rules/ (per-file symlinks) ────────────────────
echo "--- Setting up .claude/rules/ ---"
prune_stale_links "$WORKSPACE_ROOT/.claude/rules" "framework/claude/rules/"
link_files_in_dir \
  "$KIT_DIR/framework/claude/rules" \
  "$WORKSPACE_ROOT/.claude/rules" \
  "../../$KIT_REL/framework/claude/rules"

# ── 2. .claude/skills/ (per-skill directory symlinks) ────────
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

# ── 3. .claude/hooks/ (per-file symlinks) ────────────────────
echo ""
echo "--- Setting up .claude/hooks/ ---"
prune_stale_links "$WORKSPACE_ROOT/.claude/hooks" "framework/claude/hooks/"
link_files_in_dir \
  "$KIT_DIR/framework/claude/hooks" \
  "$WORKSPACE_ROOT/.claude/hooks" \
  "../../$KIT_REL/framework/claude/hooks"

# ── 3b. .claude/agents/ (per-file symlinks; Claude Code subagents) ──
# Subagents are the canonical source here; sync_agents.py regenerates the
# Cursor / Gemini / Codex variants distributed in sections 8-10 below.
if [ -d "$KIT_DIR/framework/claude/agents" ]; then
  echo ""
  echo "--- Setting up .claude/agents/ ---"
  prune_stale_links "$WORKSPACE_ROOT/.claude/agents" "framework/claude/agents/"
  link_files_in_dir \
    "$KIT_DIR/framework/claude/agents" \
    "$WORKSPACE_ROOT/.claude/agents" \
    "../../$KIT_REL/framework/claude/agents"
fi

# ── 4. docs/ guides/ scripts/ templates/ (directory symlinks) ──
echo ""
echo "--- Setting up top-level directories ---"
link_dir "$KIT_DIR/docs"      "docs"      "docs"
link_dir "$KIT_DIR/guides"    "guides"    "guides"
link_dir "$KIT_DIR/scripts"   "scripts"   "scripts"
link_dir "$KIT_DIR/templates" "templates" "templates"

# ── 5. .claude/settings.json merge ───────────────────────────
echo ""
echo "--- Setting up .claude/settings.json ---"

KIT_SETTINGS="$KIT_DIR/framework/claude/settings.json"
USER_SETTINGS="$WORKSPACE_ROOT/.claude/settings.json"

if [ ! -f "$USER_SETTINGS" ]; then
  # First run: copy the kit's settings.json template, rewriting hook paths.
  #
  # We pass values via env vars to Python. Splicing shell variables straight
  # into `python3 -c "..."` would break if paths contain quotes, newlines, or
  # backslashes (and could approach arbitrary code execution). A <<'PY'
  # heredoc fully disables variable expansion inside the Python block.
  KIT_SETTINGS="$KIT_SETTINGS" USER_SETTINGS="$USER_SETTINGS" KIT_REL="$KIT_REL" \
    python3 <<'PY'
import json
import os

kit_settings = os.environ['KIT_SETTINGS']
user_settings = os.environ['USER_SETTINGS']
kit_rel = os.environ['KIT_REL']

with open(kit_settings) as f:
    s = json.load(f)

# Rewrite hook command paths to point inside kit/framework/claude/.
# The template uses ".claude/hooks/<name>", but the real files live at
# kit/framework/claude/hooks/<name>. We embed the real path directly in
# the consumer's .claude/settings.json (i.e. no symlink indirection).
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
  # Existing settings: migrate hook paths written by older setup.sh to the
  # framework/claude/ layout, and top up the credential-guard hook + the
  # permissions.deny credential rules. Leave hooks / rules the user added
  # (non-kit ones) alone.
  USER_SETTINGS="$USER_SETTINGS" KIT_REL="$KIT_REL" \
    CRED_PATTERNS_FILE="$KIT_DIR/framework/credential-patterns.txt" \
    python3 <<'PY'
import json
import os

user_settings = os.environ['USER_SETTINGS']
kit_rel = os.environ['KIT_REL']
patterns_file = os.environ.get('CRED_PATTERNS_FILE', '')
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

# Top up the block-credential-read PreToolUse hook.
hooks_root = s.setdefault('hooks', {})
pre = hooks_root.setdefault('PreToolUse', [])
def _has_cred_hook(pre_list):
    for group in pre_list:
        for h in group.get('hooks', []):
            if 'block-credential-read' in h.get('command', ''):
                return True
    return False

added_hook = False
if not _has_cred_hook(pre):
    pre.append({
        'matcher': 'Bash|Read|Edit|Write|NotebookEdit|Grep|Glob',
        'hooks': [{
            'type': 'command',
            'command': new_prefix + 'block-credential-read.sh',
        }],
    })
    added_hook = True

# Top up permissions.deny with Read(./**/<glob>) for every credential pattern.
perms = s.setdefault('permissions', {})
deny = perms.setdefault('deny', [])
added_deny = 0
if patterns_file and os.path.isfile(patterns_file):
    with open(patterns_file) as pf:
        for line in pf:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            rule = f'Read(./**/{line})'
            if rule not in deny:
                deny.append(rule)
                added_deny += 1

# Migrate: .workatoenv is no longer a credential. Older kit versions added a
# deny rule for it; remove the stale entry so existing installs can read it.
removed_deny = 0
stale = 'Read(./**/.workatoenv)'
while stale in deny:
    deny.remove(stale)
    removed_deny += 1

if migrated or added_hook or added_deny or removed_deny:
    with open(user_settings, 'w') as f:
        json.dump(s, f, indent=2, ensure_ascii=False)
        f.write('\n')
    msgs = []
    if migrated:
        msgs.append(f'migrated {migrated} kit hook path(s)')
    if added_hook:
        msgs.append('added block-credential-read PreToolUse hook')
    if added_deny:
        msgs.append(f'added {added_deny} credential deny rule(s)')
    if removed_deny:
        msgs.append('removed stale .workatoenv deny rule')
    print('  ✓ Updated .claude/settings.json (' + '; '.join(msgs) + ')')
else:
    print('  EXISTS .claude/settings.json (kit entries already present)')
PY
fi

# ── 6. Generate CLAUDE.md ────────────────────────────────────
echo ""
echo "--- Setting up CLAUDE.md ---"

CLAUDE_MD="$WORKSPACE_ROOT/.claude/CLAUDE.md"
KIT_CLAUDE_MD="$KIT_DIR/framework/claude/CLAUDE.md"

if [ ! -f "$CLAUDE_MD" ]; then
  cat > "$CLAUDE_MD" << 'HEREDOC'
# Workato Workspace

This workspace uses [workato-dev-kit](kit/) as its framework.

## Framework

HEREDOC

  # Append the kit's CLAUDE.md (skipping its top-level heading).
  tail -n +2 "$KIT_CLAUDE_MD" >> "$CLAUDE_MD"

  echo "  ✓ Created .claude/CLAUDE.md"
else
  echo "  EXISTS .claude/CLAUDE.md (not overwritten)"
fi

# ── 7. Update .gitignore ─────────────────────────────────────
echo ""
echo "--- Updating .gitignore ---"

GITIGNORE="$WORKSPACE_ROOT/.gitignore"
touch "$GITIGNORE"

ENTRIES=(
  "# Workato Dev Kit (managed by kit/setup.sh)"
  # NOTE: .workatoenv is intentionally NOT ignored — it holds only project /
  # folder / workspace IDs (no credentials) and is committed so the
  # project↔Workato binding is shared across the team.
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

# ── 7b. Per-editor credential ignore files ───────────────────
# Distribute the credential glob list from framework/credential-patterns.txt
# to each editor's ignore mechanism so the agent will not even index / read
# credentials:
#   .cursorignore   — Cursor: "hard block" (.cursorindexingignore is partial).
#   .geminiignore   — Gemini CLI: gitignore-style; respected by tools.
#   .codexignore    — Codex CLI: shipped for forward-compat; Codex currently
#                     does not respect it (openai/codex#6530), so the .codex/
#                     hooks/block-credential-read.sh hook (Bash-only) is the
#                     enforcement layer available today.
# Claude has no working ignore-file convention — credential reads are blocked
# by the .claude/hooks/block-credential-read.sh PreToolUse hook and the
# permissions.deny list in .claude/settings.json (section 5).
CRED_PATTERNS_FILE="$KIT_DIR/framework/credential-patterns.txt"
if [ -f "$CRED_PATTERNS_FILE" ]; then
  echo ""
  echo "--- Setting up per-editor credential ignore files ---"
  add_credential_patterns() {
    local target="$1"
    local header="$2"
    touch "$target"
    local added=0
    while IFS= read -r line; do
      case "$line" in '#'*|'') continue ;; esac
      if ! grep -qxF "$line" "$target" 2>/dev/null; then
        if [ $added -eq 0 ] && [ -n "$header" ] && ! grep -qF "$header" "$target" 2>/dev/null; then
          { [ -s "$target" ] && echo ""; echo "$header"; } >> "$target"
        fi
        echo "$line" >> "$target"
        added=$((added + 1))
      fi
    done < "$CRED_PATTERNS_FILE"
    local name
    name="$(basename "$target")"
    if [ $added -gt 0 ]; then
      echo "  ✓ Added $added credential entries to $name"
    else
      echo "  ✓ $name already covers credentials"
    fi
  }
  HEADER="# workato-dev-kit credential patterns (managed by kit/setup.sh)"
  add_credential_patterns "$WORKSPACE_ROOT/.cursorignore"  "$HEADER"
  add_credential_patterns "$WORKSPACE_ROOT/.geminiignore"  "$HEADER"
  add_credential_patterns "$WORKSPACE_ROOT/.codexignore"   "$HEADER"
fi

# ── 7c. Migrate: drop stale `.workatoenv` ignore entries ─────
# Older kit versions treated .workatoenv as a credential and added it to the
# gitignore / per-editor ignore files. It is now git-managed (no secrets), so
# strip the exact `.workatoenv` line from each kit-managed ignore file on
# re-run. Only the standalone entry is removed; user content is untouched.
strip_workatoenv_ignore() {
  local target="$1"
  [ -f "$target" ] || return 0
  if grep -qxF ".workatoenv" "$target" 2>/dev/null; then
    # Portable in-place delete of lines that are exactly `.workatoenv`.
    # grep exits 1 when it selects no lines (i.e. the file was only
    # `.workatoenv`); that is success here, so accept rc 0 and 1 and only
    # bail on a real error (rc > 1), leaving the original untouched.
    local tmp rc
    tmp="$(mktemp)"
    grep -vxF ".workatoenv" "$target" > "$tmp"; rc=$?
    if [ "$rc" -le 1 ]; then
      mv "$tmp" "$target"
      echo "  ✓ Removed stale .workatoenv entry from $(basename "$target") (now git-managed)"
    else
      rm -f "$tmp"
    fi
  fi
}
strip_workatoenv_ignore "$GITIGNORE"
strip_workatoenv_ignore "$WORKSPACE_ROOT/.cursorignore"
strip_workatoenv_ignore "$WORKSPACE_ROOT/.geminiignore"
strip_workatoenv_ignore "$WORKSPACE_ROOT/.codexignore"

# ── 8. Cursor distribution (copy mode) ───────────────────────
# framework/cursor/ is pre-generated on the kit side via
# `python3 scripts/sync_agents.py`.
#
# Other agents (Claude / Codex / Gemini) get symlinks, but Cursor cannot
# reliably resolve symlinks, so we ship real files instead:
#   - .cursor/rules/*.mdc symlinks load silently as empty (forum.cursor.com)
#   - .cursor/skills/<name>/ directory symlinks stop being detected after a restart
#   - v2.5 partially fixed this, but regressions have been reported
#
# We track kit-managed files in .cursor/.kit-manifest. Files dropped by
# the kit are pruned; files the user added themselves (real files not
# listed in the manifest) are left untouched.
if [ -d "$KIT_DIR/framework/cursor" ]; then
  echo ""
  echo "--- Setting up .cursor/ (copy mode — Cursor does not reliably follow symlinks) ---"

  CURSOR_DST="$WORKSPACE_ROOT/.cursor"
  MANIFEST="$CURSOR_DST/.kit-manifest"
  mkdir -p "$CURSOR_DST"

  # Remove symlinks left by older setup.sh runs (keep real files / dirs
  # so user-authored content survives).
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

  # Build the new list of kit-managed files.
  NEW_MANIFEST="$(mktemp)"
  (
    cd "$KIT_DIR/framework/cursor"
    find rules skills agents -type f 2>/dev/null | sort
    [ -f hooks.json ] && echo "hooks.json"
  ) > "$NEW_MANIFEST"

  # Drop files that were in the old manifest but no longer ship with the
  # kit (i.e. the kit retired them).
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
    # Clean up empty directories. Directories containing user files are
    # not empty and so are not removed by -type d -empty.
    find "$CURSOR_DST" -mindepth 1 -type d -empty -delete 2>/dev/null || true
  fi

  # Copy each kit file. Record the paths we actually copied as the next
  # manifest — paths we skipped (to protect user files) stay out of it.
  COPIED_PATHS="$(mktemp)"
  copied=0
  skipped=0
  while IFS= read -r rel_path; do
    [ -z "$rel_path" ] && continue
    src="$KIT_DIR/framework/cursor/$rel_path"
    dst="$CURSOR_DST/$rel_path"

    # User file protection:
    # - No manifest yet (first run): every existing real file is treated
    #   as user-authored and preserved. This mirrors the old symlink-mode
    #   setup.sh behaviour of "do not touch non-symlinks", protecting
    #   hand-written .cursor/hooks.json or user-replaced files.
    # - Manifest exists (subsequent runs): a real file whose path is NOT
    #   in the old manifest is a user file. (Only paths we actually
    #   copied last time end up in the new manifest, so first-run-
    #   protected paths stay outside the manifest indefinitely.)
    if [ -f "$dst" ] && [ ! -L "$dst" ]; then
      if [ ! -f "$MANIFEST" ]; then
        echo "  SKIP .cursor/$rel_path (existing real file, preserving on first run — delete it to opt into kit version)"
        skipped=$((skipped + 1))
        continue
      elif ! grep -qxF "$rel_path" "$MANIFEST"; then
        echo "  SKIP .cursor/$rel_path (user file, preserving)"
        skipped=$((skipped + 1))
        continue
      fi
    fi

    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    echo "$rel_path" >> "$COPIED_PATHS"
    copied=$((copied + 1))
  done < "$NEW_MANIFEST"

  # Update the manifest with only the paths we actually copied; do not
  # record user-authored files there.
  sort "$COPIED_PATHS" > "$MANIFEST"
  rm -f "$NEW_MANIFEST" "$COPIED_PATHS"

  echo "  ✓ Copied $copied kit-managed file(s) into .cursor/"
  if [ $skipped -gt 0 ]; then
    echo "  ✓ Preserved $skipped user file(s)"
  fi
fi

# ── 9. Codex CLI distribution ────────────────────────────────
# Codex CLI (skills mode) reads ``.agents/skills/<name>/SKILL.md``.
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

  # Subagents → .codex/agents/<name>.toml (Codex CLI reads .codex/agents/).
  if [ -d "$KIT_DIR/framework/codex/agents" ]; then
    echo "--- Setting up .codex/agents/ ---"
    prune_stale_links "$WORKSPACE_ROOT/.codex/agents" "framework/codex/agents/"
    link_files_in_dir \
      "$KIT_DIR/framework/codex/agents" \
      "$WORKSPACE_ROOT/.codex/agents" \
      "../../$KIT_REL/framework/codex/agents"
  fi

  # Hooks → .codex/hooks/<file>.sh (referenced by .codex/hooks.json below).
  if [ -d "$KIT_DIR/framework/codex/hooks" ]; then
    echo "--- Setting up .codex/hooks/ ---"
    prune_stale_links "$WORKSPACE_ROOT/.codex/hooks" "framework/codex/hooks/"
    link_files_in_dir \
      "$KIT_DIR/framework/codex/hooks" \
      "$WORKSPACE_ROOT/.codex/hooks" \
      "../../$KIT_REL/framework/codex/hooks"
  fi

  # .codex/hooks.json — initial copy only, never overwrites a user-customised
  # hooks config.
  if [ -f "$KIT_DIR/framework/codex/hooks.json" ] && [ ! -f "$WORKSPACE_ROOT/.codex/hooks.json" ]; then
    mkdir -p "$WORKSPACE_ROOT/.codex"
    cp "$KIT_DIR/framework/codex/hooks.json" "$WORKSPACE_ROOT/.codex/hooks.json"
    echo "  ✓ Created .codex/hooks.json (from kit template)"
  fi
fi

# ── 10. Gemini CLI distribution ──────────────────────────────
# Gemini CLI (skills mode) reads ``.gemini/skills/<name>/SKILL.md``.
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

  # Subagents → .gemini/agents/<name>.md (Gemini CLI reads .gemini/agents/).
  if [ -d "$KIT_DIR/framework/gemini/agents" ]; then
    echo "--- Setting up .gemini/agents/ ---"
    prune_stale_links "$WORKSPACE_ROOT/.gemini/agents" "framework/gemini/agents/"
    link_files_in_dir \
      "$KIT_DIR/framework/gemini/agents" \
      "$WORKSPACE_ROOT/.gemini/agents" \
      "../../$KIT_REL/framework/gemini/agents"
  fi
fi

# ── 11. AGENTS.md / GEMINI.md (cross-agent conventions) ──────
# Agent-neutral document consumed by Codex CLI / Gemini CLI / Aider etc.
# Its content aggregates CLAUDE.md + rules and is pre-generated by the
# kit. Gemini reads GEMINI.md, so we symlink it to the same AGENTS.md
# target under a second name.
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

# ── 12. Install git post-checkout hook ───────────────────────
# `git worktree add` does not populate submodules, so a new worktree
# starts with an empty kit/. A post-checkout hook — shared across every
# worktree via the common .git — initialises submodules automatically
# whenever a worktree or branch is checked out.
echo ""
echo "--- Setting up git post-checkout hook ---"
if ! git -C "$WORKSPACE_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "  SKIP (workspace is not a git repository yet)"
else
  _hooks_path_cfg="$(git -C "$WORKSPACE_ROOT" config --get core.hooksPath 2>/dev/null || true)"
  if [ -n "$_hooks_path_cfg" ]; then
    echo "  SKIP (core.hooksPath is set — hooks are managed elsewhere, e.g. husky)"
    echo "        To auto-init submodules in new worktrees, add to your post-checkout hook:"
    echo "          [ \"\$3\" = \"1\" ] && git submodule update --init --recursive"
  else
    # Submodule git data and hooks both live in the *common* git dir, so
    # the hook is installed once and every worktree shares it.
    _common_dir="$(git -C "$WORKSPACE_ROOT" rev-parse --git-common-dir 2>/dev/null || echo .git)"
    case "$_common_dir" in
      /*) ;;
      *) _common_dir="$WORKSPACE_ROOT/$_common_dir" ;;
    esac
    HOOK="$_common_dir/hooks/post-checkout"
    if [ -e "$HOOK" ] && ! grep -q 'workato-dev-kit:post-checkout' "$HOOK" 2>/dev/null; then
      echo "  SKIP post-checkout (a non-kit hook exists — preserving it)"
      echo "        To auto-init submodules in new worktrees, add to $HOOK:"
      echo "          [ \"\$3\" = \"1\" ] && git submodule update --init --recursive"
    else
      _had_hook=0
      [ -e "$HOOK" ] && _had_hook=1
      mkdir -p "$_common_dir/hooks"
      cat > "$HOOK" <<'HOOK_EOF'
#!/bin/sh
# workato-dev-kit:post-checkout — managed by kit/setup.sh (safe to delete).
# `git worktree add` does not check out submodules; without this the kit/
# submodule stays empty in new worktrees and every setup.sh symlink dangles.
# $3 == 1 marks a branch / worktree checkout (vs. a file checkout).
if [ "$3" = "1" ]; then
  git submodule update --init --recursive
fi
HOOK_EOF
      chmod +x "$HOOK"
      if [ "$_had_hook" -eq 1 ]; then
        echo "  ✓ post-checkout hook refreshed ($HOOK)"
      else
        echo "  ✓ Installed post-checkout hook — 'git worktree add' now auto-inits the kit/ submodule"
      fi
    fi
  fi
fi

# ── 13. Verify kit symlinks resolve ──────────────────────────
# A linked worktree with an un-initialised kit submodule leaves the
# symlinks above pointing at nothing. Surface that instead of letting
# Claude Code / Cursor silently fail to load rules and skills.
echo ""
echo "--- Verifying kit symlinks ---"
DANGLING=0
while IFS= read -r -d '' link; do
  target="$(readlink "$link")"
  case "$target" in
    *"$KIT_REL/"*) ;;
    *) continue ;;
  esac
  if [ -e "$link" ]; then
    continue
  fi
  echo "  ⚠️  DANGLING: ${link#$WORKSPACE_ROOT/} → $target" >&2
  DANGLING=$((DANGLING + 1))
done < <(
  find "$WORKSPACE_ROOT/.claude" "$WORKSPACE_ROOT/.agents" "$WORKSPACE_ROOT/.codex" \
       "$WORKSPACE_ROOT/.gemini" -type l -print0 2>/dev/null
  for top in docs guides scripts templates AGENTS.md GEMINI.md; do
    if [ -L "$WORKSPACE_ROOT/$top" ]; then
      printf '%s\0' "$WORKSPACE_ROOT/$top"
    fi
  done
)
if [ "$DANGLING" -gt 0 ]; then
  echo "" >&2
  echo "  $DANGLING kit symlink(s) above do not resolve — the kit submodule" >&2
  echo "  is not checked out in this working tree. Fix with:" >&2
  echo "    git submodule update --init --recursive" >&2
else
  echo "  ✓ all kit symlinks resolve"
fi

# ── Done ─────────────────────────────────────────────────────
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

if [ "$IS_WORKTREE" -eq 1 ]; then
  echo ""
  echo "Note: this is a linked git worktree. The installed post-checkout hook"
  echo "auto-populates the kit/ submodule whenever you run 'git worktree add'."
  echo "If kit/ is ever empty, run 'git submodule update --init --recursive'"
  echo "then 'bash $KIT_NAME/setup.sh'. See guides/quickstart-claude-code.md."
fi
