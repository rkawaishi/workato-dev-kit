# リソースプロバイダーレジストリ

レシピ設計時（`/create-recipe`, `/design`）に、接続先リソースの情報を外部ツール経由で自動取得するためのリファレンス。

## 概要

レシピの入力フィールドには、ユーザーが正確な ID やフィールド名を把握していないと設定できない値がある（Jira プロジェクトキー、Slack チャンネル ID 等）。MCP サーバーや CLI ツールが利用可能な場合、自動取得してユーザーに選択肢として提示する。

### 優先順位

1. **MCP サーバー** — セッションで利用可能な MCP ツール
2. **CLI ツール** — PATH にあるコマンドラインツール
3. **WebFetch** — OpenAPI spec や REST API エンドポイントへの直接アクセス
4. **ヒアリング** — 上記が全て利用不可の場合のフォールバック

### 検出方法

- **MCP ツール**: `ToolSearch` で `mcp__<provider>__` を検索し、ツールが存在するか確認
- **CLI ツール**: `which <command>` で PATH にあるか確認
- 検出に失敗した場合はサイレントにヒアリングにフォールバック（エラーを出さない）

---

## プロバイダー別リファレンス

### GitHub

| 項目 | 値 |
|---|---|
| Workato プロバイダー名 | `github` |
| 検出 | `which gh` で `gh` CLI の存在を確認 |
| 認証確認 | `gh auth status` |

#### 取得可能な情報

| 情報 | コマンド | レシピでの用途 |
|---|---|---|
| リポジトリ一覧 | `gh repo list <owner> --json name,description --limit 50` | トリガー/アクションの対象リポジトリ |
| ラベル一覧 | `gh label list -R <owner/repo> --json name` | Issue 作成時のラベル指定 |
| マイルストーン一覧 | `gh api repos/<owner>/<repo>/milestones --jq '.[].title'` | Issue 作成時のマイルストーン |
| Issue テンプレート | `ls <repo>/.github/ISSUE_TEMPLATE/` | Issue 本文のテンプレート |
| ブランチ一覧 | `gh api repos/<owner>/<repo>/branches --jq '.[].name'` | ブランチ指定 |

#### ヒアリングとの統合例

```
従来: 「対象のリポジトリは？」→ ユーザーが手入力
改善: gh repo list → 「以下のリポジトリがあります。どれを使いますか？」
      1. workato-dev-kit
      2. my-app
      → ユーザーが番号で選択
```

---

### Jira

| 項目 | 値 |
|---|---|
| Workato プロバイダー名 | `jira` |
| 検出 | `ToolSearch` で `mcp__jira__` を検索 |
| フォールバック | Jira REST API v3 を WebFetch（要ベース URL） |

#### 取得可能な情報（MCP 経由）

| 情報 | MCP ツール候補 | レシピでの用途 |
|---|---|---|
| プロジェクト一覧 | `mcp__jira__list_projects` 等 | プロジェクトキー指定 |
| Issue Type 一覧 | `mcp__jira__get_issue_types` 等 | イシュータイプ指定 |
| カスタムフィールド | `mcp__jira__get_fields` 等 | カスタムフィールド ID（customfield_XXXXX） |
| ステータス一覧 | `mcp__jira__get_statuses` 等 | トランジション指定 |
| 優先度一覧 | `mcp__jira__get_priorities` 等 | 優先度指定 |

> **注意**: MCP ツール名はサーバーの実装により異なる。`ToolSearch` の結果から実際のツール名を特定すること。

---

### Slack

| 項目 | 値 |
|---|---|
| Workato プロバイダー名 | `slack`, `slack_bot` |
| 検出 | `ToolSearch` で `mcp__slack__` を検索 |

#### 取得可能な情報（MCP 経由）

| 情報 | MCP ツール候補 | レシピでの用途 |
|---|---|---|
| チャンネル一覧 | `mcp__slack__list_channels` 等 | メッセージ投稿先の channel_id |
| ユーザー一覧 | `mcp__slack__list_users` 等 | DM 送信先の user_id |
| チャンネル情報 | `mcp__slack__get_channel_info` 等 | チャンネル名 → ID の解決 |

#### ヒアリングとの統合例

