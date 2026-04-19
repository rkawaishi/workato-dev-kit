# Workato Dev Kit ガイド

本ツールキットは **Claude Code** と **Cursor** の両方に対応している。スキル (`/create-recipe` 等) やルールはどちらのエディタでも同じ形式で利用できる。

## はじめに

| ガイド | 内容 |
|---|---|
| [Claude Code クイックスタート](quickstart-claude-code.md) | Claude Code でのセットアップと初回開発 |
| [Cursor クイックスタート](quickstart-cursor.md) | Cursor でのセットアップとルール同期 |

> **Note:** スキル・ルールの正本は `.claude/` にあり、Cursor 用の `.cursor/` は `bash scripts/sync-cursor-rules.sh` で同期される。詳細は [設計思想・アーキテクチャ](architecture.md) を参照。

## 設計思想

| ガイド | 内容 |
|---|---|
| [設計思想・アーキテクチャ](architecture.md) | デュアルリポジトリ、ナレッジ階層、学習サイクル、スキル/ルール体系 |

## 開発ガイド

| ガイド | 内容 |
|---|---|
| [ライフサイクルと責務マップ](lifecycle.md) | 各スキル・docs の「いつ・誰が・何のために」呼ぶ/書く/読むかの全体像 |
| [スキルリファレンス](skills-reference.md) | 全 12 スキルの用途・オプション・使い方 |
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
