# Google BigQuery recipes

Provider value to use in every step: `google_big_query`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "google_big_query"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `new_job_completed` | New job completed | - |
| `new_row` | New row | - |
| `new_rows_batch` | New rows | yes |
| `scheduled_query` | Scheduled query | yes |


## Actions (12)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `get_query_job_output` | Get batch of rows by Job ID | yes |
| `insert_row` | Insert row | - |
| `insert_rows_stream` | Insert rows | yes |
| `load_data_from_file` | Load data into BigQuery | - |
| `load_data_from_google_table` | Load data from Google Cloud Storage into BigQuery | - |
| `run_custom_sql_sync` | Run custom SQL in BigQuery | - |
| `search_rows` | Select rows (Old) | yes |
| `search_rows_sync` | Select rows | yes |
| `search_rows_using_custom_sql` | Select rows using custom SQL (Old) | yes |
| `search_rows_using_custom_sql_sync` | Select rows using custom SQL | yes |
| `search_rows_using_custom_sql_sync_insert_table` | Select rows using custom SQL and insert into table | yes |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `insert_rows` | Insert rows | yes |
| `run_custom_sql` | Run custom SQL in BigQuery | - |


## Field details

Input/output field definitions observed from the Workato UI. The Workato API does not expose these, so treat them as the authoritative source for required fields and types.

### new_job_completed (New job completed)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| When first started, this recipe should pick up events from | date-time | - | Yes | When you start recipe for the first time, it picks up trigger events from this specified date and time. Defaults to fetching records created an hour ago if left blank. Once recipe has been run or tested, value cannot be changed. |
| Trigger poll interval | integer | - | No | — |
| Dataset | text | - | No | — |
| Table | text | - | No | — |
| All users | text | - | No | — |
| Job type | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| ID | text | — |
| Kind | text | — |
| Job reference | object | — |
| Project ID | text | — |
| Job ID | text | — |
| Location | text | — |
| State | text | — |
| Statistics | object | — |
| Creation time | text | — |
| Start time | text | — |
| End time | text | — |
| Total bytes processed | text | — |
| Load | object | — |
| Completion ratio | integer | — |
| Extract | object | — |
| Query | object | — |
| Total slot ms | text | — |
| Reservation usage | array | — |
| Reservation ID | text | — |
| Configuration | object | — |
| Job type | text | — |
| COPY | object | — |
| Status | object | — |
| Error result | object | — |
| Errors | array | — |
| User email | text | — |

> ⚠ `Load` / `Extract` / `Query` / `State` appear duplicated under both the `Statistics` and `Configuration` objects. Note that they look flat because the data tree's paddingLeft is uniformly 0.

### new_row (New row)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_missing, dynamic schema unresolved (project not selected)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Dataset |  | Yes | Yes | The dataset which contains the table to load the data to. |
| Table |  | Yes | Yes | The table of the dataset to load the data to. |
| Unique key |  | Yes | Yes | Select a unique key column to deduplicate rows. Performance can be improved if the selected unique key is indexed. |
| Use Standard SQL | text | - | Yes | Set to true to use Standard SQL instead of legacy SQL. |
| Trigger poll interval | integer | - | No | — |
| Location | text | - | No | — |
| Output columns | text | - | No | — |

#### Output fields
(Unlearned: dynamic schema — output is not displayed unless Project/Dataset/Table are selected)

### new_rows_batch (New rows)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_missing, dynamic schema unresolved (project not selected)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Dataset |  | Yes | Yes | The dataset which contains the table to load the data to. |
| Table |  | Yes | Yes | The table of the dataset to load the data to. |
| Unique key |  | Yes | Yes | Select a unique key column to deduplicate rows. Performance can be improved if the selected unique key is indexed. |
| Batch size | integer | - | Yes | Number of rows to process in each job. Larger batch size will increase recipe speed & data throughput. Defaults to 100. |
| Use Standard SQL | text | - | Yes | Set to true to use Standard SQL instead of legacy SQL. |
| Trigger poll interval | integer | - | No | — |
| Location | text | - | No | — |
| Output columns | text | - | No | — |

#### Output fields
(Unlearned: dynamic schema — output is not displayed unless Project/Dataset/Table are selected)

### scheduled_query (Scheduled query)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_missing, dynamic schema unresolved (project not selected)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Query | string (code editor) | Yes | Yes | Provide a valid SQL string to be executed. Toggle the 'use legacy SQL' field if you want to use legacy SQL in the input above. It will support only select query. |
| Automatic schema introspection | text | - | Yes | Toggle to Yes to automatically generate schema based on the query result. Defaults to No to minimize cost. To define columns manually, use the Output fields below. |
| Schedule settings |  | - | Yes | — |
| Unique key | text | - | No | — |
| Max batch size | integer | - | Yes | — |
| Location | text | - | No | — |
| Use legacy SQL | text | - | No | — |

#### Output fields
(Unlearned: dynamic schema — the Query result columns become the output. Only resolved when `Automatic schema introspection=Yes` or `Output fields` is defined manually)

