# Jira コネクタ

Provider: `jira`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Deleted object | `deleted_object` | - |  |
| Export new issues in Jira | `issue_created_bulk` | - |  |
| Export new/updated issues in Jira | `issue_created_or_updated_bulk` | - |  |
| New event | `new_event` | - |  |
| New issue | `new_issue` | - |  |
| New issue | `new_issue_batch` | Yes |  |
| Updated issue priority | `new_issue_priority` | - |  [deprecated] |
| New project | `new_project` | - |  [deprecated] |
| New/updated comment | `updated_comment_webhook` | - |  |
| Updated issue | `updated_issue` | - |  |
| Updated issue | `updated_issue_batch` | Yes |  |
| Updated issue status | `updated_issue_status` | - |  [deprecated] |
| New/updated issue | `updated_issue_webhook` | - |  |
| New/updated worklog | `updated_worklog_webhook` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Assign user to issue | `assign_issue` | - |  |
| Create comment | `create_comment` | - |  |
| Create issue | `create_issue` | - |  |
| Create user | `create_user` | - |  |
| Get user details | `find_user` | - |  |
| Download attachment | `get_attachment` | - |  |
| Get changelog of an issue | `get_changelog` | - |  |
| Get issue | `get_issue` | - |  |
| Get issue comments | `get_issue_comments` | Yes |  |
| Get issue schema | `get_object_schema` | - |  |
| Search assignable users | `search_assignable_users` | Yes |  |
| Search issues | `search_issues` | Yes |  |
| Search issues by JQL | `search_issues_by_JQL` | Yes |  |
| Update comment | `update_comment` | - |  |
| Update issue | `update_issue` | - |  |
| Update issue status | `update_issue_status` | - |  |
| Upload attachment | `upload_attachment` | - |  |

## フィールド詳細

