---
name: wpull
description: Workato リモートからプロジェクトを pull する。引数なしで現在のプロジェクト、プロジェクト名指定で切り替え後 pull。
disable-model-invocation: true
---

# /wpull

Workato Platform CLI でリモートからプロジェクトを pull する。

## 使い方

- `/wpull` — 現在のプロジェクトを pull
- `/wpull <project-name>` — 指定プロジェクトに切り替えて pull
- `/wpull --all` — 全リモートプロジェクトを pull
- `/wpull --list` — リモートプロジェクト一覧を表示

## 実行手順

### 0. Pull 前チェック（必須）

pull は未コミット変更をサイレントに上書きする。`projects/` 配下は workato-dev-kit とは別の git リポジトリ（gitignore 対象）なので、プロジェクトディレクトリ内に入ってから `git status` を確認する:

```bash
# 対象プロジェクト内に入って確認（projects/ は別 git リポジトリ）
(cd projects/<project-name> && git status)
```

未コミット変更がある場合は、ユーザーに commit / stash を提案してから pull に進む。何も聞かずに pull すると編集中のファイルが失われる可能性がある。`--all` では対象プロジェクトごとにこのチェックを繰り返す。`projects/<project-name>/` が git 管理下でない（`.git` が無い）場合はこのチェックをスキップする。

### 引数なし / プロジェクト名指定
```bash
# プロジェクト名指定の場合は先に切り替え
workato projects use "<project-name>"
# pull
workato pull
```

### --all の場合
1. `workato projects list --source remote --output-mode json` でリモート一覧取得
2. 各プロジェクトについて:
   - ローカルに存在しない場合: `workato init --non-interactive --profile default --project-id <id> --folder-name "projects/<name>"`
   - 存在する場合: **ステップ 0 の git status チェックを実施** → `workato projects use "<name>" && workato pull`

### --list の場合
```bash
workato projects list --source both
```

## 出力

pull 完了後、変更されたファイルの一覧を表示。新しいパターンが見つかった場合は `/learn-recipe` の実行を提案。
