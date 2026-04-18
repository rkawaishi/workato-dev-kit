# リソースプロバイダーレジストリ

レシピ設計時（`/create-recipe`, `/design`）に、接続先リソースの情報を外部ツール経由で自動取得するためのリファレンス。

## 概要

レシピの入力フィールドには、ユーザーが正確な ID やフィールド名を把握していないと設定できない値がある（Jira プロジェクトキー、Slack チャンネル ID 等）。MCP サーバーや CLI ツールが利用可能な場合、自動取得してユーザーに選択肢として提示する。

### 環境固有設定ファイル

利用可能なツールは端末ごとに異なるため、環境固有の設定を `.resource-providers.yml` に記述する。

- **場所**: `workato-dev-kit/.resource-providers.yml`（gitignore 対象）
- **作成**: 初回セットアップ時にユーザーにヒアリングして生成
- **参照**: `/create-recipe` Step 4、`/design` Phase 3 でこのファイルを読む

ファイルが存在しない場合はリソース自動取得をスキップし、従来のヒアリングフローを使う。

### アクセス手段の優先順位

1. **MCP サーバー** — セッションで利用可能な MCP ツール
2. **CLI ツール** — PATH にあるコマンドラインツール
3. **WebFetch** — REST API / OpenAPI spec への直接アクセス
4. **ヒアリング** — 上記が全て利用不可の場合のフォールバック

---

## `.resource-providers.yml` のフォーマット

```yaml
# 環境固有のリソースプロバイダー設定
# このファイルは gitignore 対象。端末ごとに作成する。

providers:
  jira:
    method: mcp
    tool_prefix: "mcp__jira__"           # ToolSearch で検索するプレフィックス
    notes: "Jira Cloud MCP server"       # メモ（任意）

  slack:
    method: mcp
    tool_prefix: "mcp__slack__"

  github:
    method: cli
    command: "gh"                         # which で検出するコマンド名
    auth_check: "gh auth status"         # 認証確認コマンド（任意）

  salesforce:
    method: mcp
    tool_prefix: "mcp__salesforce__"

  google_sheets:
    method: mcp
    tool_prefix: "mcp__google_drive__"   # Google Drive MCP 経由でシートも操作可能な場合

  workato:
    method: cli
    command: "workato"
```

### フィールド説明

| フィールド | 必須 | 説明 |
|---|---|---|
| `method` | Yes | `mcp`, `cli`, `webfetch` のいずれか |
| `tool_prefix` | MCP 時 | `ToolSearch` で検索するプレフィックス（例: `mcp__jira__`） |
| `command` | CLI 時 | `which` で検出するコマンド名（例: `gh`） |
| `auth_check` | No | 認証状態を確認するコマンド（例: `gh auth status`） |
| `base_url` | No | WebFetch 時の API ベース URL |
| `notes` | No | メモ（人間向け） |

ユーザーが利用しないプロバイダーは記載不要。記載があるプロバイダーのみ自動取得を試みる。

---

## プロバイダー別: 取得したい情報

各プロバイダーに対して「何を取得すべきか」を定義する。具体的なツール名やコマンドは `.resource-providers.yml` の設定と実際のツールのスキーマに従う。

### Jira

| 取得したい情報 | レシピでの用途 | 取得のヒント |
|---|---|---|
| プロジェクト一覧（キー・名前） | プロジェクトキー指定 | "list projects" 系のツール/API |
| Issue Type 一覧 | イシュータイプ指定 | プロジェクト指定で取得 |
| カスタムフィールド一覧（名前・ID） | `customfield_XXXXX` の特定 | "get fields" 系のツール/API |
| ステータス一覧 | トランジション指定 | プロジェクト/ワークフロー指定 |
| 優先度一覧 | 優先度指定 | グローバル設定 |

### Slack

| 取得したい情報 | レシピでの用途 | 取得のヒント |
|---|---|---|
| チャンネル一覧（名前・ID） | メッセージ投稿先の `channel_id` | "list channels" 系。名前と ID の両方を取得 |
| ユーザー一覧（名前・ID） | DM 送信先の `user_id` | "list users" 系 |

### GitHub

