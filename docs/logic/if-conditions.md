# IF 条件分岐

公式ドキュメント: https://docs.workato.com/en/features/if-conditions.html

## 構造

```
IF (condition) → actions
ELSE IF (condition) → actions    ← 複数チェーン可
ELSE → actions                   ← デフォルト分岐
```

- 順次評価され、最初に true になった分岐のみ実行される
- ELSE IF / ELSE は省略可

## JSON 構造（推定）

```json
{
  "number": N,
  "keyword": "if",
  "input": {
    "conditions": [
      {
        "operand": "contains",
        "lhs": "#{_dp('...')}",
        "rhs": "値",
        "uuid": "..."
      }
    ],
    "operand": "and",
    "type": "compound"
  },
  "block": [ /* true 時のアクション */ ]
}
```

## 条件演算子一覧（14種）

| 演算子 | 対応型 | 説明 |
|---|---|---|
| `contains` | Array, String | 値を含む（大文字小文字区別） |
| `doesn't contain` | Array, String | 値を含まない |
| `starts with` | String | 指定値で始まる |
| `doesn't start with` | String | 指定値で始まらない |
| `ends with` | String | 指定値で終わる |
| `doesn't end with` | String | 指定値で終わらない |
| `equals` | All | 完全一致（数値はfloat変換比較） |
| `doesn't equal` | All | 不一致 |
| `greater than` | String, Integer, Number | より大きい（文字列はASCII比較） |
| `less than` | String, Integer, Number | より小さい |
| `is true` | Boolean | true である |
| `is not true` | Boolean | true でない |
| `is present` | All | 値が存在する（null/空文字はfalse） |
| `is not present` | All | 値が存在しない |

## 注意事項

- 全テキスト比較は **大文字小文字を区別する**
- null 値を数値演算子で比較するとエラー
- 複数条件は `and` / `or` で結合可能
- トリガーの `filter` と同じ条件構造を使用
