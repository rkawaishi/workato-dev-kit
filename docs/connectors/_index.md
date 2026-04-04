# Workato コネクタ一覧

## コネクタの分類

### Pre-built Connectors（標準コネクタ）
Workato が公式に提供する 1,000+ のコネクタ。セットアップガイド、必要な権限、利用可能なトリガー/アクション、トラブルシューティングが文書化されている。

### Universal Connectors（汎用コネクタ）
標準コネクタが存在しない API やサービスに接続するための汎用コネクタ。

| コネクタ | 用途 | ドキュメント |
|---|---|---|
| **HTTP** | 任意の HTTP API に接続。認証、コンテンツタイプ、全 HTTP メソッド対応 | https://docs.workato.com/en/developing-connectors/http-v2.html |
| **OpenAPI** | OpenAPI 仕様で記述された API に接続 | https://docs.workato.com/en/connectors/openapi/ |
| **GraphQL** | GraphQL API でクエリ/ミューテーション実行 | https://docs.workato.com/en/connectors/graphql.html |
| **SOAP** | WSDL 記述による Web サービスに接続 | https://docs.workato.com/en/connectors/soap.html |

### Community Connectors（コミュニティコネクタ）
ユーザーが開発・共有したコネクタ。Community Library で検索可能。

### Custom Connectors（カスタムコネクタ）
Connector SDK を使って自作するコネクタ。プライベートスコープで作成後、共有やマーケットプレイス公開が可能。
- SDK ドキュメント: https://docs.workato.com/en/developing-connectors/sdk.html

### Custom Action (`__adhoc_http_action`)
コネクタ内に適切なアクションがない場合、コネクタの認証を利用しつつ API を直接呼び出す。
- 詳細: `@docs/learned-patterns.md` の Custom Action セクション参照

## 主要 Pre-built コネクタ（個別ドキュメントあり）

個別のナレッジファイルがあるコネクタ:
- [Slack](slack.md) — メッセージング、Workbot for Slack
- [Jira](jira.md) — プロジェクト管理、チケット管理
- [Salesforce](salesforce.md) — CRM
- [Gmail](gmail.md) — メール
- [Google Drive](google-drive.md) — クラウドストレージ
- [HubSpot](hubspot.md) — CRM / マーケティング
- [ServiceNow](servicenow.md) — IT サービス管理
- [Snowflake](snowflake.md) — データウェアハウス

`/sync-connectors <name>` で新しいコネクタのドキュメントを追加・更新できます。

## 全 Pre-built コネクタ一覧

以下は公式ドキュメントにページがあるコネクタの一覧（139件）。
ドキュメント URL パターン: `https://docs.workato.com/en/connectors/<name>.html`

<details>
<summary>全コネクタ一覧（クリックで展開）</summary>

