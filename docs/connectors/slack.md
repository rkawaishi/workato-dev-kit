# Slack connector

Provider: `slack`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Button click | `button_action` | - |  |
| New event | `new_event` | - |  |

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Archive channel | `archive_channel` | - |  [deprecated] |
| Archive conversation | `archive_conversation` | - |  |
| Create channel | `create_channel` | - |  [deprecated] |
| Create conversation (channels and groups) | `create_conversation` | - |  |
| Get user info | `get_user_by_email` | - |  |
| Invite users to channel | `invite_user_to_channel` | - |  [deprecated] |
| Invite users to conversation | `invite_user_to_conversation` | - |  |
| Invite users to group | `invite_user_to_group` | - |  [deprecated] |
| Respond to button click | `post_button_action_reply` | - |  |
| Post message | `post_message_to_channel` | - |  |
| Set channel purpose | `set_channel_purpose` | - |  [deprecated] |
| Set channel topic | `set_channel_topic` | - |  [deprecated] |
| Set conversation purpose | `set_conversation_purpose` | - |  |
| Set conversation topic | `set_conversation_topic` | - |  |
| Unarchive channel | `unarchive_channel` | - |  [deprecated] |
| Unarchive conversation | `unarchive_conversation` | - |  |

### Triggers
| Name | Description |
|---|---|
| New button click | Button click event |

### Actions
| Name | Description |
|---|---|
| Post message | Post message to channel/DM |
| Respond to button | Response message to button click |

### Notes
- Uses Slack Web API v1
- Supports both Slack for teams and Enterprise Grid
- Not available in CN data center

## Field details

### button_action (Button click)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|

#### Output fields
| Field | Type | Description |
|---|---|---|
| Action name | text | — |
| Action ID | text | — |
| Channel | object | — |
| ID | text | — |
| Name | text | — |
| User | object | — |
| Team | object | — |
| Domain | text | — |
| Action timestamp | text | — |
| Message ID | text | — |
| Attachment ID | text | — |
| Response URL | text | — |

> ⚠ Duplicate labels "ID" / "Name" / "User" are nested fields under the `Channel` and `Team` groups. Note that the data tree's paddingLeft is uniformly 0, so they appear flat.

### new_event (New event)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Event name | text | Yes | Yes | Allows to run separate triggers for separate connections. E.g. your Team name could be the value. Must be one word, lowercase and contain no special characters. Hyphens and underscores allowed. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Team ID | text | — |
| Api app ID | text | — |
| Event ID | text | — |
| Event time | date | — |
| Event | object | — |
| Type | text | — |
| User | text | — |
| Text | text | — |
| Ts | date | — |
| Channel | text | — |
| Event ts | date | — |
| ID | text | — |
| Authorizations | array | — |
| Enterprise ID | text | — |
| User ID | text | — |
| Is bot | text | — |
| Is enterprise install | text | — |
| List size | integer | — |
| List index | integer | — |
| Is ext shared channel | boolean | — |
| Event context | text | — |
| Original event json | text | — |

> ⚠ Type/User/Text/Ts/Channel/Event ts are subfields under the `Event` object. Under Authorizations, Enterprise ID/User ID/Is bot/Is enterprise install are nested. Note that the data tree's paddingLeft is uniformly 0, so they appear flat.
> ⚠ Partial learning: `webhook_suffix` (event type field) should exist in input, but the mapping between the UI's "Event name" field and the internal key cannot be fully captured via UI observation (complete with `/learn-recipe`).

### archive_conversation (Archive conversation)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: no output schema (no_output_schema, fire-and-forget action)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Conversation |  | Yes | Yes | Select from available conversations. If not found, you may toggle to 'Enter conversation ID/name'. |

#### Output fields
| Field | Type | Description |
|---|---|---|

### create_conversation (Create conversation (channels and groups))

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Conversation name | text | Yes | Yes | Enter conversation name without '#' prefix. Conversation names may only contain lowercase letters, numbers, hyphens, and underscores, and must be 80 characters or less. |
| Private conversation? | boolean | - | Yes | Creates a private group. |
| Return conversation details if already exists? | boolean | - | No | (optional field) |

#### Output fields
| Field | Type | Description |
|---|---|---|
| ID | text | — |
| Name | text | — |
| Is archived | boolean | — |
| Created date | date | — |
| Creator | text | — |
| Latest | object | — |
| User | text | — |
| Inviter | text | — |
| Type | text | — |
| Subtype | text | — |
| Text | text | — |
| Unread count | integer | — |
| Unread count display | integer | — |
| Members | text-array | — |
| Topic | object | — |
| Value | text | — |
| Last set | integer | — |
| Purpose | object | — |
| Is channel | boolean | — |
| Is general | boolean | — |
| Is member | boolean | — |
| Is ext shared | boolean | — |
| Is group | boolean | — |
| Is im | boolean | — |
| Is mpim | boolean | — |
| Is pending ext shared | boolean | — |
| Priority | integer | — |

