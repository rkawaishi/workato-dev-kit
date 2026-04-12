# Workato Dev Kit

Workato (エンタープライズ iPaaS) の自動化開発を [Claude Code](https://claude.com/claude-code) / [Cursor](https://cursor.com) で行うためのツールキット。

レシピ開発、Workflow App 構築、AI エージェント (Genie / MCP) 作成、カスタムコネクタ開発をカバーする。

## 特徴

- **レシピの JSON 生成** — Workato レシピを対話的に構築し `workato push` でデプロイ
- **Workflow App の構築** — Data Table、ページ、承認フローを JSON で定義
- **MCP サーバーの構築** — AI エージェントが使えるツールを MCP プロトコルで公開
- **Genie (AI エージェント)** — スキル付き AI エージェントの構成を生成
- **カスタムコネクタ** — Connector SDK (Ruby DSL) の開発支援
- **ナレッジベース** — 316 コネクタ、7 ロジックパターン、11 プラットフォーム機能のドキュメント
- **学習サイクル** — pull → 分析 → パターン蓄積 → 次回生成に反映
- **設計書管理** — プロジェクトごとの DESIGN.md でセッション跨ぎの計画・進捗追跡

## 前提条件

- [Workato](https://www.workato.com/) アカウント + API トークン
- [Workato Platform CLI (フォーク版推奨)](https://github.com/rkawaishi/workato-platform-cli) (`pipx install git+https://github.com/rkawaishi/workato-platform-cli.git`)
- [Claude Code](https://claude.com/claude-code) または [Cursor](https://cursor.com)

## セットアップ

> 詳しい手順は **[Quick Start Guide (Claude Code)](docs/QUICKSTART-CLAUDE-CODE.md)** または **[Quick Start Guide (Cursor)](docs/QUICKSTART-CURSOR.md)** を参照してください。

```bash
# リポジトリをクローン
git clone <repo-url>
cd workato-dev-kit

# Platform CLI の初期化
workato init
```

## 使い方 — デュアルリポジトリ構造

このリポジトリは **開発フレームワーク** です。組織固有のレシピプロジェクトは `projects/` 配下に別の git リポジトリとして管理します。

```
workato-dev-kit/                ← このリポジトリ（フレームワーク）
├── .claude/                    ← Claude Code 用（スキル、ルール、hooks）
├── .cursor/                    ← Cursor 用（ルール、スキル相当のルール）
├── docs/                       ← ナレッジベース
│
├── connectors/                 ← 組織の別リポジトリ（gitignore 対象）
│   ├── docs/                   ← カスタムコネクタのナレッジ（自動生成）
│   └── <name>/
│       └── connector.rb        ← Connector SDK ソース
│
└── projects/                   ← 組織の別リポジトリ（gitignore 対象）
    └── <project-name>/
        ├── DESIGN.md           ← 設計書
        ├── Recipes/
        ├── Pages/
        └── ...
```

### フレームワーク (workato-dev-kit)

スキル、ルール、ドキュメントを含む。開発中に新しいパターンを学んだら PR で反映して育てる。

```bash
# スキルの改善を PR
git checkout -b feature/improve-create-recipe
# ... スキルやドキュメントを更新 ...
git push origin feature/improve-create-recipe
# GitHub で PR を作成
```

### レシピプロジェクト (projects/)

組織固有のレシピ・ページ・コネクションを管理。`projects/` 配下で別途 git init する。

```bash
# 組織リポジトリの初期化
cd projects
git init
git remote add origin <org-repo-url>

# Workato からプロジェクトを pull
cd ..
workato projects use "<project-name>"
workato pull

# 開発 → コミット
cd projects
git add -A && git commit -m "Add IT Onboarding workflow"
```

### 設計書 (DESIGN.md)

各プロジェクトに `DESIGN.md` を配置して設計・進捗・意思決定を記録。
`.workatoignore` に含めて `workato pull` で消えないようにする。

```bash
# Claude Code で設計書を作成
/design new "[App] IT Onboarding"

# 設計書を参照
/design "[App] IT Onboarding"

# 実装状況を自動更新
/design update
```

## スキル一覧

| スキル | 説明 |
|---|---|
| `/create-recipe` | レシピ JSON を対話的に生成 |
| `/create-workflow-app` | Workflow App を段階的に構築 (Data Table, ページ, レシピ) |
| `/create-genie` | Genie / MCP サーバー + スキルの構成を生成 |
| `/create-connector` | カスタムコネクタをスキャフォールド |
| `/catalog` | 共有アセットのスキャン・カタログ化 |
| `/validate-recipe` | レシピ JSON の構造を検証 |
| `/wpull` | Workato リモートからプロジェクトを pull |
| `/wpush` | ローカル変更を push (バリデーション + レシピ起動対応) |
| `/learn-recipe` | pull したレシピからフィールド情報を学習 |
| `/learn-pattern` | レシピ構築パターンをカタログに記録・更新 |
| `/sync-connectors` | コネクタ情報を収集・更新（Pre-built: API、カスタム: connector.rb パース） |
| `/design` | プロジェクト設計書の作成・更新・参照 |

### Cursor での使い方

Cursor では `.cursor/rules/` にルールが、`.cursor/skills/` にスキルが配置されています。
スキルの呼び出し方は Claude Code と同じ `/skill-name` 形式です（例: `/create-recipe`）。

> 詳しくは **[Quick Start Guide (Cursor)](docs/QUICKSTART-CURSOR.md)** を参照。

### ルールの同期

Claude ルール（`.claude/rules/`）が正（canonical source）です。Cursor ルールは同期スクリプトで自動生成できます:

```bash
bash scripts/sync-cursor-rules.sh
```

## 開発フロー

### 新規プロジェクト

```
/design new "<project-name>"     ← 設計書を作成
/create-workflow-app             ← Workflow App を構築（またはレシピ単体）
/wpush --start                   ← push + レシピ起動
Workato UI で確認・調整
/wpull → /learn-recipe           ← 学習サイクル
/design update                   ← 設計書の進捗を更新
```

### 学習サイクル

```
workato pull → /learn-recipe → docs/ 更新 → 次回の生成がより正確に
             → /learn-pattern → パターンカタログ更新 → workato-dev-kit に PR
```

## ディレクトリ構成

```
workato-dev-kit/
├── .claude/
│   ├── CLAUDE.md                # プロジェクト規約（常時ロード）
│   ├── rules/                   # パス別フォーマットルール（7ファイル）
│   ├── skills/                  # 開発スキル（12個）
│   └── hooks/                   # 自動化フック
├── .cursor/
│   ├── rules/                   # Cursor 用ルール（.claude/rules/ から自動生成）
│   │   └── workato-project.mdc          # 常時適用（プロジェクトコンテキスト）
│   └── skills/                  # Cursor 用スキル（.claude/skills/ から自動生成、12個）
├── scripts/
│   └── sync-cursor-rules.sh     # .claude/ → .cursor/ 同期スクリプト
├── docs/
│   ├── logic/                   # レシピロジック (7ファイル)
│   ├── connectors/              # コネクタナレッジ (316件)
│   ├── platform/                # プラットフォーム機能 (11ファイル)
│   ├── connector-sdk/           # Connector SDK リファレンス
│   └── patterns/                # デプロイガイド、共有アセット、構築パターン
│       └── recipe-patterns/     # 汎用レシピ構築パターン
├── connectors/                  # カスタムコネクタ (gitignore, 組織リポジトリ)
│   ├── docs/                    # カスタムコネクタのナレッジ（自動生成）
│   └── <name>/connector.rb     # Connector SDK ソース
└── projects/                    # レシピプロジェクト (gitignore, 組織リポジトリ)
    ├── docs/patterns/           # 組織ドメインのレシピ構築パターン
```

## CLI クイックリファレンス

```bash
workato projects list --source remote   # プロジェクト一覧
workato projects use "<name>"           # プロジェクト切替
workato pull                            # リモートから取得
workato push                            # リモートへ反映
workato push --restart-recipes          # push + 実行中レシピを再起動
workato push --delete                   # 不要なリモートアセットも削除
workato assets                          # プロジェクトのアセット一覧（ID 付き）
workato recipes start --id <id>         # レシピ起動
workato jobs list --recipe-id <id>      # ジョブ一覧
```

## ライセンス

MIT License. 詳細は [LICENSE](LICENSE) を参照。

> **注意**: このツールキットは Workato の公式製品ではありません。Workato の利用については [Workato Terms of Service](https://www.workato.com/legal/terms-of-service) を確認してください。
