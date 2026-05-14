# Jira connector

Provider: `jira`

## Triggers

| Name | Internal name | Batch | Description |
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

| Name | Internal name | Batch | Description |
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

## Field details

### new_issue

#### Output fields
| Field | Type | Description |
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
| fields.statuscategorychangedate | date_time | Status category changed |
| fields.issuetype.self | string | Self |
| fields.issuetype.id | string | ID |
| fields.issuetype.description | string | Description |
| fields.issuetype.iconUrl | string | Icon URL |
| fields.issuetype.name | string | Name |
| fields.issuetype.subtask | boolean | Sub task |
| fields.timespent | number | Time spent |
| fields.project.self | string | Self |
| fields.project.id | string | ID |
| fields.project.key | string | Key |
| fields.project.name | string | Name |
| fields.fixVersions[].self | string | Self |
| fields.fixVersions[].id | string | ID |
| fields.fixVersions[].description | string | Description |
| fields.fixVersions[].name | string | Name |
| fields.aggregatetimespent | number | Σ time spent |
| fields.statusCategory | string | Status category |
| fields.resolution.self | string | Self |
| fields.resolution.id | string | ID |
| fields.resolution.description | string | Description |
| fields.resolution.name | string | Name |
| fields.resolutiondate | date_time | Resolved date |
| fields.workratio | number | Work ratio |
| fields.lastViewed | date_time | Last viewed |
| fields.watches.self | string | Self |
| fields.watches.watchCount | integer | Watch count |
| fields.watches.isWatching | boolean | Is watching |
| fields.issuerestriction | string | Restricted to |
| fields.thumbnail | string | Image |
| fields.created | date_time | Created date |
| fields.priority.self | string | Self |
| fields.priority.iconUrl | string | Icon URL |
| fields.priority.name | string | Name |
| fields.priority.id | string | ID |
| fields.labels[] | string | Labels |
| fields.timeestimate | number | Remaining estimate |
| fields.aggregatetimeoriginalestimate | number | Σ original estimate |
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
| fields.updated | date_time | Updated date |
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
| fields.issuekey | string | Key |
| fields.timeoriginalestimate | number | Original estimate |
| fields.description | string | Description |
| fields.timetracking | string | Time tracking |
| fields.security | string | Security level |
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
| fields.aggregatetimeestimate | number | Σ remaining estimate |
| fields.summary | string | Summary |
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
| fields.environment | string | Environment |
| fields.duedate | date_time | Due date |
| fields.progress.progress | integer | Progress |
| fields.progress.total | integer | Total |
| fields.votes.self | string | Self |
| fields.votes.votes | integer | Votes |
| fields.votes.hasVoted | boolean | Has voted |
| fields.comment | string | Comment |
| fields.worklog[].worklog | string | Work log |
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

**Custom fields (project-dependent):**

| Field | Type | Description |
|---|---|---|
| fields.customfield_10034 | string | Vulnerability |
| fields.customfield_10021[].self | string | Flagged - Self |
| fields.customfield_10021[].value | string | Flagged - Value |
| fields.customfield_10021[].id | string | Flagged - ID |
| fields.customfield_10017 | string | Issue color |
| fields.customfield_10019 | string | Rank |
| fields.customfield_10015 | date_time | Start date |
| fields.customfield_10000 | string | Development |
| fields.customfield_10001 | string | Team |

### search_issues

#### Input fields
| Field | Type | Required | Description |
|---|---|---|---|
| Description | string | - | Search keyword |
| reconcileIssues | string | - | Reconcile Issue IDs (comma-separated, max 50) |

