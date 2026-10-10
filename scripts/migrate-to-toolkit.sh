#!/usr/bin/env bash
# migrate-to-toolkit.sh — re-point the kit submodule from the retired
# workato-dev-kit repository to its successor, workato-toolkit.
#
# workato-dev-kit has been retired and its development moved to a new,
# separate repository:
#
#     https://github.com/rkawaishi/workato-toolkit
#
# Because the successor is a *separate* repository (not a GitHub rename),
# the old clone URL no longer receives updates and does not redirect.
# Existing workspaces that added this kit as a submodule must re-point
# that submodule at the new URL. This script performs that switch safely
# and idempotently.
#
# Usage (run from anywhere inside your workspace repository):
#
#     bash kit/scripts/migrate-to-toolkit.sh [NEW_URL]
#
# Options:
#     NEW_URL         Override the destination clone URL. When omitted, the
#                     URL is derived from the current submodule URL by
#                     swapping the repository name (workato-dev-kit →
#                     workato-toolkit), preserving host, protocol, and org.
#                     This keeps SSH remotes and organization forks working.
#     -y, --yes       Do not prompt for confirmation.
#     -n, --dry-run   Print the actions that would be taken, change nothing.
#     -h, --help      Show this help and exit.
#
# After a successful run, re-generate the editor symlinks/copies and commit:
#
#     bash kit/setup.sh
#     git add .gitmodules kit && git commit -m "Migrate kit to workato-toolkit"

set -euo pipefail

OLD_SLUG="workato-dev-kit"
NEW_SLUG="workato-toolkit"

# ── Parse arguments ──────────────────────────────────────────
ASSUME_YES=0
DRY_RUN=0
NEW_URL_OVERRIDE=""

usage() {
  # Print the header comment block (skip the shebang, stop before the code).
  awk 'NR==1 {next} /^set -euo pipefail/ {exit} /^#/ {sub(/^# ?/, ""); print}' "$0"
}

while [ $# -gt 0 ]; do
  case "$1" in
    -y|--yes)     ASSUME_YES=1 ;;
    -n|--dry-run) DRY_RUN=1 ;;
    -h|--help)    usage; exit 0 ;;
    -*)
      echo "ERROR: unknown option: $1" >&2
      echo "Run with --help for usage." >&2
      exit 2
      ;;
    *)
      if [ -n "$NEW_URL_OVERRIDE" ]; then
        echo "ERROR: unexpected extra argument: $1" >&2
        exit 2
      fi
      NEW_URL_OVERRIDE="$1"
      ;;
  esac
  shift
done

# ── Locate ourselves ─────────────────────────────────────────
# This script lives at <kit>/scripts/migrate-to-toolkit.sh.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KIT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
KIT_NAME="$(basename "$KIT_DIR")"

# The superproject (workspace) is the repository that *contains* the kit
# as a submodule — i.e. the first git repo above the kit directory.
WORKSPACE_ROOT="$(git -C "$KIT_DIR/.." rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$WORKSPACE_ROOT" ]; then
  echo "ERROR: could not find a git repository containing '$KIT_NAME'." >&2
  echo "  Run this from inside your workspace repository, e.g.:" >&2
  echo "    bash $KIT_NAME/scripts/migrate-to-toolkit.sh" >&2
  exit 1
fi

GITMODULES="$WORKSPACE_ROOT/.gitmodules"
if [ ! -f "$GITMODULES" ]; then
  echo "ERROR: no .gitmodules found in $WORKSPACE_ROOT." >&2
  echo "  This workspace does not track the kit as a git submodule, so there" >&2
  echo "  is nothing to migrate. If you vendored the kit some other way," >&2
  echo "  update your clone URL to point at:" >&2
  echo "    https://github.com/rkawaishi/$NEW_SLUG" >&2
  exit 1
fi

# Path of the kit relative to the workspace root, as recorded in .gitmodules.
KIT_REL="$(cd "$WORKSPACE_ROOT" && realpath --relative-to="$WORKSPACE_ROOT" "$KIT_DIR" 2>/dev/null || echo "$KIT_NAME")"

# ── Find the submodule entry for the kit ─────────────────────
# Match by path first (the kit directory), which is unambiguous even when
# the workspace tracks several submodules.
SUBMODULE_NAME=""
while read -r key path; do
  # key looks like: submodule.<name>.path
  if [ "$path" = "$KIT_REL" ]; then
    SUBMODULE_NAME="${key#submodule.}"
    SUBMODULE_NAME="${SUBMODULE_NAME%.path}"
    break
  fi
done < <(git config -f "$GITMODULES" --get-regexp '^submodule\..*\.path$' || true)

# Fall back to matching by URL slug if no path matched (e.g. the kit lives
# under a non-standard relative path).
if [ -z "$SUBMODULE_NAME" ]; then
  while read -r key url; do
    if printf '%s' "$url" | grep -q "$OLD_SLUG"; then
      SUBMODULE_NAME="${key#submodule.}"
      SUBMODULE_NAME="${SUBMODULE_NAME%.url}"
      KIT_REL="$(git config -f "$GITMODULES" --get "submodule.$SUBMODULE_NAME.path")"
      break
    fi
  done < <(git config -f "$GITMODULES" --get-regexp '^submodule\..*\.url$' || true)
fi

if [ -z "$SUBMODULE_NAME" ]; then
  echo "ERROR: could not find a submodule entry for the kit in .gitmodules." >&2
  echo "  Looked for a submodule with path '$KIT_REL' or a URL containing" >&2
  echo "  '$OLD_SLUG'. Nothing matched, so there is nothing to migrate." >&2
  exit 1
