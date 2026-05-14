# Workato connectors

## Scope of this list

This file is the **inventory of 316 Workato pre-built connectors** (connector name, provider key, trigger count, action count). `/sync-connectors` auto-generates and updates it from the Workato API.

The details for each connector (individual trigger/action lists, field specifications) are split into **`docs/connectors/<provider>.md`** files. `/sync-connectors` creates the skeleton (`## Triggers` / `## Actions` tables + an empty `## Field details` section) in each of those files too, but **descriptions and field details are initialized empty because they cannot be retrieved from the API**.

### Growing the documentation

Descriptions and field details are filled in incrementally through this cycle:

1. **`/learn-recipe <project>`** — extract field-usage examples from existing recipe JSON and append them to the relevant `<provider>.md` under `## Field details`.
2. **`/auto-learn <provider>`** — drive the Workato UI through Claude in Chrome, autonomously collect input/output fields for every op, and append them (Claude Code only).
3. **Manual corrections** — write knowledge gained from official docs or hands-on verification into `org/docs/connectors/<provider>.md` (the organization knowledge layer) or contribute it back to the kit via PR.

A blank "Description" column in the Triggers / Actions table therefore means **"not yet learned", not "out of spec"**. To contribute knowledge back via community PR, see [CONTRIBUTING.md](../../CONTRIBUTING.md) and the [connector_doc_update](../../.github/ISSUE_TEMPLATE/connector_doc_update.yml) issue template.

## Connector classification

### Pre-built connectors
Connectors officially provided by Workato. Setup guides, required permissions, available triggers/actions, and troubleshooting are documented.

### Universal connectors
Generic connectors for APIs or services that don't have a dedicated pre-built connector.

| Connector | Use | Documentation |
|---|---|---|
| **HTTP** | Connect to any HTTP API | https://docs.workato.com/en/developing-connectors/http-v2.html |
| **OpenAPI** | Connect to APIs described by an OpenAPI spec | https://docs.workato.com/en/connectors/openapi/ |
| **GraphQL** | Run queries / mutations against a GraphQL API | https://docs.workato.com/en/connectors/graphql.html |
| **SOAP** | Connect to web services described by WSDL | https://docs.workato.com/en/connectors/soap.html |

### Community connectors
User-developed and -shared connectors. Searchable in the Community Library.

### Custom connectors
Connectors built with the Connector SDK. Initially private-scoped; can be shared or published to the marketplace later.
- SDK docs: https://docs.workato.com/en/developing-connectors/sdk.html

### Custom Action (`__adhoc_http_action`)
When a connector has no suitable action, call the API directly while still using the connector's authentication.
- Details: see the Custom Action section in `@.claude/rules/workato-recipe-format.md`.

## Full pre-built connector list (316)

Fetched from the API (`workato connectors list --platform`). Refreshed by `/sync-connectors`.

