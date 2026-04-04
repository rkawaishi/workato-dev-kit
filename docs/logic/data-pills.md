# データピルとデータマッピング

公式: https://docs.workato.com/en/recipes/data-pills-and-mapping.html

## データピルとは

トリガーやアクションステップの出力変数。後続のステップで参照してデータフローを構成する。

## データ型

| 型 | 説明 |
|---|---|
| String | 文字列 |
| Integer / Number | 整数 / 数値 |
| Date / Datetime | 日付 / 日時 |
| Boolean | 真偽値 |
| Object | オブジェクト（ネストされたフィールド群） |
| List (Array) | リスト（配列） |

### 型変換フォーミュラ

| 変換先 | フォーミュラ |
|---|---|
| 整数 | `.to_i` |
| 浮動小数点 | `.to_f` |
| 文字列 | `.to_s` |
| 日付 | `.to_date` |
| 日時 | `.to_time` |
| 通貨 | `.to_currency` |

## マッピングルール

### 変数 vs 定数

- **変数（datapill）**: トリガーイベントごとに値が変化（例: 各リードの Account Name）
- **定数**: 固定値（例: メールテンプレート内の固定テキスト）
- **ハイブリッド**: 1つのフィールドに datapill と定数を混在

### システムデータピル

全ジョブで利用可能な組み込み datapill:

| datapill | 説明 |
|---|---|
| User ID / User name / User email | 実行ユーザー情報 |
| Recipe ID / Recipe URL / Recipe name | レシピ情報 |
| Job ID / Job created at | ジョブ情報 |
| Root recipe ID / Root job ID | ネスト呼出し元 |
| Is repeat / Repeat count | リトライ情報 |
| Is test | テストモードかどうか |

### エラーデータピル

エラーハンドリング（Handle errors）ブロック内で利用可能:

| datapill | 説明 |
|---|---|
| Error type | エラー種別 |
| Error message | エラーメッセージ |
| Retry count | リトライ回数 |
| Errored step number | エラー発生ステップ番号 |
| Errored app | エラー発生アプリ |
| Errored action | エラー発生アクション |
| Inner message | サードパーティの生レスポンス |

## JSON 内での datapill 表現

```
#{_dp('{"pill_type":"output","provider":"<provider>","line":"<as>","path":["field","nested"]}')}
```

詳細は `@docs/learned-patterns.md` の Datapill 記法セクション参照。

## 注意事項

- **隠しフィールド**: スキーマ未定義のフィールドはブラケット記法で参照: `Parent_object['field_name']`
- **条件分岐未実行時**: 未実行の分岐のデータピルは null になる
- **同名フィールド**: 異なるステップの同名データピルに注意。参照元ステップを確認する
- **必須フィールド**: 設計時にマッピングしても実行時に値が欠損する可能性がある
