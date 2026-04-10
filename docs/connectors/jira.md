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

## 備考
- リアルタイムトリガーには Jira 側の Webhook 登録が必要
- `search_issues` は UI 上で検索フィールドを指定する形式（JQL 直接入力は `Search issues by JQL` を使用）
