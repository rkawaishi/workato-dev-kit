#!/bin/bash
# PreToolUse hook: warn when git commands likely target the wrong repo
#
# This repo has 3 nested git repos:
#   - workato-dev-kit/     (outer, framework)
#   - projects/            (inner, gitignored by outer)
#   - connectors/          (inner, gitignored by outer)
#
# Common mistakes this hook catches:
#   A. `git add projects/<name>/...` run from outer → gitignored, silent no-op
#   B. `git add connectors/<name>/...` run from outer → gitignored, silent no-op
#   C. `git commit` in outer while inner repos have uncommitted changes
#
# The hook warns (exit 0) rather than blocks so legitimate edge cases still work.
# See .claude/rules/workato-multi-repo-git.md for the full guidance.

INPUT=$(cat)

# Fast exit: only care about git commands
case "$INPUT" in
  *"git "*) ;;
  *) exit 0 ;;
esac

CWD="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Extract command
COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)
[ -z "$COMMAND" ] && exit 0

# Note: no global early-exit for "(cd <inner> && git ...)" patterns.
# A compound command can mix correct and incorrect segments (e.g.
# `git add projects/x/foo && cd projects/x && git status`), so each check
# analyzes segments individually instead of all-or-nothing.

WARNINGS=()

# Check A/B: git add <path> where <path> is under projects/ or connectors/
# Match `git add ... projects/...` or `git add ... connectors/...`
# Exclude paths that look like the outer repo's own docs/connectors/ (different prefix).
ADDED_INNER_PATHS=$(echo "$COMMAND" | python3 -c "
import sys, re, shlex
cmd = sys.stdin.read().strip()
# Only scan git add invocations; ignore git add -p, git add --patch interactive flows.
# We handle the common form: 'git add <path> [<path> ...]'
hits = []
# Split on && / ; / | to handle compound commands
for seg in re.split(r'&&|;|\|\|', cmd):
    seg = seg.strip()
    if not re.match(r'^git\s+add\b', seg):
        continue
    try:
        parts = shlex.split(seg)
    except ValueError:
        continue
    # parts[0]='git', parts[1]='add', rest=paths/flags
    for p in parts[2:]:
        if p.startswith('-'):
            continue
        # Match paths starting with projects/ or connectors/ (but not docs/connectors/)
        if re.match(r'^(projects|connectors)/', p):
            hits.append(p)
print('\n'.join(hits))
" 2>/dev/null)

if [ -n "$ADDED_INNER_PATHS" ]; then
  WARNINGS+=("git add with path(s) under projects/ or connectors/ detected:")
  while IFS= read -r p; do
    [ -z "$p" ] && continue
    WARNINGS+=("    - $p")
  done <<< "$ADDED_INNER_PATHS"
  WARNINGS+=("  These are gitignored by the outer repo — git add will be a silent no-op.")
  WARNINGS+=("  Use: (cd projects/<name> && git add <relative-path>)  or  (cd connectors && git add <name>/...)")
  WARNINGS+=("  See .claude/rules/workato-multi-repo-git.md for the full pattern.")
fi

# Check C: git commit at outer root while inner repos have staged/unstaged changes
# Fire only when the command has a bare outer-level `git commit`:
#   - subshells `(...)` are stripped (they don't propagate cd to the outer shell)
#   - segments after `cd projects/...` or `cd connectors` in the outer shell are skipped
#   - --amend / --fixup / --squash are excluded (documented intent)
#   - path-specific commits (`git commit -- <path>` or `git commit <path>`) are excluded
IS_OUTER_COMMIT=$(echo "$COMMAND" | python3 -c "
import sys, re, shlex
cmd = sys.stdin.read().strip()
# Strip parenthesized subshells (cd inside a subshell doesn't affect outer cwd).
# Iterate to collapse nested parens.
prev = None
while prev != cmd:
    prev = cmd
    cmd = re.sub(r'\([^()]*\)', '', cmd)
segments = [s.strip() for s in re.split(r'&&|;|\|\|', cmd) if s.strip()]
in_inner = False
for seg in segments:
    if re.match(r'^cd\s+(projects|connectors)(\b|/)', seg):
        in_inner = True
        continue
    m = re.match(r'^git\s+commit\b(.*)$', seg)
    if not m:
        continue
    if in_inner:
        continue
    rest = m.group(1)
    if re.search(r'(?:^|\s)--(amend|fixup|squash)(?:\s|=|$)', rest):
        continue
    # Path-specific via explicit -- separator
    if re.search(r'\s--(\s|$)', rest):
        continue
    # Path-specific via bare pathspec arg (non-flag token that isn't a flag value)
    try:
        tokens = shlex.split(rest)
    except ValueError:
        print('yes')
        sys.exit(0)
    value_flags = {'-m', '-C', '-F', '-c', '--message', '--reuse-message', '--file',
                   '--reedit-message', '--fixup', '--squash', '--author', '--date',
                   '--cleanup', '--gpg-sign', '-S', '--trailer'}
    skip_next = False
    pathspec = False
    for t in tokens:
        if skip_next:
            skip_next = False
            continue
        if t.startswith('-'):
            if '=' not in t and t in value_flags:
                skip_next = True
            continue
        pathspec = True
        break
    if pathspec:
        continue
    print('yes')
    sys.exit(0)
" 2>/dev/null)

if [ "$IS_OUTER_COMMIT" = "yes" ]; then
  for inner in projects connectors; do
    [ -d "$CWD/$inner/.git" ] || continue
    # `git -C <path> status --porcelain` lists changes; non-empty = dirty
    DIRTY=$(git -C "$CWD/$inner" status --porcelain 2>/dev/null | head -5)
    if [ -n "$DIRTY" ]; then
      WARNINGS+=("Outer-repo git commit detected, but inner repo '$inner/' has uncommitted changes:")
      while IFS= read -r line; do
        [ -z "$line" ] && continue
        WARNINGS+=("    $line")
      done <<< "$DIRTY"
      WARNINGS+=("  These will NOT be included in the outer commit. Commit them separately:")
      WARNINGS+=("    (cd $inner && git add . && git commit -m \"...\")")
    fi
  done
fi

# Emit warnings (non-blocking)
if [ ${#WARNINGS[@]} -gt 0 ]; then
  echo "" >&2
  echo "=== Multi-repo git warning ===" >&2
  for w in "${WARNINGS[@]}"; do
    echo "  ⚠️  $w" >&2
  done
  echo "" >&2
fi

exit 0
