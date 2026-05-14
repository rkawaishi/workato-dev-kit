# Workbot for Slack connector

Provider: `slack_bot`

## Triggers

| Name | Provider internal name | Description |
|---|---|---|
| New command (old version) | `bot_command` | [deprecated] |
| New command | `bot_command_v2` | On command execution (button click, text input) |
| New URL mention | `bot_document_mention` | On URL mention (Salesforce, GitHub) |
| New dynamic menu event | `dynamic_menu` | Dynamic menu search event |
| New help message trigger | `help_event` | On help message request |
| New Shortcut trigger | `message_action` | On global/message shortcut execution |
| New event | `new_event` | On Slack Events API event |

## Actions

| Name | Provider internal name | Description |
|---|---|---|
| Custom action | `__adhoc_http_action` | Direct API call |
| Open/update or push modal view | `block_kit_modals` | Open, update, or push modals |
| Delete message | `delete_message` | Delete message |
| Download attachment | `download_attachment` | Download attachment file |
| Return menu options | `generate_menu_options` | Return dynamic menu options |
| Get user info | `get_user_by_email` | Fetch user info by email address |
| Publish App Home view | `open_bot_app_home` | Display App Home |
| Post dialog | `open_bot_dialog` | Display dialog |
| Post message | `post_bot_message` | Post message to channel/DM |
| Post notification (old version) | `post_bot_notification` | [deprecated] |
| Post command reply (old version) | `post_bot_reply` | [deprecated] |
| Post command reply | `post_bot_reply_v2` | Reply to command |
| Update blocks by block id | `update_blocks_by_block_id` | Update message at block granularity |
| Upload file | `upload_file` | File upload (⚠ mislabeled as "Return menu options" + File badge in the UI picker) |

---

## Trigger details

### bot_command_v2 (New command)

Fires on command execution. Triggered by button clicks, text input, or shortcuts.

#### Input fields
| Field | Type | Description |
|---|---|---|
| domain | string | Command category (e.g. `it_onboarding`) — corresponds to `app` in Recipe JSON |
| name | string | Command name (e.g. `approve`) — corresponds to `action` in Recipe JSON |
| scope | string | Scope (e.g. `request`) — corresponds to `action_data` in Recipe JSON |
| allow_dialog | string | Allow dialog (`true` / `false`) |

#### Output fields
| Field | Path | Description |
|---|---|---|
| message_id | `message_id` | Epoch timestamp (used for thread replies) |
| context.team_id | `context.team_id` | Slack team ID |
| context.user_id | `context.user_id` | Slack ID of the executing user |
| context.channel_id | `context.channel_id` | Channel ID |
| context.user_handle | `context.user_handle` | User handle |
| context.email | `context.email` | User email |
| context.name | `context.name` | User name |
| context.thread_id | `context.thread_id` | Thread ID |
| parameters.* | `parameters.<key>` | Values passed via the button's `params` |
| modals.view_id | `modals.view_id` | Modal's View ID |

#### params reference

Values passed via the button's `params` are accessible from the trigger output via `parameters.<key>`:
```
Button definition: "params": "record_id: #{_dp('...')}"
Trigger output: path:["parameters","record_id"]
```

### new_event (New event)

Fires on Slack Events API events. **Slash commands also actually go through this new_event** (there is no dedicated trigger).

#### Input fields

**`format_version: 2` and later (new version)**:
| Field | Type | Description |
|---|---|---|
| event_name | string | Event name (e.g. `slash_command`, `reaction_added`, `message`, `app_home_opened`) |

When created via the UI, `dynamicPickListSelection.event_name` (for display) and `toggleCfg.event_name: true` are also attached.

**Old version (no format_version / 1)**:
| Field | Type | Description |
|---|---|---|
| webhook_suffix | string | Event type (synonym) |

**Note**: Use `event_name` for new recipes (Workato manages recipes at format_version=2).

#### Output fields (for slash_command)

When using `event_name: "slash_command"`, the following are placed under the `slash_command` object in the trigger output:

| Field | Path | Type | Description |
|---|---|---|---|
| api_app_id | `slash_command.api_app_id` | string | Slack App ID |
| channel_id | `slash_command.channel_id` | string | Channel where the command was executed |
| channel_name | `slash_command.channel_name` | string | Channel name |
| command | `slash_command.command` | string | Slash command name (e.g. `/workato-key`) |
| is_enterprise_install | `slash_command.is_enterprise_install` | boolean | Enterprise Grid install flag |
| response_url | `slash_command.response_url` | string | URL for deferred response |
| team_domain | `slash_command.team_domain` | string | Slack workspace domain |
| team_id | `slash_command.team_id` | string | Slack workspace ID |
| text | `slash_command.text` | string | Command arguments (e.g. `foo bar` for `/workato-key foo bar`) |
| trigger_id | `slash_command.trigger_id` | string | For opening modals |
| user_id | `slash_command.user_id` | string | Slack user ID of the executor |
| user_name | `slash_command.user_name` | string | User name of the executor |

⚠️ **email is not included in the slash_command output**. If you need email, pass `user_id` to the `get_user_by_email` action to fetch the profile (see below).

### dynamic_menu (New dynamic menu event)

Dynamic menu search event. Fires after at least 5 characters of input.

#### Input fields
| Field | Type | Description |
|---|---|---|
| menu_name | string | Dynamic menu name |

#### Output fields
| Field | Description |
|---|---|
| typeahead.parameter_name | Parameter name |
| typeahead.value | User input value |
| parameters.* | Parameters from the parent command |

Used in pair with the `generate_menu_options` action.

### message_action (New Shortcut trigger)

Fires on execution of a global shortcut or message shortcut.

#### Input fields
| Field | Type | Description |
|---|---|---|
| shortcut_type | string | `global` or `message` |

### bot_document_mention (New URL mention)

Real-time. Fires when a target app's URL is mentioned in a channel. Workbot understands Salesforce / Zendesk URLs. Used for unfurling scenarios.

Learned from: `/auto-learn` (UI observation) — 2026-04-25

#### Input fields
| Field | Type | Required | Description |
|---|---|---|---|
| Application | string (picklist) | Yes | App to detect URLs for |
| Business data | string (picklist) | Yes | Target business data type (e.g. invoice, bill, customer) |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Application | string | App name contained in the URL |
| Object | string | Target object type (e.g. account, opportunity) |
| Object ID | string | ID of the target object |
| Context | object | Execution context (container) |
| Context.Team ID | string | Slack team ID |
| Context.User ID | string | Slack ID of the executing user |
| Context.User handle | string | User handle |
| Context.User name | string | User name |
| Context.User email | string | User email |
| Context.Conversation ID | string | Channel / DM ID |
| Context.Message text | string | Full message text containing the URL |
| Context.Reply to | string | Reply target |
| Context.Timestamp | datetime | Fire timestamp |
| Context.Thread ID | string | Thread ID |
| Context.Interactive | boolean | Whether the execution is interactive |
| Context.Trigger ID | string | Slack Trigger ID |
| Context.Callback ID | string | Callback ID |
| Context.Response URL | string | Slack Response URL |
| Context.Original message JSON | string | JSON of the original message |
| Context.Original message timestamp | string | Timestamp of the original message |
| Modals & App home | object | Modal / App home context (container) |

### help_event (New help message trigger)

Real-time. Fires when a user DMs `help` or mentions the bot in a channel like `@workbot help`. Used in pair with the `Post command reply` action to customize the bot's help message. Only one help_event recipe can be enabled per Connection (takes precedence over the custom help).

Learned from: `/auto-learn` (UI observation) — 2026-04-25

#### Input fields
No input fields ("Setup done — This step doesn't need any custom configuration.").

