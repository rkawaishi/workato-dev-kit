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
- [Workato Platform CLI](https://github.com/workato-devs/workato-platform-cli) (`pipx install workato-platform-cli`)
- [Claude Code](https://claude.com/claude-code) または [Cursor](https://cursor.com)

## セットアップ

> 詳しい手順は **[Quick Start Guide (Claude Code)](guides/quickstart-claude-code.md)** または **[Quick Start Guide (Cursor)](guides/quickstart-cursor.md)** を参照してください。

### セットアップ

組織のワークスペースリポジトリに workato-dev-kit を submodule として追加します。フレームワークの更新を `git submodule update` で簡単に取り込めます。

```bash
# 組織のワークスペースリポジトリを作成
mkdir my-org-workato && cd my-org-workato
git init

# workato-dev-kit を submodule として追加
git submodule add <repo-url> kit

# セットアップスクリプトを実行（symlink 作成、設定ファイル生成）
bash kit/setup.sh

# Platform CLI の初期化
workato init

# 初回コミット
git add -A && git commit -m "Initial setup with workato-dev-kit"
```

セットアップ後のディレクトリ構造:

```
my-org-workato/                 ← 組織のリポジトリ（作業ルート）
├── .claude/
│   ├── CLAUDE.md               ← 自動生成（カスタマイズ可）
│   ├── rules/                  ← kit のルールへの symlink + 組織独自ルール
│   ├── skills/                 ← kit のスキルへの symlink + 組織独自スキル
│   ├── hooks/                  ← kit のフックへの symlink
│   └── settings.json           ← 自動生成（カスタマイズ可）
├── docs/ → kit/docs/           ← symlink
├── guides/ → kit/guides/       ← symlink
├── kit/                        ← git submodule（workato-dev-kit、読み取り専用）
├── projects/                   ← 組織のレシピ
└── connectors/                 ← 組織のカスタムコネクタ
```

**フレームワークの更新:**

```bash
git submodule update --remote kit
bash kit/setup.sh   # 新しいスキル/ルールの symlink を追加
git add kit && git commit -m "Update workato-dev-kit"
```

**組織独自のスキル/ルールの追加:**

`.claude/rules/` や `.claude/skills/` に通常のファイルとして追加すれば、kit のものと共存します（symlink でないファイルは setup.sh で上書きされません）。

## ワークスペース構造

組織のレシピ・コネクタは `projects/` と `connectors/` に配置します。

### レシピプロジェクト (projects/)

組織固有のレシピ・ページ・コネクションを管理。

```bash
# Workato からプロジェクトを pull
workato projects use "<project-name>"
workato pull

# 開発 → コミット
git add projects/<project-name> && git commit -m "Add IT Onboarding workflow"
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
| `/pull-project` | Workato リモートからプロジェクトを pull |
| `/push-project` | ローカル変更を push (バリデーション + レシピ起動対応) |
| `/learn-recipe` | pull したレシピからフィールド情報を学習 |
| `/learn-pattern` | レシピ構築パターンをカタログに記録・更新 |
| `/sync-connectors` | コネクタ情報を収集・更新（Pre-built: API、カスタム: connector.rb パース） |
| `/design` | プロジェクト設計書の作成・更新・参照 |

### Cursor での使い方

Cursor では `.cursor/rules/` にルールが、`.cursor/skills/` にスキルが配置されています。
スキルの呼び出し方は Claude Code と同じ `/skill-name` 形式です（例: `/create-recipe`）。

> 詳しくは **[Quick Start Guide (Cursor)](guides/quickstart-cursor.md)** を参照。

### ルールの同期

Claude ルール（`framework/claude/rules/`）が正（canonical source）です。Cursor ルールは同期スクリプトで自動生成できます:

```bash
bash scripts/sync-cursor-rules.sh
```

## 開発フロー

### 新規プロジェクト

```
/design new "<project-name>"     ← 設計書を作成
/create-workflow-app             ← Workflow App を構築（またはレシピ単体）
/push-project --start            ← push + レシピ起動
Workato UI で確認・調整
/pull-project → /learn-recipe    ← 学習サイクル
/design update                   ← 設計書の進捗を更新
```

### 学習サイクル

```
workato pull → /learn-recipe → docs/ 更新 → 次回の生成がより正確に
             → /learn-pattern → パターンカタログ更新 → workato-dev-kit に PR
```

## ディレクトリ構成

このリポジトリ（workato-dev-kit）の構成。組織のワークスペースリポジトリに `kit/` として submodule 追加して使う。

配布物（Workato 開発用のスキル・ルール・フック）は `framework/claude/` に集約し、ルートの `.claude/` は **このリポジトリ自身を開発するための設定** に使う。これにより、kit を Claude Code で開いたときに `/create-recipe` 等の Workato 用スキルが誤って提供されないようにしている。

```
workato-dev-kit/              ← このリポジトリ (kit/ として submodule 追加)
├── .claude/                     # kit 自体の開発用（CLAUDE.md・最小限の settings.json のみ）
├── framework/                   # 配布物（利用者の .claude/ に symlink される対象）
│   └── claude/
│       ├── CLAUDE.md               # 利用者向け規約（Workato 開発ルール）
│       ├── rules/                  # パス別フォーマットルール
│       ├── skills/                 # 開発スキル（13個）
│       ├── hooks/                  # 自動化フック
│       └── settings.json           # 利用者向け設定テンプレート
├── .cursor/
│   ├── rules/                   # Cursor 用ルール（framework/claude/rules/ から自動生成）
│   └── skills/                  # Cursor 用スキル（framework/claude/skills/ から自動生成）
├── scripts/
│   └── sync-cursor-rules.sh     # framework/claude/ → .cursor/ 同期スクリプト
├── setup.sh                     # ワークスペースリポジトリ用セットアップスクリプト
├── docs/
│   ├── logic/                   # レシピロジック
│   ├── connectors/              # コネクタナレッジ (316件)
│   ├── platform/                # プラットフォーム機能
│   ├── connector-sdk/           # Connector SDK リファレンス
│   └── patterns/                # デプロイガイド、共有アセット、構築パターン
│       └── recipe-patterns/     # 汎用レシピ構築パターン
└── guides/                      # 利用者向けガイド
```

セットアップ後のワークスペースリポジトリ構成:

```
my-org-workato/
├── kit/                                 ← このリポジトリ (submodule、読み取り専用)
├── .claude/                             ← symlink + 組織独自ルール/スキル
│   ├── rules/<file>.md      → kit/framework/claude/rules/<file>.md
│   ├── skills/<name>/       → kit/framework/claude/skills/<name>/
│   ├── hooks/<file>.sh      → kit/framework/claude/hooks/<file>.sh
│   ├── CLAUDE.md            （初回コピー、カスタマイズ可）
│   └── settings.json        （初回コピー、カスタマイズ可）
├── docs/ → kit/docs/                   ← symlink
├── guides/ → kit/guides/               ← symlink
├── projects/                           ← 組織のレシピ
└── connectors/                         ← 組織のカスタムコネクタ
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