| 取得したい情報 | レシピでの用途 | CLI コマンド |
|---|---|---|
| リポジトリ一覧 | トリガー/アクションの対象 | `gh repo list <owner> --json name,description --limit 50` |
| ラベル一覧 | Issue 作成時のラベル | `gh label list -R <owner/repo> --json name` |
| マイルストーン一覧 | Issue のマイルストーン | `gh api repos/<owner>/<repo>/milestones --jq '.[].title'` |
| ブランチ一覧 | ブランチ指定 | `gh api repos/<owner>/<repo>/branches --jq '.[].name'` |

### Salesforce

| 取得したい情報 | レシピでの用途 | 取得のヒント |
|---|---|---|
| オブジェクト一覧 | 対象オブジェクト指定 | "list objects" / `sf sobject list` |
| フィールド一覧（名前・型） | フィールドマッピング | "describe object" / `sf sobject describe -s <obj>` |
| PickList 値 | 選択肢の事前解決 | describe 結果の picklistValues |
| レコードタイプ | RecordTypeId 指定 | describe 結果の recordTypeInfos |

### Google Sheets

| 取得したい情報 | レシピでの用途 | 取得のヒント |
|---|---|---|
| スプレッドシート一覧 | スプレッドシート ID | Google Drive の検索/一覧 |
| シート名一覧 | シート名指定 | スプレッドシート ID 指定で取得 |
| ヘッダー行 | カラム名のマッピング | 1行目の読み取り |

### Google Drive

| 取得したい情報 | レシピでの用途 | 取得のヒント |
|---|---|---|
| フォルダ一覧 | アップロード先フォルダ ID | "list files" でフォルダ型をフィルタ |
| ファイル一覧 | 対象ファイル ID | "list files" / "search files" |

### Workato

| 取得したい情報 | レシピでの用途 | CLI コマンド |
|---|---|---|
| コネクション一覧 | コネクション ID | `workato exec connections.list` |
| レシピ一覧 | `call_recipe` の対象 | `workato exec recipes.list` |
| フォルダ構成 | `zip_name` / `folder` 指定 | `workato exec folders.list` |

### 任意の REST API

| 取得したい情報 | レシピでの用途 | 取得のヒント |
|---|---|---|
| エンドポイント一覧 | HTTP アクションの URL | WebFetch で OpenAPI spec を取得 |
| リクエスト/レスポンススキーマ | input/output フィールド定義 | OpenAPI spec の schemas |
| 認証方式 | コネクション設定の参考 | OpenAPI spec の securitySchemes |

---

## スキルでの利用手順

### 1. 環境設定の読み込み

`.resource-providers.yml` を読む。ファイルが存在しない場合はリソース自動取得をスキップ。

### 2. 対象プロバイダーの照合

レシピで使用するプロバイダーが `.resource-providers.yml` に定義されているか確認。

### 3. ツールの検出と実行

```
method が mcp の場合:
  → ToolSearch で tool_prefix を検索
  → 見つかったツールのスキーマを読み、適切なツールを実行

method が cli の場合:
  → which <command> で存在確認
  → auth_check があれば認証状態を確認
  → 上記テーブルのコマンドを実行

method が webfetch の場合:
  → base_url を使って API にアクセス
```

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

以下の場合は従来のヒアリングにサイレントに移行する:
- `.resource-providers.yml` が存在しない
- 対象プロバイダーが定義されていない
- ツールの検出に失敗した
- リソース取得でエラーが発生した

エラーメッセージは表示せず、自然にヒアリングフローに移行する。

---

## 初回セットアップ

`.resource-providers.yml` が存在しない状態で `/create-recipe` や `/design` を実行した場合、以下のようにセットアップを案内する:

```
リソース自動取得の設定ファイル (.resource-providers.yml) がまだありません。
外部サービスのリソース情報（Jira プロジェクト一覧、Slack チャンネル等）を
自動取得できるように設定しますか？

設定する場合、利用している MCP サーバーや CLI ツールを教えてください:
- Jira MCP を使っていますか？ → ツール名のプレフィックスは？（例: mcp__jira__）
- Slack MCP を使っていますか？
- gh CLI は入っていますか？
- その他、利用可能な MCP サーバーや CLI はありますか？

スキップする場合は「スキップ」と入力してください（従来通りヒアリングで進めます）。
```
