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

## Call Recipe Function

別のレシピを呼び出してロジックを再利用する。

公式: https://docs.workato.com/en/connectors/recipe-functions.html

- レシピ間でロジックを共有
- 入力パラメータを渡し、結果を受け取る
- メンテナンスの一元化