fi

OLD_URL="$(git config -f "$GITMODULES" --get "submodule.$SUBMODULE_NAME.url" || true)"
if [ -z "$OLD_URL" ]; then
  echo "ERROR: submodule '$SUBMODULE_NAME' has no url in .gitmodules." >&2
  exit 1
fi

# ── Determine the destination URL ────────────────────────────
if [ -n "$NEW_URL_OVERRIDE" ]; then
  NEW_URL="$NEW_URL_OVERRIDE"
elif printf '%s' "$OLD_URL" | grep -q "$OLD_SLUG"; then
  # Swap only the repository slug, preserving host / protocol / org so that
  # SSH remotes and organization forks continue to resolve.
  NEW_URL="$(printf '%s' "$OLD_URL" | sed "s#${OLD_SLUG}#${NEW_SLUG}#g")"
elif printf '%s' "$OLD_URL" | grep -q "$NEW_SLUG"; then
  # Already points at the successor — re-running is a no-op, not an error.
  echo "Already migrated: the submodule URL already references '$NEW_SLUG':"
  echo "    $OLD_URL"
  echo "Nothing to do."
  exit 0
else
  echo "ERROR: the current submodule URL does not reference '$OLD_SLUG':" >&2
  echo "    $OLD_URL" >&2
  echo "  It may already be migrated, or use a custom URL. If you still need" >&2
  echo "  to change it, pass the destination explicitly:" >&2
  echo "    bash $KIT_NAME/scripts/migrate-to-toolkit.sh https://github.com/rkawaishi/$NEW_SLUG.git" >&2
  exit 1
fi

# ── Report the plan ──────────────────────────────────────────
echo "=== workato-dev-kit → workato-toolkit migration ==="
echo "  Workspace:  $WORKSPACE_ROOT"
echo "  Submodule:  $SUBMODULE_NAME  (path: $KIT_REL)"
echo "  Old URL:    $OLD_URL"
echo "  New URL:    $NEW_URL"
echo ""

if [ "$OLD_URL" = "$NEW_URL" ]; then
  echo "Nothing to do: the submodule URL already points at the destination."
  exit 0
fi

if [ "$DRY_RUN" -eq 1 ]; then
  echo "[dry-run] Would run:"
  echo "  git -C \"$WORKSPACE_ROOT\" config -f .gitmodules submodule.$SUBMODULE_NAME.url \"$NEW_URL\""
  echo "  git -C \"$WORKSPACE_ROOT\" submodule sync -- \"$KIT_REL\""
  echo "  git -C \"$KIT_DIR\" remote set-url origin \"$NEW_URL\""
  echo "  git -C \"$KIT_DIR\" fetch origin"
  echo "  git -C \"$WORKSPACE_ROOT\" submodule update --remote -- \"$KIT_REL\""
  echo ""
  echo "[dry-run] No changes were made."
  exit 0
fi

if [ "$ASSUME_YES" -ne 1 ]; then
  printf "Proceed with the migration? [y/N] "
  read -r reply < /dev/tty || reply=""
  case "$reply" in
    y|Y|yes|YES) ;;
    *) echo "Aborted."; exit 1 ;;
  esac
fi

# ── Apply the change ─────────────────────────────────────────
echo ""
echo "--- Updating .gitmodules ---"
git -C "$WORKSPACE_ROOT" config -f .gitmodules "submodule.$SUBMODULE_NAME.url" "$NEW_URL"

echo "--- Syncing submodule config (git submodule sync) ---"
git -C "$WORKSPACE_ROOT" submodule sync -- "$KIT_REL"

# submodule sync propagates the URL into the submodule's remote, but only
# when the submodule is initialised. Set it explicitly to be safe.
if [ -d "$KIT_DIR/.git" ] || [ -f "$KIT_DIR/.git" ]; then
  echo "--- Pointing submodule 'origin' at the new remote ---"
  git -C "$KIT_DIR" remote set-url origin "$NEW_URL"

  echo "--- Fetching from the new remote ---"
  fetch_ok=0
  for attempt in 1 2 3 4; do
    if git -C "$KIT_DIR" fetch origin; then
      fetch_ok=1
      break
    fi
    wait=$((1 << attempt))  # 2, 4, 8, 16
    echo "  fetch failed (attempt $attempt); retrying in ${wait}s..." >&2
    sleep "$wait"
  done
  if [ "$fetch_ok" -ne 1 ]; then
    echo "WARNING: could not fetch from $NEW_URL after several attempts." >&2
    echo "  The .gitmodules URL has been updated. Once you have network" >&2
    echo "  access, finish with:" >&2
    echo "    git submodule update --init --remote -- $KIT_REL" >&2
    exit 1
  fi

  echo "--- Updating the submodule to the new remote's tracked branch ---"
  git -C "$WORKSPACE_ROOT" submodule update --remote -- "$KIT_REL"
else
  echo "--- Submodule not yet initialised; initialising from the new remote ---"
  git -C "$WORKSPACE_ROOT" submodule update --init --remote -- "$KIT_REL"
fi

# ── Done ─────────────────────────────────────────────────────
echo ""
echo "=== Migration complete ==="
echo ""
echo "The kit submodule now tracks:"
echo "    $NEW_URL"
echo ""
echo "Next steps:"
echo "  1. Re-run setup to refresh editor symlinks/copies:"
echo "       bash $KIT_REL/setup.sh"
echo "  2. Review and commit the change:"
echo "       git add .gitmodules $KIT_REL"
echo "       git commit -m \"Migrate kit submodule to workato-toolkit\""
