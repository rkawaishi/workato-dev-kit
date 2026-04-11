---
description: 組織の共有アセット（Recipe Function、コネクション）をスキャンしてカタログ化する。/create-recipe や /design から参照される。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /catalog

組織の `projects/` 配下にある共有アセットをスキャンし、カタログファイルを生成・更新するスキル。
他のスキル（`/create-recipe`, `/design`）がカタログを参照して、既存アセットの再利用を提案する。

## 使い方

- `/catalog` — カタログを表示
- `/catalog scan` — `projects/` 配下をスキャンしてカタログを再生成
- `/catalog scan <project-name>` — 特定プロジェクトのみスキャン
- `/catalog add <file-path>` — 手動でアセットをカタログに追加

## カタログファイル

`projects/CATALOG.md`

組織リポジトリ（`projects/` 内）に配置。`.workatoignore` で保護。

## カタログの構造

```markdown
# Shared Asset Catalog
Last updated: <YYYY-MM-DD>

## Connections

| 名前 | Provider | プロジェクト | 共有スコープ |
|---|---|---|---|
| Shared \| Slack | slack_bot | Shared | 全プロジェクト |
| Shared \| Jira | jira | Shared | 全プロジェクト |

## Recipe Functions

### fnc: Get line manager
- **プロジェクト**: Shared
- **ファイル**: `Shared/Recipes/fnc_get_line_manager.recipe.json`
- **入力**: `employee_email` (string) — 従業員のメールアドレス
- **出力**: `manager_name` (string), `manager_email` (string)
- **用途**: HRMS / Google Sheets からマネージャー情報を取得

### fnc: Send Slack notification
- **プロジェクト**: Shared
- **ファイル**: `Shared/Recipes/fnc_send_slack_notification.recipe.json`
- **入力**: `channel` (string), `message` (string), `thread_ts` (string, optional)
- **出力**: `ok` (boolean), `ts` (string)
- **用途**: Slack チャンネルに通知を送信

## Workflow Apps

| 名前 | プロジェクト | Data Table | ステージ |
|---|---|---|---|
| IT Onboarding | [App] IT Onboarding | IT Onboarding Requests | New → Manager review → Done / Canceled |
```

## `/catalog scan` — スキャン手順

### 1. プロジェクト一覧の取得

`projects/` 配下のサブディレクトリを走査:
```bash
find projects/ -name ".workatoenv" -maxdepth 2 -exec dirname {} \;
```

### 2. コネクションの収集

各プロジェクトの `*.connection.json` をスキャン:
```
projects/<project>/Connections/*.connection.json
projects/<project>/*.connection.json
```

各ファイルから `name` と `provider` を抽出。

### 3. Recipe Function の収集

`fnc_*.recipe.json` または `fnc: *` という名前のレシピをスキャン。
各ファイルから以下を抽出:

- `name` — レシピ名
- `code.input.parameters_schema_json` — 入力パラメータスキーマ（JSON 文字列をパース）
- `code.input.result_schema_json` — 出力スキーマ（JSON 文字列をパース）
- レシピの `comment` — 用途の説明

パラメータスキーマから各フィールドの `name`, `type`, `label`, `optional` を抽出してカタログに記載。

### 4. Workflow App の収集

`*.lcap_app.json` をスキャン。各ファイルから以下を抽出:
- `name` — アプリ名
- `workato_db_table.name` — Data Table 名
- `workflow_stages[].name` — ステージ一覧

### 5. MCP サーバーの収集

`*.mcp_server.json` をスキャン。各ファイルから以下を抽出:
- `name` — サーバー名
- `tools[].description` — ツールの説明

### 6. カタログファイルの生成

収集した情報を `projects/CATALOG.md` に書き出す。
既存のカタログがあれば差分更新（手動で追加した `用途` 等の記述は保持）。

## `/catalog add <file-path>` — 手動追加

スキャン対象外のアセットや、用途の説明を手動で追加する場合に使用。

1. 指定ファイルを読む
2. アセット種別を判定（connection / recipe / lcap_app / mcp_server）
3. カタログの該当セクションに追記
4. Recipe Function の場合はインターフェース（入力/出力）を自動抽出

## 他スキルからの参照

### `/create-recipe` からの参照

`/create-recipe` がレシピを生成する際、以下のステップを追加:

1. `projects/CATALOG.md` が存在するか確認
2. 存在すれば読み込み、要件に合致する既存アセットを検索:
   - コネクション: 同じ provider のコネクションが共有されているか
   - Recipe Function: 必要なロジック（マネージャー取得、通知送信等）が既に存在するか
3. 合致するアセットがあれば提案:
   ```
   既存の共有アセットが利用可能です:
   - fnc: Get line manager (Shared) — マネージャー検索が必要な場合
   - Shared | Slack (slack_bot) — Slack 通知用コネクション
   
   これらを使用しますか？
   ```
4. ユーザーが承認すれば、`call_recipe` や `config` で共有アセットを参照するレシピを生成

### `/design` からの参照

`/design new` の Phase 3（技術設計）で:

1. カタログを読み込み
2. ユーザー体験から必要な機能を特定
3. 既存の共有アセットで対応可能な部分を明示:
   ```
   ## Architecture
   
   ### 既存アセットの再利用
   - マネージャー取得: `fnc: Get line manager` (Shared) を使用
   - Slack 通知: `Shared | Slack` コネクションを使用
   
   ### 新規作成が必要
   - メインレシピ（承認フロー）
   - Jira チケット起票ロジック
   ```