### new_issue

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| id | string | ID |
| self | string | Self |
| key | string | Key |
| changelog.startAt | number | Start at |
| changelog.maxResults | number | Max results |
| changelog.total | number | Total |
| changelog.histories[].id | string | ID |
| changelog.histories[].author.self | string | Self (nested) |
| changelog.histories[].author.name | string | Name (nested) |
| changelog.histories[].author.key | string | Key (nested) |
| changelog.histories[].author.accountId | string | Account ID (nested) |
| changelog.histories[].author.emailAddress | string | Email address (nested) |
| changelog.histories[].author.displayName | string | Display name (nested) |
| changelog.histories[].author.active | boolean | Active (nested) |
| changelog.histories[].author.timeZone | string | Time zone (nested) |
| changelog.histories[].created | date_time | Created |
| changelog.histories[].items[].field | string | Field |
| changelog.histories[].items[].fieldtype | string | Field type |
| changelog.histories[].items[].fieldId | string | Field ID |
| changelog.histories[].items[].from | string | From |
| changelog.histories[].items[].fromString | string | From string |
| changelog.histories[].items[].to | string | To |
| changelog.histories[].items[].toString | string | To string |
| fields.statuscategorychangedate | date_time | ステータス カテゴリが変更されました |
| fields.issuetype.self | string | Self |
| fields.issuetype.id | string | ID |
| fields.issuetype.description | string | Description |
| fields.issuetype.iconUrl | string | Icon URL |
| fields.issuetype.name | string | Name |
| fields.issuetype.subtask | boolean | Sub task |
| fields.timespent | number | 消費時間 |
| fields.project.self | string | Self |
| fields.project.id | string | ID |
| fields.project.key | string | Key |
| fields.project.name | string | Name |
| fields.fixVersions[].self | string | Self |
| fields.fixVersions[].id | string | ID |
| fields.fixVersions[].description | string | Description |
| fields.fixVersions[].name | string | Name |
| fields.aggregatetimespent | number | Σ 消費時間 |
| fields.statusCategory | string | ステータス カテゴリ |
| fields.resolution.self | string | Self |
| fields.resolution.id | string | ID |
| fields.resolution.description | string | Description |
| fields.resolution.name | string | Name |
| fields.resolutiondate | date_time | 解決日 |
| fields.workratio | number | 作業比率 |
| fields.lastViewed | date_time | 最終閲覧日 |
| fields.watches.self | string | Self |
| fields.watches.watchCount | integer | Watch count |
| fields.watches.isWatching | boolean | Is watching |
| fields.issuerestriction | string | 制限対象 |
| fields.thumbnail | string | 画像 |
| fields.created | date_time | 作成日 |
| fields.priority.self | string | Self |
| fields.priority.iconUrl | string | Icon URL |
| fields.priority.name | string | Name |
| fields.priority.id | string | ID |
| fields.labels[] | string | ラベル |
| fields.timeestimate | number | 残余見積 |
| fields.aggregatetimeoriginalestimate | number | Σ 初期見積もり |
| fields.versions[].self | string | Self |
| fields.versions[].id | string | ID |
| fields.versions[].description | string | Description |
| fields.versions[].name | string | Name |
| fields.issuelinks[].self | string | Self |
| fields.issuelinks[].id | string | ID |
| fields.issuelinks[].type.id | string | ID (nested) |
| fields.issuelinks[].type.name | string | Name (nested) |
| fields.issuelinks[].type.inward | string | Inward (nested) |
| fields.issuelinks[].type.outward | string | Outward (nested) |
| fields.issuelinks[].inwardIssue.self | string | Self (nested) |
| fields.issuelinks[].inwardIssue.key | string | Key (nested) |
| fields.issuelinks[].inwardIssue.id | string | ID (nested) |
| fields.issuelinks[].outwardIssue.self | string | Self (nested) |
| fields.issuelinks[].outwardIssue.key | string | Key (nested) |
| fields.issuelinks[].outwardIssue.id | string | ID (nested) |
| fields.assignee.self | string | Self |
| fields.assignee.key | string | Key |
| fields.assignee.name | string | Name |
| fields.assignee.accountId | string | Account ID |
| fields.assignee.emailAddress | string | Email address |
| fields.assignee.displayName | string | Display name |
| fields.assignee.active | boolean | Active |
| fields.assignee.timeZone | string | Time zone |
| fields.updated | date_time | 更新日 |
| fields.status.self | string | Self |
| fields.status.description | string | Description |
| fields.status.iconUrl | string | Icon URL |
| fields.status.name | string | Name |
| fields.status.id | string | ID |
| fields.status.statusCategory.self | string | Self (nested) |
| fields.status.statusCategory.id | integer | ID (nested) |
| fields.status.statusCategory.key | string | Key (nested) |
| fields.status.statusCategory.colorName | string | Color name (nested) |
| fields.status.statusCategory.name | string | Name (nested) |
| fields.components[].self | string | Self |
| fields.components[].id | string | ID |
| fields.components[].name | string | Name |
| fields.issuekey | string | キー |
| fields.timeoriginalestimate | number | 初期見積もり |
| fields.description | string | 説明 |
| fields.timetracking | string | 時間管理 |
| fields.security | string | セキュリティ レベル |
| fields.attachment[].self | string | Self |
| fields.attachment[].filename | string | Filename |
| fields.attachment[].author.self | string | Self url (nested) |
| fields.attachment[].author.name | string | Name (nested) |
| fields.attachment[].author.accountId | string | Account ID (nested) |
| fields.attachment[].author.emailAddress | string | Email address (nested) |
| fields.attachment[].author.displayName | string | Display name (nested) |
| fields.attachment[].created | date_time | Created |
| fields.attachment[].size | string | Size |
| fields.attachment[].mimeType | string | Mime type |
| fields.attachment[].content | string | Content |
| fields.attachment[].thumbnail | string | Thumbnail |
| fields.aggregatetimeestimate | number | Σ 残余見積 |
| fields.summary | string | 要約 |
| fields.creator.self | string | Self |
| fields.creator.key | string | Key |
| fields.creator.name | string | Name |
| fields.creator.accountId | string | Account ID |
| fields.creator.emailAddress | string | Email address |
| fields.creator.displayName | string | Display name |
| fields.creator.active | boolean | Active |
| fields.creator.timeZone | string | Time zone |
| fields.subtasks[].self | string | Self |
| fields.subtasks[].key | string | Key |
| fields.subtasks[].id | string | ID |
| fields.reporter.self | string | Self |
| fields.reporter.key | string | Key |
| fields.reporter.name | string | Name |
| fields.reporter.accountId | string | Account ID |
| fields.reporter.emailAddress | string | Email address |
| fields.reporter.displayName | string | Display name |
| fields.reporter.active | boolean | Active |
| fields.reporter.timeZone | string | Time zone |
| fields.aggregateprogress.progress | integer | Progress |
| fields.aggregateprogress.total | integer | Total |
| fields.environment | string | 環境 |
| fields.duedate | date_time | 期限 |
| fields.progress.progress | integer | Progress |
| fields.progress.total | integer | Total |
| fields.votes.self | string | Self |
| fields.votes.votes | integer | Votes |
| fields.votes.hasVoted | boolean | Has voted |
| fields.comment | string | コメント |
| fields.worklog[].worklog | string | ログ作業 |
| fields.parent.id | string | ID |
| fields.parent.key | string | Key |
| fields.parent.self | string | Self |
| fields.parent.fields.summary | string | Summary (nested) |
| fields.parent.fields.status.self | string | Self (nested) |
| fields.parent.fields.status.description | string | Description (nested) |
| fields.parent.fields.status.iconUrl | string | Icon URL (nested) |
| fields.parent.fields.status.name | string | Name (nested) |
| fields.parent.fields.status.id | string | ID (nested) |
| fields.parent.fields.priority.self | string | Self (nested) |
| fields.parent.fields.priority.iconUrl | string | Icon URL (nested) |
| fields.parent.fields.priority.name | string | Name (nested) |
| fields.parent.fields.priority.id | string | ID (nested) |
| fields.parent.fields.issuetype.self | string | Self (nested) |
| fields.parent.fields.issuetype.description | string | Description (nested) |
| fields.parent.fields.issuetype.iconUrl | string | Icon URL (nested) |
| fields.parent.fields.issuetype.name | string | Name (nested) |
| fields.parent.fields.issuetype.id | string | ID (nested) |
| fields.parent.fields.issuetype.subtask | boolean | Subtask (nested) |

**カスタムフィールド（プロジェクト依存）:**

| フィールド | 型 | 説明 |
|---|---|---|
| fields.customfield_10034 | string | Vulnerability |
| fields.customfield_10021[].self | string | Flagged - Self |
| fields.customfield_10021[].value | string | Flagged - Value |
| fields.customfield_10021[].id | string | Flagged - ID |
| fields.customfield_10017 | string | Issue color |
| fields.customfield_10019 | string | Rank |
| fields.customfield_10015 | date_time | Start date |
| fields.customfield_10000 | string | 開発 |
| fields.customfield_10001 | string | Team |

