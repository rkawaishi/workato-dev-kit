# Google Drive コネクタ

Provider: `google_drive`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New activity | `new_activity` | - |  |
| New CSV file | `new_csv_file_batch` | Yes |  |
| New file or folder in folder hierarchy | `new_file_in_subfolder` | - |  |
| New file or folder | `new_file_or_folder` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add permission to a file | `add_permission` | - |  |
| Copy file | `copy_file` | - |  |
| Create folder | `create_folder` | - |  |
| Delete file | `delete_file` | - |  |
| Download file | `download_file_contents` | - |  |
| Export file | `export_file` | - |  |
| Get permission of a file | `get_permission` | - |  |
| List permissions of a file | `list_permission` | Yes |  |
| Rename or move file/folder | `move_rename_file` | - |  |
| Remove permissions from a file | `remove_permission` | - |  |
| Search files or folders | `search_file_or_folder` | Yes |  |
| Update permission of a file | `update_permission` | - |  |
| Upload small file | `upload_file` | - |  [deprecated] |
| Upload file | `upload_file_stream` | - |  |

## フィールド詳細

### new_activity (New activity)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Parent folder |  | Yes | Yes | The parent folder which needs to be monitored for activities. Note that the subfolders are monitored too. Either the drive or drive.readonly scope is necessary to populate the picklist. |
| Start time | date-time | - | Yes | When you start recipe for the first time, it picks up activity from this specified date and time. Defaults to fetching activity an hour ago if left blank. |
| Activity to monitor |  | Yes | Yes | Choose one or more activities to monitor from. |
| Trigger poll interval | integer | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| ID | text | — |
| Title | text | — |
| Mime type | text | — |
| Owner | object | — |
| Team drive | object | — |
| Domain | object | — |
| Drive | object | — |
| Actions | array | — |
| Detail | object | — |
| List size | integer | — |
| List index | integer | — |
| Actors | array | — |
| User | object | — |
| Primary action detail | object | — |
| Rename | object | — |
| Move | object | — |
| Permission change | object | — |
| Comment | object | — |
| Reference | object | — |
| Settings change | object | — |
| Edit | number | — |
| Dlp change | object | — |
| Create | object | — |
| Delete | object | — |
| Restore | object | — |
| Drive file | object | — |
| Type | text | — |
| Timestamp | date-time | — |

> ⚠ `List size` / `List index` は `Actions` と `Actors` の各配列配下に重複登場する。データツリーの paddingLeft が一律 0 のためフラットに見える点に注意。

### new_csv_file_batch (New CSV file)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| When first started, this recipe should pick up events from | date-time | - | Yes | When you start recipe for the first time, it picks up files created from specified time. Defaults to fetching files created an hour ago if left blank. Once recipe has been run or tested, value cannot be changed. |
| Parent folder |  | Yes | Yes | Select the parent folder. The uploaded file will be saved under My Drive if not specified. |
| Sample CSV file | text | - | Yes | Required: Select a CSV file for Workato to understand the data columns in your files. Otherwise, toggle to provide column names manually. |
| Column delimiter |  | Yes | Yes | The character used to separate column values within each CSV line. |
| Contains header line? | text | - | Yes | Set to Yes if the first CSV line is a header line, containing column names. |
| Batch size | number | - | Yes | Number of CSV rows per batch. Workato reads a batch of CSV rows at a time to increase throughput. |
| Expected encoding | text | - | Yes | Default encoding type is set to UTF-8, and typically doesn't need to be changed. |
| Trigger poll interval | integer | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Event | object | — |
| ID | text | — |
| Name | text | — |
| MIME type | text | — |
| Description | text | — |
| Starred | boolean | — |
| Trashed | boolean | — |
| Explicitly trashed | boolean | — |
| Parents | array | — |
| Version | integer | — |
| Web content link | text | — |
| Web view link | text | — |
| Icon link | text | — |
| Thumbnail link | text | — |
| Viewed by me | boolean | — |
| Viewed by me time | date-time | — |
| Created time | date-time | — |
| Modified time | date-time | — |
| Modified by me time | date-time | — |
| Sharing user | object | — |
| Owners | array | — |
| Last modifying user | object | — |
| Shared | boolean | — |
| Owned by me | boolean | — |
| Viewers can copy content | boolean | — |
| Writers can share | boolean | — |
| Original filename | text | — |
| Full file extension | text | — |
| File extension | text | — |
| Md 5 checksum | text | — |
| Size | number | — |
| Quota bytes used | number | — |
| Head revision ID | text | — |
| Error message | text | — |