| Connector | Provider | Triggers | Actions |
|---|---|---|---|
| 2Checkout | `two_checkout` | 3 | 0 |
| 4me | `connector_4me` | 1 | 4 |
| ADP Workforce Now | `adp7` | 2 | 2 |
| AI by Workato | `open_ai_utility` | 0 | 8 |
| AMcards | `amcards` | 0 | 1 |
| API platform by Workato | `workato_api_platform` | 1 | 1 |
| API proxy by Workato | `workato_api_proxy` | 1 | 2 |
| AWS Lambda | `aws_lambda` | 1 | 3 |
| Active Directory | `active_directory` | 3 | 15 |
| Adobe Experience Manager | `adobe_experience_manager` | 2 | 10 |
| AirREGI | `air_regi` | 2 | 0 |
| Airbrake | `airbrake` | 0 | 1 |
| Airtable | `airtable` | 2 | 10 |
| Amazon Cognito | `aws_cognito` | 0 | 3 |
| Amazon Lex | `amazon_lex_nlu` | 0 | 0 |
| Amazon S3 | `amazon_s3` | 4 | 10 |
| Amazon S3 secondary | `amazon_s3_secondary` | 4 | 10 |
| Amazon SES | `amazon_ses` | 0 | 8 |
| Amazon SNS | `aws_sns` | 1 | 1 |
| Amazon SQS | `aws_sqs` | 2 | 5 |
| Anaplan | `anaplan` | 0 | 8 |
| Apache Kafka | `kafka` | 4 | 2 |
| Apttus | `apttus` | 3 | 5 |
| Apttus Intelligent Cloud | `apttus_intelligent_cloud` | 2 | 3 |
| Ariba ⚠️ | `ariba` | 2 | 1 |
| Asana | `asana` | 3 | 17 |
| AscentERP | `ascent_erp` | 3 | 5 |
| Azure Blob Storage | `azure_blob_storage` | 2 | 10 |
| Azure Blob Storage secondary | `azure_blob_storage_secondary` | 2 | 10 |
| Azure Key Vault | `azure_key_vault` | 0 | 0 |
| Azure Monitor | `azure_monitor` | 0 | 2 |
| Azure OpenAI | `azure_open_ai` | 0 | 12 |
| BILL | `bill` | 4 | 15 |
| BIM 360 | `bim360` | 5 | 24 |
| BambooHR | `bamboohr` | 5 | 14 |
| Basecamp 2 | `basecamp` | 9 | 9 |
| Bigtincan | `bigtincan` | 2 | 12 |
| Bitbucket | `bitbucket` | 3 | 8 |
| Box | `box` | 10 | 28 |
| BrickFTP | `brick_ftp` | 1 | 0 |
| Bynder | `bynder` | 2 | 13 |
| CSV tools by Workato | `csv_parser` | 0 | 2 |
| Callable recipes by Workato | `workato_service` | 1 | 4 |
| Capsule CRM ⚠️ | `capsulecrm` | 4 | 8 |
| Celonis | `celonis` | 1 | 0 |
| Charts by Workato ⚠️ | `graphs_and_charts` | 0 | 2 |
| Chatter | `salesforce_chatter` | 0 | 1 |
| Cisco Webex Teams | `cisco_spark` | 2 | 10 |
| Citrix Podio | `podio` | 4 | 4 |
| Clearbit | `clearbit` | 0 | 2 |
| Cloud Watch | `cloud_watch` | 1 | 3 |
| Coda ⚠️ | `coda` | 0 | 7 |
| Codeship | `codeship` | 0 | 2 |
| Confluence | `confluence` | 0 | 12 |
| Confluence secondary | `confluence_secondary` | 0 | 12 |
| Confluent Cloud | `confluent_cloud` | 2 | 2 |
| Cornerstone OnDemand | `cornerstone_ondemand` | 0 | 0 |
| Coupa | `coupa` | 1 | 13 |
| Custom LLM For Workato Genie | `byollm` | 0 | 0 |
| Cyberark Conjur | `cyberark_conjur` | 0 | 0 |
| Databricks | `databricks` | 3 | 8 |
| Decision Models by Workato | `workato_decision_engine` | 0 | 1 |
| Deputy | `deputy` | 3 | 13 |
| DocuSign | `docusign` | 4 | 5 |
| DocuSign secondary | `docusign_secondary` | 4 | 5 |
| Dropbox | `dropbox` | 6 | 16 |
| EDI tools by Workato | `edi_parser` | 0 | 4 |
| Egnyte | `egnyte` | 1 | 9 |
| Ellucian Banner | `ellucian_banner` | 0 | 0 |
| Eloqua | `eloqua` | 2 | 6 |
| Email by Workato | `email` | 0 | 1 |
| Eventbrite | `event_brite` | 7 | 5 |
| Excel | `excel` | 0 | 11 |
| Expensify | `expensify` | 1 | 7 |
| FTP/FTPS | `ftps` | 2 | 7 |
| FTP/FTPS secondary | `ftps_secondary` | 2 | 7 |
| Facebook | `facebook` | 0 | 6 |
| Facebook Lead Ads | `facebook_lead_ads` | 1 | 1 |
| Fairsail | `fairsail` | 3 | 5 |
| Feedly | `feedly` | 1 | 0 |
| File tools by Workato | `file_connector` | 0 | 4 |
| FinancialForce | `financialforce` | 3 | 5 |
| Force.com | `forcecom` | 3 | 5 |
| Formstack Documents | `webmerge` | 0 | 2 |
| FreshBooks | `fresh_books` | 4 | 11 |
| Freshdesk ⚠️ | `fresh_desk` | 6 | 19 |
| FullContact | `fullcontact` | 0 | 2 |
| Funraise | `funraise` | 1 | 0 |
| GitHub | `github` | 7 | 7 |
| Gmail | `gmail` | 1 | 3 |
| Gong.io | `gong` | 1 | 13 |
| Google BigQuery | `google_big_query` | 4 | 14 |
| Google Calendar | `google_calendar` | 4 | 14 |
| Google Cloud Storage | `google_cloud_storage` | 0 | 12 |
| Google Contacts | `google_contacts` | 2 | 3 |
| Google Dialogflow | `api_ai_nlu` | 0 | 0 |
| Google Docs | `google_docs` | 0 | 3 |
| Google Drive | `google_drive` | 4 | 15 |
| Google People | `google_people` | 2 | 6 |
| Google Secret Manager | `google_secret_manager` | 0 | 0 |
| Google Sheets | `google_sheets` | 9 | 12 |
| Google Speech to Text | `google_speech_to_text` | 0 | 2 |
| Google Text to Speech | `google_text_to_speech` | 0 | 2 |
| Google Translate | `google_translate` | 0 | 2 |
| Google Vision | `google_vision` | 0 | 2 |
| Google Workspace | `google_workspace` | 3 | 9 |
| Goombal | `goombal` | 1 | 2 |
| GotoWebinar | `goto_webinar` | 1 | 3 |
| Greenhouse | `greenhouse` | 5 | 16 |
| HTTP | `rest` | 2 | 3 |
| HTTP (OAuth2) ⚠️ | `rest_oauth` | 2 | 3 |
| HTTP secondary | `rest_secondary` | 2 | 3 |
| HashiCorp Vault | `hashi_corp_vault` | 0 | 0 |
| HipChat | `hipchat` | 0 | 7 |
| Hive | `hive` | 1 | 7 |
| HubSpot | `hubspot` | 14 | 39 |
| IBM Db2 | `db2` | 0 | 7 |
| IDP by Workato | `workato_idp` | 0 | 2 |
| Infusionsoft | `infusionsoft` | 16 | 37 |
| Insightly | `insightly` | 5 | 12 |
| Instagram | `instagram` | 3 | 0 |
| Intercom | `intercom` | 7 | 12 |
| JDBC | `jdbc` | 5 | 8 |
| JDBC secondary | `jdbc_secondary` | 5 | 8 |
| JIRA Service Desk | `jira_service_desk` | 1 | 9 |
| JMS tools by Workato | `jms` | 2 | 3 |
| JSON Transformations by Workato | `workato_json_transformations` | 0 | 1 |
| JSON tools by Workato | `json_parser` | 0 | 2 |
| JWT tools by Workato | `jwt` | 0 | 2 |
| JavaScript snippets by Workato | `js_eval` | 0 | 1 |
| Jenkins | `jenkins` | 0 | 2 |
| Jira | `jira` | 14 | 18 |
| Jira secondary | `jira_secondary` | 14 | 18 |
| JobScience | `jobscience` | 3 | 5 |
| Jobvite | `jobvite` | 1 | 0 |
| JumpCloud | `jump_cloud` | 1 | 17 |
| Kenandy | `kenandy` | 3 | 5 |
| Kizen | `kizen` | 1 | 3 |
| Knack | `knack` | 1 | 4 |
| Librato | `librato` | 1 | 4 |
| Lightspeed Commerce | `vend` | 8 | 12 |
| LinkedIn | `linkedin` | 1 | 5 |
| Lists by Workato ⚠️ | `workato_list` | 0 | 2 |
| Logger by Workato | `logger` | 0 | 1 |
| Lookup tables by Workato | `lookup_table` | 0 | 9 |
| MCP (Model Context Protocol) | `mcp` | 0 | 0 |
| Magento 2 | `magento` | 6 | 8 |
| MailChimp | `mailchimp` | 6 | 13 |
| Mapper by Workato | `workato_mapper` | 0 | 1 |
| Marketo | `marketo` | 8 | 48 |
| Marketo secondary | `marketo_secondary` | 8 | 48 |
| Maxio | `chargify` | 3 | 8 |
| Message template by Workato | `workato_template` | 0 | 1 |
| Microsoft Dynamics 365 | `microsoft_dynamics_crm` | 13 | 9 |
| Microsoft Sharepoint | `microsoft_sharepoint` | 6 | 24 |
| Miro | `miro_board` | 0 | 4 |
| Mixpanel | `mixpanel` | 0 | 5 |
| MongoDB Atlas | `mongo` | 0 | 5 |
| MySQL | `mysql` | 5 | 13 |
| MySQL secondary | `mysql_secondary` | 5 | 13 |
| Namely | `namely` | 4 | 6 |
| Nasuni Management Console | `nasuni_management` | 1 | 25 |
| NationBuilder | `nationbuilder` | 1 | 0 |
| NetSuite REST | `netsuite_rest` | 0 | 14 |
| NetSuite SOAP | `netsuite` | 24 | 44 |
| NetSuite SOAP secondary | `netsuite_secondary` | 24 | 44 |
| NetSuite2 | `netsuite2` | 0 | 0 |
| New Relic | `new_relic` | 0 | 2 |
| Nimble CRM | `nimblecrm` | 1 | 1 |
| Okta | `okta` | 3 | 22 |
| Okta secondary | `okta_secondary` | 3 | 22 |
| On-prem command-line scripts | `onprem_command_line_scripts` | 0 | 1 |
| On-prem files | `onprem_files` | 5 | 16 |
| On-prem files secondary | `onprem_files_secondary` | 5 | 16 |
| OneDrive | `onedrive` | 5 | 13 |
| OpenAI | `open_ai` | 0 | 17 |
| Oracle | `oracle` | 4 | 17 |
| Oracle E-Business Suite | `oracle_ebs` | 2 | 1 |
| Oracle Fusion Cloud | `oracle_fusion_cloud` | 7 | 28 |
| Oracle secondary | `oracle_secondary` | 4 | 17 |
| OutSystems | `out_systems` | 4 | 6 |
| Outlook | `outlook` | 8 | 19 |
| Outreach | `outreach` | 3 | 8 |
| PDF tools by Workato | `pdf_tools` | 0 | 1 |
| PGP tools by Workato | `pgp` | 0 | 5 |
| Pagerduty | `pagerduty` | 2 | 7 |
| ParseHub | `parsehub` | 0 | 3 |
| People Task by Workato ⚠️ | `workflow` | 0 | 1 |
| Percolate | `percolate` | 3 | 11 |
| Pingdom | `pingdom` | 1 | 1 |
| Pipedrive | `pipedrive` | 4 | 10 |
| PipelineOps by Workato | `data_pipelines` | 1 | 0 |
| Pivotal Tracker | `pivotal_tracker` | 1 | 10 |
| PlanGrid | `plan_grid` | 2 | 8 |
| PostgreSQL | `postgresql` | 4 | 11 |
| PostgreSQL secondary | `postgresql_secondary` | 4 | 11 |
| Postman | `postman` | 0 | 0 |
| Prontoforms | `prontoforms` | 1 | 1 |
| Propel | `propel` | 3 | 5 |
| Python snippets by Workato | `py_eval` | 0 | 1 |
| QuickBooks Online | `quickbooks` | 29 | 107 |
| Quickbase | `quickbase` | 9 | 11 |
| Quickbase secondary | `quickbase_secondary` | 9 | 11 |
| Quip | `quip` | 1 | 4 |
| RPA by Workato | `workato_rpa` | 0 | 6 |
| Raiser's Edge NXT | `raisers_edge` | 15 | 37 |
| Recipe function by Workato | `workato_recipe_function` | 1 | 4 |
| RecipeOps by Workato | `workato_app` | 21 | 9 |
| Redshift | `redshift` | 6 | 12 |
| Redshift secondary | `redshift_secondary` | 6 | 12 |
| RegOnline® by Lanyon | `active_reg_online` | 3 | 6 |
| Replicon | `replicon` | 7 | 49 |
| Revel Systems | `revel_systems` | 6 | 7 |
| RingCentral | `ringcentral` | 6 | 4 |
| Rollbar | `rollbar` | 2 | 2 |
| RowShare | `row_share` | 1 | 7 |
| Ruby snippets by Workato | `workato_custom_code` | 0 | 1 |
| SAP Concur | `concur` | 9 | 33 |
| SAP OData | `sap_s4_hana_cloud` | 2 | 9 |
| SAP RFC | `sap` | 2 | 8 |
| SAP RFC secondary | `sap_secondary` | 2 | 8 |
| SAP SuccessFactors OData | `success_factors` | 2 | 10 |
| SFTP | `sftp` | 2 | 12 |
| SFTP secondary | `sftp_secondary` | 2 | 12 |
| SMB | `smb` | 1 | 6 |
| SMS by Workato | `sms_secondary` | 0 | 1 |
| SMS by Workato (deprecated) ⚠️ | `sms` | 0 | 1 |
| SOAP tools by Workato ⚠️ | `soap` | 0 | 2 |
| SQL Collection by Workato | `workato_smart_list` | 0 | 5 |
| SQL Server | `mssql` | 7 | 19 |
| SQL Server secondary | `mssql_secondary` | 7 | 19 |
| SQL Transformations by Workato | `workato_transformations` | 0 | 2 |
| Sage Intacct | `intacct` | 19 | 51 |
| Sage Live | `sagelive` | 3 | 5 |
| Salesforce | `salesforce` | 36 | 60 |
| Salesforce CPQ | `steelbrick` | 3 | 5 |
| Salesforce Marketing Cloud | `salesforce_marketing_cloud` | 1 | 10 |
| Salesforce secondary | `salesforce_secondary` | 36 | 60 |
| SalesforceIQ | `relateiq` | 0 | 2 |
| Scheduler by Workato | `clock` | 3 | 4 |
| Segment ⚠️ | `segment` | 0 | 3 |
| SendGrid | `sendgrid` | 0 | 5 |
| ServiceM8 | `servicem8` | 7 | 19 |
| ServiceMax | `service_max` | 3 | 5 |
| ServiceNow | `service_now` | 14 | 29 |
| ServiceNow secondary | `service_now_secondary` | 14 | 29 |
| Shopify | `shopify` | 17 | 56 |
| Showpad | `showpad` | 0 | 5 |
| Slack | `slack` | 2 | 17 |
| Slack secondary | `slack_secondary` | 2 | 17 |
| Smartsheet | `smartsheet` | 3 | 5 |
| Snowflake | `snowflake` | 5 | 15 |
| Snowflake secondary | `snowflake_secondary` | 5 | 15 |
| Splunk ⚠️ | `splunk` | 2 | 3 |
| Stripe | `stripe` | 4 | 12 |
| SurveyMonkey | `surveymonkey` | 2 | 3 |
| Syslog | `syslog` | 0 | 1 |
| TSheets | `tsheets` | 4 | 9 |
| Tango Card | `tango_card` | 0 | 5 |
| TaskRay | `taskray` | 3 | 5 |
| TrackVia | `trackvia` | 3 | 10 |
| Tradeshift | `tradeshift` | 2 | 11 |
| Trello | `trello` | 2 | 10 |
| Twilio | `twilio` | 1 | 5 |
| Unbounce | `unbounce` | 1 | 0 |
| Utilities ⚠️ | `utility` | 0 | 10 |
| Variables by Workato | `workato_variable` | 0 | 7 |
| Veeva CRM | `veeva` | 3 | 5 |
| Vlocity | `vlocity` | 3 | 5 |
| Watson Tone Analyzer | `watson_tone_analyzer` | 0 | 1 |
| Webhooks | `workato_webhooks` | 1 | 0 |
| WooCommerce | `woocommerce` | 5 | 4 |
| WordPress.com | `word_press` | 2 | 5 |
| Workato Data Tables | `workato_db_table` | 4 | 10 |
| Workato EDI | `workato_edi` | 1 | 9 |
| Workato Event Streams | `workato_pub_sub` | 2 | 2 |
| Workato FileStorage | `workato_files` | 3 | 10 |
| Workato Genie | `workato_genie` | 1 | 7 |
| Workato Genie MS Teams | `workato_genie_ms_teams` | 0 | 0 |
| Workato Genie Slack | `workato_genie_slack` | 0 | 0 |
| Workbot  for  Slack | `slack_bot` | 7 | 14 |
| Workbot for Microsoft Teams | `teams_bot` | 5 | 11 |
| Workbot for Microsoft Teams Old ⚠️ | `skype_bot` | 1 | 2 |
| Workbot for Workplace | `workplace_bot` | 1 | 6 |
| Workday | `workday` | 4 | 10 |
| Workday REST | `workday_rest` | 1 | 23 |
| Workday Web Services | `workday_oauth` | 2 | 4 |
| Workflow apps by Workato | `workato_workflow_task` | 5 | 16 |
| Workfront | `workfront` | 3 | 6 |
| Workfront secondary | `workfront_secondary` | 3 | 6 |
| Wrike | `wrike` | 12 | 44 |
| Wrike secondary | `wrike_secondary` | 12 | 44 |
| Wufoo | `wufoo` | 1 | 0 |
| X | `twitter` | 1 | 4 |
| XML tools by Workato | `xml_parser` | 0 | 5 |
| Xactly | `xactly` | 0 | 2 |
| Xero | `xero` | 10 | 50 |
| Xero Practice Manager | `xero_practice_manager` | 0 | 4 |
| YAML tools by Workato | `yaml_parser` | 0 | 1 |
| Zendesk | `zendesk` | 12 | 33 |
| Zendesk Conversations | `zendesk_conversations` | 0 | 1 |
| Zendesk Demo | `zendesk_demo` | 0 | 6 |
| Zendesk Sunshine ⚠️ | `zendesk_sunshine` | 12 | 33 |
| Zendesk secondary | `zendesk_secondary` | 12 | 33 |
| Zenefits | `zenefits` | 2 | 3 |
| Zoho CRM | `zohocrm` | 19 | 45 |
| Zoho Invoice | `zoho_invoice` | 2 | 4 |
| ZoneBilling for NetSuite ⚠️ | `zonebilling` | 0 | 14 |
| Zoom | `zoom` | 1 | 20 |
| ZoomInfo | `zoom_info` | 1 | 17 |
| Zuora | `zuora` | 2 | 12 |
| Zuora for Salesforce | `zuora_forcecom` | 3 | 5 |
| cXML | `cxml` | 1 | 1 |
| docparser | `docparser` | 1 | 2 |
| eTapestry | `etapestry` | 2 | 5 |
| everydayhero | `everydayhero` | 2 | 0 |