### search_issues

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| Description | string | - | 検索キーワード |
| reconcileIssues | string | - | Reconcile Issue IDs (カンマ区切り、最大50件) |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| issues[].id | string | ID |
| issues[].self | string | Self |
| issues[].key | string | Key |
| issues[].changelog.startAt | number | Start at |
| issues[].changelog.maxResults | number | Max results |
| issues[].changelog.total | number | Total |
| issues[].changelog.histories[].id | string | ID |
| issues[].changelog.histories[].author.self | string | Self (nested) |
| issues[].changelog.histories[].author.name | string | Name (nested) |
| issues[].changelog.histories[].author.accountId | string | Account ID (nested) |
| issues[].changelog.histories[].author.emailAddress | string | Email address (nested) |
| issues[].changelog.histories[].author.displayName | string | Display name (nested) |
| issues[].changelog.histories[].author.active | boolean | Active (nested) |
| issues[].changelog.histories[].author.timeZone | string | Time zone (nested) |
| issues[].changelog.histories[].created | date_time | Created |
| issues[].changelog.histories[].items[].field | string | Field |
| issues[].changelog.histories[].items[].fieldtype | string | Field type |
| issues[].changelog.histories[].items[].fieldId | string | Field ID |
| issues[].changelog.histories[].items[].from | string | From |
| issues[].changelog.histories[].items[].fromString | string | From string |
| issues[].changelog.histories[].items[].to | string | To |
| issues[].changelog.histories[].items[].toString | string | To string |
| issues[].fields.statuscategorychangedate | date_time | ステータス カテゴリが変更されました |
| issues[].fields.issuetype.self | string | Self |
| issues[].fields.issuetype.id | string | ID |
| issues[].fields.issuetype.description | string | Description |
| issues[].fields.issuetype.iconUrl | string | Icon URL |
| issues[].fields.issuetype.name | string | Name |
| issues[].fields.issuetype.subtask | boolean | Sub task |
| issues[].fields.timespent | number | 消費時間 |
| issues[].fields.project.self | string | Self |
| issues[].fields.project.id | string | ID |
| issues[].fields.project.key | string | Key |
| issues[].fields.project.name | string | Name |
| issues[].fields.fixVersions[].self | string | Self |
| issues[].fields.fixVersions[].id | string | ID |
| issues[].fields.fixVersions[].description | string | Description |
| issues[].fields.fixVersions[].name | string | Name |
| issues[].fields.aggregatetimespent | number | Σ 消費時間 |
| issues[].fields.statusCategory | string | ステータス カテゴリ |
| issues[].fields.resolution.self | string | Self |
| issues[].fields.resolution.id | string | ID |
| issues[].fields.resolution.description | string | Description |
| issues[].fields.resolution.name | string | Name |
| issues[].fields.resolutiondate | date_time | 解決日 |
| issues[].fields.workratio | number | 作業比率 |
| issues[].fields.lastViewed | date_time | 最終閲覧日 |
| issues[].fields.watches.self | string | Self |
| issues[].fields.watches.watchCount | integer | Watch count |
| issues[].fields.watches.isWatching | boolean | Is watching |
| issues[].fields.issuerestriction | string | 制限対象 |
| issues[].fields.thumbnail | string | 画像 |
| issues[].fields.created | date_time | 作成日 |
| issues[].fields.priority.self | string | Self |
| issues[].fields.priority.iconUrl | string | Icon URL |
| issues[].fields.priority.name | string | Name |
| issues[].fields.priority.id | string | ID |
| issues[].fields.labels[] | string | ラベル |
| issues[].fields.timeestimate | number | 残余見積 |
| issues[].fields.aggregatetimeoriginalestimate | number | Σ 初期見積もり |
| issues[].fields.versions[].self | string | Self |
| issues[].fields.versions[].id | string | ID |
| issues[].fields.versions[].description | string | Description |
| issues[].fields.versions[].name | string | Name |
| issues[].fields.issuelinks[].self | string | Self |
| issues[].fields.issuelinks[].id | string | ID |
| issues[].fields.issuelinks[].type.id | string | ID (nested) |
| issues[].fields.issuelinks[].type.name | string | Name (nested) |
| issues[].fields.issuelinks[].type.inward | string | Inward (nested) |
| issues[].fields.issuelinks[].type.outward | string | Outward (nested) |
| issues[].fields.issuelinks[].inwardIssue.self | string | Self (nested) |
| issues[].fields.issuelinks[].inwardIssue.key | string | Key (nested) |
| issues[].fields.issuelinks[].inwardIssue.id | string | ID (nested) |
| issues[].fields.issuelinks[].outwardIssue.self | string | Self (nested) |
| issues[].fields.issuelinks[].outwardIssue.key | string | Key (nested) |
| issues[].fields.issuelinks[].outwardIssue.id | string | ID (nested) |
| issues[].fields.assignee.self | string | Self |
| issues[].fields.assignee.key | string | Key |
| issues[].fields.assignee.name | string | Name |
| issues[].fields.assignee.accountId | string | Account ID |
| issues[].fields.assignee.emailAddress | string | Email address |
| issues[].fields.assignee.displayName | string | Display name |
| issues[].fields.assignee.active | boolean | Active |
| issues[].fields.assignee.timeZone | string | Time zone |
| issues[].fields.updated | date_time | 更新日 |
| issues[].fields.status.self | string | Self |
| issues[].fields.status.description | string | Description |
| issues[].fields.status.iconUrl | string | Icon URL |
| issues[].fields.status.name | string | Name |
| issues[].fields.status.id | string | ID |
| issues[].fields.status.statusCategory.self | string | Self (nested) |
| issues[].fields.status.statusCategory.id | integer | ID (nested) |
| issues[].fields.status.statusCategory.key | string | Key (nested) |
| issues[].fields.status.statusCategory.colorName | string | Color name (nested) |
| issues[].fields.status.statusCategory.name | string | Name (nested) |
| issues[].fields.components[].self | string | Self |
| issues[].fields.components[].id | string | ID |
| issues[].fields.components[].name | string | Name |
| issues[].fields.issuekey | string | キー |
| issues[].fields.timeoriginalestimate | number | 初期見積もり |
| issues[].fields.description | string | 説明 |
| issues[].fields.timetracking | string | 時間管理 |
| issues[].fields.security | string | セキュリティ レベル |
| issues[].fields.attachment[].self | string | Self |
| issues[].fields.attachment[].filename | string | Filename |
| issues[].fields.attachment[].author.self | string | Self url (nested) |
| issues[].fields.attachment[].author.name | string | Name (nested) |
| issues[].fields.attachment[].author.accountId | string | Account ID (nested) |
| issues[].fields.attachment[].author.emailAddress | string | Email address (nested) |
| issues[].fields.attachment[].author.displayName | string | Display name (nested) |
| issues[].fields.attachment[].created | date_time | Created |
| issues[].fields.attachment[].size | string | Size |
| issues[].fields.attachment[].mimeType | string | Mime type |
| issues[].fields.attachment[].content | string | Content |
| issues[].fields.attachment[].thumbnail | string | Thumbnail |
| issues[].fields.aggregatetimeestimate | number | Σ 残余見積 |
| issues[].fields.summary | string | 要約 |
| issues[].fields.creator.self | string | Self |
| issues[].fields.creator.key | string | Key |
| issues[].fields.creator.name | string | Name |
| issues[].fields.creator.accountId | string | Account ID |
| issues[].fields.creator.emailAddress | string | Email address |
| issues[].fields.creator.displayName | string | Display name |
| issues[].fields.creator.active | boolean | Active |
| issues[].fields.creator.timeZone | string | Time zone |
| issues[].fields.subtasks[].self | string | Self |
| issues[].fields.subtasks[].key | string | Key |
| issues[].fields.subtasks[].id | string | ID |
| issues[].fields.reporter.self | string | Self |
| issues[].fields.reporter.key | string | Key |
| issues[].fields.reporter.name | string | Name |
| issues[].fields.reporter.accountId | string | Account ID |
| issues[].fields.reporter.emailAddress | string | Email address |
| issues[].fields.reporter.displayName | string | Display name |
| issues[].fields.reporter.active | boolean | Active |
| issues[].fields.reporter.timeZone | string | Time zone |
| issues[].fields.aggregateprogress.progress | integer | Progress |
| issues[].fields.aggregateprogress.total | integer | Total |
| issues[].fields.environment | string | 環境 |
| issues[].fields.duedate | date_time | 期限 |
| issues[].fields.progress.progress | integer | Progress |
| issues[].fields.progress.total | integer | Total |
| issues[].fields.votes.self | string | Self |
| issues[].fields.votes.votes | integer | Votes |
| issues[].fields.votes.hasVoted | boolean | Has voted |
| issues[].fields.comment | string | コメント |
| issues[].fields.worklog[].worklog | string | ログ作業 |
| issues[].fields.parent.id | string | ID |
| issues[].fields.parent.key | string | Key |
| issues[].fields.parent.self | string | Self |
| issues[].fields.parent.fields.summary | string | Summary (nested) |
| issues[].fields.parent.fields.status.name | string | Name (nested) |
| issues[].fields.parent.fields.priority.name | string | Name (nested) |
| issues[].fields.parent.fields.issuetype.name | string | Name (nested) |

