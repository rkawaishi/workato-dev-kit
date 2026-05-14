# AI by Workato connector

Provider: `open_ai_utility`

## Triggers

None

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Analyze text | `analyse_document` | - |  |
| Analyze image | `analyse_image` | - |  |
| Categorize text | `categorise_text` | - |  |
| Draft email | `draft_email` | - |  |
| Parse text | `parse_text` | - |  [deprecated] |
| Parse text | `parse_text_v2` | - |  |
| Summarize text | `summarize_text` | - |  |
| Translate text | `translate_text` | - |  |

## Field details

### analyse_document (Action)

Recipe: Update Contract in Salesforce
Provider: `open_ai_utility`

#### Input fields
| Field | Type | Required | Description |
|---|---|---|---|
| _settings_version | string | - | Configuration version |
| text | string | Yes | Text/URL to analyze (can reference a document via datapill) |
| question | string | Yes | Prompt instruction for the analysis |

