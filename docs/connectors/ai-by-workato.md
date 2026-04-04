# AI by Workato コネクタ

公式: https://docs.workato.com/en/connectors/ai-by-workato.html

## Triggers

なし

## Actions
| 名前 | 説明 |
|---|---|
| Analyze text | テキストデータの内容と意味を分析してインサイトを提供する |
| Categorize text | テキストを事前定義されたカテゴリやグループに分類する |
| Draft email | 提供されたコンテキストやプロンプトに基づいてメール内容を生成する |
| Parse text | 非構造化テキストから特定の情報を抽出・構造化する |
| Summarize text | 長いテキストの要約を作成する |
| Translate text | テキストをある言語から別の言語に翻訳する |
| Analyse document | ドキュメントの内容を分析する |

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
