# データ同期 (Data Sync)

## いつ使うか

| 条件 | 該当 |
|---|---|
| ソースシステムのレコード変更を検知する | Yes |
| 宛先システムにレコードを反映する | Yes |
| 新規なら作成、既存なら更新したい | Yes |
| リアルタイム同期が必要 | Optional（ポーリングも可） |
| 双方向同期が必要 | No（別パターン） |

## レシピ構成図

### 基本形: トリガー → 検索 → Upsert

```
[トリガー] New/Updated record in ソースシステム
    │
    ├── [Action] Search record in 宛先システム（一意キーで検索）
    │
    ├── [IF] レコードが見つかった
    │   └── [Action] Update record in 宛先システム
    │
    └── [ELSE] レコードが見つからない
        └── [Action] Create record in 宛先システム
```

### 変換付き: トリガー → 変換 → Upsert

```
[トリガー] New/Updated record in ソースシステム
    │
    ├── [Function] データ変換・バリデーション（必要に応じて）
    ├── [Action] Search record in 宛先システム
    │
    └── [IF/ELSE] Create or Update
```

### バッチ同期: スケジュール → リスト取得 → ループ

```
[トリガー] Scheduled trigger（定期実行）
    │
    ├── [Action] Search records in ソースシステム（条件: 更新日 >= 前回実行日）
    │
    └── [Loop] 各レコードについて
        ├── [Action] Search in 宛先システム
        └── [IF/ELSE] Create or Update
```

## ステップ構成（基本形）

| # | Provider | Action | 目的 |
|---|---|---|---|
| 0 | ソースシステム | new_updated_record | レコード変更を検知 |
| 1 | 宛先システム | search_records | 一意キーで既存レコードを検索 |
| 2 | (if/else) | | 検索結果の有無で分岐 |
| 3a | 宛先システム | create_record | 新規レコード作成 |
| 3b | 宛先システム | update_record | 既存レコード更新 |

## 設計判断ポイント

| 判断 | 選択肢 | 判断基準 |
|---|---|---|
| トリガー種別 | Webhook / Polling / Schedule | リアルタイム性の要件。Webhook が最速、Schedule はバッチ向き |
| 一意キー | メールアドレス / 外部 ID / 名前 | 両システムで共通して持つ不変のフィールド |
| Upsert 方式 | Search + IF/ELSE / コネクタの upsert アクション | コネクタが upsert をサポートしていれば 1 ステップで済む |
| データ変換 | インライン / Recipe Function | 変換ロジックが複雑 or 再利用する場合は Function に分離 |
| エラーハンドリング | try/catch + 通知 / スキップ + ログ | 1件の失敗で全体を止めるか、スキップして続行するか |

## Upsert をサポートするコネクタ

一部のコネクタは `upsert` アクションを持ち、Search + IF/ELSE が不要:

- **Salesforce**: `upsert_sobject`（外部 ID フィールドで判定）
- **Database**: `upsert_row`（主キーで判定）
- **Google Sheets**: `upsert_row`（一意列で判定）

これらの場合は構成が単純になる:

```
[トリガー] New/Updated record
    └── [Action] Upsert record（1ステップで完了）
```

## 既知の注意点

- **無限ループの回避**: ソースと宛先が同じシステムの場合、Update がトリガーを再発火する。トリガーの条件フィルタや `updated_by` フィールドで自身の更新を除外する
- **検索結果が複数件**: Search で複数レコードがヒットする場合のハンドリングを決めておく（先頭を使う / エラーにする）
- **レート制限**: バッチ同期でループ処理する場合、宛先システムの API レート制限に注意。必要に応じてウェイトを入れる
- **フィールドマッピング**: ソースと宛先でフィールド名・型が異なる場合、明示的な変換が必要（特に日付フォーマット、数値型）
- **初回同期（バックフィル）**: 既存データの一括同期が必要な場合は、バッチ同期パターンを使い段階的に実行する

## 参照

- `docs/logic/loops.md` — ループ処理の構文
- `docs/logic/if-conditions.md` — IF/ELSE の条件設定
- `docs/patterns/recipe-patterns/error-notification.md` — 同期エラー時の通知パターン