### get_query_job_output (Get batch of rows by Job ID)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_missing, dynamic schema unresolved (project not selected)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Job ID | text | Yes | Yes | ID of the job. This can be found from the 'Job completed in BigQuery Trigger'. |
| Page token | text | - | Yes | Page token, returned by a previous call, to request the next page of results. |
| Output fields |  | Yes | Yes | Use this to manually define the columns returned in your query. Only needed when queries take too long. |
| Page size | integer | - | No | — |
| Start index | integer | - | No | — |
| Location | text | - | No | — |

#### Output fields
(Unlearned: dynamic schema — result columns are generated based on the manual definition in `Output fields`)

### insert_row (Insert row)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Dataset |  | Yes | Yes | The dataset which contains the table to load the data to. |
| Table |  | Yes | Yes | The table of the dataset to load the data to. |
| Ignore schema mismatch | text | - | No | — |
| Skip invalid rows | text | - | No | — |

> ⚠ Dynamic input: after Project/Dataset/Table are selected, the target table's columns expand as input fields (UI observation captures only the static fields).

#### Output fields
| Field | Type | Description |
|---|---|---|
| Errors | array | — |
| Reason | text | — |
| Location | text | — |
| Debug info | text | — |
| Message | text | — |
| List size | integer | — |
| List index | integer | — |

### insert_rows_stream (Insert rows)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_missing, dynamic schema unresolved (project not selected)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Dataset |  | Yes | Yes | The dataset which contains the table to load the data to. |
| Table |  | Yes | Yes | The table of the dataset to load the data to. |
| Ignore schema mismatch | text | - | No | — |
| Skip invalid rows | text | - | No | — |

> ⚠ Dynamic input: after Project/Dataset/Table are selected, the target table's columns expand as the schema inside the input array.

#### Output fields
(Unlearned: dynamic schema. As a batch action, an `Errors[]`-based output similar to insert_row is expected.)

### load_data_from_file (Load data into BigQuery)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_missing (file loads are fire-and-forget-ish actions and the output can be empty).

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Dataset |  | Yes | Yes | The dataset which contains the table to load the data to. |
| Table |  | Yes | Yes | The table of the dataset to load the data to. |
| File contents | text | Yes | Yes | The file contents to upload to BigQuery. |
| File size | text | Yes | Yes | Input file size in bytes. |
| Source format | text | - | Yes | The format of the data files. The default value is CSV. |
| Autodetect | text | - | Yes | Only applied to CSV and JSON files. Allows BigQuery to automatically infer the schema and options of the data being loaded into the table. |
| Alter table columns when required? | text | - | Yes | ALLOW_FIELD_ADDITION: allow adding a nullable field to the schema, ALLOW_FIELD_RELAXATION: allow relaxing a required field in the original schema to nullable. |
| Create disposition | text | - | Yes | CREATE_IF_NEEDED / CREATE_NEVER. Default CREATE_IF_NEEDED. |
| Write disposition | text | - | No | — |
| Schema | object | - | No | — |
| Fields | array | - | No | — |
| Column name | text | - | No | — |
| Column type | text | - | No | — |
| Mode | text | - | No | — |
| Destination table properties | object | - | No | — |
| Friendly name | text | - | No | — |
| Description | text | - | No | — |

#### Output fields
(Unlearned: load-job actions likely do not have an output schema.)

### load_data_from_google_table (Load data from Google Cloud Storage into BigQuery)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_missing (load-job action; output schema may be empty).

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Dataset |  | Yes | Yes | The dataset which contains the table to load the data to. |
| Table |  | Yes | Yes | The table of the dataset to load the data to. |
| Source URI | text | Yes | Yes | Fully qualified URIs that point to your data in Google Cloud. |
| Source format | text | - | Yes | The format of the data files. The default value is CSV. |
| Autodetect | text | - | Yes | Only applied to CSV and JSON files. Allows BigQuery to automatically infer the schema and options of the data being loaded into the table. |
| Alter table columns when required? | text | - | Yes | ALLOW_FIELD_ADDITION / ALLOW_FIELD_RELAXATION. |
| Create disposition | text | - | Yes | CREATE_IF_NEEDED / CREATE_NEVER. Default CREATE_IF_NEEDED. |
| Write disposition | text | - | No | — |
| Schema | object | - | No | — |
| Fields | array | - | No | — |
| Column name | text | - | No | — |
| Column type | text | - | No | — |
| Mode | text | - | No | — |
| Destination table properties | object | - | No | — |
| Friendly name | text | - | No | — |
| Description | text | - | No | — |

#### Output fields
(Unlearned: load-job action; output schema may be empty.)

### run_custom_sql_sync (Run custom SQL in BigQuery)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_missing

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project ID of the project that contains the destination table. |
| Query | string (code editor) | Yes | Yes | Provide a valid SQL string to be executed. Toggle the 'use legacy SQL' field if you want to use legacy SQL in the input above. |
| Use legacy SQL | text | - | Yes | Toggle to true to use legacy SQL instead of Standard SQL. |
| Location | text | - | No | — |

