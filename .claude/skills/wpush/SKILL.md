---
description: ローカルのプロジェクト変更を Workato リモートに push する。push 後にレシピの起動・ジョブ確認・エラー修正のサイクルを実行。
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# /wpush

ローカルの変更を Workato リモートに push し、レシピの動作確認まで行う。

## 使い方

- `/wpush` — 現在のプロジェクトを push
- `/wpush <project-name>` — 指定プロジェクトに切り替えて push
- `/wpush --start` — push 後にレシピを起動
- `/wpush --test` — push 後にレシピを起動し、ジョブの成否を確認

## 実行手順

### 1. バリデーション + 確認

- push 前に `/validate-recipe` 相当のチェックを実行
  - Error がある場合は push を中断し、問題を報告
  - Warning のみの場合はユーザーに確認後に push
- 変更されるファイルをユーザーに表示し、確認を得てから push を実行する
- push は Workato リモートの内容を上書きする操作のため、必ずユーザーの承認を得ること

### 2. push

```bash
# プロジェクト名指定の場合
workato projects use "<project-name>"
# push
workato push
```

### 3. レシピ起動（--start / --test 指定時）

```bash
# プロジェクト内のレシピ一覧を取得
workato recipes list --output-mode json

# 個別レシピを起動
workato recipes start --id <recipe-id>

# 全レシピを起動
workato recipes start --all
```

### 4. ジョブ確認（--test 指定時）

レシピ起動後、ジョブの実行結果を確認する:

```bash
# レシピのジョブ一覧を取得（失敗のみ）
workato jobs list --recipe-id <recipe-id> --status failed

# ジョブの詳細（エラー内容）を取得
workato jobs get --recipe-id <recipe-id> --job-id <job-id>
```

### 5. エラー修正サイクル

ジョブが失敗した場合:

1. `workato jobs get` でエラー内容を確認
2. エラー原因を分析:
   - **datapill 参照エラー**: path の指定ミス → レシピ JSON を修正
   - **コネクション未設定**: UI でコネクション認証を設定するよう案内
   - **フィールドマッピングエラー**: input のフィールド名/UUID を修正
   - **外部 API エラー**: 接続先の設定確認を案内
3. 修正を適用して再 push
4. レシピを再起動してジョブを再確認
5. 成功するまで繰り返す

### 6. 結果報告

- push 結果
- レシピの起動状態
- ジョブの成否（--test 時）
- エラーがあった場合はエラー内容と修正提案

## 注意

- push は Workato リモートの内容を上書きする操作
- レシピ起動前にコネクションの認証設定が必要
- Workflow App のトリガー（new_requests_realtime 等）はフォーム送信でテスト