#### Output fields
| Field | Type | Description |
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
| issues[].fields.statuscategorychangedate | date_time | Status category changed |
| issues[].fields.issuetype.self | string | Self |
| issues[].fields.issuetype.id | string | ID |
| issues[].fields.issuetype.description | string | Description |
| issues[].fields.issuetype.iconUrl | string | Icon URL |
| issues[].fields.issuetype.name | string | Name |
| issues[].fields.issuetype.subtask | boolean | Sub task |
| issues[].fields.timespent | number | Time spent |
| issues[].fields.project.self | string | Self |
| issues[].fields.project.id | string | ID |
| issues[].fields.project.key | string | Key |
| issues[].fields.project.name | string | Name |
| issues[].fields.fixVersions[].self | string | Self |
| issues[].fields.fixVersions[].id | string | ID |
| issues[].fields.fixVersions[].description | string | Description |
| issues[].fields.fixVersions[].name | string | Name |
| issues[].fields.aggregatetimespent | number | Σ time spent |
| issues[].fields.statusCategory | string | Status category |
| issues[].fields.resolution.self | string | Self |
| issues[].fields.resolution.id | string | ID |
| issues[].fields.resolution.description | string | Description |
| issues[].fields.resolution.name | string | Name |
| issues[].fields.resolutiondate | date_time | Resolved date |
| issues[].fields.workratio | number | Work ratio |
| issues[].fields.lastViewed | date_time | Last viewed |
| issues[].fields.watches.self | string | Self |
| issues[].fields.watches.watchCount | integer | Watch count |
| issues[].fields.watches.isWatching | boolean | Is watching |
| issues[].fields.issuerestriction | string | Restricted to |
| issues[].fields.thumbnail | string | Image |
| issues[].fields.created | date_time | Created date |
| issues[].fields.priority.self | string | Self |
| issues[].fields.priority.iconUrl | string | Icon URL |
| issues[].fields.priority.name | string | Name |
| issues[].fields.priority.id | string | ID |
| issues[].fields.labels[] | string | Labels |
| issues[].fields.timeestimate | number | Remaining estimate |
| issues[].fields.aggregatetimeoriginalestimate | number | Σ original estimate |
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
| issues[].fields.updated | date_time | Updated date |
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
| issues[].fields.issuekey | string | Key |
| issues[].fields.timeoriginalestimate | number | Original estimate |
| issues[].fields.description | string | Description |
| issues[].fields.timetracking | string | Time tracking |
| issues[].fields.security | string | Security level |
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
| issues[].fields.aggregatetimeestimate | number | Σ remaining estimate |
| issues[].fields.summary | string | Summary |
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
| issues[].fields.environment | string | Environment |
| issues[].fields.duedate | date_time | Due date |
| issues[].fields.progress.progress | integer | Progress |
| issues[].fields.progress.total | integer | Total |
| issues[].fields.votes.self | string | Self |
| issues[].fields.votes.votes | integer | Votes |
| issues[].fields.votes.hasVoted | boolean | Has voted |
| issues[].fields.comment | string | Comment |
| issues[].fields.worklog[].worklog | string | Work log |
| issues[].fields.parent.id | string | ID |
| issues[].fields.parent.key | string | Key |
| issues[].fields.parent.self | string | Self |
| issues[].fields.parent.fields.summary | string | Summary (nested) |
| issues[].fields.parent.fields.status.name | string | Name (nested) |
| issues[].fields.parent.fields.priority.name | string | Name (nested) |
| issues[].fields.parent.fields.issuetype.name | string | Name (nested) |

### deleted_object (Deleted object)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output schema depends on the Object picklist selection (dynamic). Cannot be fetched via UI observation because no project was selected.

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Object | select | Yes | Yes | Select the object to receive deleted events from Jira. |

### issue_created_bulk (Export new issues in Jira)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
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
| Field | Type | Description |
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

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
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
| Field | Type | Description |
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

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output schema depends on the Object selection (dynamic). Cannot be fetched via UI observation because no Object/project was selected.

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Object | select | Yes | Yes | Select the object to receive events from Jira. |
| Event name | string | Yes | Yes | Use a unique name to generate webhook URL. |

### new_issue_batch (New issue — Batch)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| When first started, this recipe should pick up events from | date-time | - | Yes | When you start recipe for the first time, it picks up trigger events from this specified date and time. Leave empty to get created records one hour ago. |
| Batch size | integer | - | Yes | Maximum number of records per trigger event. Min 1, max 100, default 100. |
| Trigger poll interval | integer | - | No | — |
| JQL where class | string | - | No | — |
| Fields to retrieve | toggle-field | - | No | — |

#### Output fields
| Field | Type | Description |
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

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| JQL WHERE clause | string | - | Yes | JQL query to filter the records you want, e.g. `project = "PRJ" AND status = "Done"`. Only issueKey, project, issuetype, status, assignee, reporter, issue.property and cf[id] JQL queries are supported. ORDER BY clause is not supported. |

#### Output fields
| Field | Type | Description |
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

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| When first started, this recipe should pick up events from | date-time | Yes | Yes | When you start recipe for the first time, it picks up new/updated issues from this specified date and time. Once recipe has been run or tested, value cannot be changed. |
| JQL WHERE clause | string | - | Yes | JQL query to filter records (issueKey, project, issuetype, status, assignee, reporter, issue.property, cf[id]). ORDER BY not supported. |