#### Output fields
(Unlearned: the output structure of the synchronous SQL run did not surface a group during UI observation. Capture it at runtime.)

### search_rows_sync (Select rows)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_missing, dynamic schema unresolved (project not selected)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Dataset |  | Yes | Yes | The dataset which contains the table to load the data to. |
| Table |  | Yes | Yes | The table of the dataset to load the data to. |
| WHERE Predicates | array | - | Yes | Build your where conditions with predicates. All options are assumed to be joined with the AND condition. Use select rows with custom SQL for more complex queries. |
| Wait for query to complete? |  | Yes | Yes | Set to true to wait for queries to run. This turns the action into asynchronous. |
| Location | text | - | No | — |
| Output columns | text | - | No | — |
| Value | text | - | Yes | — |
| Order by | text | - | No | — |
| Limit | integer | - | No | — |
| Offset | integer | - | No | — |

#### Output fields
(Unlearned: dynamic schema. When Project/Dataset/Table are selected, the table's columns expand under Rows[].)

### search_rows (Select rows (Old))

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_missing, dynamic schema unresolved (project not selected). Legacy version (prefer `search_rows_sync` for new implementations).

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Dataset |  | Yes | Yes | The dataset which contains the table to load the data to. |
| Table |  | Yes | Yes | The table of the dataset to load the data to. |
| Location | text | - | No | — |
| Output columns | text | - | No | — |
| Where | text | - | No | — |
| Order by | text | - | No | — |
| Limit | integer | - | No | — |
| Offset | text | - | No | — |

#### Output fields
(Unlearned: dynamic schema.)

### search_rows_using_custom_sql_sync (Select rows using custom SQL)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project which contains the table. |
| Query | string (code editor) | Yes | Yes | Provide a valid SQL string to be executed. Use bind variables, e.g. id = @id, and the parameter field below to parameters inputs. |
| Parameters |  | - | Yes | First provide the full name assigned to your bind variable in the WHERE condition. e.g. id. Second, provide the actual parameter value. Parameter values can be static or datapills. Select the closest corresponding data type that your database is expecting for the bind variable. |
| Output fields |  | Yes | Yes | Use this to manually define the columns returned in your query. |
| Data | object | - | No | — |
| Location | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Output contains rows? | boolean | — |
| Rows | array | — |
| List size | integer | — |
| List index | integer | — |
| Kind | text | — |
| Job reference | object | — |
| Project ID | text | — |
| Job ID | text | — |
| Location | text | — |
| Total rows | text | — |
| Page token | text | — |
| Schema | object | — |
| Fields | array | — |
| Etag | text | — |
| Total bytes processed | text | — |
| Job complete | boolean | — |
| Cache hit | boolean | — |

> ⚠ Each column under `Rows[]` expands dynamically based on the contents defined in `Output fields` (UI observation captures only the static fields).

### search_rows_using_custom_sql (Select rows using custom SQL (Old))

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_missing, dynamic schema unresolved (project not selected). Legacy version (prefer `search_rows_using_custom_sql_sync` for new implementations).

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Query | string (code editor) | Yes | Yes | Provide a valid SQL string to be executed. Toggle the 'use legacy SQL' field if you want to use legacy SQL in the input above. |
| Automatic schema introspection | text | - | Yes | Toggle to true for automatic schema introspection. Defaults to false. |
| Destination table |  | - | Yes | — |
| Create disposition | text | - | Yes | CREATE_IF_NEEDED / CREATE_NEVER. Default CREATE_IF_NEEDED. |
| Use legacy SQL | text | - | Yes | Set to true to use legacy SQL instead of Standard SQL. |
| Location | text | - | No | — |
| Write disposition | text | - | No | — |
| Limit | integer | - | No | — |
| Offset | text | - | No | — |

#### Output fields
(Unlearned: dynamic schema.)

### search_rows_using_custom_sql_sync_insert_table (Select rows using custom SQL and insert into table)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project which contains the table. |
| Query | string (code editor) | Yes | Yes | Provide a valid SQL string to be executed. Use bind variables, e.g. id = @id, and the parameter field below to parameters inputs. |
| Parameters |  | - | Yes | First provide the full name assigned to your bind variable in the WHERE condition. e.g. id. Second, provide the actual parameter value. Parameter values can be static or datapills. |
| Output fields |  | Yes | Yes | Use this to manually define the columns returned in your query. |
| Data | object | - | No | — |
| Location | text | - | No | — |
| Create disposition | text | - | Yes | — |
| Write disposition | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Rows | array | — |
| List size | integer | — |
| List index | integer | — |
| Kind | text | — |
| Job reference | object | — |
| Project ID | text | — |
| Job ID | text | — |
| Location | text | — |
| Total rows | text | — |
| Page token | text | — |
| Schema | object | — |
| Fields | array | — |
| Etag | text | — |
| Total bytes processed | text | — |
| Job complete | boolean | — |
| Cache hit | boolean | — |

> ⚠ The column structure under `Rows[]` expands dynamically based on the contents defined in `Output fields`.


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
