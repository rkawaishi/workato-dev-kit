# Workato Dev Kit

Workato (エンタープライズ iPaaS) の自動化開発を Claude Code / Cursor で行うためのツールキット。

## リポジトリ構造（デュアルリポジトリ）

このリポジトリは **フレームワーク** であり、組織固有のレシピプロジェクトは含まない。

```
workato-dev-kit/              ← このリポジトリ（スキル・ルール・ナレッジ）
├── .claude/
│   ├── rules/                # パス別フォーマットルール（7ファイル）
│   ├── skills/               # 開発スキル（12個）
│   └── hooks/                # 自動化フック
├── guides/                   # 利用者向けガイド
│   ├── quickstart-claude-code.md
│   ├── quickstart-cursor.md
│   └── recipe-patterns.md    # パターンカタログの使い方
├── docs/                     # AI向けナレッジベース
│   ├── logic/                # レシピロジック（7ファイル）
│   ├── connectors/           # コネクタ知識（316件）
│   ├── platform/             # プラットフォーム機能（11ファイル）
│   ├── patterns/             # 設計パターン・デプロイガイド
│   └── connector-sdk/        # Connector SDK リファレンス
│
├── connectors/               ← 組織の別リポジトリ（gitignore 対象）
│   ├── docs/                  # カスタムコネクタのナレッジ（自動生成）
│   └── <name>/
│       └── connector.rb       # Connector SDK ソース
│
└── projects/                 ← 組織の別リポジトリ（gitignore 対象）
    ├── docs/
    │   └── patterns/          # 組織ドメインのレシピ構築パターン
    └── <project-name>/
        ├── DESIGN.md          # 設計書（組織リポジトリで git 管理）
        ├── .workatoenv
        ├── Recipes/
        ├── Pages/
        ├── Connections/
        ├── Data Tables/
        └── Agents/
```

### 2つの git リポジトリ

| | workato-dev-kit | projects/ / connectors/ |
|---|---|---|
| **内容** | スキル、ルール、ドキュメント | レシピ、ページ、コネクタ |
| **性質** | フレームワーク（汎用） | 組織固有 |
| **進化方法** | PR でスキル学習結果を反映 | 組織内で開発・コミット |
| **git 管理** | このリポジトリ | 組織の別リポジトリ |

### 設計書 (DESIGN.md)

各プロジェクトに `DESIGN.md` を配置。セッション開始時に読み、実装後に更新する。
`.workatoignore` に含めて `workato pull` で消えないようにする。
作成・更新は `/design` スキルを使用。

## ナレッジの参照優先順位

### レシピ開発
1. `@docs/connectors/` — Pre-built コネクタのトリガー/アクション/フィールド一覧
2. `@connectors/docs/` — カスタムコネクタのトリガー/アクション/フィールド一覧
3. `@docs/logic/` — ロジックステップの組み方（datapill 記法含む）
4. `@docs/platform/` — プラットフォーム機能の理解
5. `@.claude/rules/` — JSON フォーマット、プロジェクト構造
6. `@docs/patterns/recipe-patterns/` — 汎用レシピ構築パターン
7. `@projects/docs/patterns/` — 組織ドメインのレシピ構築パターン
8. `@docs/patterns/` — デプロイガイド、共有アセットパターン

### カスタムコネクタ開発
1. `@docs/connector-sdk/connector-rb.md` — connector.rb リファレンス
2. `@docs/connector-sdk/overview.md` — SDK 概要・CLI コマンド
3. `@.claude/rules/workato-connector-sdk.md` — フォーマットルール

## 開発ルール

- レシピ JSON: `@.claude/rules/workato-recipe-format.md`
- Genie/Skill/MCP: `@.claude/rules/workato-agentic-format.md`
- ページ: `@.claude/rules/workato-page-components.md`
- カスタムコネクタ: `@.claude/rules/workato-connector-sdk.md`
- CLI: `@.claude/rules/workato-cli.md`
- コネクタ詳細: Pre-built は `@docs/connectors/`、カスタムは `@connectors/docs/` を参照。未作成分は WebFetch
- 新しい独自知見は適切なドキュメントに直接追記（`docs/learned-patterns.md` は一時保管のみ）
- `*.connection.json` に認証情報は含まれない
- `.workatoenv` / `master.key` はコミットしない

## ツールキット開発ルール

このリポジトリ自体（スキル、ルール、ドキュメント）を変更する際のルール。

- **Cursor 同期**: `.claude/rules/` や `.claude/skills/` を変更したら `bash scripts/sync-cursor-rules.sh` を実行して `.cursor/` に反映する。コミットには両方を含めること

## スキル一覧

| スキル | 用途 |
|---|---|
| `/create-recipe` | レシピ JSON を対話的に生成 |
| `/create-workflow-app` | Workflow App を構築 |
| `/create-genie` | Genie / MCP サーバーを生成 |
| `/create-connector` | カスタムコネクタをスキャフォールド |
| `/catalog` | 共有アセットのスキャン・カタログ化 |
| `/validate-recipe` | JSON 構造を検証 |
| `/wpull` | Workato からプロジェクトを pull |
| `/wpush` | プロジェクトを push（バリデーション付き） |
| `/learn-recipe` | レシピからフィールド情報を学習しドキュメントに反映 |
| `/learn-pattern` | レシピから構築パターンを抽出しカタログに蓄積 |
| `/sync-connectors` | コネクタ情報を収集・更新（Pre-built: API、カスタム: connector.rb パース） |
| `/design` | プロジェクト設計書の作成・更新・参照 |
