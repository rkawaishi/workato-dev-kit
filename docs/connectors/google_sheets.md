# Google Sheets connector

Provider: `google_sheets`

## Triggers

| Name | Internal name | Batch | Description |
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

| Name | Internal name | Batch | Description |
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

## Field details

### search_spreadsheet_rows_v4_new (Search rows)

Kind: Action
Learned from: existing knowledge (manual)

#### Input fields
| Field | Type | Required | Description |
|---|---|---|---|
| spreadsheet_id | string | Yes | Spreadsheet ID (between /d/ and /edit in the URL) |
| sheet | string | Yes | Sheet name |
| team_drives | string | - | `my_drive` or Team Drive ID |
| count | integer | - | Number of entries to fetch (default: 200) |

#### Output fields
| Field | Type | Description |
|---|---|---|
| rows[] | array of object | List of rows in the search result |
| rows[].col_<column_name> | string | The spreadsheet header name becomes the field name prefixed with `col_` |

### new_polling_spreadsheet_row_v4 (New row in sheet in My Drive)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: dynamic schema unresolved (spreadsheet/sheet not selected)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to monitor for new row. |
| Trigger poll interval | integer | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Row number (deprecated) | text | — |
| Row number | integer | — |

### new_spreadsheet_row_v4 (New row in sheet in My Drive)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: Real-time variant; dynamic schema unresolved (spreadsheet/sheet not selected)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to monitor for new row. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Row number (deprecated) | text | — |
| Row number | integer | — |

### team_drive_new_spreadsheet_row_v4 (New row in sheet in Team Drive)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: dynamic schema unresolved (spreadsheet/sheet not selected)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Google Drive | text | - | Yes | Select a team drive. |
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to monitor for new row. |
| Trigger poll interval | integer | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Row number (deprecated) | text | — |
| Row number | integer | — |

### updated_polling_spreadsheet_row_v4_2 (New/updated row in sheet in My Drive)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: Polling variant; dynamic schema unresolved (spreadsheet/sheet not selected)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to monitor for new/updated row. |
| Trigger poll interval | integer | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Row number (deprecated) | text | — |
| Row number | integer | — |
| Updated | boolean | — |

### updated_spreadsheet_row_v4_2 (New/updated row in sheet in My Drive)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: Real-time variant; dynamic schema unresolved

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to monitor for new/updated row. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Row number (deprecated) | text | — |
| Row number | integer | — |
| Updated | boolean | — |

### team_drive_updated_spreadsheet_row_v4_2 (New/updated row in sheet in Team Drive)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: dynamic schema unresolved (spreadsheet/sheet not selected)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Google Drive | text | - | Yes | Select a team drive. |
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to monitor for new/updated row. |
| Trigger poll interval | integer | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Row number (deprecated) | text | — |
| Row number | integer | — |
| Updated | boolean | — |

### add_spreadsheet_row_v4 (Add row)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: dynamic Rows column schema unresolved (no spreadsheet selected)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Google Drive | text | - | Yes | Select a personal drive or a team drive. Defaults to your personal drive. |
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to add row to. |
| Enforce top-left insert | text | - | Yes | Choose this option to insert into the leftmost logical table when there are more than one table in same sheet. Default is set to no. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Updated range | text | — |
| Updated rows | text | — |
| Updated columns | text | — |
| Updated cells | text | — |

### add_row_v4_bulk (Add rows in bulk)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: Batch action; List of batches contains repeated child fields (per row). Dynamic Rows column schema unresolved.

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Google Drive | text | - | Yes | Select a personal drive or a team drive. Defaults to your personal drive. |
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to add row to. |
| Enforce top-left insert | text | - | Yes | Choose this option to insert into the leftmost logical table when there are more than one table in same sheet. Default is set to no. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Spreadsheet ID | text | — |
| Sheet name | text | — |
| All rows successfully added? | boolean | — |
| Number of rows added | integer | — |
| Number of rows failed | integer | — |
| CSV contents of failed rows | text | — |
| List of batches | array | Array elements: Batch number / All rows successfully added? / Starting row / Ending row / Number of rows added / Number of rows failed / Error code / Error text / List size / List index |

### update_row_v4_new (Update row)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: Dynamic input row columns and search criteria unresolved (no spreadsheet selected)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Google Drive | text | - | Yes | Select a personal drive or a team drive. Defaults to your personal drive. |
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to update row. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Spreadsheet ID | text | — |
| Spreadsheet name | text | — |
| Sheet name | text | — |
| Updated range | text | — |
| Updated columns count | integer | — |

### update_row_v4_bulk (Update rows in bulk)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: Batch action; List of batches contains repeated child fields (per row). Dynamic Rows column schema unresolved.

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Google Drive | text | - | Yes | Select a personal drive or a team drive. Defaults to your personal drive. |
| Spreadsheet |  | Yes | Yes | Select a spreadsheet to update row. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Spreadsheet ID | text | — |
| Sheet name | text | — |
| All rows successfully updated? | boolean | — |
| Number of rows updated | integer | — |
| Number of rows failed | integer | — |
| CSV contents of failed rows | text | — |
| List of batches | array | Array elements: Batch number / All rows successfully updated? / Starting row / Ending row / Number of rows updated / Number of rows failed / Error code / Error text / List size / List index |

## Learning failures

(None — all ops completed with `status=ok`. The output schema of `get_spreadsheet_rows_v4` is partial due to dynamic schema, recorded under the `> ⚠ Partial learning` notes in the sections above rather than in this log.)

---

## Learning summary

Last run: 2026-04-27 by `/auto-learn`
- Attempted: 11 op (6 triggers + 5 actions)
- Fully learned: 1 — `update_row_v4_new`
- Partially learned: 10 — 6 triggers (`new_polling_spreadsheet_row_v4`, `new_spreadsheet_row_v4`, `team_drive_new_spreadsheet_row_v4`, `updated_polling_spreadsheet_row_v4_2`, `updated_spreadsheet_row_v4_2`, `team_drive_updated_spreadsheet_row_v4_2`) + 4 actions (`add_spreadsheet_row_v4`, `add_row_v4_bulk`, `get_spreadsheet_rows_v4`, `update_row_v4_bulk`)
- Failed: 0
- Skipped:
  - Deprecated: 7
  - adhoc: 1 — `__adhoc_http_action`
  - Already learned: 1 — `search_spreadsheet_rows_v4_new`

### Needs follow-up

- **Dynamic schema (needs `/learn-recipe`)** — Because the Spreadsheet/Sheet picklist is not selected, the dynamic column schema under `Rows[]` cannot be captured
  - 6 triggers — columns under output `Rows[]` are not expanded (`new_polling_spreadsheet_row_v4` and 5 others)
  - `get_spreadsheet_rows_v4` — the entire output schema is unresolved (no group appears in the datatree)
  - `add_spreadsheet_row_v4` — input Rows columns are not expanded
  - `add_row_v4_bulk` / `update_row_v4_bulk` — the per-row column schema under `List of batches` is unresolved
  - Common to all ops: columns under `Rows[]` are only expanded once the `Spreadsheet` picklist is selected

### Structural notes (for reference)

- The output for triggers can only resolve metadata (`Spreadsheet ID`, `Spreadsheet name`, `Sheet name`, `Row number`). Capturing actual columns requires selecting a sandbox spreadsheet.
- The existing `search_spreadsheet_rows_v4_new` section uses a snake_case manual schema. When re-learning, prefer `--force` to unify on the UI-derived label format.
- Row misalignment in the existing Actions table (rows 47-50) was fixed in this run.