#### Output fields
| Field | Type | Description |
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
| fields.statuscategorychangedate | date_time | Status category changed |
| fields.issuetype | object | Issue type |
| fields.timespent | number | Time spent |
| fields.project | object | Project |
| fields.fixVersions | array | Fix versions |
| fields.aggregatetimespent | number | Σ time spent |
| fields.statusCategory | string | Status category |
| fields.customfield_xxx (Vulnerability) | string | Vulnerability |
| fields.parent | object | Parent |
| fields.resolution | object | Resolution |
| fields.customfield_xxx (Design) | string | Design |
| fields.resolutiondate | date_time | Resolved date |
| fields.workratio | number | Work ratio |
| fields.lastViewed | date_time | Last viewed |
| fields.watches | object | Watchers |
| fields.issuerestriction | string | Restricted to |
| fields.thumbnail | string | Image |
| fields.created | date_time | Created date |
| fields.customfield_xxx (Flagged) | array | Flagged |
| fields.priority | object | Priority |
| fields.labels[] | string | Labels |
| fields.customfield_xxx (Issue color) | string | Issue color |
| fields.customfield_xxx (Rank) | string | Rank |
| fields.timeestimate | number | Remaining estimate |
| fields.aggregatetimeoriginalestimate | number | Σ original estimate |
| fields.versions | array | Affects versions |
| fields.issuelinks | array | Linked issues |
| fields.assignee | object | Assignee |
| fields.updated | date_time | Updated date |
| fields.status | object | Status |
| fields.components | array | Components |
| fields.issuekey | string | Key |
| fields.timeoriginalestimate | number | Original estimate |
| fields.description | string | Description |
| fields.timetracking | string | Time tracking |
| fields.customfield_xxx (Start date) | date | Start date |
| fields.security | string | Security level |
| fields.attachment | array | Attachment |
| fields.aggregatetimeestimate | number | Σ remaining estimate |
| fields.summary | string | Summary |
| fields.creator | object | Creator |
| fields.subtasks | array | Subtasks |
| fields.reporter | object | Reporter |
| fields.aggregateprogress | object | Σ progress |
| fields.customfield_xxx (Development) | string | Development |
| fields.customfield_xxx (Team) | string | Team |
| fields.environment | string | Environment |
| fields.duedate | date | Due date |
| fields.progress | object | Progress |
| fields.votes | object | Votes |
| fields.comment | string | Comment |
| fields.worklog | array | Work log |
| webhookData | object | Webhook data |
| webhookData.timestamp | integer | Timestamp |
| webhookData.webhookEvent | string | Webhook event |
| webhookData.user | object | User |
| webhookData.changelog | object | Changelog |

> ⚠ Label names depend on the Workato tenant's Jira UI language setting (Japanese). The same trigger surfaces them as `Issue type` / `Project` / etc. on an English tenant. For custom field internal keys (`customfield_10000` series), see the `new_issue` section.

### updated_worklog_webhook (New/updated worklog)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: no form-field is shown; webhook registration only.

#### Input fields
(no parameters — driven by webhook events)

#### Output fields
| Field | Type | Description |
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

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| When first started, this recipe should pick up events from | date-time | Yes | Yes | When you start recipe for the first time, it picks up trigger events from this specified date and time. Once recipe has been run or tested, value cannot be changed. |
| Trigger poll interval | integer | - | No | — |
| JQL where class | string | - | No | — |

#### Output fields
| Field | Type | Description |
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

> The structure of the issue body fields (`fields.*`) matches `new_issue` / `updated_issue_webhook`. On a Japanese tenant the labels surface in Japanese (Summary, Assignee, Due date, etc.).

### updated_issue_batch (Updated issue — Batch)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| When first started, this recipe should pick up events from | date-time | - | Yes | When you start recipe for the first time, it picks up trigger events from this specified date and time. Leave empty to get updated records one hour ago. |
| Batch size | integer | - | Yes | Maximum number of records per trigger event. Min 1, max 100, default 100. |
| Trigger poll interval | integer | - | No | — |
| JQL where class | string | - | No | — |
| Fields to retrieve | toggle-field | - | No | — |

#### Output fields
| Field | Type | Description |
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

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_not_found (fire-and-forget action; no output schema).

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. Use issue ID if your issue moves between projects. |
| Assignee username | toggle-field | Yes | Yes | Assignee's Jira username (e.g. `johndoe` for `johndoe@workato.com`). Only usable in older Jira server. On Cloud, use the Account ID. |

