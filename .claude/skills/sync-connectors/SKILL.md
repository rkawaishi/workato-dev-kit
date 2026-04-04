---
description: Workato 公式ドキュメントからコネクタ情報を取得し docs/connectors/ を差分更新する。新規コネクタ追加や既存コネクタの更新に使用。
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch, Agent
---

# /sync-connectors

Workato 公式ドキュメントからコネクタのトリガー/アクション情報を取得し、`docs/connectors/` を更新するスキル。

## 使い方

- `/sync-connectors <connector-name>` — 指定コネクタの情報を取得・更新
- `/sync-connectors <name1> <name2> ...` — 複数コネクタを一括更新
- `/sync-connectors --all` — 未作成の主要コネクタをすべて取得
- `/sync-connectors --check` — 既存ドキュメントと公式の差分を確認

## 実行手順

### 1. コネクタ名から公式ドキュメント URL を特定

`@docs/connectors/_index.md` の全コネクタ一覧からドキュメント URL を検索する。
URL パターン: `https://docs.workato.com/en/connectors/<path>.html`

### 2. 公式ドキュメントからトリガー/アクション情報を取得

コネクタのドキュメントは以下のパターンがある:

**パターン A**: トップページにトリガー/アクション一覧がある
- URL: `/en/connectors/<name>.html`
- WebFetch で直接取得

**パターン B**: サブページに分かれている
- トリガー: `/en/connectors/<name>/triggers.html`
- アクション: `/en/connectors/<name>/actions.html`
- 両方を WebFetch で取得

**パターン C**: トリガー/アクションごとに個別ページ
- トップページのナビゲーションリンクから個別ページを特定
- 各ページから情報を取得

WebFetch のプロンプト例:
```
Extract ALL available triggers and actions for this connector.
For each, list the exact name and a one-line description.
Also note the provider name used in Workato recipes if visible.
```

### 3. docs/connectors/<name>.md を作成/更新

以下のフォーマットで作成:

```markdown
# <コネクタ名> コネクタ

公式: <ドキュメントURL>
Provider: `<provider_name>`

## Triggers
| 名前 | 説明 |
|---|---|
| <trigger_name> | <説明> |

## Actions
| 名前 | 説明 |
|---|---|
| <action_name> | <説明> |

## 備考
- <認証方式、制限事項、重要な注意点>
```

### 4. 差分更新のルール

- **新規作成**: ファイルが存在しなければ新規作成
- **更新**: 既存ファイルがある場合:
  - 公式から取得したトリガー/アクションと比較
  - 新しいものがあれば追加
  - 削除されたものがあれば注記（即削除しない）
  - 「備考」セクションの独自追記は保持する
- **Provider 名の確認**: 実際のレシピ JSON で使用される provider 名がわかっている場合は記載。不明な場合は `(要確認)` と注記

### 5. _index.md の更新

新しくドキュメントを作成したコネクタがあれば、`docs/connectors/_index.md` の「個別ドキュメントあり」セクションにリンクを追加する。

## --all の対象

以下のカテゴリで未作成のコネクタを優先的に取得:

1. **CRM**: Salesforce, HubSpot, Zoho CRM, Microsoft Dynamics 365
2. **HR**: Workday, BambooHR, ADP Workforce Now
3. **コミュニケーション**: Slack, Gmail, Outlook, Microsoft Teams
4. **プロジェクト管理**: Jira, Asana, Trello, Wrike
5. **クラウドストレージ**: Google Drive, Dropbox, Box, OneDrive, SharePoint
6. **データベース**: Snowflake, PostgreSQL, MySQL, Oracle, SQL Server, Redshift
7. **Finance**: NetSuite, QuickBooks, Xero, Stripe
8. **Workato 内部**: AI by Workato, Recipe function, RecipeOps, Workbot for Slack

## --check の動作

1. `docs/connectors/` 内の全 `.md` ファイルを読み取り
2. 各ファイルの公式 URL を取得
3. WebFetch で公式ページの現在のトリガー/アクション一覧を取得
4. ローカルとの差分を報告:
   - ✅ 変更なし
   - ⚠️ 新しいトリガー/アクションが公式に追加
   - ❌ ローカルにあるが公式から削除された項目

## 出力

更新完了後、以下を報告:
- 作成/更新したファイル一覧
- 追加されたトリガー/アクションの数
- 取得できなかった情報（要手動確認）
