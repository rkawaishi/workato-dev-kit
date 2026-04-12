# Workflow App 構築ガイド

Workato Workflow App（承認ワークフロー等）を JSON ベースで構築する手順と設計ポイント。Claude Code / Cursor のどちらでも同じスキル・同じ手順で構築できる。

## Workflow App とは

Workflow App は Workato 上でフォームベースの業務アプリケーションを構築する機能。承認ワークフロー、申請フォーム、タスク管理などに使われる。

**構成要素:**

```
<project>/
├── lcap_app.json           # アプリ定義（ステージ・ページ紐付け）
├── Data Tables/
│   └── <table>.data_table.json   # データスキーマ
├── Pages/
│   ├── submit.page.json    # 申請フォーム
│   ├── review.page.json    # レビュー画面
│   └── done.page.json      # 完了画面
└── Recipes/
    └── *.recipe.json        # ワークフローロジック
```

## 構築手順

### 1. 設計

`/design` で全体設計を固める。Workflow App では以下を明確にする:

- **ステージ**: どんな状態遷移があるか（例: 申請 → レビュー → 承認/却下）
- **データ**: 各ステージで必要なデータ項目
- **ページ**: 各ステージで表示する画面
- **レシピ**: ステージ遷移時に実行するロジック

### 2. アセット生成

```
/create-workflow-app
```

対話的に以下を生成する:

#### Data Table (`*.data_table.json`)

データスキーマを定義する。システムフィールドが自動付与される:

| フィールド | 型 | 説明 |
|---|---|---|
| `id` | integer | 自動採番 |
| `created_at` | date_time | 作成日時 |
| `updated_at` | date_time | 更新日時 |
| `stage` | string | 現在のステージ |
| `created_by` | object | 作成者情報 |

これらに加え、業務固有のフィールドを定義する。

#### ページ (`*.page.json`)

各ステージの画面を定義する。主なコンポーネント:

- **Form** — 入力フォーム（テキスト、ドロップダウン、日付など）
- **Table** — データ一覧表示
- **Detail** — 詳細表示
- **Button** — アクションボタン（承認、却下など）

ページコンポーネントの詳細は `.claude/rules/workato-page-components.md`（Cursor: `.cursor/rules/workato-page-components.mdc`）を参照。

#### アプリ定義 (`lcap_app.json`)

ステージ遷移とページの紐付けを定義する:

```json
{
  "stages": [
    { "name": "submitted", "page": "submit.page.json" },
    { "name": "in_review", "page": "review.page.json" },
    { "name": "approved", "page": "done.page.json" }
  ]
}
```

#### レシピ

ステージ遷移時のロジック（通知送信、外部システム更新など）は `/create-recipe` に委譲して生成する。

### 3. デプロイ

```
ステップ 1: Workato UI → Settings → Workflow Apps → 有効化
  （初回のみ。これが唯一の UI 操作）

ステップ 2: /wpush
  → Data Table → lcap_app → Pages → Recipes の順で自動プッシュ

ステップ 3: UI で動作確認
  → フォーム入力 → ステージ遷移 → 通知 をテスト
```

## 設計のポイント

### ステージ設計

- ステージ名は **英語の snake_case** で定義する（UI 表示名は別途設定可能）
- 分岐がある場合（承認/却下）は、それぞれ別ステージにする
- 「差し戻し」がある場合は、元のステージに戻す遷移を定義する

### Data Table 設計

- **正規化しすぎない**: Workflow App のデータはアプリ内で完結するため、1テーブルにまとめるのが基本
- **外部 ID を持つ**: 外部システム連携がある場合は、外部システムの ID をフィールドに含める
- **ステージ履歴**: 承認者・承認日時を記録するフィールドを設ける

### ページ設計

- **1ステージ1ページ** が基本
- フォームの `dataSource` は Data Table のカラムにバインドする
- 読み取り専用のフィールドと編集可能なフィールドを明確に分ける
- ボタンの `action` でステージ遷移を定義する

## 既知の制限

- Workflow App の有効化は UI からのみ可能（CLI/API 非対応）
- `/wpush --delete` で Workflow App のアセットを削除すると、アプリが壊れる可能性がある。削除は UI から行う
- ページコンポーネントの一部（カスタム CSS 等）は UI でのみ設定可能。push 後に UI で微調整し、pull で取得する
