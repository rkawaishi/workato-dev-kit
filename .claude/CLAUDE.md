# Workato Dev Kit

Workato (エンタープライズ iPaaS) の自動化開発を Claude Code / Cursor で行うためのツールキット。

## リポジトリ構造（デュアルリポジトリ）

このリポジトリは **フレームワーク** であり、組織固有のレシピプロジェクトは含まない。

```
workato-dev-kit/              ← このリポジトリ（スキル・ルール・ナレッジ）
├── .claude/
│   ├── rules/                # パス別フォーマットルール（7ファイル）
│   ├── skills/               # 開発スキル（10個）
│   └── hooks/                # 自動化フック
├── docs/                     # ナレッジベース
│   ├── logic/                # レシピロジック（7ファイル）
│   ├── connectors/           # コネクタ知識（139+件）
│   ├── platform/             # プラットフォーム機能（11ファイル）
│   ├── patterns/             # 設計パターン・デプロイガイド
│   └── connector-sdk/        # Connector SDK リファレンス
├── connectors/               # カスタムコネクタ（Connector SDK）
│
└── projects/                 ← 組織の別リポジトリ（gitignore 対象）
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

| | workato-dev-kit | projects/ 配下 |
|---|---|---|
| **内容** | スキル、ルール、ドキュメント | レシピ、ページ、コネクション |
| **性質** | フレームワーク（汎用） | 組織固有 |
| **進化方法** | PR でスキル学習結果を反映 | 組織内で開発・コミット |
| **git 管理** | このリポジトリ | 組織の別リポジトリ |

### 設計書 (DESIGN.md)

各プロジェクトに `DESIGN.md` を配置。セッション開始時に読み、実装後に更新する。
`.workatoignore` に含めて `workato pull` で消えないようにする。
作成・更新は `/design` スキルを使用。

## ナレッジの参照優先順位

### レシピ開発
1. `@docs/connectors/` — コネクタのトリガー/アクション/フィールド一覧
2. `@docs/logic/` — ロジックステップの組み方（datapill 記法含む）
3. `@docs/platform/` — プラットフォーム機能の理解
4. `@.claude/rules/` — JSON フォーマット、プロジェクト構造
5. `@docs/patterns/` — デプロイガイド、共有アセットパターン

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
- コネクタ詳細: `@docs/connectors/` を参照。未作成分は WebFetch
- 新しい独自知見は適切なドキュメントに直接追記（`docs/learned-patterns.md` は一時保管のみ）
- `*.connection.json` に認証情報は含まれない
- `.workatoenv` / `master.key` はコミットしない

## スキル一覧

| スキル | 用途 |
|---|---|
| `/create-recipe` | レシピ JSON を対話的に生成 |
| `/create-workflow-app` | Workflow App を構築 |
| `/create-genie` | Genie / MCP サーバーを生成 |
| `/create-connector` | カスタムコネクタをスキャフォールド |
| `/validate-recipe` | JSON 構造を検証 |
| `/wpull` | Workato からプロジェクトを pull |
| `/wpush` | プロジェクトを push（バリデーション付き） |
| `/learn-recipe` | レシピからパターンを学習しドキュメントに反映 |
| `/sync-connectors` | コネクタ一覧を API から更新 |
| `/design` | プロジェクト設計書の作成・更新・参照 |
