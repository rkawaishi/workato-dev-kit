# ループ（Repeat）

## Repeat for each

公式: https://docs.workato.com/en/recipes/repeat-for-each.html

リスト内の各アイテムに対してアクションを繰り返す。

### JSON 構造

```json
{
  "number": N,
  "keyword": "foreach",
  "as": "foreach",
  "clear_scope": false,
  "input": {},
  "source": "#{_dp('{\"pill_type\":\"output\",...,\"path\":[\"list_field\"]}')}",
  "block": [ /* 各アイテムに対するアクション */ ]
}
```

### ポイント

- `source`: イテレート対象のリスト（datapill）
- `clear_scope: false` で親スコープの変数にアクセス可能
- ループ内で現在アイテムを参照: `provider: "foreach"`, `line: "foreach"`, `path: ["fieldName"]`
- IF 条件をループ内で使う場合は「Clear step output」を Yes にする

### Repeat for each in batches

大量データをバッチ処理する場合:
- バッチサイズ設定可（デフォルト100）
- 高速データ転送に適する

## Repeat while

公式: https://docs.workato.com/en/recipes/loops.html

条件が true の間、アクションを繰り返す（do-while 型: 最低1回実行）。

### 主な用途

- **オフセットページネーション**: `Index * page_size` で順次取得
- **ページトークン**: 次ページトークンが存在する間ループ
- **固定回数**: `Index < (n-1)` で n 回実行
- **条件付き**: 特定結果になるまで繰り返し

### 制約

- **最大50,000回**のイテレーション制限
- 無限ループ防止のため、必ず終了条件を設計する
