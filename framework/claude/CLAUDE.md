# Workato Dev Kit

Workato (エンタープライズ iPaaS) の自動化開発を Claude Code / Cursor で行うためのツールキット。

## リポジトリ構造

このリポジトリは **フレームワーク** であり、組織のワークスペースリポジトリに `kit/` として submodule 追加して使う。
`bash kit/setup.sh` でスキル・ルール・ドキュメントへの symlink（Cursor のみコピー）を作成する。

```
my-org-workato/                   ← 組織のリポジトリ（作業ルート）
├── .claude/
│   ├── CLAUDE.md                 # setup.sh が生成（カスタマイズ可）
│   ├── rules/                    # kit のルールへの symlink + 組織独自ルール
│   ├── skills/                   # kit のスキルへの symlink + 組織独自スキル
│   ├── hooks/                    # kit のフックへの symlink
│   └── settings.json             # setup.sh が生成（カスタマイズ可）
├── docs/ → kit/docs/             # symlink（kit canonical なナレッジベース。直接編集しない）
├── guides/ → kit/guides/         # symlink
├── org/                          ← 組織ナレッジ層（kit が一切 touch しない）
│   └── docs/                     # docs/ と同じ階層を mirror。kit 版の補正・組織独自情報を置く
├── kit/                          ← git submodule（workato-dev-kit、読み取り専用）
├── projects/                     ← 組織のレシピ
│   └── <project-name>/
│       ├── DESIGN.md
│       ├── Recipes/
│       ├── Pages/
│       └── ...
└── connectors/                   ← 組織のカスタムコネクタ
    ├── docs/
    └── <name>/connector.rb
```

フレームワーク更新: `git submodule update --remote kit && bash kit/setup.sh`

### 設計書 (DESIGN.md)

各プロジェクトに `DESIGN.md` を配置。セッション開始時に読み、実装後に更新する。
`.workatoignore` に含めて `workato pull` で消えないようにする。
作成・更新は `/design` スキルを使用。

## ナレッジの参照優先順位

`@docs/<path>` を参照する際は、対応する `@org/docs/<path>` も必ず確認する（存在すれば併読、矛盾は org 版が優先）。詳細は `@.claude/rules/org-knowledge-overlay.md`。

### レシピ開発
1. `@docs/connectors/` (+ `@org/docs/connectors/`) — Pre-built コネクタのトリガー/アクション/フィールド一覧
2. `@connectors/docs/` — カスタムコネクタのトリガー/アクション/フィールド一覧
3. `@docs/logic/` (+ `@org/docs/logic/`) — ロジックステップの組み方（datapill 記法含む）
4. `@docs/platform/` (+ `@org/docs/platform/`) — プラットフォーム機能の理解
5. `@.claude/rules/` — JSON フォーマット、プロジェクト構造
6. `@docs/patterns/recipe-patterns/` (+ `@org/docs/patterns/recipe-patterns/`) — レシピ構築パターン
7. `@projects/docs/patterns/` — レガシーパターン（後方互換のため読み込みのみ。新規記録は `@org/docs/patterns/recipe-patterns/` へ）
8. `@docs/patterns/` (+ `@org/docs/patterns/`) — デプロイガイド、共有アセットパターン

### カスタムコネクタ開発
1. `@docs/connector-sdk/connector-rb.md` — connector.rb リファレンス
2. `@docs/connector-sdk/overview.md` — SDK 概要・CLI コマンド
3. `@.claude/rules/workato-connector-sdk.md` — フォーマットルール

### Workato API を扱う設計（CLI/MCP、API Platform、OEM 連携など）
Workato には「API Client」という名前の似て非なる 4 系統（Developer API / API Platform v1 / v2 / OEM）があり、混同すると設計自体をやり直すことになる。設計に着手する前に必ず `@docs/platform/workato-api-systems.md` の比較表と判断フローを読む。

## レシピ実装ライフサイクル（必須遵守）

ナレッジベースを育て続けるため、ドキュメント参照 → 実装 → 学習の順に進め、個別プロジェクトのコピペで済ませない。全体像（フロー図、スキル×docs 責務マップ、典型シナリオ）は **`@guides/lifecycle.md`** を参照（grep に逃げる前に、本来通るべきスキルを思い出すための地図）。

ここでは不可侵の 3 原則のみ記す:

1. **docs-first**: アクション/トリガーを使う前に `@docs/connectors/<provider>.md`（Pre-built、kit canonical）と `@org/docs/connectors/<provider>.md`（組織側の補正・追記、存在すれば）を必ず参照する。カスタムは `@connectors/docs/<provider>.md`。公式ドキュメントに無ければ WebFetch で補完
2. **既存プロジェクトの grep 禁止**: input/output スキーマを得る目的で `projects/<other-project>/Recipes/` を漁るのは禁止。個別プロジェクト固有のロジック・命名・datapill 参照が混入し、ナレッジの欠落も可視化されなくなる（例外: `@docs/patterns/recipe-patterns/`、`@org/docs/patterns/recipe-patterns/`、`@projects/docs/patterns/`（レガシー）でのパターン学習目的の参照は可）
3. **未学習は記録＋`/learn-recipe` 必須**: ドキュメントに無いアクションをベストエフォート実装した場合は `DESIGN.md` の「Unlearned Actions」または GitHub Issue に記録し、push/pull 後に `/learn-recipe <project-name>` を回して `org/docs/` に追記。学習後はエントリから外す

## 開発ルール

- レシピ JSON: `@.claude/rules/workato-recipe-format.md`
- Genie/Skill/MCP: `@.claude/rules/workato-agentic-format.md`
- ページ: `@.claude/rules/workato-page-components.md`
- カスタムコネクタ: `@.claude/rules/workato-connector-sdk.md`
- CLI: `@.claude/rules/workato-cli.md`
- CLI/API 自律性（ユーザーに UI 作業を投げる前に必ず確認）: `@.claude/rules/workato-cli-autonomy.md`
- 組織ナレッジの上書きレイヤー: `@.claude/rules/org-knowledge-overlay.md`
- コネクタ詳細: Pre-built は `@docs/connectors/` (+ `@org/docs/connectors/`)、カスタムは `@connectors/docs/` を参照。未作成分は WebFetch
- 新しい独自知見は `org/docs/<相対パス>` に追記（kit の `docs/` は直接編集しない）
- `*.connection.json` に認証情報は含まれない
- `.workatoenv` / `master.key` はコミットしない

## スキル一覧

各スキルが「いつ呼ばれ、何を読み、何を書くか」の責務マップは `@guides/lifecycle.md` を参照。

| スキル | 用途 |
|---|---|
| `/create-recipe` | レシピ JSON を対話的に生成 |
| `/create-workflow-app` | Workflow App を構築 |
| `/create-genie` | Genie / MCP サーバーを生成 |
| `/create-connector` | カスタムコネクタをスキャフォールド |
| `/catalog` | 共有アセットのスキャン・カタログ化 |
| `/validate-recipe` | JSON 構造を検証 |
| `/pull-project` | Workato からプロジェクトを pull |
| `/push-project` | プロジェクトを push（バリデーション付き） |
| `/learn-recipe` | レシピからフィールド情報を学習しドキュメントに反映 |
| `/learn-pattern` | レシピから構築パターンを抽出しカタログに蓄積 |
| `/sync-connectors` | コネクタ情報を収集・更新（Pre-built: API、カスタム: connector.rb パース） |
| `/auto-learn` | 1 コネクタの全 op を Claude in Chrome で自律収集（対話なし、不確実なものは skip + log）。完全性より網羅性を優先 |
| `/design` | プロジェクト設計書の作成・更新・参照 |
