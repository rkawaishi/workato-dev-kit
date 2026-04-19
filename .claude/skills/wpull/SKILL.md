---
description: Workato リモートからプロジェクトを pull する。引数なしで現在のプロジェクト、プロジェクト名指定で切り替え後 pull。
allowed-tools: Bash, Read, Glob
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

pull は未コミット変更をサイレントに上書きする。実行前に以下を確認する:

```bash
git status projects/<project-name>/
```

未コミット変更がある場合は、ユーザーに commit / stash を提案してから pull に進む。何も聞かずに pull すると編集中のファイルが失われる可能性がある。

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
   - 存在する場合: `workato projects use "<name>" && workato pull`

### --list の場合
```bash
workato projects list --source both
```

## 出力

pull 完了後、変更されたファイルの一覧を表示。新しいパターンが見つかった場合は `/learn-recipe` の実行を提案。
