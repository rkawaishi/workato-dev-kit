#!/usr/bin/env bash
# sync-cursor-rules.sh
#
# 後方互換ラッパー。実体は scripts/sync_agents.py に移行済み。
# 既存のドキュメント・利用者の手元のメモから呼ばれるためファイルを残してある。

set -eo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$REPO_ROOT/scripts/sync_agents.py" "$@"
