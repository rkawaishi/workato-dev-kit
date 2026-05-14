# Google Drive connector

Provider: `google_drive`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New activity | `new_activity` | - |  |
| New CSV file | `new_csv_file_batch` | Yes |  |
| New file or folder in folder hierarchy | `new_file_in_subfolder` | - |  |
| New file or folder | `new_file_or_folder` | - |  |

## Actions

| Name | Internal name | Batch | Description |
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

## Field details

### new_activity (New activity)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Parent folder |  | Yes | Yes | The parent folder which needs to be monitored for activities. Note that the subfolders are monitored too. Either the drive or drive.readonly scope is necessary to populate the picklist. |
| Start time | date-time | - | Yes | When you start recipe for the first time, it picks up activity from this specified date and time. Defaults to fetching activity an hour ago if left blank. |
| Activity to monitor |  | Yes | Yes | Choose one or more activities to monitor from. |
| Trigger poll interval | integer | - | No | — |

#### Output fields
| Field | Type | Description |
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

> ⚠ `List size` / `List index` appear duplicated under both the `Actions` and `Actors` arrays. Note that they look flat because the data tree uses a uniform paddingLeft of 0.

### new_csv_file_batch (New CSV file)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
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
| Field | Type | Description |
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

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Folder |  | Yes | Yes | Select the folder to monitor for new files or folders. All subfolders will be monitored as well. |
| Trigger poll interval | integer | - | No | — |
| Chunk size (KB) | integer | - | No | — |

#### Output fields
| Field | Type | Description |
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
| Parents | array | Child element of the Parents array is ID (text) |
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
| Sharing user | object | Includes Display name / Email address / Permission ID / Photo link / Me |
| Owners | array | Each element has Display name / Email address / Permission ID / Photo link / Me / List size / List index |
| Last modifying user | object | Includes Display name / Email address / Permission ID / Photo link / Me |
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

> ⚠ Because the data tree observation renders the nested structure as flat, the child elements of Sharing user / Owners / Last modifying user (Display name, Email address, Permission ID, Photo link, Me) appear duplicated at the same hierarchy level. In the actual schema they live under the object/array.

### new_file_or_folder (New file or folder)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Folder |  | Yes | Yes | Select the folder to monitor for new files or folders. Sub-folders will not be monitored. |
| When first started, this recipe should pick up events from | date-time | - | Yes | When you start recipe for the first time, it picks up new files or folders created from this specified date and time. Defaults to fetching files or folders created an hour ago if left blank. Once recipe has been run or tested, value cannot be changed. |
| Chunk size (KB) | text | - | No | — |

#### Output fields
| Field | Type | Description |
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
| Parents | array | Each element is ID (text) |
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
| Sharing user | object | Includes Display name / Email address / Permission ID / Photo link / Me |
| Owners | array | Each element has Display name / Email address / Permission ID / Photo link / Me |
| Last modifying user | object | Includes Display name / Email address / Permission ID / Photo link / Me |
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

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
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
| Field | Type | Description |
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
| Team drive permission details | array | Array element: Team drive permission type / Role / Inherited from / Inherited / List size / List index |
| Permission details | array | Array element: Permission type / Role / Inherited from / Inherited / List size / List index |
| Deleted | number | — |

### copy_file (Copy file)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of the shareable link. |
| File name | text | - | Yes | Define new file name for the copied file. |
| Destination folder | text | - | Yes | Select the folder to place the copied file in. By default the file will be copied within the same folder. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Kind | text | — |
| Name | text | — |
| File ID | text | — |
| Mime type | text | — |
| Parents | array | Each element is ID (text) |

### create_folder (Create folder)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Parent folder |  | Yes | Yes | Select parent folder to create new folder in. |
| Name |  | Yes | Yes | Name of new folder. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| ID | text | — |
| Name | text | — |
| Mime type | text | — |

### delete_file (Delete file)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of the shareable link. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Success | text | — |

### download_file_contents (Download file)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of the shareable link. |
| Chunk size (KB) | text | - | No | — |
| Encoding of the file content | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| File contents | text | — |
| Size | integer | — |

### export_file (Export file)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of a file's shareable link. |
| MIME type |  | Yes | Yes | Eg: text/csv. Supported MIME types can be found in Google Drive API docs. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| File content | text | — |
| Size | text | — |

### get_permission (Get permission of a file)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of a file's shareable link. |
| Permission |  | Yes | Yes | Permission ID can be obtained from list permissions action. |
| Use domain admin access? | text | - | No | — |

#### Output fields
| Field | Type | Description |
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
| Team drive permission details | array | Array element: Team drive permission type / Role / Inherited from / Inherited / List size / List index |
| Permission details | array | Array element: Permission type / Role / Inherited from / Inherited / List size / List index |
| Deleted | number | — |