### new_file_in_subfolder (New file or folder in folder hierarchy)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Folder |  | Yes | Yes | Select the folder to monitor for new files or folders. All subfolders will be monitored as well. |
| Trigger poll interval | integer | - | No | — |
| Chunk size (KB) | integer | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Is folder | boolean | — |
| Is google file | boolean | — |
| Is other file | boolean | — |
| File contents | text | — |
| ID | text | — |
| Name | text | — |
| MIME type | text | — |
| Description | text | — |
| Starred | boolean | — |
| Trashed | boolean | — |
| Explicitly trashed | boolean | — |
| Parents | array | Parents 配列の子要素は ID (text) |
| Version | integer | — |
| Web content link | text | — |
| Web view link | text | — |
| Icon link | text | — |
| Thumbnail link | text | — |
| Viewed by me | boolean | — |
| Viewed by me time | date-time | — |
| Created time | date-time | — |
| Modified time | date-time | — |
| Modified by me time | date-time | — |
| Sharing user | object | Display name / Email address / Permission ID / Photo link / Me を含む |
| Owners | array | 各要素は Display name / Email address / Permission ID / Photo link / Me / List size / List index |
| Last modifying user | object | Display name / Email address / Permission ID / Photo link / Me を含む |
| Shared | boolean | — |
| Owned by me | boolean | — |
| Viewers can copy content | boolean | — |
| Writers can share | boolean | — |
| Original filename | text | — |
| Full file extension | text | — |
| File extension | text | — |
| Md 5 checksum | text | — |
| Size | number | — |
| Quota bytes used | number | — |
| Head revision ID | text | — |

> ⚠ データツリー観察ではネスト構造がフラットに表示されるため、Sharing user / Owners / Last modifying user の子要素 (Display name, Email address, Permission ID, Photo link, Me) が同じ階層に重複出現する。実際のスキーマ上は object/array の配下に位置する。

### new_file_or_folder (New file or folder)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Folder |  | Yes | Yes | Select the folder to monitor for new files or folders. Sub-folders will not be monitored. |
| When first started, this recipe should pick up events from | date-time | - | Yes | When you start recipe for the first time, it picks up new files or folders created from this specified date and time. Defaults to fetching files or folders created an hour ago if left blank. Once recipe has been run or tested, value cannot be changed. |
| Chunk size (KB) | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Is folder | number | — |
| Is google file | number | — |
| Is other file | number | — |
| File contents | text | — |
| ID | text | — |
| Name | text | — |
| Mime type | text | — |
| Description | text | — |
| Starred | number | — |
| Trashed | number | — |
| Explicitly trashed | number | — |
| Parents | array | 各要素は ID (text) |
| Version | integer | — |
| Web content link | text | — |
| Web view link | text | — |
| Icon link | text | — |
| Thumbnail link | text | — |
| Viewed by me | number | — |
| Viewed by me time | date-time | — |
| Created time | date-time | — |
| Modified time | date-time | — |
| Modified by me time | date-time | — |
| Sharing user | object | Display name / Email address / Permission ID / Photo link / Me を含む |
| Owners | array | 各要素は Display name / Email address / Permission ID / Photo link / Me |
| Last modifying user | object | Display name / Email address / Permission ID / Photo link / Me を含む |
| Shared | number | — |
| Owned by me | number | — |
| Viewers can copy content | number | — |
| Writers can share | number | — |
| Original filename | text | — |
| Full file extension | text | — |
| File extension | text | — |
| Md 5 checksum | text | — |
| Size | integer | — |
| Quota bytes used | integer | — |
| Head revision ID | text | — |