### create_comment (Create comment)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key to add comment to, e.g. `10105` or `ABC-123`. |
| Comment text | string | Yes | Yes | Use the Jira format `[~username]` to mention a user. |
| Visibility | string | - | No | — |
| Role | string | - | No | — |

#### Output fields
| Field | Type | Description |
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

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
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
| Field | Type | Description |
|---|---|---|
| id | string | ID |
| key | string | Key |
| self | string | Self |

> ⚠ Partial learning: dynamic schema unresolved (custom fields are not expanded because Sample project issue type was not selected). Project-specific custom field inputs are added to the form dynamically once `Sample project issue type` is selected.

### create_user (Create user)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Email address | string | Yes | Yes | New user's e-mail address. |
| Products | toggle-field | - | Yes | Products the new user has access to. Select none to create a user without any product access. Leave empty for default access. |
| Password | string | - | No | — |
| Display name (deprecated) | string | - | No | — |

#### Output fields
| Field | Type | Description |
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

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Username | string | - | No | — |
| Email | string | - | No | — |

> There are no required fields, but the action fails if both are left empty (Provide at least one search criteria).

#### Output fields
| Field | Type | Description |
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

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Attachment URI | string | Yes | Yes | Obtainable from the step output of objects that support attachments, e.g. the Content datapill from the Get issue action. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Attachment content | string | — |
| Size | integer | — |

### get_changelog (Get changelog of an issue)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | — |

#### Output fields
| Field | Type | Description |
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

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. Use issue ID if your issue moves between projects. |
| Output fields | toggle-field | - | Yes | Select the fields you wish to use in your recipe. All fields will be returned if left blank. |

#### Output fields
The structure matches the output of the `new_issue` trigger (including `fields.*`); no significant differences. On a Japanese tenant the labels surface in Japanese (Summary, Assignee, etc.).

| Field | Type | Description |
|---|---|---|
| id | string | ID |
| self | string | Self |
| key | string | Key |
| changelog | object | Changelog |
| fields | object | Fields |
| fields.summary | string | Summary |
| fields.issuetype | object | Issue type |
| fields.project | object | Project |
| fields.assignee | object | Assignee |
| fields.reporter | object | Reporter |
| fields.creator | object | Creator |
| fields.status | object | Status |
| fields.priority | object | Priority |
| fields.labels[] | string | Labels |
| fields.components | array | Components |
| fields.fixVersions | array | Fix versions |
| fields.versions | array | Affects versions |
| fields.issuelinks | array | Linked issues |
| fields.subtasks | array | Subtasks |
| fields.attachment | array | Attachment |
| fields.comment | string | Comment |
| fields.worklog | array | Work log |
| fields.description | string | Description |
| fields.environment | string | Environment |
| fields.created | date_time | Created date |
| fields.updated | date_time | Updated date |
| fields.duedate | date | Due date |
| fields.resolutiondate | date_time | Resolved date |
| fields.lastViewed | date_time | Last viewed |
| fields.timespent | number | Time spent |
| fields.timeestimate | number | Remaining estimate |
| fields.timeoriginalestimate | number | Original estimate |
| fields.aggregatetimespent | number | Σ time spent |
| fields.aggregatetimeestimate | number | Σ remaining estimate |
| fields.aggregatetimeoriginalestimate | number | Σ original estimate |
| fields.workratio | number | Work ratio |
| fields.parent | object | Parent |
| fields.statusCategory | string | Status category |
| fields.statuscategorychangedate | date_time | Status category changed |
| fields.security | string | Security level |
| fields.issuerestriction | string | Restricted to |
| fields.thumbnail | string | Image |
| fields.timetracking | string | Time tracking |
| fields.watches | object | Watchers |
| fields.votes | object | Votes |
| fields.progress | object | Progress |
| fields.aggregateprogress | object | Σ progress |
| fields.resolution | object | Resolution |
| fields.issuekey | string | Key |

### get_issue_comments (Get issue comments — Batch)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. |

#### Output fields
| Field | Type | Description |
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

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Output fields | toggle-field | - | Yes | Select the fields you wish to use in your recipe. All fields will be returned if left blank. |

#### Output fields
| Field | Type | Description |
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

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Project ID or key | string | Yes | Yes | Project ID or key of project. |
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. |
| Username | string | - | No | — |
| Assignee account ID | string | - | No | — |

