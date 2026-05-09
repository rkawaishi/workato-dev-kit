# Quick Start Guide (Claude Code)

Claude Code で Workato Dev Kit をセットアップして最初のレシピを作るまでの手順を説明します。

## 1. 前提条件を確認

以下が必要です:

- **Workato アカウント** — [workato.com](https://www.workato.com/) で作成
- **Workato API トークン** — Workato UI > Settings > API Tokens で発行
- **Claude Code** — [claude.com/claude-code](https://claude.com/claude-code) からインストール
- **Python 3** — `python3 --version` で確認（Platform CLI に必要）

## 2. ワークスペースをセットアップ

```bash
# 組織のワークスペースリポジトリを作成
mkdir my-org-workato && cd my-org-workato
git init

# workato-dev-kit を submodule として追加
git submodule add https://github.com/rkawaishi/workato-dev-kit.git kit

# セットアップスクリプトを実行
bash kit/setup.sh

# 初回コミット
git add -A && git commit -m "Initial setup with workato-dev-kit"
```

セットアップ後の構造:

```
my-org-workato/                 ← 作業ルート
├── .claude/                    ← kit から symlink（+ 組織独自ルール/スキルを追加可）
├── docs/ → kit/docs/           ← symlink
├── guides/ → kit/guides/       ← symlink
├── kit/                        ← git submodule（読み取り専用）
├── projects/                   ← 組織のレシピ（ワークスペースリポジトリで直接管理）
└── connectors/                 ← 組織のカスタムコネクタ（ワークスペースリポジトリで直接管理）
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

## 5. フレームワークの更新（Submodule 利用時）

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

## 7. Claude Code を起動

```bash
cd workato-dev-kit
claude
```

Claude Code が起動すると、`.claude/` フォルダのスキルとルールが自動的にロードされます。

## 8. 最初のプロジェクトを作る

### 方法 A: 設計から始める（推奨）

```
あなた: /design new "[App] 経費申請"
```

Claude が以下をヒアリングします:
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
あなた: /wpush --start
```

Claude が以下を実行します:
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

これらは **実際にレシピを作って Workato UI でフィードバックし、pull して初めてわかる情報** です。`/learn-recipe` はこれらの情報を分析し、ツールキットのナレッジベース（`docs/`）やルール（`.claude/rules/`）に反映します。学習が蓄積されるほど、次回の `/create-recipe` や `/create-workflow-app` の生成精度が上がります。

### やり方

Workato UI でレシピを調整したら、その変更を取り込んでナレッジを育てます。

```
あなた: /wpull
あなた: /learn-recipe
```

### ツールキットへの還元

学んだパターンがツールキットの改善になる場合は、workato-dev-kit に PR を出してください:

```bash
# workato-dev-kit 側で
git checkout -b feature/learn-jira-fields
# docs/ や .claude/rules/ への変更をコミット
git push origin feature/learn-jira-fields
# GitHub で PR を作成
```

## よくある質問

### Q: Workato のプロジェクトとは？

Workato UI 上でレシピやコネクションをまとめる単位です。`workato pull` でローカルに JSON ファイルとしてダウンロードし、`workato push` でアップロードします。

### Q: projects/ フォルダはどう git 管理するの？

ワークスペースリポジトリに直接含まれます。`git add projects/<name> && git commit` で通常通り管理してください。

### Q: DESIGN.md は workato pull で消える？

各プロジェクトの `.workatoignore` に `DESIGN.md` を記載しておけば消えません。`/design new` コマンドが自動で設定します。

### Q: Cursor でも使える？

はい。`.cursor/rules/` にも同等のルールとスキル相当のルールが配置されています。詳しくは [QUICKSTART-CURSOR.md](quickstart-cursor.md) を参照してください。

### Q: オフラインでも使える？

ドキュメント参照とレシピ JSON の生成はオフラインで可能です。`workato push/pull` には Workato API への接続が必要です。

## 次のステップ

- [README.md](../README.md) — 全スキル一覧、ディレクトリ構成、CLI リファレンス
- [デプロイガイド](../docs/patterns/deployment-guide.md) — push 後の UI 操作手順、よくあるエラー
- [コネクタ一覧](../docs/connectors/_index.md) — 対応コネクタの確認
