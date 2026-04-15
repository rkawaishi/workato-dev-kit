# Connector SDK 概要

公式: https://docs.workato.com/en/developing-connectors/sdk.html

## Custom Connector とは

Workato が標準で提供していないアプリケーションに接続するための自作コネクタ。Ruby DSL で記述し、トリガー・アクション・認証を定義する。

## 開発手段

### 1. Web エディタ（Cloud SDK）
- Workato UI 上の Tools > Connector SDK からブラウザで開発
- CodeMirror エディタ（構文ハイライト、エラー表示）
- Test code タブでインタラクティブテスト

### 2. SDK CLI（ローカル開発）
- `gem install workato-connector-sdk` でインストール
- ローカルで開発・テスト → `workato push` でアップロード
- RSpec + VCR によるユニットテスト
- Git 連携、CI/CD パイプライン対応

## SDK CLI コマンド

### SDK CLI (`gem install workato-connector-sdk`)

ローカルでのテスト・開発に使用する。Platform CLI と `workato` コマンド名が競合するため、`bundle exec` で実行する。

| コマンド | 説明 |
|---|---|
| `bundle exec workato new <PATH>` | 新規コネクタプロジェクト作成 |
| `bundle exec workato exec <PATH>` | コネクタの lambda ブロックを実行・テスト |
| `bundle exec workato edit <PATH>` | 暗号化ファイルを編集 |
| `bundle exec workato generate <SUBCOMMAND>` | テンプレートからコード生成 |

### Workato へのアップロード（API ヘルパー推奨）

コネクタの push は API ヘルパーを使う。Platform CLI のプロファイルで認証するため、gem 側の認証設定（API Client トークン）が不要。

```bash
# 新規作成
python3 scripts/workato-api.py sdk push --connector connectors/<name>/connector.rb --title "<Title>"

# 既存コネクタの更新
python3 scripts/workato-api.py sdk push --connector connectors/<name>/connector.rb --connector-id <id>
```

> **Note**: `bundle exec workato push` も引き続き使用可能だが、別途 API Client トークンの設定が必要。

## プロジェクト構造

`workato new <name>` で生成されるファイル:

```
<name>/
├── connector.rb          # メインのコネクタ定義
├── settings.yaml.enc     # 認証情報（暗号化）
├── settings.yaml         # 認証情報（平文、開発用）
├── master.key            # 暗号化キー（.gitignore 必須）
├── Gemfile               # Ruby 依存関係
├── spec/                 # テストファイル
│   ├── spec_helper.rb    # RSpec + VCR 設定
│   ├── connector_spec.rb # コネクタテスト
│   └── cassettes/        # VCR 録画（HTTP モック）
└── .rspec
```

## 前提条件

- Ruby 2.7.x / 3.0.x / 3.1.x（ローカルテスト用）
- API ヘルパーでの push は Platform CLI のプロファイル認証のみで可能（Ruby 不要）
- `bundle exec workato push` を使う場合は API クライアント（"Get details" 権限）が別途必要
