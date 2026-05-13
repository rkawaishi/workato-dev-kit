#!/usr/bin/env bash
# sync-cursor-rules.sh
#
# Backwards-compatible wrapper. The implementation lives in
# scripts/sync_agents.py. This file is kept because existing
# documentation and user notes still reference it.

set -eo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$REPO_ROOT/scripts/sync_agents.py" "$@"