> ⚠ Under Topic / Purpose objects, Value / Last set are nested. Under the Latest object, User / Inviter / Type / Subtype / Text etc. are nested.

### get_user_by_email (Get user info)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Email | text | - | Yes | Provide the user email address |
| User ID | text | - | Yes | Provide the user ID |

> Specify either Email or User ID (both appear as optional but are effectively required as an OR).

#### Output fields
| Field | Type | Description |
|---|---|---|
| ID | text | — |
| Name | text | — |
| Real name | text | — |
| Team ID | text | — |
| Color | text | — |
| Time zone | text | — |
| Profile | object | — |
| Title | text | — |
| Phone | text | — |
| Skype | text | — |
| Real name (normalized) | text | — |
| Display name | text | — |
| Display name (normalized) | text | — |
| Email | text | — |
| Team | text | — |
| Image 512 | text | — |
| Is admin | boolean | — |
| Is owner | boolean | — |
| Is primary owner | boolean | — |
| Is restricted | boolean | — |
| Is ultra restricted | boolean | — |
| Is bot | boolean | — |
| Is app user | boolean | — |

> ⚠ Title / Phone / Skype / Real name (normalized) / Display name / Display name (normalized) / Email / Team / Image 512 are nested under the `Profile` object.

### invite_user_to_conversation (Invite users to conversation)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| User |  | Yes | Yes | Select from available users. For dynamic user names, toggle to 'Enter user ID/name'. |
| Conversation |  | Yes | Yes | Select from available conversations. If not found, you may toggle to 'Enter conversation ID/name'. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| ID | text | — |
| Name | text | — |
| Is archived | boolean | — |
| Created date | date | — |
| Creator | text | — |
| Latest | object | — |
| User | text | — |
| Inviter | text | — |
| Type | text | — |
| Subtype | text | — |
| Text | text | — |
| Unread count | integer | — |
| Unread count display | integer | — |
| Members | text-array | — |
| Topic | object | — |
| Value | text | — |
| Last set | integer | — |
| Purpose | object | — |
| Is channel | boolean | — |
| Is general | boolean | — |
| Is member | boolean | — |
| Is ext shared | boolean | — |
| Is group | boolean | — |
| Is im | boolean | — |
| Is mpim | boolean | — |
| Is pending ext shared | boolean | — |
| Priority | integer | — |

> ⚠ Same schema structure as create_conversation. Under Topic / Purpose objects, Value / Last set are nested.

### post_button_action_reply (Respond to button click)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: no output schema (no_output_schema, fire-and-forget action)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Button response URL | text | Yes | Yes | Identifies button to respond to. Response URL datapill can be found in New button click trigger output. Learn more. |
| Response type | text | Yes | Yes | In channel posts a normal chat message; ephemeral posts message only visible to user. |
| Replace original? | boolean | - | Yes | Replaces the original message with buttons. New message will be posted in the same position in channel. |
| Delete original? | boolean | - | Yes | Deletes the original message with buttons. New message will be posted at the end of channel. |
| Basic text | text | Yes | Yes | Slack message to send. |
| Attachment title | text | - | Yes | Title of the Slack message attachment. |
| Attachment title link | text | - | Yes | Attachment titles are clickable. Provide URL of page to direct users when clicked. |
| Attachment text | text | - | Yes | Text that appears within the attachment block. |
| Attachment message fields |  | - | No | (optional field) |
| Attachment color |  | - | No | (optional field) |
| Thumb URL | text | - | No | (optional field) |
| Image URL | text | - | No | (optional field) |
| Allow Slack formatting |  | - | No | (optional field) |

#### Output fields
| Field | Type | Description |
|---|---|---|

### post_message_to_channel (Post message)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Channel |  | Yes | Yes | Select from available channels. If not found, you may toggle to 'Enter channel ID/name'. |
| Basic text | text | Yes | Yes | Slack message to send. |
| Attachment title | text | - | Yes | Title of the Slack message attachment. |
| Attachment title link | text | - | Yes | Attachment titles are clickable. Provide URL of page to direct users when clicked. |
| Attachment text | text | - | Yes | Text that appears within the attachment block. |
| Buttons |  | - | Yes | — |
| Attachment color |  | - | Yes | Determines the vertical bar color. Red for danger, orange for warning, green for good. |
| Allow Slack formatting |  | - | Yes | Allow parsing of <URL link\|title> <userID> <channel\|name> tags in the message. More information here. Links should be expressed in full e.g. https://workato.com. |
| Attachment message fields |  | - | No | (optional field) |
| Thumb URL | text | - | No | (optional field) |
| Image URL | text | - | No | (optional field) |
| Thread ID | text | - | No | (optional field) |
| Post message as | text | - | No | (optional field) |
| Icon image URL | text | - | No | (optional field) |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Text | text | — |
| Username | text | — |
| User | text | — |
| Type | text | — |
| Subtype | text | — |
| Message ID | text | — |
| Thread ID | text | — |

