---
paths:
  - ".workatoenv"
  - "projects/**"
  - "connectors/**"
---

# Workato CLI ツール

## Platform CLI（レシピ管理）

2つのバリアントがある。インストール済みの方を使用する:

| | 本家 | フォーク (rkawaishi) |
|---|---|---|
| インストール | `pipx install workato-platform-cli` | `pipx install git+https://github.com/rkawaishi/workato-platform-cli.git` |
| 追加機能 | — | Jobs, SDK統合, OAuth Profile管理, workspace_id自動解決 |
| リポジトリ | [workato-devs/workato-platform-cli](https://github.com/workato-devs/workato-platform-cli) | [rkawaishi/workato-platform-cli](https://github.com/rkawaishi/workato-platform-cli) |

共通コマンド:
- Pull: `workato projects use "<name>" && workato pull`
- Push: `workato push`
- Init: `workato init --non-interactive --profile <profile> --project-id <id> --folder-name "projects/<name>"`

フォーク版の追加コマンド:
- Jobs: `workato jobs list` / `workato jobs get <id>`
- SDK: `workato sdk new <path>` / `workato sdk push` / `workato sdk exec` / `workato sdk generate schema`
- OAuth: `workato oauth-profiles list` / `create` / `update` / `delete`
- Connectors: `workato connectors` 管理

## Connector SDK CLI（コネクタ開発）

本家 CLI の場合:
- インストール: `gem install workato-connector-sdk`
- 新規作成: `workato new connectors/<name>`
- テスト: `workato exec connectors/<name>/connector.rb test`
- Push: `workato push connectors/<name>`

フォーク版 CLI の場合（SDK コマンド統合済み）:
- 新規作成: `workato sdk new connectors/<name>`
- テスト: `workato sdk exec connectors/<name>/connector.rb test`
- Push: `workato sdk push connectors/<name>`
- スキーマ生成: `workato sdk generate schema connectors/<name>`

## コネクタの分類

- **Pre-built**: Workato 公式の標準コネクタ（1,000+）
- **Universal**: HTTP, OpenAPI, GraphQL, SOAP — 標準にない API 用
- **Community**: ユーザー共有コネクタ
- **Custom**: Connector SDK で自作 → `connectors/` ディレクトリ
- **Custom Action**: コネクタ内の `__adhoc_http_action` で API 直接呼出し