### deleted_object (Deleted object)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: 出力スキーマは Object picklist の選択結果に依存（dynamic）。プロジェクト未選択のため UI 観察では取得不可。

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Object | select | Yes | Yes | Select the object to receive deleted events from Jira. |

### issue_created_bulk (Export new issues in Jira)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| When first started, this recipe should pick up events from | date-time | - | Yes | When you start recipe for the first time, it picks up trigger events from this specified date and time. Defaults to one hour from time of start of recipe. |
| JQL where class | string | - | Yes | JQL query to filter the records you want, e.g. `project = "PRJ" AND status = "Done"`. Only issueKey, project, issuetype, status, assignee, reporter, issue.property and cf[id] JQL queries are supported. ORDER BY clause is not supported. |
| Fields to retrieve | toggle-field | - | Yes | Select one or more fields from the dropdown. If left blank, defaults to retrieving all navigable fields. |
| Schedule settings | select | Yes | Yes | — |
| Time unit | select | Yes | Yes | Select an interval or custom schedule to specify cron expression. |
| Trigger every | integer | Yes | Yes | Define repeating schedule. Minimum 5 minutes. |
| When exporting records to form the CSV, fetch them in batches of | integer | - | No | — |
| Start after | date-time | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| CSV content | string | — |
| Object name | string | — |
| Object schema | array | — |
| Field name | string | — |
| Field label | string | — |
| Original type | string | — |
| Mapped type | string | — |
| List size | integer | — |
| List index | integer | — |
| New From | date_time | — |

### issue_created_or_updated_bulk (Export new/updated issues in Jira)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| When first started, this recipe should pick up events from | date-time | - | Yes | When you start recipe for the first time, it picks up trigger events from this specified date and time. Defaults to one hour from time of start of recipe. |
| JQL where class | string | - | Yes | JQL query to filter the records you want, e.g. `project = "PRJ" AND status = "Done"`. Only issueKey, project, issuetype, status, assignee, reporter, issue.property and cf[id] JQL queries are supported. ORDER BY clause is not supported. |
| Fields to retrieve | toggle-field | - | Yes | Select one or more fields from the dropdown. If left blank, defaults to retrieving all navigable fields. |
| Schedule settings | select | Yes | Yes | — |
| Time unit | select | Yes | Yes | Select an interval or custom schedule to specify cron expression. |
| Trigger every | integer | Yes | Yes | Define repeating schedule. Minimum 5 minutes. |
| When exporting records to form the CSV, fetch them in batches of | integer | - | No | — |
| Start after | date-time | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| CSV content | string | — |
| Object name | string | — |
| Object schema | array | — |
| Field name | string | — |
| Field label | string | — |
| Original type | string | — |
| Mapped type | string | — |
| List size | integer | — |
| List index | integer | — |
| New/updated From | date_time | — |

### new_event (New event)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: 出力スキーマは Object 選択に依存（dynamic）。Object/プロジェクト未選択のため UI 観察では取得不可。

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Object | select | Yes | Yes | Select the object to receive events from Jira. |
| Event name | string | Yes | Yes | Use a unique name to generate webhook URL. |

### new_issue_batch (New issue — Batch)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| When first started, this recipe should pick up events from | date-time | - | Yes | When you start recipe for the first time, it picks up trigger events from this specified date and time. Leave empty to get created records one hour ago. |
| Batch size | integer | - | Yes | Maximum number of records per trigger event. Min 1, max 100, default 100. |
| Trigger poll interval | integer | - | No | — |
| JQL where class | string | - | No | — |
| Fields to retrieve | toggle-field | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Range | string | — |
| First issue ID | string | — |
| Last issue ID | string | — |
| Issues | array | — |
| issues[].id | string | ID |
| issues[].self | string | Self |
| issues[].key | string | Key |
| issues[].changelog | object | Changelog |
| issues[].fields | object | Fields |
| List size | integer | — |
| List index | integer | — |

