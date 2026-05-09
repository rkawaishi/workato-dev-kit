# Quick Start Guide (Cursor)

Cursor で Workato Dev Kit をセットアップして最初のレシピを作るまでの手順を説明します。

## 1. 前提条件を確認

以下が必要です:

- **Workato アカウント** — [workato.com](https://www.workato.com/) で作成
- **Workato API トークン** — Workato UI > Settings > API Tokens で発行
- **Cursor** — [cursor.com](https://www.cursor.com/) からインストール
- **Python 3** — `python3 --version` で確認（Platform CLI に必要）

## 2. ワークスペースをセットアップ

```bash
# 組織のワークスペースリポジトリを作成
mkdir my-org-workato && cd my-org-workato
git init

# workato-dev-kit を submodule として追加
git submodule add https://github.com/rkawaishi/workato-dev-kit.git kit

# セットアップスクリプトを実行（symlink 作成、設定ファイル生成）
bash kit/setup.sh

# 初回コミット
git add -A && git commit -m "Initial setup with workato-dev-kit"
```

セットアップ後の構造:

```
my-org-workato/                 ← 作業ルート
├── .claude/                    ← kit から symlink（+ 組織独自ルール/スキルを追加可）
├── .cursor/                    ← kit から symlink（Cursor 用ルール・スキル）
├── docs/ → kit/docs/           ← symlink
├── guides/ → kit/guides/       ← symlink
├── kit/                        ← git submodule（読み取り専用）
├── projects/                   ← 組織のレシピ
└── connectors/                 ← 組織のカスタムコネクタ
```

## 3. Workato Platform CLI をインストール

```bash
pipx install workato-platform-cli
```

> `pipx` がない場合: `brew install pipx && pipx ensurepath`

> **Note**: 公式 CLI でプロジェクトの pull/push を行います。ジョブ管理やコネクタ情報取得など CLI にない機能は、付属の API ヘルパー (`python3 scripts/workato-api.py`) で補完します。詳細は `.claude/rules/workato-cli.md` を参照。

## 4. CLI の初期認証

```bash
workato init
```

対話形式で以下を入力:
- **Profile name**: `default`（複数環境がある場合は `dev`, `prod` など）
- **Data Center**: お使いのデータセンター（`us`, `eu`, `jp`, `sg`）
- **API Token**: 手順1で発行したトークン

## 5. フレームワークの更新

```bash
git submodule update --remote kit
bash kit/setup.sh
git add kit && git commit -m "Update workato-dev-kit"
```

新しいスキルやルールが追加された場合、`setup.sh` が自動で symlink を作成します。
組織独自に追加したファイル（symlink でないもの）は上書きされません。

## 6. Workato プロジェクトを取得

```bash
# 利用可能なプロジェクトを確認
workato projects list --source remote

# プロジェクトを取得
workato projects use "<プロジェクト名>"
workato pull
```

> まだプロジェクトがない場合は、次のステップでゼロから作れます。

## 7. Cursor を起動

```bash
cd my-org-workato
cursor .
```

Cursor が起動すると、以下が自動的にロードされます:
- `.cursor/rules/` — ファイルの種類に応じたフォーマットルール（レシピ JSON、ページ JSON、コネクタ等）
- `.cursor/skills/` — 開発スキル（レシピ生成、デプロイ、設計等）

## スキルの使い方

Cursor の Agent モードで `/` を入力し、スキル名を選択して呼び出します。Claude Code と同じ `/skill-name` 形式です。

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
| `/learn-recipe` | レシピからパターンを学習 |
| `/sync-connectors` | コネクタ情報を収集・更新 |
| `/design` | プロジェクト設計書の作成・更新 |

> **Tip**: Agent モードで利用してください。スキルの `description` に基づき、エージェントがタスクに関連するスキルを自動的に選択することもあります。

## 8. 最初のプロジェクトを作る

### 方法 A: 設計から始める（推奨）

```
あなた: /design new "[App] 経費申請"
```

Agent が以下をヒアリングします:
1. 誰が・何をしたいか（業務の言葉で）
2. どんな流れをイメージしているか
3. 関わる人は誰か
4. 最終的に何が起きれば成功か
5. 既存のツールやデータソースはあるか

ヒアリング後、ユーザー体験を整理 → 技術設計に変換 → `DESIGN.md` を生成します。

### 方法 B: すぐに作り始める

```
あなた: /create-recipe
```

または Workflow App が必要なら:

```
あなた: /create-workflow-app
```

## 9. デプロイ

```
あなた: /push-project --start
```

Agent が以下を実行します:
1. JSON バリデーション
2. `workato push`
3. 新規コネクションがあれば認証手順を案内
4. レシピを起動

## 10. 学習サイクル

### なぜ学習サイクルが必要か

Workato のレシピ JSON には公式ドキュメントに記載されていない構造が多くあります。たとえば:

- コネクタごとのフィールド名やスキーマ（`extended_output_schema` の中身）
- UI で設定した際に自動生成される `dynamicPickListSelection` や `toggleCfg`
- コネクション依存のフィールド（push しただけでは空になり、UI で設定→pull して初めて判明する）

これらは **実際にレシピを作って Workato UI でフィードバックし、pull して初めてわかる情報** です。`/learn-recipe` はこれらの情報を分析し、ツールキットのナレッジベース（`docs/`）やルール（`.cursor/rules/`）に反映します。学習が蓄積されるほど、次回の `/create-recipe` や `/create-workflow-app` の生成精度が上がります。

### やり方

Workato UI でレシピを調整したら、その変更を取り込んでナレッジを育てます。

```
あなた: /pull-project
あなた: /learn-recipe
```

### ツールキットへの還元

学んだパターンがツールキットの改善になる場合は、workato-dev-kit に PR を出してください:

```bash
# kit/ ディレクトリで
cd kit
git checkout -b feature/learn-jira-fields
# docs/ や .claude/rules/ への変更をコミット
git push origin feature/learn-jira-fields
# GitHub で PR を作成
```

## ルールの仕組み

`.cursor/rules/` にはファイルの種類に応じて自動適用されるルールが配置されています:

| ルール | 自動適用対象 |
|---|---|
| `workato-recipe-format.mdc` | `**/*.recipe.json` |
| `workato-agentic-format.mdc` | `**/*.agentic_genie.json`, `**/*.agentic_skill.json` 等 |
| `workato-page-components.mdc` | `**/*.lcap_page.json` |
| `workato-connector-sdk.mdc` | `connectors/**/*.rb` |
| `workato-project-structure.mdc` | `projects/**` |
| `workato-shared-assets.mdc` | `projects/**` |
| `workato-cli.mdc` | `.workatoenv`, `projects/**`, `connectors/**` |
| `workato-project.mdc` | 常時適用（プロジェクト全体のコンテキスト） |

これらのルールとスキルは `kit/.claude/` から自動変換されています。最新化するには:

```bash
bash scripts/sync-cursor-rules.sh
```

## よくある質問

### Q: Workato のプロジェクトとは？

Workato UI 上でレシピやコネクションをまとめる単位です。`workato pull` でローカルに JSON ファイルとしてダウンロードし、`workato push` でアップロードします。

### Q: projects/ フォルダはどう git 管理するの？

ワークスペースリポジトリに直接含まれます。`git add projects/<name> && git commit` で通常通り管理してください。

### Q: DESIGN.md は workato pull で消える？

各プロジェクトの `.workatoignore` に `DESIGN.md` を記載しておけば消えません。`/design` スキルが自動で設定します。

### Q: Claude Code でも使える？

はい。`.claude/rules/` と `.claude/skills/` にも同等のルールとスキルが配置されています。呼び出し方は同じ `/skill-name` 形式です。詳しくは [QUICKSTART-CLAUDE-CODE.md](quickstart-claude-code.md) を参照。

### Q: ルールとスキルを最新の状態に保つには？

Claude 側（`.claude/rules/`、`.claude/skills/`）が正（canonical source）です。更新があった場合は同期スクリプトを実行してください:

```bash
bash scripts/sync-cursor-rules.sh
```

### Q: オフラインでも使える？

ドキュメント参照とレシピ JSON の生成はオフラインで可能です。`workato push/pull` には Workato API への接続が必要です。

## 次のステップ

- [README.md](../README.md) — 全スキル一覧、ディレクトリ構成、CLI リファレンス
- [デプロイガイド](../docs/patterns/deployment-guide.md) — push 後の UI 操作手順、よくあるエラー
- [コネクタ一覧](../docs/connectors/_index.md) — 対応コネクタの確認