### add_permission (Add permission to a file)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of a file's shareable link. |
| Role |  | Yes | Yes | The role granted by this permission. |
| Share with |  | Yes | Yes | When creating a permission, if this is set to a user or group, you must provide the email address. When set to domain, you must provide a domain. |
| Email address | text | - | No | — |
| Domain | text | - | No | — |
| Allow file discovery? | text | - | No | — |
| Send notifications | text | - | No | — |
| Notification message | text | - | No | — |
| Transfer ownership | text | - | No | — |
| Move file to root of the user | text | - | No | — |
| Use domain admin access? | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Kind | text | — |
| Type | text | — |
| Permission ID | text | — |
| Email address | text | — |
| Domain | text | — |
| Role | text | — |
| View | text | — |
| Allow file discovery | number | — |
| Display name | text | — |
| Photo link | text | — |
| Team drive permission details | array | 配列要素: Team drive permission type / Role / Inherited from / Inherited / List size / List index |
| Permission details | array | 配列要素: Permission type / Role / Inherited from / Inherited / List size / List index |
| Deleted | number | — |

### copy_file (Copy file)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of the shareable link. |
| File name | text | - | Yes | Define new file name for the copied file. |
| Destination folder | text | - | Yes | Select the folder to place the copied file in. By default the file will be copied within the same folder. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Kind | text | — |
| Name | text | — |
| File ID | text | — |
| Mime type | text | — |
| Parents | array | 各要素は ID (text) |

### create_folder (Create folder)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Parent folder |  | Yes | Yes | Select parent folder to create new folder in. |
| Name |  | Yes | Yes | Name of new folder. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| ID | text | — |
| Name | text | — |
| Mime type | text | — |

### delete_file (Delete file)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of the shareable link. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Success | text | — |

### download_file_contents (Download file)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of the shareable link. |
| Chunk size (KB) | text | - | No | — |
| Encoding of the file content | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| File contents | text | — |
| Size | integer | — |

### export_file (Export file)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of a file's shareable link. |
| MIME type |  | Yes | Yes | Eg: text/csv. Supported MIME types can be found in Google Drive API docs. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| File content | text | — |
| Size | text | — |

### get_permission (Get permission of a file)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of a file's shareable link. |
| Permission |  | Yes | Yes | Permission ID can be obtained from list permissions action. |
| Use domain admin access? | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Kind | text | — |
| Type | text | — |
| Permission ID | text | — |
| Email address | text | — |
| Domain | text | — |
| Role | text | — |
| View | text | — |
| Allow file discovery | number | — |
| Display name | text | — |
| Photo link | text | — |
| Team drive permission details | array | 配列要素: Team drive permission type / Role / Inherited from / Inherited / List size / List index |
| Permission details | array | 配列要素: Permission type / Role / Inherited from / Inherited / List size / List index |
| Deleted | number | — |

### list_permission (List permissions of a file)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of the shareable link. |
| Maximum results | integer | - | Yes | Enter a value for maximum results to be returned per page. Default maximum is 100. |
| Page token | integer | - | Yes | Token to specify the next page in a query. This can be found from the "nextPageToken" value in the output of an earlier 'List permissions' action. |
| Use domain admin access? | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Kind | text | — |
| Next page token | text | — |
| Permissions | array | 配列要素: Kind / Type / Permission ID / Email address / Domain / Role / View / Allow file discovery / Display name / Photo link / Team drive permission details / Permission details / Deleted / List size / List index |

### move_rename_file (Rename or move file/folder)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| File or folder ID |  | Yes | Yes | For folder ID, click on the required folder and folder ID can be found at the end of URL. For file ID, right click on the file and select Get shareable link. |
| Name | text | - | Yes | New name of the file or folder. |
| Parent folder | text | - | Yes | Select the parent folder. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Kind | text | — |
| Name | text | — |
| File ID | text | — |
| Mime type | text | — |
| Parents | array | 各要素は ID (text) |

### remove_permission (Remove permissions from a file)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of the shareable link. |
| Permission |  | Yes | Yes | Permission ID can be obtained using the List permissions action. In the select permission option, permissions are listed in the role - type - email address format. |
| Enforce expansive access | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Success | text | — |

