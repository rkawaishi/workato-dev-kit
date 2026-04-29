# Google BigQuery コネクタ

Provider: `google_big_query`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New job completed | `new_job_completed` | - |  |
| New row | `new_row` | - |  |
| New rows | `new_rows_batch` | Yes |  |
| Scheduled query | `scheduled_query` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Get batch of rows by Job ID | `get_query_job_output` | Yes |  |
| Insert row | `insert_row` | - |  |
| Insert rows | `insert_rows` | Yes |  [deprecated] |
| Insert rows | `insert_rows_stream` | Yes |  |
| Load data into BigQuery | `load_data_from_file` | - |  |
| Load data from Google Cloud Storage into BigQuery | `load_data_from_google_table` | - |  |
| Run custom SQL in BigQuery | `run_custom_sql` | - |  [deprecated] |
| Run custom SQL in BigQuery | `run_custom_sql_sync` | - |  |
| Select rows (Old) | `search_rows` | Yes |  |
| Select rows | `search_rows_sync` | Yes |  |
| Select rows using custom SQL (Old) | `search_rows_using_custom_sql` | Yes |  |
| Select rows using custom SQL | `search_rows_using_custom_sql_sync` | Yes |  |
| Select rows using custom SQL and insert into table | `search_rows_using_custom_sql_sync_insert_table` | Yes |  |

## フィールド詳細

### new_job_completed (New job completed)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| When first started, this recipe should pick up events from | date-time | - | Yes | When you start recipe for the first time, it picks up trigger events from this specified date and time. Defaults to fetching records created an hour ago if left blank. Once recipe has been run or tested, value cannot be changed. |
| Trigger poll interval | integer | - | No | — |
| Dataset | text | - | No | — |
| Table | text | - | No | — |
| All users | text | - | No | — |
| Job type | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
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

> ⚠ `Load` / `Extract` / `Query` / `State` は Statistics と Configuration の各 object 配下に重複登場する。データツリーの paddingLeft が一律 0 のためフラットに見える点に注意。

### new_row (New row)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_missing, dynamic schema unresolved (project not selected)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
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
（未学習: 動的スキーマのため Project/Dataset/Table を選択しないと output が表示されない）

### new_rows_batch (New rows)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_missing, dynamic schema unresolved (project not selected)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
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
（未学習: 動的スキーマのため Project/Dataset/Table を選択しないと output が表示されない）

### scheduled_query (Scheduled query)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_missing, dynamic schema unresolved (project not selected)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
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
（未学習: 動的スキーマのため Query の結果カラムが output になる。`Automatic schema introspection=Yes` か `Output fields` 手動定義時のみ確定）

### get_query_job_output (Get batch of rows by Job ID)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_missing, dynamic schema unresolved (project not selected)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Job ID | text | Yes | Yes | ID of the job. This can be found from the 'Job completed in BigQuery Trigger'. |
| Page token | text | - | Yes | Page token, returned by a previous call, to request the next page of results. |
| Output fields |  | Yes | Yes | Use this to manually define the columns returned in your query. Only needed when queries take too long. |
| Page size | integer | - | No | — |
| Start index | integer | - | No | — |
| Location | text | - | No | — |

#### Output fields
（未学習: 動的スキーマ。`Output fields` の手動定義に依存して結果カラムが生成される）

### insert_row (Insert row)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Dataset |  | Yes | Yes | The dataset which contains the table to load the data to. |
| Table |  | Yes | Yes | The table of the dataset to load the data to. |
| Ignore schema mismatch | text | - | No | — |
| Skip invalid rows | text | - | No | — |

> ⚠ 動的入力: Project/Dataset/Table 選択後に対象テーブルのカラムが入力フィールドとして展開される（UI 観察時は static のみキャプチャ）

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Errors | array | — |
| Reason | text | — |
| Location | text | — |
| Debug info | text | — |
| Message | text | — |
| List size | integer | — |
| List index | integer | — |

### insert_rows_stream (Insert rows)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_missing, dynamic schema unresolved (project not selected)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project to be billed for the query. |
| Dataset |  | Yes | Yes | The dataset which contains the table to load the data to. |
| Table |  | Yes | Yes | The table of the dataset to load the data to. |
| Ignore schema mismatch | text | - | No | — |
| Skip invalid rows | text | - | No | — |

> ⚠ 動的入力: Project/Dataset/Table 選択後に対象テーブルのカラムが入力配列内 schema として展開される

#### Output fields
（未学習: 動的スキーマ。Batch アクションのため、insert_row と同様 `Errors[]` ベースの output が想定される）

### load_data_from_file (Load data into BigQuery)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_missing（ファイルロードは fire-and-forget 寄りのアクションで output が空になる場合あり）

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
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
（未学習: ロードジョブ系アクションは output schema を持たない可能性が高い）

### load_data_from_google_table (Load data from Google Cloud Storage into BigQuery)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_missing（ロードジョブ系のため output schema が空の可能性）

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
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
（未学習: ロードジョブ系のため output schema が空の可能性）