### set_conversation_purpose (Set conversation purpose)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: no output schema (no_output_schema, fire-and-forget action)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Conversation |  | Yes | Yes | Select from available conversations. To set dynamic conversation names, toggle to 'Enter conversation ID/name'. |
| Conversation purpose | text | Yes | Yes | Set conversation purpose. Slack formatting useable here, including user tagging. Learn more. |

#### Output fields
| Field | Type | Description |
|---|---|---|

### set_conversation_topic (Set conversation topic)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: no output schema (no_output_schema, fire-and-forget action)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Conversation |  | Yes | Yes | Select from available conversations. To set dynamic conversation names, toggle to 'Enter conversation ID/name'. |
| Conversation topic | text | Yes | Yes | Set conversation topic. Slack formatting useable here, including user tagging. Learn more. |

#### Output fields
| Field | Type | Description |
|---|---|---|

### unarchive_conversation (Unarchive conversation)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: no output schema (no_output_schema, fire-and-forget action)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Conversation |  | Yes | Yes | Select from available conversations. If not found, you may toggle to 'Enter conversation ID/name'. |

#### Output fields
| Field | Type | Description |
|---|---|---|

## Workbot for Slack (`slack_bot`)

### Triggers
| Name | Provider internal name | Description |
|---|---|---|
| New event | `new_event` | Subscribe to Slack events (specify event type with `event_name`) |

### Actions
| Name | Provider internal name | Description |
|---|---|---|
| Post bot message | `post_bot_message` | Post message as Bot. Block Kit supported |
| Custom action | `__adhoc_http_action` | Call Slack API directly |

### event_name list (confirmed)
- `reaction_added` — Reaction added

### new_event (reaction_added)

#### Output fields
| Field | Type | Description |
|---|---|---|
| reaction_added.type | string | Type |
| reaction_added.user | string | User |
| reaction_added.reaction | string | Reaction |
| reaction_added.item_user | string | Item user |
| reaction_added.item.type | string | Type (nested) |
| reaction_added.item.channel | string | Channel (nested) |
| reaction_added.item.ts | string | Ts (nested) |
| reaction_added.event_ts | string | Event ts |

### Custom action: conversations.history (GET)

#### Input fields
| Field | Type | Required | Description |
|---|---|---|---|
| path | string | Yes | Path (API endpoint) |
| response_type | string | - | Response type (json, raw, xml2, text) |
| input.data.channel | string | - | channel |
| input.data.latest | string | - | latest |
| input.data.oldest | string | - | oldest |
| input.data.inclusive | boolean | - | inclusive |
| input.data.limit | integer | - | limit |

#### Output fields
| Field | Type | Description |
|---|---|---|
| ok | boolean | Ok |
| messages[].type | string | Type |
| messages[].user | string | User |
| messages[].text | string | Text |
| messages[].ts | string | Ts |
| has_more | boolean | Has more |
| pin_count | number | Pin count |
| response_metadata.next_cursor | string | Next cursor (nested) |

### Event specification field: `slack` vs `slack_bot`

| | `slack` (standard) | `slack_bot` (Workbot) |
|---|---|---|
| Event type field | `input.webhook_suffix` | `input.event_name` |
| dynamicPickListSelection | None | Present |

- Standard connector: specify value directly, e.g. `"webhook_suffix": "reaction_added"`
- Workbot: `"event_name": "reaction_added"` + `dynamicPickListSelection` is attached

### Key fields of post_bot_message
- `channel` — destination channel
- `text` — message text
- `advanced.thread_ts` — timestamp of the thread reply target
- `blocks` — Block Kit block definitions

---

## Learning summary

Last run: 2026-04-27 by `/auto-learn`
- Attempted: 11 op (2 triggers + 9 actions)
- Fully learned: 5 — `button_action`, `create_conversation`, `get_user_by_email`, `invite_user_to_conversation`, `post_message_to_channel`
- Partially learned: 6 — `new_event` (internal key), `archive_conversation` / `unarchive_conversation` / `set_conversation_purpose` / `set_conversation_topic` / `post_button_action_reply` (fire-and-forget)
- Failed: 0
- Skipped:
  - Deprecated: 7
  - adhoc: 1 — `__adhoc_http_action`
  - Already learned: 0

### Needs follow-up

- **Fire-and-forget (UI spec, no additional learning needed)**
  - `archive_conversation` — Archive channel
  - `unarchive_conversation` — Unarchive channel
  - `set_conversation_purpose` — Set channel purpose
  - `set_conversation_topic` — Set channel topic
  - `post_button_action_reply` — Block Kit button response
- **Internal key unknown (needs `/learn-recipe`)**
  - `new_event` — `Event name` field maps to internal `webhook_suffix` key. UI observation can only capture the label

### Structural notes (for reference)

- Duplicate labels `ID` / `Name` / `User`: nested fields under the `Channel` and `Team` groups. Displayed flat with data tree paddingLeft=0 (`button_action`, `new_event`, etc.)
- Dynamic `Channel` picklist: Channel selection is required in many actions (no sandbox value; only static captured)
