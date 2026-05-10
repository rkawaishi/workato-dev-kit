# Workato Dev Kit ガイド

本ツールキットは **Claude Code** / **Cursor** / **Codex CLI** / **Gemini CLI** に対応している。スキル (`/create-recipe` 等) やルールはどのエディタでも同じ形式で利用できる（Codex のみ `/foo` の代わりに `$foo` 構文）。

## はじめに

| ガイド | 内容 |
|---|---|
| [Claude Code クイックスタート](quickstart-claude-code.md) | Claude Code でのセットアップと初回開発 |
| [Cursor クイックスタート](quickstart-cursor.md) | Cursor でのセットアップとルール同期 |

> **Note:** スキル・ルールの正本は kit の `framework/claude/` にあり、`framework/{cursor,codex,gemini}/` および `framework/AGENTS.md` は `python3 scripts/sync_agents.py` で kit メンテナーが事前生成している。利用者は `bash kit/setup.sh` で各エディタ用ディレクトリへの symlink が張られる（個別に sync を回す必要はない）。詳細は [設計思想・アーキテクチャ](architecture.md) を参照。

## 設計思想

| ガイド | 内容 |
|---|---|
| [設計思想・アーキテクチャ](architecture.md) | デュアルリポジトリ、ナレッジ階層、学習サイクル、スキル/ルール体系 |

## 開発ガイド

| ガイド | 内容 |
|---|---|
| [ライフサイクルと責務マップ](lifecycle.md) | 各スキル・docs の「いつ・誰が・何のために」呼ぶ/書く/読むかの全体像 |
| [スキルリファレンス](skills-reference.md) | 全 13 スキルの用途・オプション・使い方 |
| [デプロイ手順](deployment.md) | レシピ、Workflow App、Genie/MCP のデプロイとトラブルシューティング |
| [レシピパターン](recipe-patterns.md) | パターンカタログの仕組みと活用方法 |

## 機能別ガイド

| ガイド | 内容 |
|---|---|
| [Workflow App 構築](workflow-apps.md) | 承認ワークフロー等の Workflow App を JSON で構築 |
| [Genie & MCP 構築](genie-and-mcp.md) | AI エージェント (Genie) と MCP サーバーの構築 |
| [カスタムコネクタ開発](connector-development.md) | Connector SDK でカスタム API コネクタを開発 |

## 運用ガイド

| ガイド | 内容 |
|---|---|
| [ナレッジ管理](knowledge-management.md) | 学習サイクル、ナレッジベースの育て方 |
| [共有アセット管理](shared-assets.md) | ワークスペース構成、命名規則、カタログ運用 |
