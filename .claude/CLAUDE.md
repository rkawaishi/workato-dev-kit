# Workato Dev Kit

Workato (エンタープライズ iPaaS) の自動化開発を Claude Code / Cursor で行うためのツールキット。
レシピ開発とカスタムコネクタ開発の両方をカバーする。

## プロジェクト構造

```
<workspace-root>/
  projects/                  # レシピプロジェクト（Platform CLI 管理）
    <project-name>/
      *.recipe.json          # レシピ（ワークフロー定義）
      *.connection.json      # コネクション（接続情報）
      *.agentic_genie.json   # Genie（AIエージェント定義）
      *.agentic_skill.json   # Genieスキル定義
      *.mcp_server.json      # MCP サーバー定義
      .workatoenv            # プロジェクト設定（project_id等）
  connectors/                # カスタムコネクタ（Connector SDK）
    <connector-name>/
      connector.rb           # コネクタ定義（Ruby DSL）
      settings.yaml          # 認証情報（開発用）
      spec/                  # テスト
  docs/
    logic/                   # レシピのロジック（公式ドキュメントベース）
      triggers.md            # トリガーの種類、条件、Since
      if-conditions.md       # IF/ELSE IF/ELSE + 14条件演算子
      loops.md               # repeat-while, repeat-for-each
      error-handling.md      # Monitor/Error ブロック、Recipe Functions
      data-pills.md          # データピル、マッピング、型変換
      formulas.md            # フォーミュラ操作
      file-handling.md       # ファイル処理
    patterns/                # 設計パターン
      shared-assets.md       # 共有アセット（Shared プロジェクト、Recipe Function 設計）
    connectors/              # Pre-built コネクタナレッジ（139件）
      _index.md              # 全コネクタ一覧 + 分類
    platform/                # Workato プラットフォーム機能
      data-tables.md         # Data Tables
      lookup-tables.md       # Lookup Tables
      environment-properties.md # Environment Properties
      event-streams.md       # Event Streams
      workflow-apps.md       # Workflow Apps
      api-platform.md        # API Platform
      insights.md            # Insights
      data-orchestration.md  # Data Orchestration
      workbot.md             # Workbot
      agent-studio.md        # Agent Studio（Genie）
      mcp.md                 # MCP
    connector-sdk/           # Connector SDK リファレンス
      overview.md            # SDK 概要、CLI コマンド、プロジェクト構造
      connector-rb.md        # connector.rb 全ブロックリファレンス
    learned-patterns.md      # 一時保管用（分類先が不明な知見のみ。通常は各ドキュメントに直接追記）
  .claude/
    rules/                   # フォーマットルール + ガイダンス
      workato-recipe-format.md    # レシピ JSON
      workato-agentic-format.md   # Genie/Skill/MCP Server/Workflow App JSON
      workato-connector-sdk.md    # connector.rb (Ruby DSL)
      workato-project-structure.md # プロジェクト内ディレクトリ構成
      workato-shared-assets.md    # 共有アセットガイダンス
    skills/                  # 開発スキル
      create-recipe/         # /create-recipe
      create-genie/          # /create-genie
      create-workflow-app/    # /create-workflow-app
      create-connector/      # /create-connector
      validate-recipe/       # /validate-recipe
      wpull/                 # /wpull
      wpush/                 # /wpush
      learn-recipe/          # /learn-recipe
      sync-connectors/       # /sync-connectors
```

## ナレッジの参照優先順位

### レシピ開発
1. `@docs/connectors/` — コネクタのトリガー/アクション/フィールド一覧
2. `@docs/logic/` — ロジックステップの組み方（datapill 記法含む）
3. `@docs/platform/` — プラットフォーム機能の理解
4. `@.claude/rules/workato-recipe-format.md` / `workato-agentic-format.md`
5. `@docs/patterns/` — デプロイガイド、共有アセットパターン

### カスタムコネクタ開発
1. `@docs/connector-sdk/connector-rb.md` — connector.rb リファレンス
2. `@docs/connector-sdk/overview.md` — SDK 概要・CLI コマンド
3. `@.claude/rules/workato-connector-sdk.md` — フォーマットルール

## CLI ツール

### Platform CLI（レシピ管理）

2つのバリアントがある。インストール済みの方を使用する:

| | 本家 | フォーク (rkawaishi) |
|---|---|---|
| インストール | `pipx install workato-platform-cli` | `pipx install git+https://github.com/rkawaishi/workato-platform-cli.git` |
| 追加機能 | — | Jobs, SDK統合, OAuth Profile管理, workspace_id自動解決 |
| リポジトリ | [workato-devs/workato-platform-cli](https://github.com/workato-devs/workato-platform-cli) | [rkawaishi/workato-platform-cli](https://github.com/rkawaishi/workato-platform-cli) |

共通コマンド:
- Pull: `workato projects use "<name>" && workato pull`
- Push: `workato push`
- Init: `workato init --non-interactive --profile <profile> --project-id <id> --folder-name "projects/<name>"`

フォーク版の追加コマンド:
- Jobs: `workato jobs list` / `workato jobs get <id>`
- SDK: `workato sdk new <path>` / `workato sdk push` / `workato sdk exec` / `workato sdk generate schema`
- OAuth: `workato oauth-profiles list` / `create` / `update` / `delete`
- Connectors: `workato connectors` 管理

### Connector SDK CLI（コネクタ開発）

本家 CLI の場合:
- インストール: `gem install workato-connector-sdk`
- 新規作成: `workato new connectors/<name>`
- テスト: `workato exec connectors/<name>/connector.rb test`
- Push: `workato push connectors/<name>`

フォーク版 CLI の場合（SDK コマンド統合済み）:
- 新規作成: `workato sdk new connectors/<name>`
- テスト: `workato sdk exec connectors/<name>/connector.rb test`
- Push: `workato sdk push connectors/<name>`
- スキーマ生成: `workato sdk generate schema connectors/<name>`

## コネクタの分類

- **Pre-built**: Workato 公式の標準コネクタ（1,000+）
- **Universal**: HTTP, OpenAPI, GraphQL, SOAP — 標準にない API 用
- **Community**: ユーザー共有コネクタ
- **Custom**: Connector SDK で自作 → `connectors/` ディレクトリ
- **Custom Action**: コネクタ内の `__adhoc_http_action` で API 直接呼出し

## 開発ルール

- レシピ JSON: `@.claude/rules/workato-recipe-format.md` を参照
- Genie/Skill/MCP: `@.claude/rules/workato-agentic-format.md` を参照
- カスタムコネクタ: `@.claude/rules/workato-connector-sdk.md` を参照
- コネクタ詳細: `@docs/connectors/` を参照。未作成分は WebFetch
- 新しい独自知見は適切なドキュメントに直接追記（`docs/learned-patterns.md` は一時保管のみ）
- `*.connection.json` に認証情報は含まれない
- `.workatoenv` / `master.key` はコミットしない
