---
name: sync-connectors
description: コネクタ情報を収集しドキュメントを更新する。Pre-built は API 経由で docs/connectors/ を、カスタムコネクタは connector.rb パースで connectors/docs/ を更新。
---

# /sync-connectors

コネクタ情報を収集しドキュメントを更新するスキル。

- **Pre-built コネクタ**: Workato API から取得 → `docs/connectors/` を更新
- **カスタムコネクタ**: `connector.rb` をパース → `connectors/docs/` を更新

## 使い方

- `/sync-connectors <provider-name>` — 指定 Pre-built コネクタの情報を取得・更新
- `/sync-connectors <name1> <name2> ...` — 複数 Pre-built コネクタを一括更新
- `/sync-connectors --all` — Pre-built + カスタムコネクタを一括更新
- `/sync-connectors --check` — 既存ドキュメントと API の差分を確認
- `/sync-connectors --custom` — `connectors/` 配下の全カスタムコネクタをスキャン・更新
- `/sync-connectors --custom <name>` — 指定カスタムコネクタのみスキャン・更新

## データソース

### Pre-built コネクタ

#### 1次ソース: Workato API（CLI 経由）

```bash
# 特定コネクタのトリガー/アクション一覧（JSON）
python3 scripts/workato-api.py connectors list-platform --provider <name>

# カスタムコネクタ一覧
python3 scripts/workato-api.py connectors list-custom
```

API から取得できる情報:
- コネクタ名 (`name`), 表示名 (`title`)
- カテゴリ, OAuth 対応, deprecated フラグ
- **トリガー一覧**: `name`, `title`, `deprecated`, `bulk`, `batch`
- **アクション一覧**: `name`, `title`, `deprecated`, `bulk`, `batch`

API から取得 **できない** 情報:
- input/output フィールドの定義（コネクション接続後のみ）
- フィールドの型、必須/任意

### カスタムコネクタ

#### ソース: connector.rb（ローカルパース）

`connectors/<name>/connector.rb` の Ruby DSL を直接読み取って情報を抽出する。
API コールは不要。Claude が Ruby DSL を理解して以下を抽出:

- `title:` — コネクタ表示名
- `actions:` ブロック — アクション名（ハッシュキー）、`title`、`batch`/`bulk` フラグ
- `triggers:` ブロック — トリガー名（ハッシュキー）、`title`、タイプ判定:
  - `poll` + `dedup` があれば Polling
  - `webhook_subscribe` があれば Webhook
- `object_definitions:` — 共有フィールド定義（`fields` ラムダ内の配列）
- `input_fields` / `output_fields` — フィールド定義を抽出:
  - `object_definitions['name']` 参照の場合は該当定義を解決
  - インラインの場合は直接配列を抽出
  - 各フィールドから `name`, `type`, `label`, `optional`, `hint` を取得

#### connector.rb が存在しない場合

`connectors/<name>/` にソースがない（UI 上のみのカスタムコネクタ）場合:
- ユーザーに `workato sdk pull` の実行を提案
- pull 後に再度 `/sync-connectors --custom` を実行

### Pre-built 補足ソース

#### 2次ソース: 公式ドキュメント（WebFetch）

API で取得できない説明文や備考を補完する場合に使用。
URL パターン: `https://docs.workato.com/en/connectors/<name>.html`

### 3次ソース: pull 済みレシピ

`extended_output_schema` / `extended_input_schema` からフィールド情報を抽出。
これは `/learn-recipe` スキルの役割。

## 実行手順

### カスタムコネクタの更新（--custom）

1. `connectors/` 配下をスキャンし、`connector.rb` が存在するディレクトリを列挙:
```bash
ls connectors/*/connector.rb 2>/dev/null
```

2. 各 `connector.rb` を Read で読み込み、Ruby DSL を解析:
   - `title:` からコネクタ表示名を取得
   - `actions:` ブロックから各アクションの名前（キー）、`title`、`batch`/`bulk` フラグを抽出
   - `triggers:` ブロックから各トリガーの名前（キー）、`title`、タイプ（Polling/Webhook）を判定
   - `object_definitions:` からフィールド定義を抽出
   - 各 action/trigger の `input_fields` / `output_fields` を解決:
     - `object_definitions['name']` 参照 → 該当 object_definition の fields を展開
     - インライン配列 → 直接抽出

3. `connectors/docs/<name>.md` を作成または更新:

```markdown
# <Title> コネクタ

Provider: `<name>`
Source: Custom (Connector SDK)

## Triggers

| 名前 | provider 内名称 | Type | 説明 |
|---|---|---|---|
| <title> | `<name>` | Polling/Webhook | |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| <title> | `<name>` | Yes/- | |

## フィールド詳細

### <action/trigger name>

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| <name> | <type> | Yes/- | <label or hint> |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| <name> | <type> | <label or hint> |
```

4. `connectors/docs/` ディレクトリが存在しない場合は作成

5. `--custom <name>` の場合は指定コネクタのみ処理

### Pre-built 単一コネクタの更新

1. CLI でコネクタ情報を取得:
```bash
python3 scripts/workato-api.py connectors list-platform --provider <name>
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

#### Pre-built コネクタ
```bash
# 全 Pre-built コネクタを取得
python3 scripts/workato-api.py connectors list-platform
```
全コネクタの JSON を取得し、各コネクタの `docs/connectors/<name>.md` を生成・更新する。

#### カスタムコネクタ
`connectors/` 配下の全 `connector.rb` をスキャンし、`connectors/docs/<name>.md` を生成・更新する（「カスタムコネクタの更新」手順に従う）。

### --check の動作

1. API から全コネクタのトリガー/アクションを取得
2. `docs/connectors/` 内の既存ファイルと比較
3. 差分を報告:
   - ✅ 一致
   - ⚠️ API に存在するがドキュメントにない（新しいトリガー/アクション）
   - ❌ ドキュメントにあるが API にない（削除 or 名前変更）
   - 📄 ドキュメントファイルが存在しないコネクタ

## `docs/connectors/_index.md` の更新（Pre-built のみ）

`--all` 実行時に `_index.md` も更新:
- Pre-built コネクタの一覧を API データで正確に更新
- provider 名（`name` フィールド）を記載
- カスタムコネクタは含めない（組織固有のため `connectors/docs/` で管理）

## 出力

更新完了後、以下を報告:

### Pre-built コネクタ
- 作成/更新したファイル一覧（`docs/connectors/`）
- 追加されたトリガー/アクションの数
- deprecated になったトリガー/アクション

### カスタムコネクタ
- 作成/更新したファイル一覧（`connectors/docs/`）
- 抽出されたトリガー/アクション/フィールドの数
- connector.rb が見つからなかったディレクトリ（pull が必要）
