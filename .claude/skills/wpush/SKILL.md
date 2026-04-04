---
description: ローカルのプロジェクト変更を Workato リモートに push する。push 前にバリデーションを実行。
allowed-tools: Bash, Read, Glob, Grep
disable-model-invocation: true
---

# /wpush

ローカルの変更を Workato リモートに push する。

## 使い方

- `/wpush` — 現在のプロジェクトを push
- `/wpush <project-name>` — 指定プロジェクトに切り替えて push

## 実行手順

1. **バリデーション**: push 前に `/validate-recipe` 相当のチェックを実行
   - Error がある場合は push を中断し、問題を報告
   - Warning のみの場合はユーザーに確認後に push

2. **差分確認**: 変更されるファイルをユーザーに表示

3. **push 実行**:
```bash
# プロジェクト名指定の場合
workato projects use "<project-name>"
# push
workato push
```

4. **結果報告**: push 結果を表示

## 注意

- push は Workato リモートの内容を上書きする破壊的操作
- 必ずユーザーの確認を得てから実行する
