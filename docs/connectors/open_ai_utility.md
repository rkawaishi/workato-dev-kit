# AI by Workato コネクタ

Provider: `open_ai_utility`

## Triggers

なし

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Analyze text | `analyse_document` | - |  |
| Analyze image | `analyse_image` | - |  |
| Categorize text | `categorise_text` | - |  |
| Draft email | `draft_email` | - |  |
| Parse text | `parse_text` | - |  [deprecated] |
| Parse text | `parse_text_v2` | - |  |
| Summarize text | `summarize_text` | - |  |
| Translate text | `translate_text` | - |  |

## フィールド詳細

### analyse_document (Action)

レシピ: Update Contract in Salesforce
Provider: `open_ai_utility`

#### Input fields
| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| _settings_version | string | - | 設定バージョン |
| text | string | Yes | 分析対象のテキスト/URL（datapill でドキュメント参照可） |
| question | string | Yes | 分析のプロンプト指示 |