#### Output fields
| Field | Type | Description |
|---|---|---|
| Help message text | string | Default help message text |
| Personalized connections command | string | Command for personal connection management |
| Bot info command | string | Command to display bot info |
| Is bot admin? | boolean | Whether the executing user is a bot admin |
| Bot commands | array | List of commands registered on the bot (container) |
| Bot commands[].Recipe ID | string | Recipe ID implementing the command |
| Bot commands[].Command | string | Command name |
| Bot commands[].Description | string | Command description |
| Bot commands[].Recipe Name | string | Recipe name |
| Bot commands[].Recipe URL | string | URL to the Recipe |
| Bot commands[].Recipe jobs URL | string | URL to the jobs list |
| Bot commands[].List size | integer | Array size |
| Bot commands[].List index | integer | Array iteration index |
| Context | object | Execution context (container) |
| Context.Team ID | string | Slack team ID |
| Context.User ID | string | Slack ID of the executing user |
| Context.User handle | string | User handle |
| Context.User name | string | User name |
| Context.User email | string | User email |
| Context.Conversation ID | string | Channel / DM ID |
| Context.Message text | string | Message text |
| Context.Reply to | string | Reply target |
| Context.Timestamp | datetime | Fire timestamp |
| Context.Thread ID | string | Thread ID |
| Context.Interactive | boolean | Whether the execution is interactive |
| Context.Trigger ID | string | Slack Trigger ID (used to open modals or dialogs) |
| Context.Callback ID | string | Callback ID |
| Context.Response URL | string | Slack Response URL |
| Context.Original message JSON | string | JSON of the original message |
| Context.Original message timestamp | string | Timestamp of the original message |
| Modals & App home | object | Modal / App home context (container) |

---

## Action details

### post_bot_message (Post message)

Posts a message to a channel or DM. The most general-purpose message-posting action.

#### Input fields
| Field | Type | Description |
|---|---|---|
| channel | string | Destination (`#channel` or user ID for DM) |
| text | string | Message text (shown as notification text when blocks are used) |
| blocks | array | Block Kit block definitions |
| attachment_buttons | array | Message with buttons (legacy format) |
| advanced.thread_ts | string | Timestamp of the thread reply target |
| advanced.message_to_update | string | Message ID of the update target |

#### Structure of attachment_buttons

```json
"attachment_buttons": [
  {
    "title": "Button display name",
    "bot_command": "<domain> <name> <scope>",
    "params": "key1: value1\nkey2: value2"
  }
]
```

- A button click fires the `bot_command_v2` trigger
- `bot_command` is in `"<domain> <name> <scope>"` form (space-separated)
- `params` is in newline-separated key: value form

### post_bot_reply_v2 (Post command reply)

Posts a reply to a command (bot_command_v2).

#### Input fields
| Field | Type | Description |
|---|---|---|
| text | string | Reply text |
| blocks | array | Block Kit block definitions |
| send_only_to_user | boolean | Ephemeral (visible only to the user) message |
| replace_original | boolean | Replace the original message |
| delete_original | boolean | Delete the original message |

**Special feature**: `wait_for_user_action` — pauses the job to wait for user input. Allows multi-step interactions in a single Recipe.

### block_kit_modals (Open/update or push modal view)

Open, update, or push modal dialogs.

#### Input fields
| Field | Type | Description |
|---|---|---|
| modal_action | string | `open` / `update` / `push` |
| trigger_id | string | Trigger ID (required for open; auto-generated from user interaction) |
| view_id | string | View ID (required for update) |
| title | string | Modal title (max 24 chars) |
| blocks | array | Block Kit blocks inside the modal |
| submit_label | string | Submit button label (max 24 chars) |
| close_label | string | Close button label (max 24 chars) |
| clear_on_close | boolean | Clear the modal stack on close |
| notify_on_close | boolean | Fire an event on close |
| private_metadata | string | Encrypted metadata (max 3000 chars) |
| callback_id | string | Callback ID (max 255 chars) |

**Limitations**: CamelCase characters and comma-separated name-value pairs are not supported. Use JSON format.

**Special feature**: `wait_for_user_input` — pauses the job until the modal is closed.

### open_bot_app_home (Publish App Home view)

Displays rich content on the bot's App Home tab. Can be personalized per user.

#### Input fields
| Field | Type | Description |
|---|---|---|
| user_id | string | Slack ID of the target user (Required) |
| blocks | array | Block Kit blocks for App Home |