### list_permission (List permissions of a file)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of the shareable link. |
| Maximum results | integer | - | Yes | Enter a value for maximum results to be returned per page. Default maximum is 100. |
| Page token | integer | - | Yes | Token to specify the next page in a query. This can be found from the "nextPageToken" value in the output of an earlier 'List permissions' action. |
| Use domain admin access? | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Kind | text | — |
| Next page token | text | — |
| Permissions | array | Array element: Kind / Type / Permission ID / Email address / Domain / Role / View / Allow file discovery / Display name / Photo link / Team drive permission details / Permission details / Deleted / List size / List index |

### move_rename_file (Rename or move file/folder)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| File or folder ID |  | Yes | Yes | For folder ID, click on the required folder and folder ID can be found at the end of URL. For file ID, right click on the file and select Get shareable link. |
| Name | text | - | Yes | New name of the file or folder. |
| Parent folder | text | - | Yes | Select the parent folder. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Kind | text | — |
| Name | text | — |
| File ID | text | — |
| Mime type | text | — |
| Parents | array | Each element is ID (text) |

### remove_permission (Remove permissions from a file)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of the shareable link. |
| Permission |  | Yes | Yes | Permission ID can be obtained using the List permissions action. In the select permission option, permissions are listed in the role - type - email address format. |
| Enforce expansive access | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Success | text | — |

### search_file_or_folder (Search files or folders)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
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
| Field | Type | Description |
|---|---|---|
| Next page token | text | — |
| Incomplete search | number | — |
| Files | array | Array element: ID / Name / Mime type / Description / Starred / Trashed / Explicitly trashed / Parents / Version / Web content link / Web view link / Icon link / Thumbnail link / Viewed by me / Viewed by me time / Created time / Modified time / Modified by me time / Sharing user / Owners / Last modifying user / Shared / Owned by me / Viewers can copy content / Writers can share / Original filename / Full file extension / File extension / Md 5 checksum / Size / Quota bytes used / Head revision ID / List size / List index |

### update_permission (Update permission of a file)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| File |  | Yes | Yes | File ID can be found in the output of other triggers/actions of Google Drive connector, or at the end of a file's shareable link. |
| Permission |  | Yes | Yes | Permission ID can be obtained using the List permissions action. |
| Role |  | Yes | Yes | The role granted by this permission. |
| Use domain admin access? | text | - | No | — |
| Transfer ownership | text | - | No | — |
| Remove expiration | text | - | No | — |
| Enforce expansive access | text | - | No | — |

#### Output fields
| Field | Type | Description |
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
| Team drive permission details | array | Array element: Team drive permission type / Role / Inherited from / Inherited / List size / List index |
| Permission details | array | Array element: Permission type / Role / Inherited from / Inherited / List size / List index |
| Deleted | number | — |

### upload_file_stream (Upload file)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
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
| Field | Type | Description |
|---|---|---|
| Kind | text | — |
| ID | text | — |
| Name | text | — |
| Mime type | text | — |
| Parents | array | Each element is ID (text) |
| Description | text | — |
| Starred | boolean | — |
| Viewers can copy content | boolean | — |
| Writers can share | boolean | — |
| Properties | array | Each element has Key (text) / Value (text) |
| Web view link | text | — |

### upload_file (Action)

Recipe: Upload Gmail attachments to Google Drive

#### Input fields
| Field | Type | Required | Description |
|---|---|---|---|
| fileContent | string | Yes | Contents of the file to upload (binary) |
| name | string | Yes | File name at the upload destination |

## Notes
- OAuth 2.0 or service account authentication
- Uses Google Drive API v3
- provider name: `google_drive`

---

## Learning summary

Last run: 2026-04-27 by `/auto-learn`
- Attempted: 17 op
- Fully learned: 17
- Partially learned: 0
- Failed: 0
- Skipped:
  - Deprecated: 1 — `upload_file` (use `upload_file_stream` instead)
  - adhoc: 1 — `__adhoc_http_action`
  - Already learned: 0

### Structural notes (for reference)

- Duplicate label `List size` / `List index`: appears under both the `Actions` and `Actors` arrays with the same name (e.g. `new_activity`). The data tree renders flat with `paddingLeft: 0`.
- The object/array contents under Sharing user / Owners / Last modifying user appear as a flat duplicate display of `Display name` / `Email address` / `Permission ID` / `Photo link` / `Me` (e.g. `new_file_or_folder`).
- Type display inconsistency: `new_csv_file_batch` shows `Starred` / `Trashed` as `boolean`, while `new_file_or_folder` shows the same fields as `number`. This is an inconsistency on the Workato UI side.
- Case inconsistency: `MIME type` (`new_csv_file_batch`) vs `Mime type` (others). Captured as the UI presents it.

No follow-up needed (input/output captured for every op). Structural notes are to be supplemented via `/learn-recipe` or manually.
