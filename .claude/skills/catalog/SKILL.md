---
description: 組織の共有アセット（Recipe Function、コネクション）をスキャンしてカタログ化する。/create-recipe や /design から参照される。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /catalog

組織の `projects/` 配下にある **共有プロジェクト** のアセットをスキャンし、カタログファイルを生成・更新するスキル。
他のスキル（`/create-recipe`, `/design`）がカタログを参照して、既存アセットの再利用を提案する。

**重要**: private スコープのプロジェクトはスキャンしない。部門限定の閲覧制御を尊重する。

## 使い方

- `/catalog` — カタログを表示
- `/catalog scan` — 共有プロジェクトをスキャンしてカタログを再生成
- `/catalog config` — スコープ設定を表示・編集
- `/catalog add <file-path>` — 手動でアセットをカタログに追加

## ファイル構成

```
projects/
├── CATALOG.md              ← 共有アセットカタログ（自動生成）
├── CATALOG_CONFIG.yaml     ← プロジェクトのスコープ定義
├── Shared/                 ← scope: global
├── Finance - Common/       ← scope: team:finance
├── [App] IT Onboarding/    ← scope: private（カタログ対象外）
└── [App] Expense Report/   ← scope: private
```

いずれも `.workatoignore` で保護する。

## プロジェクトスコープ

### CATALOG_CONFIG.yaml

各プロジェクトの公開範囲を定義する:

```yaml
# projects/CATALOG_CONFIG.yaml
projects:
  Shared:
    scope: global          # 全チーム公開、カタログに掲載
    description: 組織横断の共通ロジック・コネクション

  "Finance - Common":
    scope: team:finance    # Finance チーム内で共有、カタログに掲載
    description: 経理部門の共通レシピ

  "[App] IT Onboarding":
    scope: private         # カタログ対象外
    description: IT部門の入社オンボーディング

# 未記載のプロジェクトは private として扱う
```

### スコープの種類

| スコープ | カタログ掲載 | 用途 |
|---|---|---|
| `global` | 全アセットを掲載 | 全チーム共通（Shared プロジェクト等） |
| `team:<name>` | 全アセットを掲載（チーム名付き） | 部門内共通（Finance - Common 等） |
| `private` | **掲載しない** | プロジェクト固有（Workflow App 等） |

### 初回セットアップ

`/catalog config` で対話的に設定:

1. `projects/` 配下のプロジェクト一覧を表示
2. 各プロジェクトのスコープをユーザーに確認
3. `CATALOG_CONFIG.yaml` を生成
4. `.workatoignore` に `CATALOG_CONFIG.yaml` と `CATALOG.md` を追加

## カタログの構造

```markdown
# Shared Asset Catalog
Last updated: <YYYY-MM-DD>

## Connections

| 名前 | Provider | プロジェクト | スコープ |
|---|---|---|---|
| Shared \| Slack | slack_bot | Shared | global |
| Shared \| Jira | jira | Shared | global |
| Finance \| SAP | sap | Finance - Common | team:finance |

## Recipe Functions

### fnc: Get line manager
- **プロジェクト**: Shared (global)
- **ファイル**: `Shared/Recipes/fnc_get_line_manager.recipe.json`
- **入力**: `employee_email` (string) — 従業員のメールアドレス
- **出力**: `manager_name` (string), `manager_email` (string)
- **用途**: HRMS / Google Sheets からマネージャー情報を取得

## MCP Servers

| 名前 | プロジェクト | スコープ | ツール数 |
|---|---|---|---|
| IT Onboarding | Shared | global | 1 |
```

## `/catalog scan` — スキャン手順

### 1. スコープ設定の読み込み

`projects/CATALOG_CONFIG.yaml` を読む。存在しなければ `/catalog config` を案内。

### 2. 対象プロジェクトのフィルタ

`scope` が `global` または `team:*` のプロジェクトのみスキャン対象。
`private` および未記載のプロジェクトはスキップ。

### 3. コネクションの収集

対象プロジェクトの `*.connection.json` をスキャン。
各ファイルから `name` と `provider` を抽出。

### 4. Recipe Function の収集

`fnc_*.recipe.json` または `fnc: *` という名前のレシピをスキャン。
各ファイルから以下を抽出:

- `name` — レシピ名
- `code.input.parameters_schema_json` — 入力パラメータスキーマ（JSON 文字列をパース）
- `code.input.result_schema_json` — 出力スキーマ（JSON 文字列をパース）
- レシピの `comment` — 用途の説明

パラメータスキーマから各フィールドの `name`, `type`, `label`, `optional` を抽出してカタログに記載。

### 5. Workflow App / MCP サーバーの収集

対象プロジェクトの `*.lcap_app.json` と `*.mcp_server.json` をスキャン。

### 6. カタログファイルの生成

収集した情報を `projects/CATALOG.md` に書き出す。
既存のカタログがあれば差分更新（手動で追加した `用途` 等の記述は保持）。

## 他スキルからの参照

### `/create-recipe` からの参照

`/create-recipe` がレシピを生成する際:

1. `projects/CATALOG.md` が存在するか確認
2. 存在すれば読み込み、要件に合致する既存の **共有** アセットを検索:
   - コネクション: 同じ provider の共有コネクションがあるか
   - Recipe Function: 必要なロジックが既に存在するか
3. 合致するアセットがあれば提案:
   ```
   既存の共有アセットが利用可能です:
   - fnc: Get line manager (Shared / global) — マネージャー検索
   - Shared | Slack (slack_bot / global) — Slack コネクション

   これらを使用しますか？
   ```
4. ユーザーが承認すれば、`call_recipe` や `config` で共有アセットを参照するレシピを生成

### `/design` からの参照

`/design new` の Phase 3（技術設計）で:

1. カタログを読み込み
2. ユーザー体験から必要な機能を特定
3. 共有アセットで対応可能な部分を明示
4. 対応できない部分について新規作成を計画

## 共通化の提案

private プロジェクト間でロジックの重複を検出した場合（`/learn-recipe` や `/design` 時）:
- 具体的なコード内容は露出しない
- 「同様のロジックが複数プロジェクトで使われているため、共通の Recipe Function への切り出しを検討してはどうか」と提案する
- 共通化するかどうかはユーザーが判断
- 共通化する場合は scope: global / team の共有プロジェクトに配置し、カタログに登録
