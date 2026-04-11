# Quick Start Guide

このガイドでは、Workato Dev Kit をセットアップして最初のレシピを作るまでの手順を説明します。

## 1. 前提条件を確認

以下が必要です:

- **Workato アカウント** — [workato.com](https://www.workato.com/) で作成
- **Workato API トークン** — Workato UI > Settings > API Tokens で発行
- **Claude Code** — [claude.com/claude-code](https://claude.com/claude-code) からインストール
- **Python 3** — `python3 --version` で確認（Platform CLI に必要）

## 2. ツールキットをクローン

```bash
git clone https://github.com/rkawaishi/workato-dev-kit.git
cd workato-dev-kit
```

## 3. Workato Platform CLI をインストール

```bash
pipx install git+https://github.com/rkawaishi/workato-platform-cli.git
```

> `pipx` がない場合: `brew install pipx && pipx ensurepath`

> **Note**: 公式 CLI (`workato-platform-cli`) も利用可能ですが、本ツールキットでは [rkawaishi/workato-platform-cli](https://github.com/rkawaishi/workato-platform-cli)（フォーク版）を推奨します。ジョブ管理、アセット一覧、レシピ起動など、開発に必要なコマンドが追加されています。

## 4. CLI の初期認証

```bash
workato init
```

対話形式で以下を入力:
- **Profile name**: `default`（複数環境がある場合は `dev`, `prod` など）
- **Data Center**: お使いのデータセンター（`us`, `eu`, `jp`, `sg`）
- **API Token**: 手順1で発行したトークン

## 5. 組織のプロジェクトリポジトリを準備

Workato Dev Kit は **開発ツール**（スキル、ルール、ドキュメント）を管理します。
組織の **レシピやページなどの実ファイル** は `projects/` フォルダに別の git リポジトリとして管理します。

```
workato-dev-kit/           ← ツールキット（スキル・ルール・ナレッジ）
└── projects/              ← あなたの組織のリポジトリ（レシピ・ページ等）
```

### なぜ分けるのか？

- **ツールキット** は汎用。誰でも使え、改善を PR で共有できる
- **レシピ** は組織固有。認証情報やビジネスロジックを含むため、組織の git リポジトリで管理すべき
- 両方を同じフォルダで扱うことで、Claude Code のスキルがそのまま使える

### セットアップ方法

#### A. 新しく始める場合

```bash
cd workato-dev-kit/projects
git init
git remote add origin <あなたの組織のリポジトリURL>
```

#### B. 既存の組織リポジトリがある場合

```bash
cd workato-dev-kit
# projects/ に既存リポジトリをクローン
git clone <あなたの組織のリポジトリURL> projects
```

#### C. まず試してみたい場合（git 管理なし）

```bash
# そのまま使えます。projects/ は workato-dev-kit の .gitignore に含まれているため、
# ツールキット側に影響しません。後から git init しても OK。
```

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

Workato UI でレシピを調整したら、その変更を取り込んでナレッジを育てます。

```
あなた: /wpull
あなた: /learn-recipe
```

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

### Q: projects/ フォルダは git に入らないの？

workato-dev-kit の `.gitignore` で除外されています。組織のレシピは `projects/` 内で別の git リポジトリとして管理してください。

### Q: DESIGN.md は workato pull で消える？

各プロジェクトの `.workatoignore` に `DESIGN.md` を記載しておけば消えません。`/design new` コマンドが自動で設定します。

### Q: Cursor でも使える？

はい。`.cursor/rules/` にも同等のルールが配置されています。スキル（`/create-recipe` 等）は Claude Code 固有の機能です。

### Q: オフラインでも使える？

ドキュメント参照とレシピ JSON の生成はオフラインで可能です。`workato push/pull` には Workato API への接続が必要です。

## 次のステップ

- [README.md](../README.md) — 全スキル一覧、ディレクトリ構成、CLI リファレンス
- [デプロイガイド](patterns/deployment-guide.md) — push 後の UI 操作手順、よくあるエラー
- [コネクタ一覧](connectors/_index.md) — 対応コネクタの確認
