# Google Sheets コネクタ

Provider: `google_sheets`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New row in sheet in My Drive | `new_polling_spreadsheet_row_v4` | - |  |
| New spreadsheet row added | `new_spreadsheet_row` | - |  [deprecated] |
| New row in sheet in My Drive | `new_spreadsheet_row_v4` | - |  |
| New row in sheet in Team Drive | `team_drive_new_spreadsheet_row_v4` | - |  |
| New/updated row in sheet in Team Drive | `team_drive_updated_spreadsheet_row_v4` | - |  [deprecated] |
| New/updated row in sheet in Team Drive | `team_drive_updated_spreadsheet_row_v4_2` | - |  |
| New/updated row in sheet in My Drive | `updated_polling_spreadsheet_row_v4_2` | - |  |
| New/updated row in sheet in My Drive | `updated_spreadsheet_row_v4` | - |  [deprecated] |
| New/updated row in sheet in My Drive | `updated_spreadsheet_row_v4_2` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add rows in bulk | `add_row_v4_bulk` | Yes |  |
| Add a new row | `add_spreadsheet_row` | - |  [deprecated] |
| Add row | `add_spreadsheet_row_v4` | - |  |
| Get rows | `get_spreadsheet_rows_v4` | Yes |  |
| Search rows by query | `search_spreadsheet_rows` | - |  [deprecated] |
| Search rows using query (old version) | `search_spreadsheet_rows_v3_new` | - |  [deprecated] |
| Search rows | `search_spreadsheet_rows_v4_new` | Yes |  |
| Update rows in bulk | `update_row_v4_bulk` | Yes |  |
| Update row | `update_row_v4_new` | - |  |
| Update a row | `update_spreadsheet_row` | - |  [deprecated] |
| Update row using row ID (Deprecated) | `update_spreadsheet_row_v3_new` | - |  |

## フィールド詳細

### search_spreadsheet_rows_v4_new (Search rows)

種別: Action
学習元: 既存ナレッジ（手動）

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| spreadsheet_id | string | Yes | スプレッドシート ID（URL の /d/ と /edit の間） |
| sheet | string | Yes | シート名 |
| team_drives | string | - | `my_drive` or Team Drive ID |
| count | integer | - | 取得件数（デフォルト: 200） |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| rows[] | array of object | 検索結果の行一覧 |
| rows[].col_<カラム名> | string | スプレッドシートのヘッダー名が `col_` プレフィックス付きでフィールド名になる |

### new_polling_spreadsheet_row_v4 (New row in sheet in My Drive)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: dynamic schema unresolved (spreadsheet/sheet not selected)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to monitor for new row. |
| Trigger poll interval | integer | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Row number (deprecated) | text | — |
| Row number | integer | — |

### new_spreadsheet_row_v4 (New row in sheet in My Drive)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: Real-time variant; dynamic schema unresolved (spreadsheet/sheet not selected)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to monitor for new row. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Row number (deprecated) | text | — |
| Row number | integer | — |

### team_drive_new_spreadsheet_row_v4 (New row in sheet in Team Drive)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: dynamic schema unresolved (spreadsheet/sheet not selected)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Google Drive | text | - | Yes | Select a team drive. |
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to monitor for new row. |
| Trigger poll interval | integer | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Row number (deprecated) | text | — |
| Row number | integer | — |

### updated_polling_spreadsheet_row_v4_2 (New/updated row in sheet in My Drive)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: Polling variant; dynamic schema unresolved (spreadsheet/sheet not selected)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to monitor for new/updated row. |
| Trigger poll interval | integer | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Row number (deprecated) | text | — |
| Row number | integer | — |
| Updated | boolean | — |

### updated_spreadsheet_row_v4_2 (New/updated row in sheet in My Drive)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: Real-time variant; dynamic schema unresolved

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to monitor for new/updated row. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Row number (deprecated) | text | — |
| Row number | integer | — |
| Updated | boolean | — |