### run_custom_sql_sync (Run custom SQL in BigQuery)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_missing

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project ID of the project that contains the destination table. |
| Query | string (code editor) | Yes | Yes | Provide a valid SQL string to be executed. Toggle the 'use legacy SQL' field if you want to use legacy SQL in the input above. |
| Use legacy SQL | text | - | Yes | Toggle to true to use legacy SQL instead of Standard SQL. |
| Location | text | - | No | — |

#### Output fields
（未学習: 同期実行 SQL の output 構造は UI 観察時に group が出現せず。実行時に取得すべき）

### search_rows_sync (Select rows)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_missing, dynamic schema unresolved (project not selected)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
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
（未学習: 動的スキーマ。Project/Dataset/Table 選択時に Rows[] 配下にテーブルのカラムが展開される）

### search_rows (Select rows (Old))

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_missing, dynamic schema unresolved (project not selected)。Legacy バージョン（新規実装は `search_rows_sync` を推奨）

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
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
（未学習: 動的スキーマ）

### search_rows_using_custom_sql_sync (Select rows using custom SQL)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Project |  | Yes | Yes | The project which contains the table. |
| Query | string (code editor) | Yes | Yes | Provide a valid SQL string to be executed. Use bind variables, e.g. id = @id, and the parameter field below to parameters inputs. |
| Parameters |  | - | Yes | First provide the full name assigned to your bind variable in the WHERE condition. e.g. id. Second, provide the actual parameter value. Parameter values can be static or datapills. Select the closest corresponding data type that your database is expecting for the bind variable. |
| Output fields |  | Yes | Yes | Use this to manually define the columns returned in your query. |
| Data | object | - | No | — |
| Location | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
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

> ⚠ `Rows[]` 配下の各カラムは `Output fields` で定義した内容に応じて動的展開される（UI 観察時は static のみ）

### search_rows_using_custom_sql (Select rows using custom SQL (Old))

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_missing, dynamic schema unresolved (project not selected)。Legacy バージョン（新規実装は `search_rows_using_custom_sql_sync` を推奨）

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
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
（未学習: 動的スキーマ）

### search_rows_using_custom_sql_sync_insert_table (Select rows using custom SQL and insert into table)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
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
| フィールド | 型 | 説明 |
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

> ⚠ `Rows[]` 配下のカラム構造は `Output fields` で定義した内容に応じて動的展開される

## 備考

- BigQuery のオペレーションは多くが「Project → Dataset → Table」picklist の選択で動的に input/output schema が生成される。`/auto-learn` の自動収集では project picklist を選ばないため、テーブル列に対応する動的フィールドは未取得（`> ⚠ 動的入力` 注記）。詳細列スキーマは `/learn-recipe` で個別レシピから補完する。
- 共通入力フィールド: `Project`、`Dataset`、`Table` は ほぼ全アクションで必須。`Location` は地域指定（オプション）。
- Legacy ops（`Select rows (Old)` / `Select rows using custom SQL (Old)`）は picker に表示されるが、新規実装では同期版（`search_rows_sync` / `search_rows_using_custom_sql_sync`）を推奨。
- Skip 済み: `__adhoc_http_action`（カスタム HTTP）、`insert_rows`（deprecated → `insert_rows_stream`）、`run_custom_sql`（deprecated → `run_custom_sql_sync`）。

## 学習失敗ログ

（なし — 全 op が `status=ok` で完了。一部は dynamic schema 由来の partial learning）

---

## 学習サマリ

最終実行: 2026-04-27 by /auto-learn
- 試行: 15 op
- 完全成功: 4
- 部分学習: 11
- 学習失敗: 0
- スキップ:
  - Deprecated: 2 — `insert_rows`（→ `insert_rows_stream`）, `run_custom_sql`（→ `run_custom_sql_sync`）
  - adhoc: 1 — `__adhoc_http_action`
  - 既学習: 0

### 要 follow-up

- **Dynamic schema (要 /learn-recipe)** — Project/Dataset/Table picklist 未選択により output schema が UI 観察では取れない
  - `new_row` / `new_rows_batch` / `scheduled_query` — 行系トリガー
  - `get_query_job_output` — Job ID から行を取得
  - `insert_row` / `insert_rows_stream` — Insert 系（output schema 動的）
  - `run_custom_sql_sync` — 同期 SQL 実行（output 出現せず要再調査）
  - `search_rows` / `search_rows_sync` — 検索 (Legacy + 現行)
  - `search_rows_using_custom_sql` / `search_rows_using_custom_sql_sync` — SQL 検索 (Legacy + 現行)
- **Fire-and-forget 寄り (要再確認)**
  - `load_data_from_file` / `load_data_from_google_table` — ファイル/GCS ロードジョブ

### 構造的注記（参考）

- `new_job_completed` の output で `Load` / `Extract` / `Query` / `State` が `Statistics` と `Configuration` の object 配下に重複登場（`paddingLeft: 0` 起因）
- `Insert rows` ピッカーは新 UI では `insert_rows_stream` のみ表示（`insert_rows` は picker から非表示）
- `Run custom SQL in BigQuery` ピッカーは `run_custom_sql_sync` のみ表示
