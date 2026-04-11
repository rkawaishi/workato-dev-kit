---
description: プロジェクトの設計書 (DESIGN.md) を作成・更新・参照する。セッション開始時やタスク完了時に使用。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /design

プロジェクトの設計書 (DESIGN.md) を管理するスキル。設計書はセッション跨ぎの計画・進捗・意思決定の永続記録。

## 使い方

- `/design` — 現在のプロジェクトの設計書を表示
- `/design <project-name>` — 指定プロジェクトの設計書を表示
- `/design new <project-name>` — 新規設計書を作成
- `/design update` — 現在の進捗で設計書を更新

## 設計書の場所

`projects/<project-name>/DESIGN.md`

プロジェクトフォルダ直下に配置。`.workatoignore` に `DESIGN.md` を含めて `workato pull` で消えないようにする。

## 設計書のテンプレート

```markdown
# <プロジェクト名>

## Status: <Draft | In Progress | Testing | Done>
Last updated: <YYYY-MM-DD>

## Overview
- **目的**: <何のためのプロジェクトか>
- **トリガー**: <何がきっかけで動くか>
- **主要フロー**: <概要>

## Architecture
- **Data Table**: <テーブル名、主要フィールド>
- **ステージ**: <ワークフローステージ>
- **外部連携**: <Jira, Slack, etc.>
- **レシピ構成**:
  - メインレシピ: <説明>
  - Recipe Function: <説明>
  - その他: <説明>

## Implementation Checklist
- [ ] Data Table スキーマ
- [ ] ページ（送信/レビュー/承認/却下）
- [ ] メインレシピ
- [ ] Recipe Function
- [ ] コネクション認証
- [ ] MCP サーバー（必要な場合）
- [ ] エンドツーエンドテスト
- [ ] pull → learn-recipe

## Decisions
<!-- 設計判断とその理由を記録 -->

## Open Issues
<!-- 未解決の問題 -->
```

## 操作

### `/design` / `/design <project-name>` — 参照

1. `projects/<project-name>/DESIGN.md` を読む
2. 内容を表示
3. 未完了のチェックリスト項目があれば次のアクションを提案

### `/design new <project-name>` — 新規作成

1. テンプレートからDESIGN.md を生成
2. ユーザーに概要をヒアリングして埋める
3. `projects/<project-name>/DESIGN.md` に書き出す
4. `.workatoignore` に `DESIGN.md` が含まれているか確認。なければ追加

### `/design update` — 更新

1. 現在の DESIGN.md を読む
2. プロジェクト内のファイルを確認し、実装済み項目を特定:
   - `*.recipe.json` があれば → レシピ項目をチェック
   - `*.lcap_page.json` があれば → ページ項目をチェック
   - `*.workato_db_table.json` があれば → Data Table 項目をチェック
   - `*.mcp_server.json` があれば → MCP 項目をチェック
   - `*.connection.json` があれば → コネクション項目をチェック
3. チェックリストを更新
4. Status と Last updated を更新
5. 変更内容をサマリー表示

## `.workatoignore` の管理

新規プロジェクトで DESIGN.md を作成する際、`.workatoignore` がなければ作成する:

```
DESIGN.md
```

既存の `.workatoignore` に `DESIGN.md` がなければ追記する。
