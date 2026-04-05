---
description: ローカルのプロジェクト変更を Workato リモートに push する。新規コネクションがあればコネクション先行 push → 認証 → 残り push のフローを実行。
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

### 1. 新規コネクションの検出

push 前にプロジェクト内の `.connection.json` ファイルを確認し、Workato リモートにまだ存在しない新規コネクションがあるか検出する。

検出方法:
- ローカルの `*.connection.json` ファイルを一覧
- `workato pull` 時に取得済みのコネクション（既に Workato 上に存在）と比較
- 新規に作成されたコネクションファイルを特定

### 2. push（2段階 or 通常）

**新規コネクションがある場合 — 2段階 push:**

1. **まずコネクションファイルのみを push**: レシピ等を一時的に `.workato-ignore` に追加するか、コネクションファイルだけのディレクトリで push する。ただし **`--delete` オプションは絶対に使わない**（既存リモートアセットが削除される）
2. ユーザーに認証設定を依頼:

```
新しいコネクションを Workato にプッシュしました:
- <connection_name> (<provider>)

Workato UI で認証を設定してください:
1. プロジェクト「<project>」を開く
2. 各コネクションの認証情報を入力して接続

認証が完了したら教えてください。残りのアセットを push します。
```

3. 認証完了後、全アセットを push

**新規コネクションがない場合 — 通常 push:**

```bash
workato projects use "<project-name>"
workato push
```

### 4. レシピ起動（--start / --test 指定時）

```bash
# プロジェクト内のレシピ一覧を取得
workato recipes list --output-mode json

# 個別レシピを起動
workato recipes start --id <recipe-id>

# 全レシピを起動
workato recipes start --all
```

### 5. ジョブ確認（--test 指定時）

```bash
# レシピのジョブ一覧を取得（失敗のみ）
workato jobs list --recipe-id <recipe-id> --status failed

# ジョブの詳細（エラー内容）を取得
workato jobs get --recipe-id <recipe-id> --job-id <job-id>
```

### 6. エラー修正サイクル

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

### 7. 結果報告

- push 結果
- レシピの起動状態
- ジョブの成否（--test 時）
- エラーがあった場合はエラー内容と修正提案

## 注意

- push は Workato リモートの内容を上書きする操作
- **新規コネクションは必ず先に push して認証を済ませる** — 未認証コネクションでレシピを push するとエラーになる
- Workflow App のトリガー（new_requests_realtime 等）はフォーム送信でテスト