#### Output fields
| Field | Type | Description |
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

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| JQL query string | string | Yes | Yes | JQL query string. |
| Output fields | toggle-field | - | Yes | Select the fields you wish to use in your recipe. All fields will be returned if left blank. |
| Pagination | string | - | Yes | — |
| Max result | integer | - | Yes | Maximum records to be returned. Integer between 1 to 5000. Defaults to 100. |
| Reconcile Issue IDs | string | - | Yes | Provide comma separated issue ids to get consistent results immediately after updating the issues. Max 50 ids. |
| Next page token | string | - | No | — |

#### Output fields
| Field | Type | Description |
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

> See the `search_issues` section for issue detail fields (equivalent).

### update_comment (Update comment)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. |
| Comment ID | string | Yes | Yes | ID of comment to update. |
| Comment | string | Yes | Yes | Content to update the comment with. Use `[~username]` to mention a user, e.g. `[~johndoe] this issue requires an urgent fix.` |
| Visibility | string | - | Yes | — |
| Role | string | - | Yes | Enter role name to restrict visibility of the comment to (e.g. role defined in your Jira account). Use `All Users` to remove restrictions. |

#### Output fields
| Field | Type | Description |
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

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_not_found (fire-and-forget action; no output schema). Custom fields are resolved dynamically only when Sample project issue type is selected.

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. |
| Sample project issue type | toggle-field | Yes | Yes | Used to retrieve custom fields specific to project and issue type. Non-English Jira instances should specify system issue types in equivalent English (e.g. the Japanese "Task" issue type should be entered as `Task`). |
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

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: output_group_not_found (fire-and-forget action; no output schema).

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. |
| Transition name | string | Yes | Yes | Case sensitive name of transition (e.g. `To do`, `In progress`, `Done`). |

### upload_attachment (Upload attachment)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Issue ID or key | string | Yes | Yes | Issue ID or key, e.g. `10105` or `ABC-123`. |
| File content | string | Yes | Yes | File content to upload, e.g. Attachment content datapill from output of preceding Download attachment action. |
| File name | string | Yes | Yes | Filename with extension, e.g. `.pdf`, `.csv`, `.jpg`. |

#### Output fields
| Field | Type | Description |
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

## Notes
- Real-time triggers require webhook registration on the Jira side
- `search_issues` takes search fields via the UI (use `Search issues by JQL` to enter JQL directly)
- On a Japanese tenant the data tree labels appear in Japanese (Summary, Assignee, Due date, etc.). Recipe datapill references must use the JSON keys (`fields.summary`, `fields.assignee`, etc.), so consult the English key reference table in the `new_issue` section.
- Custom field inputs for `update_issue` / `create_issue` are added dynamically when `Sample project issue type` is selected. Because they vary per project, supplement them from specific recipes via `/learn-recipe`.

---

## Learning summary

Last run: 2026-04-27 by `/auto-learn`
- Attempted: 26 op (10 triggers + 16 actions)
- Fully learned: 19
- Partially learned: 7 — `deleted_object`, `new_event`, `updated_worklog_webhook`, `assign_issue`, `create_issue`, `update_issue`, `update_issue_status`
- Failed: 0
- Skipped:
  - Deprecated: 3
  - adhoc: 1 — `__adhoc_http_action`
  - Already learned: 2 — `new_issue`, `search_issues`

### Needs follow-up

- **Dynamic schema (needs `/learn-recipe`)** — output schema not finalized because Object/Project picklist was not selected
  - `deleted_object` — trigger output depends on Object selection
  - `new_event` — trigger output depends on Object selection
  - `create_issue` / `update_issue` (custom field inputs) — only expanded when `Sample project issue type` is selected (project-specific)
- **Fire-and-forget (UI design; no further learning needed)**
  - `assign_issue` — assignee assignment
  - `update_issue` — issue update (output_group_not_found)
  - `update_issue_status` — status update
- **Webhook-only**
  - `updated_worklog_webhook` — no form-field input; webhook registration only

### Structural notes (for reference)

- Output labels are localized to Japanese (Summary, Assignee, Due date) — consult the English JSON key reference table in the existing `new_issue` section
- `Pagination` / `Visibility` / `Role` / `Time tracking` / `Issue link` etc. have an empty internal control type and fall back to `string`. Type precision is filled in manually.
- Custom fields (`customfield_xxxxx`) depend on project + issue type and are out of scope for UI observation