### team_drive_updated_spreadsheet_row_v4_2 (New/updated row in sheet in Team Drive)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: dynamic schema unresolved (spreadsheet/sheet not selected)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Google Drive | text | - | Yes | Select a team drive. |
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to monitor for new/updated row. |
| Trigger poll interval | integer | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Row number (deprecated) | text | — |
| Row number | integer | — |
| Updated | boolean | — |

### add_spreadsheet_row_v4 (Add row)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: dynamic Rows column schema unresolved (no spreadsheet selected)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Google Drive | text | - | Yes | Select a personal drive or a team drive. Defaults to your personal drive. |
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to add row to. |
| Enforce top-left insert | text | - | Yes | Choose this option to insert into the leftmost logical table when there are more than one table in same sheet. Default is set to no. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Updated range | text | — |
| Updated rows | text | — |
| Updated columns | text | — |
| Updated cells | text | — |

### add_row_v4_bulk (Add rows in bulk)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: Batch action; List of batches contains repeated child fields (per row). Dynamic Rows column schema unresolved.

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Google Drive | text | - | Yes | Select a personal drive or a team drive. Defaults to your personal drive. |
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to add row to. |
| Enforce top-left insert | text | - | Yes | Choose this option to insert into the leftmost logical table when there are more than one table in same sheet. Default is set to no. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Spreadsheet ID | text | — |
| Sheet name | text | — |
| All rows successfully added? | boolean | — |
| Number of rows added | integer | — |
| Number of rows failed | integer | — |
| CSV contents of failed rows | text | — |
| List of batches | array | 配列要素: Batch number / All rows successfully added? / Starting row / Ending row / Number of rows added / Number of rows failed / Error code / Error text / List size / List index |

### update_row_v4_new (Update row)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: Dynamic input row columns and search criteria unresolved (no spreadsheet selected)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Google Drive | text | - | Yes | Select a personal drive or a team drive. Defaults to your personal drive. |
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to update row. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Updated range | text | — |
| Updated columns count | integer | — |

### update_row_v4_bulk (Update rows in bulk)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: Batch action; List of batches contains repeated child fields (per row). Dynamic Rows column schema unresolved.

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Google Drive | text | - | Yes | Select a personal drive or a team drive. Defaults to your personal drive. |
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to update row. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Spreadsheet ID | text | — |
| Sheet name | text | — |
| All rows successfully updated? | boolean | — |
| Number of rows updated | integer | — |
| Number of rows failed | integer | — |
| CSV contents of failed rows | text | — |
| List of batches | array | 配列要素: Batch number / All rows successfully updated? / Starting row / Ending row / Number of rows updated / Number of rows failed / Error code / Error text / List size / List index |

## 学習失敗ログ

- get_spreadsheet_rows_v4: status=ok (output empty), reason=output schema not materialized in datatree until Spreadsheet picklist is selected (dynamic output) — 2026-04-27

---

## 学習サマリ

最終実行: 2026-04-27 by /auto-learn
- 試行: 11 op (6 triggers + 5 actions)
- 完全成功: 9
- 部分学習: 2
- 学習失敗: 0
- スキップ:
  - Deprecated: 7
  - adhoc: 1 — `__adhoc_http_action`
  - 既学習: 1 — `search_spreadsheet_rows_v4_new`

### 要 follow-up

- **Dynamic schema (要 /learn-recipe)** — Spreadsheet/Sheet picklist 未選択により `Rows[]` 配下の動的列スキーマが取れない
  - `get_spreadsheet_rows_v4` — output schema 全体が未確定（datatree に group 出現せず）
  - `add_row_v4_bulk` / `update_row_v4_bulk` — `List of batches` 配下の per-row column schema が未確定
  - 全 op 共通: `Spreadsheet` picklist 選択時にしか `Rows[]` 配下のカラムは展開されない

### 構造的注記（参考）

- Triggers の output は metadata（`Spreadsheet ID`, `Spreadsheet name`, `Sheet name`, `Row number`）のみ resolve 可能。実カラムは sandbox spreadsheet 選択が必要
- `search_spreadsheet_rows_v4_new` 既存セクションは snake_case 手動 schema。再学習時は `--force` で UI 由来の label format に統一推奨
- 既存 Actions テーブルの行ずれ（rows 47-50）を本 run で修正済み