### updated_comment_webhook (New/updated comment)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| JQL WHERE clause | string | - | Yes | JQL query to filter the records you want, e.g. `project = "PRJ" AND status = "Done"`. Only issueKey, project, issuetype, status, assignee, reporter, issue.property and cf[id] JQL queries are supported. ORDER BY clause is not supported. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| self | string | Self |
| id | string | ID |
| author | object | Author |
| author.self | string | Self (nested) |
| author.name | string | Name (nested) |
| author.accountId | string | Account ID (nested) |
| author.displayName | string | Display name (nested) |
| author.active | boolean | Active (nested) |
| body | string | Body |
| updateAuthor | object | Update author |
| updateAuthor.self | string | Self (nested) |
| updateAuthor.name | string | Name (nested) |
| updateAuthor.accountId | string | Account ID (nested) |
| updateAuthor.displayName | string | Display name (nested) |
| updateAuthor.active | boolean | Active (nested) |
| created | date_time | Created |
| updated | date_time | Updated |
| visibility | object | Visibility |
| visibility.type | string | Type (nested) |
| visibility.value | string | Value (nested) |

### updated_issue_webhook (New/updated issue)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| When first started, this recipe should pick up events from | date-time | Yes | Yes | When you start recipe for the first time, it picks up new/updated issues from this specified date and time. Once recipe has been run or tested, value cannot be changed. |
| JQL WHERE clause | string | - | Yes | JQL query to filter records (issueKey, project, issuetype, status, assignee, reporter, issue.property, cf[id]). ORDER BY not supported. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| id | string | ID |
| self | string | Self |
| key | string | Key |
| changelog | object | Changelog |
| changelog.startAt | number | Start at |
| changelog.maxResults | number | Max results |
| changelog.total | number | Total |
| changelog.histories | array | Histories |
| fields | object | Fields |
| fields.statuscategorychangedate | date_time | ステータス カテゴリが変更されました |
| fields.issuetype | object | 課題タイプ |
| fields.timespent | number | 消費時間 |
| fields.project | object | プロジェクト |
| fields.fixVersions | array | 修正バージョン |
| fields.aggregatetimespent | number | Σ 消費時間 |
| fields.statusCategory | string | ステータス カテゴリ |
| fields.customfield_xxx (Vulnerability) | string | Vulnerability |
| fields.parent | object | 親 |
| fields.resolution | object | 解決状況 |
| fields.customfield_xxx (Design) | string | Design |
| fields.resolutiondate | date_time | 解決日 |
| fields.workratio | number | 作業比率 |
| fields.lastViewed | date_time | 最終閲覧日 |
| fields.watches | object | ウォッチャー |
| fields.issuerestriction | string | 制限対象 |
| fields.thumbnail | string | 画像 |
| fields.created | date_time | 作成日 |
| fields.customfield_xxx (Flagged) | array | Flagged |
| fields.priority | object | 優先度 |
| fields.labels[] | string | ラベル |
| fields.customfield_xxx (Issue color) | string | Issue color |
| fields.customfield_xxx (Rank) | string | Rank |
| fields.timeestimate | number | 残余見積 |
| fields.aggregatetimeoriginalestimate | number | Σ 初期見積もり |
| fields.versions | array | 影響するバージョン |
| fields.issuelinks | array | リンクされた課題 |
| fields.assignee | object | 担当者 |
| fields.updated | date_time | 更新日 |
| fields.status | object | ステータス |
| fields.components | array | コンポーネント |
| fields.issuekey | string | キー |
| fields.timeoriginalestimate | number | 初期見積もり |
| fields.description | string | 説明 |
| fields.timetracking | string | 時間管理 |
| fields.customfield_xxx (Start date) | date | Start date |
| fields.security | string | セキュリティ レベル |
| fields.attachment | array | 添付ファイル |
| fields.aggregatetimeestimate | number | Σ 残余見積 |
| fields.summary | string | 要約 |
| fields.creator | object | 作成者 |
| fields.subtasks | array | サブタスク |
| fields.reporter | object | 報告者 |
| fields.aggregateprogress | object | Σ 進捗状況 |
| fields.customfield_xxx (開発) | string | 開発 |
| fields.customfield_xxx (Team) | string | Team |
| fields.environment | string | 環境 |
| fields.duedate | date | 期限 |
| fields.progress | object | 進捗状況 |
| fields.votes | object | 投票 |
| fields.comment | string | コメント |
| fields.worklog | array | ログ作業 |
| webhookData | object | Webhook data |
| webhookData.timestamp | integer | Timestamp |
| webhookData.webhookEvent | string | Webhook event |
| webhookData.user | object | User |
| webhookData.changelog | object | Changelog |

> ⚠ ラベル名は Workato テナントの Jira UI 言語設定（日本語）に依存。同じトリガーでも英語テナントでは `Issue type` / `Project` / 等で出る。custom field の内部キー（`customfield_10000` 系）は `new_issue` セクションを参照。

### updated_worklog_webhook (New/updated worklog)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: 表示される form-field がなく、Webhook 登録のみ。

#### Input fields
（パラメータなし — Webhook イベント駆動）

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| self | string | Self |
| id | string | ID |
| comment | string | Comment |
| author | object | Author |
| author.self | string | Self (nested) |
| author.name | string | Name (nested) |
| author.accountId | string | Account ID (nested) |
| author.displayName | string | Display name (nested) |
| author.key | string | Key (nested) |
| author.timeZone | string | Time zone (nested) |
| author.avatarUrls | object | Avatar urls (nested) |
| author.active | boolean | Active (nested) |
| body | string | Body |
| updateAuthor | object | Update author |
| updateAuthor.self | string | Self (nested) |
| updateAuthor.name | string | Name (nested) |
| updateAuthor.accountId | string | Account ID (nested) |
| updateAuthor.displayName | string | Display name (nested) |
| updateAuthor.key | string | Key (nested) |
| updateAuthor.timeZone | string | Time zone (nested) |
| updateAuthor.avatarUrls | object | Avatar urls (nested) |
| updateAuthor.active | boolean | Active (nested) |
| created | date_time | Created |
| updated | date_time | Updated |
| started | date_time | Started |
| timeSpent | string | Time spent |
| timeSpentSeconds | integer | Time spent seconds |
| issueId | string | Issue ID |

