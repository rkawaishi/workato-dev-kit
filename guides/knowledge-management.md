# ナレッジ管理ガイド

ツールキットのナレッジベースを育てる仕組みと運用方法。

## なぜナレッジ管理が必要か

Workato のレシピ JSON には以下の特性がある:

- **公式ドキュメントに載っていないフィールド** が多い（`extended_output_schema` の具体的な構造など）
- **UI でしか設定できない値** がある（`pick_list` の選択肢、動的スキーマ）
- **コネクタごとの癖** がある（フィールド名の命名規則、必須/任意の違い）

これらは開発を重ねるうちに判明するが、個人の記憶に留まりがち。本ツールキットでは、この暗黙知をドキュメントとして蓄積し、次のレシピ生成に活用する。

## ナレッジの構造

```
docs/
├── connectors/             # コネクタ別の仕様（316件 + カスタム）
│   ├── _index.md           # コネクタ一覧
│   ├── salesforce.md       # Salesforce のトリガー/アクション/フィールド
│   ├── jira.md             # Jira のトリガー/アクション/フィールド
│   └── ...
├── logic/                  # レシピロジック
│   ├── data-pills.md       # datapill 記法と参照パターン
│   ├── formulas.md         # 数式関数
│   ├── loops.md            # 繰り返し処理
│   ├── error-handling.md   # エラーハンドリング
│   ├── triggers.md         # トリガーの種類と設定
│   └── file-handling.md    # ファイル操作
├── platform/               # プラットフォーム機能
│   ├── data-tables.md      # Data Table
│   ├── lookup-tables.md    # Lookup Table
│   ├── agent-studio.md     # Genie (Agent Studio)
│   ├── mcp.md              # MCP サーバー
│   └── ...
├── patterns/               # 設計パターン
│   ├── recipe-patterns/    # レシピ構築パターン（汎用）
│   ├── deployment-guide.md # デプロイ手順
│   ├── shared-assets.md    # 共有アセット設計
│   └── workspace-management.md  # ワークスペース管理
└── connector-sdk/          # Connector SDK
    ├── overview.md
    └── connector-rb.md
```

加えて、組織固有のナレッジは別リポジトリで管理:

```
connectors/docs/            # カスタムコネクタの仕様
projects/docs/patterns/     # 組織ドメインの構築パターン
```

## 学習サイクルの回し方

### 1. /learn-recipe — レシピから学ぶ

UI で調整したレシピを pull した後に実行する。

```
/wpull                         # UI の変更をローカルに取得
/learn-recipe <project-name>   # プロジェクト全体を学習
```

**何が学習されるか:**

| 発見内容 | 反映先 | 例 |
|---|---|---|
| フィールド定義 | `docs/connectors/<provider>.md` | Salesforce の Account に `BillingCity` フィールドがある |
| 新アクション | `docs/connectors/<provider>.md` | Jira に `Create sprint` アクションがある |
| datapill パターン | `docs/logic/data-pills.md` | `#{_('data.xxx.yyy')}` の新しい参照パターン |
| JSON 構造 | `.claude/rules/` | `toggle_cfg` の新しい使い方 |
| デプロイ知見 | `docs/patterns/deployment-guide.md` | 特定条件で push が失敗するケース |

**ポイント:**
- 既存のドキュメントに直接追記する（中間ファイルは使わない）
- 重複チェックを行い、既知の情報は追記しない
- `docs/learned-patterns.md` は一時保管場所。適切な場所に振り分けられるまでの仮置き

### 2. /learn-pattern — 構築パターンを記録

エキスパートの「こういう時はこう組む」という知見をパターンとして記録する。

```
/learn-pattern
```

対話的にパターンの詳細を聞き出し、以下の構造でドキュメント化する:

```markdown
# パターン名

## いつ使うか
- 条件1
- 条件2

## レシピ構成図
trigger → step1 → step2 → ...

## ステップ構成
各ステップの詳細

## 設計判断
なぜこの構成を選ぶか

## 落とし穴
注意すべきポイント
```

**パターンの保存先:**
- **汎用パターン** → `docs/patterns/recipe-patterns/` — Workato 全般に適用できるもの
- **組織ドメインパターン** → `projects/docs/patterns/` — 特定の業務や組織に固有のもの

**パターンの活用:**
- `/create-recipe` のステップ設計時に自動参照される
- `/design` のアーキテクチャ決定時に候補として提案される
- パターンはモノリシックなテンプレートではなく、組み合わせ可能なブロック

### 3. /sync-connectors — コネクタ情報を同期

コネクタの最新情報を取得し、ドキュメントを更新する。

```
/sync-connectors salesforce    # Salesforce のみ同期
/sync-connectors --custom      # カスタムコネクタのみ同期
/sync-connectors --all         # 全コネクタを同期
```

**Pre-built コネクタ:**
- Workato API からトリガー/アクションのメタデータを取得
- `docs/connectors/<provider>.md` を更新
- 手書きのフィールド詳細セクションは保持される

**カスタムコネクタ:**
- `connectors/*/connector.rb` を Ruby DSL パースで解析
- `connectors/docs/<name>.md` を生成・更新
- `input_fields`, `output_fields`, `object_definitions` を抽出

## 推奨ワークフロー

### 新しいコネクタを初めて使う時

```
1. /sync-connectors <provider>     # コネクタ情報を取得
2. /create-recipe                  # レシピを生成
3. /wpush --start                  # デプロイ
4. UI で調整                       # pick_list の選択、フィールド微調整
5. /wpull                          # 変更を取得
6. /learn-recipe                   # 調整結果を学習
```

2回目以降は手順 1, 4, 5, 6 が不要になり、ナレッジから直接正しいレシピが生成できる。

### 繰り返し発生する構築パターンに気づいた時

```
1. /learn-pattern                  # パターンを記録
2. 以降の /create-recipe で自動活用
```

### プロジェクト引き継ぎ時

```
1. /wpull --all                    # 全プロジェクトを取得
2. /learn-recipe <project>         # 各プロジェクトから学習
3. /catalog                        # 共有アセットを棚卸し
```

## ナレッジの品質を保つ

- **重複を避ける**: 各スキルは追記前に既存内容をチェックする
- **適切な場所に配置する**: `docs/learned-patterns.md` は仮置き場所。発見した知見は適切なドキュメントに直接追記する
- **古い情報を更新する**: コネクタの仕様変更があれば `/sync-connectors` で上書き更新
- **組織固有と汎用を分ける**: 業務ルールに依存するパターンは `projects/docs/patterns/` に、Workato 共通のパターンは `docs/patterns/recipe-patterns/` に配置