```
従来: 「どのチャンネルに投稿しますか？」→「#general」→ ID 不明で push 後エラー
改善: MCP → チャンネル一覧取得 → 「以下のチャンネルがあります:」
      1. #general (C01234567)
      2. #it-helpdesk (C07654321)
      → 正確な channel_id でレシピ生成
```

---

### Salesforce

| 項目 | 値 |
|---|---|
| Workato プロバイダー名 | `salesforce` |
| 検出 | `ToolSearch` で `mcp__salesforce__` を検索 |
| フォールバック | `sf` CLI (`which sf`) |

#### 取得可能な情報

| 情報 | 取得方法 | レシピでの用途 |
|---|---|---|
| オブジェクト一覧 | MCP or `sf sobject list` | 対象オブジェクト指定 |
| フィールド一覧 | MCP or `sf sobject describe -s <object>` | フィールドマッピング |
| PickList 値 | MCP or describe の result | 選択肢の事前解決 |
| レコードタイプ | MCP or describe の result | RecordTypeId 指定 |

---

### Google Sheets

| 項目 | 値 |
|---|---|
| Workato プロバイダー名 | `google_sheets` |
| 検出 | `ToolSearch` で `mcp__google_sheets__` または `mcp__google_drive__` を検索 |

#### 取得可能な情報

| 情報 | 取得方法 | レシピでの用途 |
|---|---|---|
| スプレッドシート一覧 | MCP（Google Drive 検索） | スプレッドシート ID |
| シート名一覧 | MCP | シート名指定 |
| ヘッダー行 | MCP（1行目を読み取り） | カラム名のマッピング |

---

### Google Drive

| 項目 | 値 |
|---|---|
| Workato プロバイダー名 | `google_drive` |
| 検出 | `ToolSearch` で `mcp__google_drive__` を検索 |

#### 取得可能な情報

| 情報 | 取得方法 | レシピでの用途 |
|---|---|---|
| フォルダ一覧 | MCP | アップロード先フォルダ ID |
| ファイル一覧 | MCP | 対象ファイル ID |

---

### Workato 自身

| 項目 | 値 |
|---|---|
| Workato プロバイダー名 | `workato` |
| 検出 | `which workato` で CLI の存在を確認 |

#### 取得可能な情報

| 情報 | コマンド | レシピでの用途 |
|---|---|---|
| コネクション一覧 | `workato exec connections.list` | コネクション ID |
| レシピ一覧 | `workato exec recipes.list` | call_recipe の対象 |
| フォルダ構成 | `workato exec folders.list` | zip_name / folder 指定 |

---

### 任意の REST API

| 項目 | 値 |
|---|---|
| Workato プロバイダー名 | カスタムコネクタ依存 |
| 検出 | ユーザーから OpenAPI spec URL を取得 |

#### 取得可能な情報

| 情報 | 取得方法 | レシピでの用途 |
|---|---|---|
| エンドポイント一覧 | WebFetch で OpenAPI spec を取得 | HTTP アクションの URL |
| リクエスト/レスポンススキーマ | OpenAPI spec の schemas | input/output フィールド定義 |
| 認証方式 | OpenAPI spec の securitySchemes | コネクション設定の参考 |

---

## スキルでの利用手順

### 1. プロバイダーの特定

レシピで使用するプロバイダーを特定する（ヒアリングの結果から）。

### 2. ツールの検出

```
プロバイダーが github の場合:
  → which gh を実行

プロバイダーが jira, slack, salesforce, google_sheets, google_drive の場合:
  → ToolSearch で mcp__<provider>__ を検索

プロバイダーが workato の場合:
  → which workato を実行
```

### 3. リソース情報の取得

検出に成功した場合、このドキュメントの該当セクションを参照して適切なコマンド/ツールを実行。

### 4. ユーザーへの提示

取得した情報を選択肢としてユーザーに提示:

```
リソース情報を取得しました。以下から選択してください:

**Jira プロジェクト:**
1. DEV - Development
2. OPS - Operations
3. IT - IT Support

**Issue Type (DEV):**
- Bug, Story, Task, Epic

どのプロジェクトに起票しますか？
```

### 5. フォールバック

検出に失敗した場合、または取得でエラーが発生した場合:
- エラーメッセージは表示しない
- 従来通りユーザーへのヒアリングで値を収集する
- 「正確な値が不明な場合は push 後に UI で確認・修正してください」と案内する
