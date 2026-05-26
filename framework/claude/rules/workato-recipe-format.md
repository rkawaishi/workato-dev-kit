---
paths:
  - "**/*.recipe.json"
---

# Workato Recipe JSON Format

## Top-level structure

```json
{
  "name": "Recipe name",
  "description": "Description (Markdown supported)",
  "version": 1,
  "private": true,
  "concurrency": 1,
  "code": { /* trigger + action tree */ },
  "config": [ /* connection configuration */ ]
}
```

### `format_version` on the trigger inside `code`

Workato may stamp `"format_version": 2` on the trigger step so it can distinguish a newer recipe structure (it appears after pulling a UI-saved recipe). You can omit it when generating from scratch, but preserve it on push.

## UI-only fields (don't write them by hand, but they appear after pushing)

| Field | Where | Meaning |
|---|---|---|
| `dynamicPickListSelection` | step | Display label for a pick-list selection. Example: `{"event_name": "Slash Command (slash_command)"}` |
| `toggleCfg` | step | Toggle state of input fields. `true` = custom-input mode, `false` = pick-list mode. |
| `title` | action step | Override for the action's display name (`null` = default). |
| `description` | action step | The action description returned by the connector (may include HTML spans). Added automatically on pull. |
| `custom: true` | config's `account_id` | Marks a custom-connector connection (added automatically on pull). |

You can omit these when writing JSON by hand — Workato fills them in on push. Once present (e.g. after pull), keep them; do not delete them.

## `code`: step tree (recursive)

Each step has:

| Field | Type | Description |
|---|---|---|
| `number` | int | Step number (0-based; trigger is 0). |
| `provider` | string | Connector name (e.g. `gmail`, `slack`, `salesforce`). |
| `name` | string | Action name (e.g. `new_email`, `post_message`). |
| `as` | string | Step reference name (used in datapills). |
| `keyword` | string | `"trigger"` / `"action"` / `"foreach"`. |
| `input` | object | Input parameters (may include datapill references). |
| `block` | array | Array of child steps (nestable). |
| `filter` | object | Conditional filter (optional). |
| `comment` | string | Step comment (optional). |
| `uuid` | string | UUID v4. **36 characters or fewer** (do not prefix or extend it — push rejects longer values). The same limit applies to `uuid` fields inside `filter.conditions[]` and `input.conditions[]`. |
| `extended_output_schema` | array/null | Custom output schema. **Recommended on both triggers and actions** — omitting it forces a UI refresh. |
| `extended_input_schema` | array/null | Custom input schema. Required on `return_result` and similar. |

### Naming convention for `as`

| Context | `as` value |
|---|---|
| Normal recipe | Same as the action name (e.g. `new_email`, `post_message`). |
| Genie skill recipe | Random 8-character hex (e.g. `a7c3e1f9`). |
| `slack_bot` connector | Random 8-character hex even in normal recipes. |

### Slack event trigger

```json
{
  "provider": "slack",
  "name": "new_event",
  "keyword": "trigger",
  "input": {
    "webhook_suffix": "reaction_added"
  }
}
```

- The event type goes in `webhook_suffix` (not `event_type`).

### `keyword` values

- `"trigger"` — the start of the recipe (step number 0).
- `"action"` — a normal action step.
- `"foreach"` — a loop. Use `source` for the iteration target and `block` for child steps.

### Trigger for Genie workflows

When the provider is `workato_genie`:
```json
{
  "provider": "workato_genie",
  "name": "start_workflow",
  "keyword": "trigger",
  "input": {
    "requires_user_confirmation": "false",
    "description": "Description of the skill",
    "parameters_schema_json": "[{\"name\":\"param1\",\"type\":\"string\",...}]",
    "result_schema_json": "[{\"name\":\"response\",\"type\":\"string\",...}]"
  }
}
```

## Calling a Genie (`assign_task_to_genie`)

Call an AI agent (Genie) from a recipe:

```json
{
  "provider": "workato_genie",
  "name": "assign_task_to_genie",
  "keyword": "action",
  "dynamicPickListSelection": { "genie_handle": "Genie name" },
  "toggleCfg": { "genie_handle": true },
  "input": {
    "genie_handle": {
      "zip_name": "genie.agentic_genie.json",
      "name": "Genie name",
      "folder": ""
    },
    "task_instructions": "Task instructions (datapills allowed)"
  }
}
```

## Parameter references in a Genie skill recipe

- Parameters are nested under a `parameters` object:
  `path:["parameters","<param_name>"]`
