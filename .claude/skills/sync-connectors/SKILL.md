---
description: Workato API からコネクタのトリガー/アクション一覧を取得し docs/connectors/ を更新する。CLI の connectors list コマンドを使用。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# /sync-connectors

Workato API からコネクタ情報を取得し、`docs/connectors/` を更新するスキル。

## 使い方

- `/sync-connectors <provider-name>` — 指定コネクタの情報を取得・更新
- `/sync-connectors <name1> <name2> ...` — 複数コネクタを一括更新
- `/sync-connectors --all` — 全コネクタを一括更新
- `/sync-connectors --check` — 既存ドキュメントと API の差分を確認

## データソース

### 1次ソース: Workato API（CLI 経由）

```bash
# 特定コネクタのトリガー/アクション一覧（JSON）
workato connectors list --platform --provider <name> --output-mode json

# カスタムコネクタ一覧
workato connectors list --custom --output-mode json
```

API から取得できる情報:
- コネクタ名 (`name`), 表示名 (`title`)
- カテゴリ, OAuth 対応, deprecated フラグ
- **トリガー一覧**: `name`, `title`, `deprecated`, `bulk`, `batch`
- **アクション一覧**: `name`, `title`, `deprecated`, `bulk`, `batch`

API から取得 **できない** 情報:
- input/output フィールドの定義（コネクション接続後のみ）
- フィールドの型、必須/任意

### 2次ソース: 公式ドキュメント（WebFetch）

API で取得できない説明文や備考を補完する場合に使用。
URL パターン: `https://docs.workato.com/en/connectors/<name>.html`

### 3次ソース: pull 済みレシピ

`extended_output_schema` / `extended_input_schema` からフィールド情報を抽出。
これは `/learn-recipe` スキルの役割。

## 実行手順

### 単一コネクタの更新

1. CLI でコネクタ情報を取得:
```bash
workato connectors list --platform --provider <name> --output-mode json 2>/dev/null
```

2. JSON をパースし、triggers/actions を抽出

3. `docs/connectors/<name>.md` を作成または更新:

```markdown
# <Title> コネクタ

Provider: `<name>`

## Triggers
| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| <title> | `<name>` | Yes/- | |

## Actions
| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| <title> | `<name>` | Yes/- | |

## フィールド詳細

（/learn-recipe で蓄積）
```

### 差分更新のルール

- **新規作成**: ファイルが存在しなければ新規作成
- **更新**: 既存ファイルがある場合:
  - API から取得したトリガー/アクションと比較
  - 新しいものがあれば追加
  - `## フィールド詳細` 以降のセクション（/learn-recipe で蓄積した情報）は保持
  - deprecated フラグが立ったものに注記を追加
- **provider 名の確定**: API の `name` フィールドが正式な provider 名

### --all の実行

```bash
# 全 Pre-built コネクタを取得
workato connectors list --platform --output-mode json 2>/dev/null

# 全 Custom コネクタを取得
workato connectors list --custom --output-mode json 2>/dev/null
```

全コネクタの JSON を取得し、各コネクタの `docs/connectors/<name>.md` を生成・更新する。

### --check の動作

1. API から全コネクタのトリガー/アクションを取得
2. `docs/connectors/` 内の既存ファイルと比較
3. 差分を報告:
   - ✅ 一致
   - ⚠️ API に存在するがドキュメントにない（新しいトリガー/アクション）
   - ❌ ドキュメントにあるが API にない（削除 or 名前変更）
   - 📄 ドキュメントファイルが存在しないコネクタ

## `docs/connectors/_index.md` の更新

`--all` 実行時に `_index.md` も更新:
- 全コネクタの一覧を API データで正確に更新
- provider 名（`name` フィールド）を記載

## 出力

更新完了後、以下を報告:
- 作成/更新したファイル一覧
- 追加されたトリガー/アクションの数
- deprecated になったトリガー/アクション