### updated_issue (Updated issue)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| When first started, this recipe should pick up events from | date-time | Yes | Yes | When you start recipe for the first time, it picks up trigger events from this specified date and time. Once recipe has been run or tested, value cannot be changed. |
| Trigger poll interval | integer | - | No | — |
| JQL where class | string | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| id | string | ID |
| self | string | Self |
| key | string | Key |
| changelog | object | Changelog |
| changelog.startAt | number | Start at |
| changelog.maxResults | number | Max results |
| changelog.total | number | Total |
| changelog.histories | array | Histories |
| fields | object | Fields |

> 課題本体のフィールド（`fields.*`）の構造は `new_issue` / `updated_issue_webhook` と同等。日本語テナントではラベルが `要約` `担当者` `期限` 等で出る。

### updated_issue_batch (Updated issue — Batch)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| When first started, this recipe should pick up events from | date-time | - | Yes | When you start recipe for the first time, it picks up trigger events from this specified date and time. Leave empty to get updated records one hour ago. |
| Batch size | integer | - | Yes | Maximum number of records per trigger event. Min 1, max 100, default 100. |
| Trigger poll interval | integer | - | No | — |
| JQL where class | string | - | No | — |
| Fields to retrieve | toggle-field | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Range | string | — |
| First issue ID | string | — |
| Last issue ID | string | — |
| Issues | array | — |
| issues[].id | string | ID |
| issues[].self | string | Self |
| issues[].key | string | Key |
| issues[].changelog | object | Changelog |
| issues[].fields | object | Fields |
| List size | integer | — |
| List index | integer | — |

### assign_issue (Assign user to issue)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_not_found（fire-and-forget アクション。出力スキーマなし）。

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. Use issue ID if your issue moves between projects. |
| Assignee username | toggle-field | Yes | Yes | Assignee's Jira username (e.g. `johndoe` for `johndoe@workato.com`). Only usable in older Jira server. Cloud では Account ID を使う。 |

### create_comment (Create comment)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key to add comment to, e.g. `10105` or `ABC-123`. |
| Comment text | string | Yes | Yes | Use the Jira format `[~username]` to mention a user. |
| Visibility | string | - | No | — |
| Role | string | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| self | string | Self |
| id | string | ID |
| author | object | Author |
| author.self | string | Self (nested) |
| author.name | string | Name (nested) |
| author.accountId | string | Account ID (nested) |
| author.displayName | string | Display name (nested) |
| author.active | boolean | Active (nested) |
| body | string | Body |
| updateAuthor | object | Update author |
| updateAuthor.self | string | Self (nested) |
| updateAuthor.name | string | Name (nested) |
| updateAuthor.accountId | string | Account ID (nested) |
| updateAuthor.displayName | string | Display name (nested) |
| updateAuthor.active | boolean | Active (nested) |
| created | date_time | Created |
| updated | date_time | Updated |
| visibility | object | Visibility |
| visibility.type | string | Type (nested) |
| visibility.value | string | Value (nested) |

### create_issue (Create issue)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Project issue type | toggle-field | Yes | Yes | Select the project and issue type for this issue. |
| Sample project issue type | toggle-field | - | Yes | Select the project and issue type to retrieve custom fields. If Project issue type is not selected, custom fields will not be populated. |
| Summary | string | Yes | Yes | Summary of issue. |
| Reporter account ID | toggle-field | - | Yes | Account ID can be found in the people's page at the end of the URL. |
| Assignee account ID | toggle-field | - | Yes | Account ID can be found in the people's page at the end of the URL. |
| Components | string | - | No | — |
| Description | string | - | No | — |
| Issue priority | string | - | No | — |
| Labels | string | - | No | — |
| Time tracking | string | - | No | — |
| Original estimate | string | - | No | — |
| Remaining estimate | string | - | No | — |
| Issue link | string | - | No | — |
| Due date | date | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| id | string | ID |
| key | string | Key |
| self | string | Self |

> ⚠ 部分学習: dynamic schema unresolved (Sample project issue type 未選択のためカスタムフィールドは非展開)。プロジェクト固有の custom field 入力は `Sample project issue type` を選択するとフォームに動的に追加される。

### create_user (Create user)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Email address | string | Yes | Yes | New user's e-mail address. |
| Products | toggle-field | - | Yes | Products the new user has access to. Select none to create a user without any product access. Leave empty for default access. |
| Password | string | - | No | — |
| Display name (deprecated) | string | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| self | string | Self url |
| key | string | Key |
| name | string | Name |
| accountId | string | Account ID |
| emailAddress | string | Email address |
| avatarUrls | object | Avatar urls |
| avatarUrls.16x16 | string | 16 x 16 (nested) |
| avatarUrls.24x24 | string | 24 x 24 (nested) |
| avatarUrls.32x32 | string | 32 x 32 (nested) |
| avatarUrls.48x48 | string | 48 x 48 (nested) |
| displayName | string | Display name |
| active | boolean | Active |
| timeZone | string | Time zone |
| locale | string | Locale |
| groups | object | Groups |
| groups.size | integer | Size (nested) |
| groups.items | array | Items (nested) |
| applicationRoles | object | Application roles |
| applicationRoles.size | integer | Size (nested) |
| applicationRoles.items | array | Items (nested) |
| expand | string | Expand |
| lastLoginTime | date_time | Last login time |

### find_user (Get user details)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Username | string | - | No | — |
| Email | string | - | No | — |

> 必須項目はないが、両方未指定だとアクションは失敗する（Provide at least one search criteria）。

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| self | string | Self |
| key | string | Key |
| name | string | Name |
| accountId | string | Account ID |
| emailAddress | string | Email address |
| avatarUrls | object | Avatar urls |
| avatarUrls.16x16 | string | 16 x 16 (nested) |
| avatarUrls.24x24 | string | 24 x 24 (nested) |
| avatarUrls.32x32 | string | 32 x 32 (nested) |
| avatarUrls.48x48 | string | 48 x 48 (nested) |
| displayName | string | Display name |
| active | number | Active |
| timeZone | string | Time zone |
| locale | string | Locale |
| expand | string | Expand |