- `workflow_return_result` / `return_result` maps individually to `input.result.<field>`.
- **Always set both `extended_output_schema` and `extended_input_schema`** — omitting them forces an editor reload.
  ```json
  {
    "provider": "workato_genie",
    "name": "workflow_return_result",
    "input": {
      "result": {
        "field1": "#{_dp('...')}",
        "field2": "#{_dp('...')}"
      }
    },
    "extended_output_schema": [
      {
        "label": "Result", "name": "result", "type": "object",
        "properties": [
          { "name": "field1", "type": "string", "label": "Field 1" },
          { "name": "field2", "type": "string", "label": "Field 2" }
        ]
      }
    ],
    "extended_input_schema": [
      {
        "label": "Result", "name": "result", "type": "object",
        "properties": [
          { "name": "field1", "type": "string", "label": "Field 1" },
          { "name": "field2", "type": "string", "label": "Field 2" }
        ]
      }
    ]
  }
  ```

## Custom Action (`__adhoc_http_action`)

When a connector lacks the action you need, call the API directly:

```json
{
  "provider": "<connector>",
  "name": "__adhoc_http_action",
  "as": "<reference_name>",
  "keyword": "action",
  "input": {
    "mnemonic": "Display name",
    "verb": "get",
    "response_type": "json",
    "path": "api/endpoint",
    "input": {
      "schema": "[{...}]",
      "data": { "param": "#{_dp('...')}" }
    },
    "output": "[{...}]"
  },
  "extended_output_schema": [...],
  "extended_input_schema": [...],
  "visible_config_fields": [...],
  "wizardFinished": true
}
```

- `name` is always `"__adhoc_http_action"` (across every connector).
- `input.verb`: HTTP method (`get`, `post`, `put`, `delete`).
- `input.path`: API path (appended to the connector's base URI).
- `input.input.schema`: request-parameter schema (as a JSON string).
- `input.input.data`: parameter values (datapills allowed).
- `input.output`: response schema (as a JSON string).

## Datapill notation

Data references use the `_dp()` function:
```
#{_dp('{"pill_type":"output","provider":"<provider>","line":"<as>","path":["field","nested_field"]}')}
```

- `pill_type`: usually `"output"`.
- `provider`: the source step's `provider`.
- `line`: the source step's `as` value.
- `path`: array of field segments. For the current loop item, use `{"path_element_type":"current_item"}`.

### Other ways to reference data

```ruby
#{_('data.gmail.new_email.subject')}                          # dot notation
=_('data.gmail.new_email.attachments').pluck('filename').join(', ')  # Ruby expression
```

## `filter`: conditional filter

```json
{
  "conditions": [
    {
      "operand": "contains",
      "lhs": "#{_dp('...')}",
      "rhs": "High",
      "uuid": "..."
    }
  ],
  "operand": "and",
  "type": "compound"
}
```

`operand` values (the literal string in JSON, verified against a recipe exercising all 14 operators — see `@docs/logic/if-conditions.md` for details):

| Display | JSON `operand` |
|---|---|
| contains | `contains` |
| doesn't contain | `not_contains` |
| starts with | `starts_with` |
| doesn't start with | `not_starts_with` |
| ends with | `ends_with` |
| doesn't end with | `not_ends_with` |
| equals | `equals_to` (not `equals` / `eq`) |
| doesn't equal | `not_equals_to` (not `not_equals`) |
| greater than | `greater_than` |
| less than | `less_than` |
| is true | `is_true` |
| is not true | `is_not_true` |
| is present | `present` (not `is_present`) |
| is not present | `blank` (UI label is "Is not present") |

## `config`: connection references

```json
{
  "keyword": "application",
  "provider": "gmail",
  "account_id": {
    "zip_name": "sample1_gmail.connection.json",
    "name": "Sample1 | Gmail",
    "folder": ""
  },
  "skip_validation": false
}
```

If `account_id` is `null`, the connection has not been configured yet.

### Cross-project references

To reference a connection in a different project, put the project name in `folder`:
```json
"account_id": {
  "zip_name": "Other Project/Connections/shared_jira.connection.json",
  "name": "Shared | Jira",
  "folder": "Other Project"
}
```

## Schema definitions (`extended_output_schema` / `parameters_schema_json`)

```json
{
  "name": "field_name",
  "type": "string",           // string, number, boolean, object, array
  "label": "Display name",
  "control_type": "text",     // text, number, url, select, multiselect, checkbox
  "optional": false,
  "hint": "Input hint",
  "properties": [],           // child fields when type=object
  "of": "object",             // element type when type=array
  "parse_output": "float_conversion"  // output parsing (optional)
}
```

## `job_report_schema` / `job_report_config`

Custom columns for the recipe job report:
```json
"job_report_schema": [
  { "name": "custom_column_1", "label": "Display name" }
],
"job_report_config": {
  "custom_column_1": "#{_('data.provider.step.field')}"
}
```
