# Workato Dev Kit

[English](README.en.md) | 日本語

Workato (エンタープライズ iPaaS) の自動化開発を AI コーディングエージェントで行うためのツールキット。
[Claude Code](https://claude.com/claude-code) / [Cursor](https://cursor.com) / [Codex CLI](https://github.com/openai/codex) / [Gemini CLI](https://github.com/google-gemini/gemini-cli) に対応。

レシピ開発、Workflow App 構築、AI エージェント (Genie / MCP) 作成、カスタムコネクタ開発をカバーする。

## 特徴

- **レシピの JSON 生成** — Workato レシピを対話的に構築し `workato push` でデプロイ
- **Workflow App の構築** — Data Table、ページ、承認フローを JSON で定義
- **MCP サーバーの構築** — AI エージェントが使えるツールを MCP プロトコルで公開
- **Genie (AI エージェント)** — スキル付き AI エージェントの構成を生成
- **カスタムコネクタ** — Connector SDK (Ruby DSL) の開発支援
- **ナレッジベース** — 316 コネクタ、7 ロジックパターン、13 プラットフォーム機能のドキュメント
- **学習サイクル** — pull → 分析 → パターン蓄積 → 次回生成に反映
- **設計書管理** — プロジェクトごとの DESIGN.md でセッション跨ぎの計画・進捗追跡

## 前提条件

- [Workato](https://www.workato.com/) アカウント + API トークン
- [Workato Platform CLI](https://github.com/workato-devs/workato-platform-cli) (`pipx install workato-platform-cli`)
- 対応エディタのいずれか — [Claude Code](https://claude.com/claude-code) / [Cursor](https://cursor.com) / [Codex CLI](https://github.com/openai/codex) / [Gemini CLI](https://github.com/google-gemini/gemini-cli)

## セットアップ

> 詳しい手順は **[Quick Start (Claude Code)](guides/quickstart-claude-code.md)** または **[Quick Start (Cursor)](guides/quickstart-cursor.md)** を参照。

組織のワークスペースリポジトリに workato-dev-kit を submodule として追加します。フレームワークの更新は `git submodule update` で取り込めます。

```bash
# 組織のワークスペースリポジトリを作成
mkdir my-org-workato && cd my-org-workato
git init

# workato-dev-kit を submodule として追加
git submodule add https://github.com/rkawaishi/workato-dev-kit.git kit

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
├── .claude/                    ← Claude Code 用
│   ├── CLAUDE.md               # 自動生成（カスタマイズ可）
│   ├── rules/                  # kit のルール (symlink) + 組織独自ルール
│   ├── skills/                 # kit のスキル (symlink) + 組織独自スキル
│   ├── hooks/                  # kit のフック (symlink)
│   └── settings.json           # 自動生成（カスタマイズ可）
├── .cursor/                    ← Cursor 用 (symlink)
│   ├── rules/, skills/, hooks.json
├── .agents/skills/             ← Codex CLI 用 (symlink)
├── .gemini/skills/             ← Gemini CLI 用 (symlink)
├── AGENTS.md → kit/...         ← Codex / Aider 等のエージェント中立規約
├── GEMINI.md → kit/...         ← AGENTS.md と同じ実体
├── docs/ → kit/docs/           ← ナレッジベース (symlink)
├── guides/ → kit/guides/       ← symlink
├── kit/                        ← git submodule (読み取り専用)
├── projects/                   ← 組織のレシピ
└── connectors/                 ← 組織のカスタムコネクタ
```

**フレームワークの更新:**

```bash
git submodule update --remote kit
bash kit/setup.sh    # 新しいスキル/ルールの symlink を追加・古いものを除去
git add kit && git commit -m "Update workato-dev-kit"
```

**組織独自のスキル/ルールの追加:** `.claude/rules/` や `.claude/skills/` に通常のファイルとして追加すれば、kit のものと共存します（symlink でない実ファイルは setup.sh で上書きされません）。

## ワークスペース構造

組織のレシピ・コネクタは `projects/` と `connectors/` に配置します。

### レシピプロジェクト (projects/)

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
/design new "[App] IT Onboarding"   # 作成
/design "[App] IT Onboarding"       # 参照
/design update                      # 実装状況を自動更新
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
| `/auto-learn` | 1 コネクタの全 op を Claude in Chrome で自律収集（対話なし） |
| `/design` | プロジェクト設計書の作成・更新・参照 |

詳細は [スキルリファレンス](guides/skills-reference.md) と [ライフサイクルと責務マップ](guides/lifecycle.md) を参照。

### エディタ別の使い方

| エディタ | スキル配置 | 呼び出し |
|---|---|---|
| Claude Code | `.claude/skills/<name>/` | `/skill-name` |
| Cursor | `.cursor/skills/<name>/` | `/skill-name` |
| Codex CLI | `.agents/skills/<name>/` | `$skill-name` ※slash 構文を `$` に書き換え済み |
| Gemini CLI | `.gemini/skills/<name>/` | `/skill-name` |

エージェント横断の規約 (`CLAUDE.md` + `rules/` を集約) は `AGENTS.md` / `GEMINI.md`（同じ実体）として配布されます。

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

正本は `framework/claude/`。Cursor / Codex / Gemini 向けは `scripts/sync_agents.py` で自動生成される。kit を Claude Code で開いたときに `/create-recipe` 等の Workato 用スキルが誤って提供されないよう、ルートの `.claude/` には **このリポジトリ自身を開発するための設定** だけを置く。

```
workato-dev-kit/                 ← このリポジトリ (kit/ として submodule 追加)
├── .claude/                     # kit 自体の開発用（Workato 用スキルは含まない）
├── framework/                   # 配布物（利用者の各エディタ設定に symlink される）
│   ├── claude/                  # 正本 (canonical source)
│   │   ├── CLAUDE.md            #   利用者向け規約（Workato 開発ルール）
│   │   ├── rules/               #   8 ルール（recipe フォーマット等）
│   │   ├── skills/              #   13 スキル
│   │   ├── hooks/               #   自動化フック
│   │   └── settings.json        #   利用者向け設定テンプレート
│   ├── cursor/                  # 自動生成: rules/*.mdc + skills/ + hooks.json (手書き)
│   ├── codex/skills/            # 自動生成 (slash 構文を $ に書き換え)
│   ├── gemini/skills/           # 自動生成
│   └── AGENTS.md                # 自動生成: CLAUDE.md + rules を集約。GEMINI.md も同じ実体
├── docs/                        # ナレッジベース
│   ├── connectors/              #   316 コネクタ
│   ├── connector-sdk/           #   Connector SDK リファレンス
│   ├── logic/                   #   7 ロジックパターン
│   ├── platform/                #   13 プラットフォーム機能
│   └── patterns/                #   デプロイガイド、共有アセット、構築パターン
├── guides/                      # 利用者向けガイド
├── scripts/
│   ├── sync_agents.py           #   framework/claude/ → cursor/codex/gemini/ + AGENTS.md
│   ├── sync-cursor-rules.sh     #   後方互換ラッパー
│   └── workato-api.py
├── templates/                   # 利用者リポジトリ向けテンプレ (.gitignore 等)
└── setup.sh                     # 利用者リポジトリ用セットアップスクリプト
```

### 配布物の編集

- スキル・ルールは `framework/claude/` を編集する
- 編集後は **`python3 scripts/sync_agents.py`** を必ず実行（`framework/{cursor,codex,gemini}/` と `AGENTS.md` を再生成）
- 元の編集と再生成された配布物の両方をコミットに含める（CI でドリフトを自動検出）

詳細は [.claude/CLAUDE.md](.claude/CLAUDE.md) を参照。

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
