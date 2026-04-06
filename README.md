# Workato Dev Kit

Workato (エンタープライズ iPaaS) の自動化開発を [Claude Code](https://claude.com/claude-code) / [Cursor](https://cursor.com) で行うためのツールキット。

レシピ開発、Workflow App 構築、AI エージェント (Genie / MCP) 作成、カスタムコネクタ開発をカバーする。

## 特徴

- **レシピの JSON 生成** — Workato レシピを対話的に構築し `workato push` でデプロイ
- **Workflow App の構築** — Data Table、ページ、承認フローを JSON で定義
- **MCP サーバーの構築** — AI エージェントが使えるツールを MCP プロトコルで公開
- **Genie (AI エージェント)** — スキル付き AI エージェントの構成を生成
- **カスタムコネクタ** — Connector SDK (Ruby DSL) の開発支援
- **ナレッジベース** — 139 コネクタ、7 ロジックパターン、11 プラットフォーム機能のドキュメント
- **学習サイクル** — pull → 分析 → パターン蓄積 → 次回生成に反映

## 前提条件

- [Workato](https://www.workato.com/) アカウント + API トークン
- [Workato Platform CLI](https://docs.workato.com/en/platform-cli.html) (`pipx install workato-platform-cli`)
- [Claude Code](https://claude.com/claude-code) または [Cursor](https://cursor.com)

## セットアップ

```bash
# リポジトリをクローン
git clone <repo-url>
cd workato-dev-kit

# Platform CLI の初期化
workato init
```

## ディレクトリ構成

```
workato-dev-kit/
├── projects/                    # Workato レシピプロジェクト (Platform CLI)
│   └── <project-name>/
│       ├── Recipes/             # レシピ (.recipe.json)
│       ├── Pages/               # Workflow App ページ (.lcap_page.json)
│       ├── Connections/         # コネクション (.connection.json)
│       ├── Data Tables/         # Data Table (.workato_db_table.json)
│       ├── Agents/              # Genie / MCP / Skills
│       └── Insights/            # Insights クエリ
├── connectors/                  # カスタムコネクタ (Connector SDK)
├── docs/
│   ├── logic/                   # レシピのロジック (if, loop, error handling 等)
│   ├── connectors/              # Pre-built コネクタのナレッジ (139件)
│   ├── platform/                # プラットフォーム機能 (11件)
│   ├── connector-sdk/           # Connector SDK リファレンス
│   └── learned-patterns.md      # 非公開の独自知見
├── .claude/                     # Claude Code ハーネス
│   ├── rules/                   # フォーマットルール
│   └── skills/                  # 開発スキル
└── .cursor/                     # Cursor ルール
    └── rules/
```

## スキル一覧

| スキル | 説明 |
|---|---|
| `/create-recipe` | レシピ JSON を対話的に生成 |
| `/create-workflow-app` | Workflow App を段階的に構築 (Data Table, ページ, レシピ) |
| `/create-genie` | Genie + スキル + レシピの構成を生成 |
| `/create-connector` | カスタムコネクタをスキャフォールド |
| `/validate-recipe` | レシピ JSON の構造を検証 |
| `/wpull` | Workato リモートからプロジェクトを pull |
| `/wpush` | ローカル変更を push (バリデーション + レシピ起動対応) |
| `/learn-recipe` | pull したレシピからフィールド情報とパターンを学習 |
| `/sync-connectors` | 公式ドキュメントからコネクタ情報を差分更新 |

## 開発フロー

### レシピ開発

```
/create-recipe → workato push → Workato UI で調整 → workato pull → /learn-recipe
```

### Workflow App 構築

```
/create-workflow-app
  Phase 1: 設計 + UI で App 有効化
  Phase 2: JSON 生成 (Data Table, ページ, レシピ) → workato push
  Phase 3: 動作確認
```

### 学習サイクル

```
workato pull → /learn-recipe → docs 更新 → 次回の /create-recipe がより正確に
```

## ナレッジ構成

| ディレクトリ | 内容 | ファイル数 |
|---|---|---|
| `docs/logic/` | レシピ制御構造 (triggers, if, loops, error handling, formulas 等) | 7 |
| `docs/connectors/` | Pre-built コネクタのトリガー/アクション/フィールド | 143 |
| `docs/platform/` | Data Tables, Workflow Apps, MCP, Agent Studio 等 | 11 |
| `docs/connector-sdk/` | Connector SDK (Ruby DSL) リファレンス | 2 |
| `docs/learned-patterns.md` | UI フィードバックから学んだ非公開の JSON 構造知見 | 1 |

## CLI

### Platform CLI (レシピ管理)

```bash
workato projects list --source remote   # プロジェクト一覧
workato projects use "<name>"           # プロジェクト切替
workato pull                            # リモートから取得
workato push                            # リモートへ反映
workato push --delete                   # 不要なリモートアセットも削除
workato recipes list                    # レシピ一覧
workato recipes start --all             # 全レシピ起動
workato jobs list --recipe-id <id>      # ジョブ一覧
```

## ライセンス

MIT License. 詳細は [LICENSE](LICENSE) を参照。

> **注意**: このツールキットは Workato の公式製品ではありません。Workato の利用については [Workato Terms of Service](https://www.workato.com/legal/terms-of-service) を確認してください。