### search_file_or_folder (Search files or folders)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Files or folders |  | Yes | Yes | Select whether to search for files or for folders. |
| Query | text | - | Yes | Query for filtering the search results. Use this field to specify an exact query based on which the files need to be fetched. |
| Next page token | text | - | Yes | The token for continuing a previous list request on the next page. |
| Page size | integer | - | Yes | The maximum number of files to return per page. Acceptable values are 1 to 100, inclusive. |
| Folder | text | - | No | — |
| Name | text | - | No | — |
| Modified after | date-time | - | No | — |
| Trashed files? | text | - | No | — |
| Starred files? | text | - | No | — |
| Owner email | text | - | No | — |
| Writer email | text | - | No | — |
| Reader email | text | - | No | — |
| Shared with me? | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Next page token | text | — |
| Incomplete search | number | — |
| Files | array | 配列要素: ID / Name / Mime type / Description / Starred / Trashed / Explicitly trashed / Parents / Version / Web content link / Web view link / Icon link / Thumbnail link / Viewed by me / Viewed by me time / Created time / Modified time / Modified by me time / Sharing user / Owners / Last modifying user / Shared / Owned by me / Viewers can copy content / Writers can share / Original filename / Full file extension / File extension / Md 5 checksum / Size / Quota bytes used / Head revision ID / List size / List index |

### update_permission (Update permission of a file)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of a file's shareable link. |
| Permission |  | Yes | Yes | Permission ID can be obtained using the List permissions action. |
| Role |  | Yes | Yes | The role granted by this permission. |
| Use domain admin access? | text | - | No | — |
| Transfer ownership | text | - | No | — |
| Remove expiration | text | - | No | — |
| Enforce expansive access | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Kind | text | — |
| Type | text | — |
| Permission ID | text | — |
| Email address | text | — |
| Domain | text | — |
| Role | text | — |
| View | text | — |
| Allow file discovery | number | — |
| Display name | text | — |
| Photo link | text | — |
| Team drive permission details | array | 配列要素: Team drive permission type / Role / Inherited from / Inherited / List size / List index |
| Permission details | array | 配列要素: Permission type / Role / Inherited from / Inherited / List size / List index |
| Deleted | number | — |

### upload_file_stream (Upload file)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-26

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| File contents |  | Yes | Yes | Contents of the file to upload. |
| File name | text | - | Yes | Name of the uploaded file. If not specified, the uploaded file will be named as Untitled. |
| Parent folder | text | - | Yes | Select the parent folder. The uploaded file will be saved under My Drive if not specified. |
| Properties |  | Yes | Yes | A collection of arbitrary key-value pairs which are visible to all. |
| Upload file MIME type | text | - | No | — |
| Target MIME type | text | - | No | — |
| Description | text | - | No | — |
| Starred | text | - | No | — |
| Viewers can copy content | text | - | No | — |
| Writers can share | text | - | No | — |
| Chunk size (KB) | text | - | No | — |
| Copy requires writer permission | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Kind | text | — |
| ID | text | — |
| Name | text | — |
| Mime type | text | — |
| Parents | array | 各要素は ID (text) |
| Description | text | — |
| Starred | boolean | — |
| Viewers can copy content | boolean | — |
| Writers can share | boolean | — |
| Properties | array | 各要素は Key (text) / Value (text) |
| Web view link | text | — |

### upload_file (Action)

レシピ: Upload Gmail attachments to Google Drive

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| fileContent | string | Yes | アップロードするファイルのコンテンツ（バイナリ） |
| name | string | Yes | アップロード先のファイル名 |

## 備考
- OAuth 2.0 またはサービスアカウント認証
- Google Drive API v3 使用
- provider 名: `google_drive`

---

## 学習サマリ

最終実行: 2026-04-27 by /auto-learn
- 試行: 17 op
- 完全成功: 17
- 部分学習: 0
- 学習失敗: 0
- スキップ:
  - Deprecated: 1 — `upload_file`（→ `upload_file_stream` 推奨）
  - adhoc: 1 — `__adhoc_http_action`
  - 既学習: 0

### 構造的注記（参考）

- 重複ラベル `List size` / `List index`: `Actions` と `Actors` の各配列配下に同名で出現（`new_activity` 等）。データツリー `paddingLeft: 0` でフラット表示
- Sharing user / Owners / Last modifying user の object/array 配下が `Display name` / `Email address` / `Permission ID` / `Photo link` / `Me` でフラット重複表示（`new_file_or_folder` 等）
- 型表示の揺れ: `new_csv_file_batch` は `Starred` / `Trashed` を `boolean` 表示、`new_file_or_folder` は同フィールドを `number` 表示。Workato UI 側の不整合
- 大文字小文字の揺れ: `MIME type` (`new_csv_file_batch`) vs `Mime type` (他)。UI そのまま捕捉

要 follow-up なし（全 op で input/output 取得済み）。構造的注記は `/learn-recipe` または手動補完の対象。