### get_attachment (Download attachment)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Attachment URI | string | Yes | Yes | Obtainable from the step output of objects that support attachments, e.g. the Content datapill from the Get issue action. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| Attachment content | string | — |
| Size | integer | — |

### get_changelog (Get changelog of an issue)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| self | string | Self |
| maxResults | string | Max results |
| startAt | string | Start at |
| total | string | Total |
| isLast | boolean | Is last |
| values | array | Values |
| values[].id | string | ID |
| values[].author | object | Author |
| values[].created | date_time | Created |
| values[].items | array | Items |
| List size | integer | — |
| List index | integer | — |

### get_issue (Get issue)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. Use issue ID if your issue moves between projects. |
| Output fields | toggle-field | - | Yes | Select the fields you wish to use in your recipe. All fields will be returned if left blank. |

#### Output fields
構造は `new_issue` トリガーの出力（fields.* 含む）と同等。主な差分なし。日本語テナントでは label が `要約` `担当者` 等で出る。

| フィールド | 型 | 説明 |
|---|---|---|
| id | string | ID |
| self | string | Self |
| key | string | Key |
| changelog | object | Changelog |
| fields | object | Fields |
| fields.summary | string | 要約 |
| fields.issuetype | object | 課題タイプ |
| fields.project | object | プロジェクト |
| fields.assignee | object | 担当者 |
| fields.reporter | object | 報告者 |
| fields.creator | object | 作成者 |
| fields.status | object | ステータス |
| fields.priority | object | 優先度 |
| fields.labels[] | string | ラベル |
| fields.components | array | コンポーネント |
| fields.fixVersions | array | 修正バージョン |
| fields.versions | array | 影響するバージョン |
| fields.issuelinks | array | リンクされた課題 |
| fields.subtasks | array | サブタスク |
| fields.attachment | array | 添付ファイル |
| fields.comment | string | コメント |
| fields.worklog | array | ログ作業 |
| fields.description | string | 説明 |
| fields.environment | string | 環境 |
| fields.created | date_time | 作成日 |
| fields.updated | date_time | 更新日 |
| fields.duedate | date | 期限 |
| fields.resolutiondate | date_time | 解決日 |
| fields.lastViewed | date_time | 最終閲覧日 |
| fields.timespent | number | 消費時間 |
| fields.timeestimate | number | 残余見積 |
| fields.timeoriginalestimate | number | 初期見積もり |
| fields.aggregatetimespent | number | Σ 消費時間 |
| fields.aggregatetimeestimate | number | Σ 残余見積 |
| fields.aggregatetimeoriginalestimate | number | Σ 初期見積もり |
| fields.workratio | number | 作業比率 |
| fields.parent | object | 親 |
| fields.statusCategory | string | ステータス カテゴリ |
| fields.statuscategorychangedate | date_time | ステータス カテゴリが変更されました |
| fields.security | string | セキュリティ レベル |
| fields.issuerestriction | string | 制限対象 |
| fields.thumbnail | string | 画像 |
| fields.timetracking | string | 時間管理 |
| fields.watches | object | ウォッチャー |
| fields.votes | object | 投票 |
| fields.progress | object | 進捗状況 |
| fields.aggregateprogress | object | Σ 進捗状況 |
| fields.resolution | object | 解決状況 |
| fields.issuekey | string | キー |

### get_issue_comments (Get issue comments — Batch)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| comments | array | — |
| comments[].self | string | Self |
| comments[].id | string | ID |
| comments[].author | object | Author |
| comments[].body | string | Body |
| comments[].updateAuthor | object | Update author |
| comments[].created | date_time | Created |
| comments[].updated | date_time | Updated |
| comments[].visibility | object | Visibility |
| List size | integer | — |
| List index | integer | — |

### get_object_schema (Get issue schema)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Output fields | toggle-field | - | Yes | Select the fields you wish to use in your recipe. All fields will be returned if left blank. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| objectName | string | Object name |
| objectLabel | string | Object label |
| fields | array | Fields |
| fields[].fieldName | string | Field name |
| fields[].fieldLabel | string | Field label |
| fields[].originalType | string | Original type |
| fields[].mappedType | string | Mapped type |
| fields[].orderable | boolean | Orderable |
| fields[].navigable | boolean | Navigable |
| fields[].searchable | boolean | Searchable |
| fields[].customField | boolean | Custom field? |
| List size | integer | — |
| List index | integer | — |

### search_assignable_users (Search assignable users — Batch)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Project ID or key | string | Yes | Yes | Project ID or key of project. |
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. |
| Username | string | - | No | — |
| Assignee account ID | string | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| users | array | — |
| users[].self | string | Self url |
| users[].key | string | Key |
| users[].name | string | Name |
| users[].accountId | string | Account ID |
| users[].emailAddress | string | Email address |
| users[].avatarUrls | object | Avatar urls |
| users[].displayName | string | Display name |
| users[].active | boolean | Active |
| users[].timeZone | string | Time zone |
| users[].locale | string | Locale |
| users[].groups | object | Groups |
| users[].applicationRoles | object | Application roles |
| users[].expand | string | Expand |
| users[].lastLoginTime | date_time | Last login time |
| List size | integer | — |
| List index | integer | — |

### search_issues_by_JQL (Search issues by JQL — Batch)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| JQL query string | string | Yes | Yes | JQL query string. |
| Output fields | toggle-field | - | Yes | Select the fields you wish to use in your recipe. All fields will be returned if left blank. |
| Pagination | string | - | Yes | — |
| Max result | integer | - | Yes | Maximum records to be returned. Integer between 1 to 5000. Defaults to 100. |
| Reconcile Issue IDs | string | - | Yes | Provide comma separated issue ids to get consistent results immediately after updating the issues. Max 50 ids. |
| Next page token | string | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| expand | string | Expand |
| startAt | integer | Start at |
| maxResults | integer | Max results |
| total | integer | Total |
| nextPageToken | string | Next page token |
| issues | array | — |
| issues[].id | string | ID |
| issues[].self | string | Self |
| issues[].key | string | Key |
| issues[].changelog | object | Changelog |
| issues[].fields | object | Fields |
| List size | integer | — |
| List index | integer | — |