**Prerequisites**:
- Subscription to the `app_home_opened` event in Slack App settings is required
- Home Tab must be enabled

### update_blocks_by_block_id (Update blocks by block id)

Update, replace, or delete specific blocks in messages, App Home, or modals.

#### Input fields
| Field | Type | Description |
|---|---|---|
| surface | string | `message` / `app_home` / `modal` |
| original_json | string | Original block JSON (obtained from trigger output or action result) |
| blocks | array | Blocks to update (target identified by block_id) |
| remove | boolean | Set `true` to delete the block |

One block can be replaced with multiple blocks. Simultaneous updates across multiple blocks are also supported.

### generate_menu_options (Return menu options)

Returns options for a dynamic menu. Used in pair with the `dynamic_menu` trigger.

#### Input fields
| Field | Type | Description |
|---|---|---|
| options | array | List of options (static specification or list datapill) |
| group_options | boolean | Group the options |

### get_user_by_email

⚠️ **Trap where the name doesn't match the input**: although the action is named "get user by email", the input field **accepts either** `email` or `id` (Slack user ID). You can select via the UI toggle. When the trigger output lacks email (like slash_command), use the pattern of passing the Slack user_id into `id`.

#### Input fields
| Field | Type | Description |
|---|---|---|
| email | string | User's email address |
| id | string | Slack user ID (use this when `email` is not available; switch via toggle) |

#### Output fields

User info is returned nested in the `profile` object:

| Field | Path | Type | Description |
|---|---|---|---|
| id | `id` | string | Slack user ID |
| name | `name` | string | User name |
| profile.email | `profile.email` | string | Email address (primary use: fetching email after a slash_command) |
| profile.real_name | `profile.real_name` | string | Real name |
| profile.display_name | `profile.display_name` | string | Display name |

> **Pattern for fetching email after a slash_command trigger**:
> `new_event(event_name: slash_command) → get_user_by_email(id: slash_command.user_id) → reference profile.email downstream`
> This is a required one-step workaround because the Slack Events API slash_command does not include email.

### delete_message (Delete message)

Deletes a message posted as Workbot.

Learned from: `/auto-learn` (UI observation) — 2026-04-25 / output 2026-04-26

#### Input fields
| Field | Type | Required | Description |
|---|---|---|---|
| Message timestamp | string | Yes | Timestamp of the message to delete |
| Message channel | string | Yes | Channel where the message to delete was posted |

No optional fields.

#### Output fields
| Field | Type | Description |
|---|---|---|
| Channel ID | string | Channel ID where the deletion was executed |
| Timestamp | string | Timestamp of the deleted message |

### download_attachment (Download attachment)

Downloads a Slack attachment file via Workbot. Tagged with File output.

Learned from: `/auto-learn` (UI observation) — 2026-04-25 / output 2026-04-26

#### Input fields
| Field | Type | Required | Description |
|---|---|---|---|
| URL | string | Yes | URL of Slack attachment |

No optional fields.

#### Output fields
| Field | Type | Description |
|---|---|---|
| Body | string | Binary content of the attachment file (can be passed downstream as a datapill) |
| Size | integer | File size (bytes) |

### upload_file (Upload file)

Posts a file attachment to a channel or thread. An initial comment can also be added.

⚠ **UI display bug**: In the Workbot for Slack Action picker, the title of `upload_file` is incorrectly displayed as **"Return menu options"** (with File badge). Because it appears alongside `generate_menu_options` (Return menu options, no badge), you must distinguish them by **the presence/absence of the File badge**. The canvas / panel header also shows the same incorrect title, but the field structure is that of upload_file ("Post to conversations" / "File content" etc.). The Step output group name in the Recipe data panel is also displayed as "Return menu options".

