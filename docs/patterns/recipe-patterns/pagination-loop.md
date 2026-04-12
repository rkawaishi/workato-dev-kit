# ページネーションループ (Pagination Loop)

## いつ使うか

| 条件 | 該当 |
|---|---|
| API が一度に返すレコード数に上限がある | Yes |
| 全件を取得する必要がある | Yes |
| レート制限のある API を呼ぶ | Optional |

## レシピ構成図

### オフセットベース

```
[コンテキスト] 全件取得が必要な箇所
    │
    ├── [Variable] results リスト変数を初期化（カラム定義 = 後続で必要なフィールド）
    │
    └── [Repeat while] 取得件数 == page_size（まだ次ページがある）
        │
        └── [Handle Errors]
            ├── Monitor block
            │   ├── [Action] API からレコード取得（offset = index * page_size）
            │   └── [Variable] results に取得レコードを追加
            └── Error block
                ├── (retry: レート制限対策)
                └── [Action] エラー通知
```

### トークンベース

```
[コンテキスト] 全件取得が必要な箇所
    │
    ├── [Variable] results リスト変数を初期化（カラム定義 = 後続で必要なフィールド）
    ├── [Variable] next_page_token を初期化（空文字 or 初回トークン）
    │
    └── [Repeat while] next_page_token が存在する
        │
        └── [Handle Errors]
            ├── Monitor block
            │   ├── [Action] API からレコード取得（page_token = next_page_token）
            │   ├── [Variable] results に取得レコードを追加
            │   └── [Variable] next_page_token をレスポンスの値で更新
            └── Error block
                ├── (retry: レート制限対策)
                └── [Action] エラー通知
```

## ステップ構成

### オフセットベース

Repeat while の `index * page_size` で offset を算出できるため、offset 用の変数は不要。

| # | keyword / Provider | Action | 目的 |
|---|---|---|---|
| N | workato_variable | create_list | results リスト変数を初期化（カラム = 後続で必要なフィールド） |
| N+1 | repeat_while | | 終了条件: 取得件数 < page_size |
| N+1.1 | try | | エラーハンドリング |
| N+1.1.1 | 外部サービス | search / list | offset = index * page_size でレコード取得 |
| N+1.1.2 | workato_variable | append_list | results に取得レコードを追加 |
| N+1.1.3 | catch | | レート制限エラー時のリトライ + 通知 |

### トークンベース

next_page_token を変数に保管し、ループごとに更新する。

| # | keyword / Provider | Action | 目的 |
|---|---|---|---|
| N | workato_variable | create_list | results リスト変数を初期化（カラム = 後続で必要なフィールド） |
| N+1 | workato_variable | create_variable | next_page_token を初期化 |
| N+2 | repeat_while | | 終了条件: next_page_token が空 |
| N+2.1 | try | | エラーハンドリング |
| N+2.1.1 | 外部サービス | search / list | page_token = next_page_token でレコード取得 |
| N+2.1.2 | workato_variable | append_list | results に取得レコードを追加 |
| N+2.1.3 | workato_variable | update_variable | next_page_token をレスポンスの値で更新 |
| N+2.1.4 | catch | | レート制限エラー時のリトライ + 通知 |

## 設計判断ポイント

| 判断 | 選択肢 | 判断基準 |
|---|---|---|
| ページネーション方式 | オフセット / トークン | API の仕様に依存。トークン方式の方がデータの整合性が高い |
| ページサイズ | API の最大値 / 小さめの値 | レート制限が厳しければ小さめにして 1 リクエストあたりの負荷を下げる |
| 終了条件 | 取得件数 < page_size / next_token が空 / 合計件数に到達 | API のレスポンスで判断できる情報を使う |
| エラーハンドリング | try/catch + retry / ループ中断 | レート制限（429）はリトライで回復可能。その他のエラーはループ中断を検討 |
| 取得データの処理 | ループ内で即処理 / 全件取得後に一括処理 | データ量とメモリ。大量データはループ内で即処理した方が安全 |

## 既知の注意点

- **Repeat while は最大 50,000 回** のイテレーション制限がある。page_size × 50,000 を超えるデータ量の場合は別のアプローチが必要
- **Repeat while は do-while 型** — 最低 1 回は実行される。データが 0 件でも 1 回は API を呼ぶ
- **レート制限（429）対策**: try/catch 内で retry を設定する。リトライ間隔は API の制限に合わせる
- **オフセットのずれ**: ループ中にソース側でレコードが追加・削除されると、オフセットがずれてレコードの重複・欠落が起きる。クリティカルなデータ同期ではトークン方式を優先する
- **リスト変数のカラム定義**: `create_list` で定義するカラムは API の output_fields 全てではなく、後続ステップで必要なカラムだけで十分。不要なカラムを含めると datapill の選択肢が増えて煩雑になる
- **空レスポンスの扱い**: API によっては最終ページで空配列を返す場合がある。終了条件を `取得件数 == 0` にするか `取得件数 < page_size` にするかは API の挙動に合わせる

## 参照

- `docs/logic/loops.md` — Repeat while / Repeat for each の構文
- `docs/logic/error-handling.md` — Handle Errors / retry の構文