| コネクタ | ドキュメント |
|---|---|
| Active Directory | /connectors/active_directory.html |
| Adobe Commerce Magento | /connectors/adobe-commerce-magento.html |
| Adobe Experience Manager | /connectors/adobe_experience_manager.html |
| ADP Workforce Now | /connectors/adp_workforce.html |
| AI by Workato | /connectors/ai-by-workato.html |
| Airtable | /connectors/airtable.html |
| Amazon S3 | /connectors/s3.html |
| Amazon SES | /connectors/amazon-ses.html |
| Amazon SNS | /connectors/amazon-sns.html |
| Amazon SQS | /connectors/sqs.html |
| Analytics Cloud | /connectors/analytics-cloud.html |
| Anaplan | /connectors/anaplan.html |
| Apache Kafka | /connectors/kafka.html |
| Asana | /connectors/asana.html |
| AWS Lambda | /connectors/aws_lambda.html |
| Azure Blob Storage | /connectors/azure_blob_storage.html |
| Azure Monitor | /connectors/azure_monitor.html |
| Azure OpenAI | /connectors/azure-openai.html |
| BambooHR | /connectors/bamboo-hr.html |
| BILL | /connectors/bill.html |
| BIM 360 | /connectors/bim360.html |
| Box | /connectors/box.html |
| Bynder | /connectors/bynder.html |
| Celonis | /connectors/celonis.html |
| Cisco Webex Teams | /connectors/cisco-webex-teams.html |
| Confluence | /connectors/confluence.html |
| Confluent Cloud | /connectors/confluent-cloud.html |
| Coupa | /connectors/coupa.html |
| Databricks | /connectors/databricks.html |
| Dbt Cloud | /connectors/dbt-cloud.html |
| Deputy | /connectors/deputy.html |
| DocuSign | /connectors/docusign.html |
| Dropbox | /connectors/dropbox.html |
| Egnyte | /connectors/egnyte.html |
| Eloqua | /connectors/eloqua.html |
| Eventbrite | /connectors/eventbrite.html |
| Excel | /connectors/excel.html |
| Facebook Lead Ads | /connectors/facebook-ads.html |
| Freshdesk | /connectors/freshdesk.html |
| FTP/FTPS | /connectors/ftp.html |
| GitHub | /connectors/github.html |
| Gmail | /connectors/gmail.html |
| Gong | /connectors/gong.html |
| Google BigQuery | /connectors/bigquery.html |
| Google Calendar | /connectors/google-calendar.html |
| Google Cloud Storage | /connectors/google_cloud_storage.html |
| Google Dialogflow | /connectors/dialogflow.html |
| Google Drive | /connectors/google-drive.html |
| Google Sheets | /connectors/google-sheets.html |
| Google Speech to Text | /connectors/google-speech-to-text.html |
| Google Text to Speech | /connectors/google-text-to-speech.html |
| Google Translate | /connectors/google-translate.html |
| Google Vision | /connectors/google-vision.html |
| Google Workspace | /connectors/google-workspace.html |
| GoTo Webinar | /connectors/go-to-webinar.html |
| Greenhouse | /connectors/greenhouse.html |
| Hive | /connectors/hive.html |
| HubSpot | /connectors/hubspot.html |
| IBM Db2 | /connectors/ibm-db2.html |
| IDP by Workato | /connectors/idp-by-workato.html |
| Insightly | /connectors/insightly.html |
| Intercom | /connectors/intercom.html |
| Iterable | /connectors/iterable.html |
| JavaScript | /connectors/javascript.html |
| JDBC | /connectors/jdbc.html |
| Jira | /connectors/jira.html |
| Jira Service Desk | /connectors/jsd.html |
| Java Messaging Service | /connectors/jms.html |
| JWT | /connectors/jwt.html |
| LaunchDarkly | /connectors/launchdarkly.html |
| LinkedIn | /connectors/linkedin.html |
| MailChimp | /connectors/mailchimp.html |
| Marketo | /connectors/marketo.html |
| Microsoft Dynamics 365 | /connectors/dynamics-crm.html |
| MongoDB Atlas | /connectors/mongodb-atlas.html |
| MySQL | /connectors/mysql.html |
| Namely | /connectors/namely.html |
| NetSuite SOAP | /connectors/netsuite.html |
| NetSuite REST | /connectors/netsuite-rest.html |
| Okta | /connectors/okta.html |
| On-prem command scripts | /connectors/on-prem-command-line-scripts.html |
| On-prem files | /connectors/on-prem-files.html |
| OneDrive | /connectors/onedrive.html |
| OpenAI | /connectors/openai.html |
| Oracle | /connectors/oracle.html |
| Oracle E-Business Suite | /connectors/oracle-ebs.html |
| Oracle Fusion Cloud | /connectors/oracle-fusion-cloud.html |
| Outlook | /connectors/outlook/outlook.html |
| Outreach | /connectors/outreach.html |
| OutSystems | /connectors/outsystems.html |
| PagerDuty | /connectors/pagerduty.html |
| Percolate | /connectors/percolate.html |
| PlanGrid | /connectors/plangrid.html |
| PostgreSQL | /connectors/postgresql.html |
| Python | /connectors/python.html |
| Quickbase | /connectors/quickbase.html |
| QuickBooks Online | /connectors/quickbooks.html |
| Recipe function by Workato | /connectors/recipe-functions.html |
| RecipeOps by Workato | /connectors/recipeops.html |
| Redshift | /connectors/redshift.html |
| Replicon | /connectors/replicon.html |
| RingCentral | /connectors/ringcentral.html |
| Ruby snippets by Workato | /connectors/ruby-snippets-by-workato.html |
| Sage Intacct | /connectors/intacct.html |
| Salesforce | /connectors/salesforce.html |
| SAP Concur | /connectors/concur.html |
| SAP OData | /connectors/sap-odata.html |
| SAP RFC | /connectors/sap.html |
| SAP SuccessFactors | /connectors/successfactors/successfactors.html |
| SendGrid | /connectors/sendgrid.html |
| ServiceNow | /connectors/servicenow.html |
| SFTP | /connectors/sftp.html |
| SharePoint | /connectors/sharepoint.html |
| Shopify | /connectors/shopify.html |
| Slack | /connectors/slack.html |
| Smartsheet | /connectors/smartsheet.html |
| SMS by Workato | /connectors/sms-by-workato.html |
| Snowflake | /connectors/snowflake.html |
| Splunk | /connectors/splunk.html |
| SQL Server | /connectors/mssql/introduction.html |
| Stripe | /connectors/stripe.html |
| SurveyMonkey | /connectors/surveymonkey.html |
| Syslog | /connectors/syslog.html |
| Tango Card | /connectors/tango_card.html |
| TrackVia | /connectors/trackvia.html |
| Trello | /connectors/trello.html |
| Twilio | /connectors/twilio.html |
| Workato EDI | /connectors/workato-edi.html |
| Workbot for Microsoft Teams | /workbot-for-teams/workbot.html |
| Workbot for Slack | /workbot/workbot.html |
| Workday | /connectors/workday.html |
| Workday REST | /connectors/workday-rest.html |
| Workfront | /connectors/workfront.html |
| WordPress.com | /connectors/wordpress.html |
| Wrike | /connectors/wrike.html |
| Wufoo | /connectors/wufoo.html |
| Xero | /connectors/xero.html |
| Zendesk | /connectors/zendesk.html |
| Zoho CRM | /connectors/zoho-crm.html |
| Zoom | /connectors/zoom.html |
| ZoomInfo | /connectors/zoom-info.html |
| Zuora | /connectors/zuora.html |

</details>