Learned from: `/auto-learn` (UI observation) — 2026-04-25 / output 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Post to conversations | string (picklist) | Yes | Visible | Destination channel / direct conversation. Workbot must be a member. Multiple values allowed |
| File content | string | Yes | Visible | File content datapill from the previous step (e.g. Google Drive Download attachment output) |
| Initial comment | string | - | Visible | Opening comment for the file post |
| File name | string | - | Visible | File name (e.g. foo.txt) |
| File type | string | - | Visible | File format identifier (e.g. text). See Slack official docs for supported formats |
| Title | string | - | Hidden | File title |
| Thread ID | string | - | Hidden | Thread ID of the destination |

#### Output fields
Conforms to the Slack `files.upload` API response (see [Slack official reference](https://api.slack.com/methods/files.upload)).

| Field | Type | Description |
|---|---|---|
| Ok | string | API result status |
| File | object | Uploaded file metadata (container) |
| File.ID | string | File ID |
| File.Created | string | Creation timestamp |
| File.Timestamp | string | Timestamp |
| File.Name | string | File name |
| File.Title | string | Title |
| File.User | string | Uploading user ID |
| File.Editable | boolean | Whether editable |
| File.Size | integer | Size (bytes) |
| File.Mode | string | Upload mode |
| File.Is external | boolean | Whether external file |
| File.External type | string | External type |
| File.Is public | boolean | Whether public |
| File.Public URL shared | boolean | Whether public URL is shared |
| File.Display as bot | boolean | Whether to display as bot |
| File.Username | string | User name |
| File.URL private | string | Private URL |
| File.URL private download | string | Private download URL |
| File.Permalink | string | Permalink |
| File.Permalink public | string | Public permalink |
| File.User | string | User (Duplicate label — represents a different path in the Slack API) |
| File.Comments count | integer | Comment count |
| File.Is starred | boolean | Whether starred |
| File.Channels | string[] | Array of destination channel IDs |
| File.Has rich preview | boolean | Whether there is a rich preview |

### open_bot_dialog (Post dialog)

Opens a bot dialog on a button click or menu selection. **Legacy** API (modals are recommended). Used in pair with the `New command` trigger. Structured so that pressing Submit executes a separate bot command.

Learned from: `/auto-learn` (UI observation) — 2026-04-25 / output 2026-04-26

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Trigger ID | string | Yes | Visible | Trigger ID from the New command trigger output. Only valid when originating from a button / menu |
| Dialog title | string | Yes | Visible | Dialog title (max 24 chars) |
| Submit button command | string (picklist) | Yes | Visible | Workbot command to invoke on Submit |
| State(Callback id) | string | - | Visible | Dialog identifier (max 3000 chars). Passed to the Recipe on Submit |
| Submit button label | string | - | Hidden | Label of the Submit button |

#### Output fields
**No output fields** (fire-and-forget action; no `Step N output` group appears in the Recipe data panel). Post-submission processing of the dialog is done by the separate bot command Recipe specified by `Submit button command`.

---

## Block Kit

Slack's UI framework. Usable on three surfaces: messages, modals, and App Home.

### Block count limits

| Surface | Max blocks |
|---|---|
| Message | 50 |
| Modal | 100 |
| App Home | 100 |

### Available block types

| Block | Description |
|---|---|
| Section with text | Text display |
| Section with image | Text + thumbnail image |
| Section with button | Text + button (command execution / URL navigation) |
| Section with fields | Text + title-value pairs (max 10, each 2000 chars) |
| Section with select menu | Text + dropdown menu |
| Section with overflow menu | Text + overflow menu |
| Section with date picker | Text + date selection |
| Repeat block group | Workato-specific: dynamically generate blocks from a list datapill |
| Divider | Separator line |
| Image | Image display (public URL) |
| Actions | Container for interactive elements |
| Context | Context information (image/text) |

### Character limits

| Element | Max chars | Notes |
|---|---|---|
| Button | 2000 | Includes command + input values + Workbot overhead (9 chars) |
| Select menu | 255 | |
| Overflow menu | 75 | |
| Date picker | 255 | |

### attachment_buttons vs Block Kit buttons

| | attachment_buttons | Block Kit buttons |
|---|---|---|
| Format | Legacy (Slack Attachments API) | Current (Block Kit) |
| JSON field | `attachment_buttons` | section with button inside `blocks` |
| Appearance | Simple | Rich (style customizable) |
| Push in Workato | Stable | Watch the structure of blocks (a common cause of push errors) |
| Recommended for | Simple button interactions | When a rich UI is needed |

**Note**: When using Block Kit's `blocks` field, configuring it in the UI before push is reliable. When writing it directly as JSON, configuring `visible_config_fields` may be required.

### Button design guidelines

- The recommended number of buttons is **5 or fewer** (a natural range for conversational UI)
- The command text of a button must match the receiving `bot_command_v2` trigger exactly
- **Dynamic buttons**: buttons can be dynamically generated from a list datapill (Dynamic List option)
  - Button source list: list datapill (e.g. Salesforce account list)
  - Button title: field of the list item
  - Command input values: pass each item's data as parameters

---

## Interface design patterns

### Pattern 1: DM notification with approval buttons

```
post_bot_message (DM + attachment_buttons)
  → user clicks button
  → bot_command_v2 trigger fires (separate Recipe)
  → complete_task / execute processing
  → post_bot_reply_v2 returns the result
```

Use cases: approval flows, confirmation operations

### Pattern 2: Form input via modal

```
bot_command_v2 trigger (button or command)
  → block_kit_modals (open) + wait_for_user_input
  → user fills out the modal and submits
  → retrieve input values and process
```

Use cases: data entry, configuration changes

### Pattern 3: App Home dashboard

```
new_event (webhook_suffix: app_home_opened)
  → fetch data (Jira, Salesforce, etc.)
  → open_bot_app_home (display list via blocks)
  → user clicks button
  → bot_command_v2 displays detail / performs operation
```

Use cases: task lists, pending-approval lists

### Pattern 4: Command with dynamic menu

```
bot_command_v2 trigger (command input)
  → dynamic_menu trigger (separate Recipe)
  → search external system
  → generate_menu_options returns choices
  → user selects
  → execute processing
```

Use cases: record search, user search

### Pattern 5: Dynamic message updates

```
post_bot_message (initial message + blocks)
  → as processing progresses, update_blocks_by_block_id
  → update the status display
```

Use cases: progress display, reflecting status changes

---

## Modal details

### Modal operation types

| Type | Purpose | Required ID |
|---|---|---|
| Open | Open a new modal | Trigger ID |
| Update | Update an existing modal | Trigger ID + View ID |
| Push | Stack a new view on top of the current modal | Trigger ID (from the active view) |

Trigger IDs are generated from buttons, menus, select menus, date pickers, shortcuts, slash commands, and modal submissions.

### Modal-only input blocks

Input elements available only in modals (not in regular messages):
- Single-line input
- Multi-line input
- Select menu input
- Datepicker input
- Checkboxes input

**Important**: Input blocks fire the command only on view submission (not on click).

### Passing data between modals

Modals object included in the `bot_command_v2` trigger output:

| Field | Description |
|---|---|
| View ID | ID of the active view |
| Root View ID | ID of the first view |
| Previous View ID | ID of the immediately previous view |
| Private metadata | Encrypted data (max 3000 chars) |
| Hash | Validation token for asynchronous updates |

### Modal caveats

- Title is max 24 chars; button labels also max 24 chars
- CamelCase and comma-separated name-value pairs are not supported → **use JSON format**
  - Example: `{"OpportunityId": "OPP1234567"}`
- On view submission, the active view ID is invalidated → use Root View ID or Previous View ID
- Push is limited to 3 levels
- When using input blocks, defining submit / close buttons is required

---

## Dialogs (legacy)

Predecessor to modals. Composed of three recipes:

1. **Trigger Recipe** — invokes the dialog-display Recipe on a button/menu click
2. **Dialog-display Recipe** — displays the dialog via `open_bot_dialog` (max 5 fields)
3. **Execution Recipe** — triggered on dialog submission and performs the processing

### Dialogs vs modals

| | Dialog | Modal |
|---|---|---|
| Field count | Max 5 | No limit (composed via blocks) |
| UI flexibility | Text/select only | All Block Kit elements |
| Stacking | Not supported | Max 3 levels |
| Recommended for | Legacy compatibility | **Use modals for new development** |

---

## Dynamic menu details

Composed of two recipes:

### 1. Primary Recipe (command Recipe)
- Set the parameter's dialog control type to `Select`
- Choose `Dynamic` for Menu options
- Specify the dynamic menu Recipe ID
- Pass context parameters via `Dynamic menu recipe params` (comma-separated key-value)

### 2. Dynamic menu Recipe
```
dynamic_menu trigger → search external system (filter by typeahead value) → generate_menu_options
```

- Event fires when the user enters 3 or more characters
- The input string is stored in `typeahead.value`
- `generate_menu_options` returns search results as choices

### JSON configuration in Post dialog

```json
{
  "type": "select",
  "name": "your_parameter",
  "data_source": "external",
  "dynamic_menu_recipe": "28748",
  "dynamic_menu_recipe_params": "stagename: Closed Won",
  "min_query_length": 3
}
```

---

## Message menus

Provides multiple actions as a dropdown. An alternative to buttons.

### Static menus

| Field | Description |
|---|---|
| Menu Name | Menu display label |
| Display Text | Display text of an option |
| Submit Command | Command to execute (must match bot_command_v2) |
| Input Values | Name-value pairs to pass to the downstream Recipe |

### Dynamic menus

Dynamically generate options from a list datapill:
- Menu options source list: list datapill
- Display text: field of the list element
- Submit command: command to execute
- Input values: parameters to pass

Recommendation: keep the number of menu options to **5 or fewer**.

---

## Slash commands

Trigger Workbot Recipes via Slack slash commands like `/createissue`.

### Configuration steps

1. **Workato**: enable the slash command in the Recipe's trigger and enter the command name
2. **Workato**: copy the generated Request URL
3. **Slack API**: create a new command in the app's Slash Commands section
4. **Slack API**: paste the Request URL and add description and hints
5. **Slack API**: enable "Escape channels, users, and links"

### Parameter input methods

- Dialog box (when configuring)
- Inline: `/createissue project_issue_type: UI--Bug summary: bug description`
- Conversational prompt

### Enterprise vs legacy slash commands

| Feature | Enterprise Workbot | Legacy |
|---|---|---|
| Dialog launch | Yes | No |
| Dialog for missing input | Yes | No |
| Ephemeral messages | Yes | No |
| Custom Slack app required | Yes | No |
| Channel posting | Only invited channels | All channels |
| Multiple commands/Connection | Unique per Recipe | Multiple tokens can be stored |

**Legacy is planned for deprecation. Use Enterprise Workbot for new development.**

### Caution

- Slash commands have no namespace, so use names unique across the entire Enterprise Workbot
- In Enterprise Grid environments, organization-level installation is required
- Enterprise Workbot can only post to channels it has been invited to (difference from legacy)

---

## Enterprise Grid setup

Workbot configuration steps for Enterprise Grid environments.

### Prerequisites
- Slack Enterprise Grid plan
- Enterprise Workbot already created in Workato (not Standard Workbot)
- Access to Custom OAuth profiles
- Slack Org Admin or Org Owner permission

### Steps

1. **Generate App-Level Token**: Slack API → App → Basic Information → App-Level Tokens → generate with `authorizations:read` scope
2. **Update Custom OAuth Profile**: Workato → Tools → Custom OAuth profiles → paste the token
3. **Reconnect Workbot**: Platform → Workbot → Edit → Disconnect → Reconnect → authenticate at the **organization level**
4. **Approve app in Slack**: Settings → Organization settings → Apps → Approve
5. **Add to workspaces**: Apps → Add to more workspaces → select target workspaces

---

## Embed (partner distribution)

A mechanism for SaaS vendors to distribute a white-label Slack Bot to their customers.

- Share the Custom OAuth Profile to the customer's workspace
- Export the Recipe as a manifest → import into the customer's workspace
- Customers only need to authenticate with the shared OAuth Profile and the Bot works
- No need for customers to create a Slack OAuth app on their side
