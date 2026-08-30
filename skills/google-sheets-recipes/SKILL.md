# Google Sheets recipes

Provider value to use in every step: `google_sheets`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "google_sheets"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (6)

| Internal name | Title | Batch |
|---|---|---|
| `new_polling_spreadsheet_row_v4` | New row in sheet in My Drive | - |
| `new_spreadsheet_row_v4` | New row in sheet in My Drive | - |
| `team_drive_new_spreadsheet_row_v4` | New row in sheet in Team Drive | - |
| `team_drive_updated_spreadsheet_row_v4_2` | New/updated row in sheet in Team Drive | - |
| `updated_polling_spreadsheet_row_v4_2` | New/updated row in sheet in My Drive | - |
| `updated_spreadsheet_row_v4_2` | New/updated row in sheet in My Drive | - |


## Actions (8)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_row_v4_bulk` | Add rows in bulk | yes |
| `add_spreadsheet_row_v4` | Add row | - |
| `get_spreadsheet_rows_v4` | Get rows | yes |
| `search_spreadsheet_rows_v4_new` | Search rows | yes |
| `update_row_v4_bulk` | Update rows in bulk | yes |
| `update_row_v4_new` | Update row | - |
| `update_spreadsheet_row_v3_new` | Update row using row ID (Deprecated) | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_spreadsheet_row` | New spreadsheet row added | - |
| `team_drive_updated_spreadsheet_row_v4` | New/updated row in sheet in Team Drive | - |
| `updated_spreadsheet_row_v4` | New/updated row in sheet in My Drive | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `add_spreadsheet_row` | Add a new row | - |
| `search_spreadsheet_rows` | Search rows by query | - |
| `search_spreadsheet_rows_v3_new` | Search rows using query (old version) | - |
| `update_spreadsheet_row` | Update a row | - |


## Field details

Input/output field definitions observed from the Workato UI. The Workato API does not expose these, so treat them as the authoritative source for required fields and types.

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


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