> issue 詳細フィールドは `search_issues` セクションを参照（同等）。

### update_comment (Update comment)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. |
| Comment ID | string | Yes | Yes | ID of comment to update. |
| Comment | string | Yes | Yes | Content to update the comment with. Use `[~username]` to mention a user, e.g. `[~johndoe] this issue requires an urgent fix.` |
| Visibility | string | - | Yes | — |
| Role | string | - | Yes | Enter role name to restrict visibility of the comment to (e.g. role defined in your Jira account). Use `All Users` to remove restrictions. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| self | string | Self |
| id | string | ID |
| author | object | Author |
| author.self | string | Self (nested) |
| author.name | string | Name (nested) |
| author.accountId | string | Account ID (nested) |
| author.displayName | string | Display name (nested) |
| author.active | boolean | Active (nested) |
| body | string | Body |
| updateAuthor | object | Update author |
| updateAuthor.self | string | Self (nested) |
| updateAuthor.name | string | Name (nested) |
| updateAuthor.accountId | string | Account ID (nested) |
| updateAuthor.displayName | string | Display name (nested) |
| updateAuthor.active | boolean | Active (nested) |
| created | date_time | Created |
| updated | date_time | Updated |
| visibility | object | Visibility |
| visibility.type | string | Type (nested) |
| visibility.value | string | Value (nested) |

### update_issue (Update issue)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_not_found（fire-and-forget アクション。出力スキーマなし）。custom field の動的解決は Sample project issue type 選択時のみ。

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. |
| Sample project issue type | toggle-field | Yes | Yes | Used to retrieve custom fields specific to project and issue type. Non-English Jira instances should specify system issue types in equivalent English (e.g. `タスク` → `Task`). |
| Reporter account ID | toggle-field | - | Yes | Account ID can be found in the people's page at the end of the URL. |
| Assignee account ID | toggle-field | - | Yes | Account ID can be found in the people's page at the end of the URL. |
| Summary | string | - | No | — |
| Components | string | - | No | — |
| Description | string | - | No | — |
| Issue priority | string | - | No | — |
| Labels | string | - | No | — |
| Time tracking | string | - | No | — |
| Original estimate | string | - | No | — |
| Remaining estimate | string | - | No | — |
| Issue link | string | - | No | — |
| Due date | date | - | No | — |

### update_issue_status (Update issue status)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: output_group_not_found（fire-and-forget アクション。出力スキーマなし）。

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. |
| Transition name | string | Yes | Yes | Case sensitive name of transition (e.g. `To do`, `In progress`, `Done`). |

### upload_attachment (Upload attachment)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. |
| File content | string | Yes | Yes | File content to upload, e.g. Attachment content datapill from output of preceding Download attachment action. |
| File name | string | Yes | Yes | Filename with extension, e.g. `.pdf`, `.csv`, `.jpg`. |

#### Output fields
| フィールド | 型 | 説明 |
|---|---|---|
| attachments | array | — |
| attachments[].self | string | Self |
| attachments[].filename | string | Filename |
| attachments[].author | object | Author |
| attachments[].created | date_time | Created |
| attachments[].size | string | Size |
| attachments[].mimeType | string | Mime type |
| attachments[].content | string | Content |
| attachments[].thumbnail | string | Thumbnail |
| List size | integer | — |
| List index | integer | — |

## 備考
- リアルタイムトリガーには Jira 側の Webhook 登録が必要
- `search_issues` は UI 上で検索フィールドを指定する形式（JQL 直接入力は `Search issues by JQL` を使用）
- 日本語テナントのデータツリーは label が日本語（`要約`、`担当者`、`期限` 等）で出る。レシピの datapill 参照では JSON キー（`fields.summary`、`fields.assignee` 等）を使う必要があるため、`new_issue` セクションの英語キー対応表を参照。
- `update_issue` / `create_issue` の custom field 入力は `Sample project issue type` 選択により動的に追加される。プロジェクトごとに異なるため `/learn-recipe` で個別レシピから補完する。

---

## 学習サマリ

最終実行: 2026-04-27 by /auto-learn
- 試行: 26 op (10 triggers + 16 actions)
- 完全成功: 19
- 部分学習: 7 — `deleted_object`, `new_event`, `updated_worklog_webhook`, `assign_issue`, `create_issue`, `update_issue`, `update_issue_status`
- 学習失敗: 0
- スキップ:
  - Deprecated: 3
  - adhoc: 1 — `__adhoc_http_action`
  - 既学習: 2 — `new_issue`, `search_issues`

### 要 follow-up

- **Dynamic schema (要 /learn-recipe)** — Object/Project picklist 未選択により output schema が確定せず
  - `deleted_object` — トリガー output が Object 選択依存
  - `new_event` — トリガー output が Object 選択依存
  - `create_issue` / `update_issue` (custom field 入力) — `Sample project issue type` 選択時のみ展開（プロジェクト固有）
- **Fire-and-forget (UI 仕様・追加学習不要)**
  - `assign_issue` — 担当者アサイン
  - `update_issue` — 課題更新（output_group_not_found）
  - `update_issue_status` — ステータス更新
- **Webhook-only**
  - `updated_worklog_webhook` — form-field 入力なし、Webhook 登録のみ

### 構造的注記（参考）

- 出力ラベルが日本語化（`要約`, `担当者`, `期限`）— 既存 `new_issue` セクションの英語 JSON キー対応表を要参照
- `Pagination` / `Visibility` / `Role` / `Time tracking` / `Issue link` 等は内部 control type が空で `string` フォールバック。型精度はマニュアル補完
- Custom fields (`customfield_xxxxx`) は project + issue type 依存で UI 観察対象外
