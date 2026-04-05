# エラーハンドリング

公式: https://docs.workato.com/en/recipes/steps.html

## Handle Errors ステップ

2つのブロックで構成:

```
Handle errors
  ├── Monitor block — 監視対象のアクション群
  │     ├── action 1
  │     ├── action 2
  │     └── ...
  └── Error block — エラー時の処理
        ├── retry 設定（回数 + 間隔）
        └── リカバリアクション
```

### 動作

1. **Monitor block** 内の全アクションが成功 → Error block はスキップ
2. Monitor block 内でエラー発生 → Error block を実行
3. リトライ設定がある場合 → 指定回数・間隔でリトライ
4. 全リトライ失敗 → Error block 内の残りステップを実行

### リトライ設定

- リトライ回数
- リトライ間隔
- 条件付きリトライ（条件に基づいてリトライするかどうかを判定）

## Stop Job ステップ

レシピの実行を途中で停止する。

- **Failed** としてマーク: エラーメッセージ付きで失敗終了
- **Successful** としてマーク: 正常終了扱い

### 用途

- ビジネスロジック上の検証失敗時に早期終了
- 必要なデータが欠損している場合の防御的終了

## Recipe Functions（レシピ関数）

別のレシピを呼び出してロジックを再利用する。

公式: https://docs.workato.com/en/connectors/recipe-functions.html

- レシピ間でロジックを共有
- 入力パラメータを渡し、結果を受け取る
- メンテナンスの一元化

### 作成手順

1. 新規レシピを作成し、トリガーに「Recipe function」を選択
2. Input Schema（JSON）を定義 — 呼出し元から受け取るパラメータ
3. Response Schema（JSON）を定義 — 呼出し元に返すデータ
4. レシピ内にロジックを構築

### 呼び出し方

1. 呼出し元レシピで「Call recipe」アクションを追加
2. 対象の Recipe function を選択
3. Input Schema のフィールドに datapill をマッピング
4. Response のデータピルが後続ステップで利用可能に

> **注意**: 旧 Callable recipes コネクタは非推奨。新規作成は Recipe functions コネクタを使用。

## `try` キーワード（JSON 表現）

レシピ JSON では `keyword: "try"` がエラーハンドリングブロック（try/catch パターン）を示す。UI の Monitor/Error ブロックに対応する JSON 表現。

- try ブロック内のステップでエラーが発生した場合、catch ブロック（エラーハンドラー）に制御が移る
