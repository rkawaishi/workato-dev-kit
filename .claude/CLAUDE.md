# Workato Dev Kit

Workato (エンタープライズ iPaaS) の自動化開発を Claude Code / Cursor で行うためのツールキット。

## プロジェクト構造

```
<workspace-root>/
  <project-name>/           # workato pull で取得したプロジェクト
    *.recipe.json            # レシピ（ワークフロー定義）
    *.connection.json        # コネクション（接続情報）
    *.agentic_genie.json     # Genie（AIエージェント定義）
    *.agentic_skill.json     # Genieスキル定義
    .workatoenv              # プロジェクト設定（project_id等）
  docs/
    logic/                   # ロジックパターン（公式ドキュメントベース）
      triggers.md            # トリガーの種類（Polling/Real-time/Scheduled/CDC）、条件、Since
      if-conditions.md       # IF/ELSE IF/ELSE + 14条件演算子
      loops.md               # repeat-while, repeat-for-each
      error-handling.md      # Monitor/Error ブロック、Stop Job、Recipe Functions
      data-pills.md          # データピル、データマッピング、型変換、システムデータピル
      formulas.md            # フォーミュラモード、文字列/数値/日付/リスト操作
      file-handling.md       # ファイル処理（テキスト/バイナリ、ストリーミング）
      data-tables.md         # Data Tables（内蔵データストア、4トリガー+10アクション）
    connectors/              # コネクタナレッジ
      _index.md              # 全コネクタ一覧 + 分類（Pre-built/Universal/Community/Custom）
      slack.md               # Slack + Workbot for Slack
      jira.md                # Jira トリガー/アクション一覧
      salesforce.md          # Salesforce
    learned-patterns.md      # 公式に載っていない独自知見（UI フィードバックから学習）
  .claude/
    rules/                   # JSON フォーマットのリファレンス
    skills/                  # 開発用スキル
```

## ナレッジの参照優先順位

1. `@docs/connectors/` — 使用するコネクタの公式情報（トリガー/アクション一覧）
2. `@docs/logic/` — ロジックステップの組み方（if, loop, error handling）
3. `@docs/learned-patterns.md` — 公式に載っていない JSON 構造の独自知見
4. `@.claude/rules/` — レシピ/Genie JSON のフォーマット定義

## Workato Platform CLI

- インストール済み: `workato` (pipx)
- プロファイル: `workato profiles list` で確認
- プロジェクト一覧: `workato projects list --source remote`
- Pull: `workato projects use "<name>" && workato pull`
- Push: `workato push`
- Init: `workato init --non-interactive --profile <profile> --project-id <id> --folder-name "<name>"`

## コネクタの分類

- **Pre-built**: Workato 公式の標準コネクタ（1,000+）
- **Universal**: HTTP, OpenAPI, GraphQL, SOAP — 標準にない API 用
- **Community**: ユーザー共有コネクタ
- **Custom**: Connector SDK で自作
- **Custom Action**: コネクタ内の `__adhoc_http_action` で API 直接呼出し

## 開発ルール

- レシピ JSON を編集する際は `@.claude/rules/workato-recipe-format.md` を参照
- Genie/Skill を作成する際は `@.claude/rules/workato-agentic-format.md` を参照
- コネクタの詳細は `@docs/connectors/` を参照。未作成のコネクタは公式ドキュメントを WebFetch で取得
- 新しい独自知見を発見したら `docs/learned-patterns.md` に追記
- `*.connection.json` に認証情報は含まれない（名前とプロバイダーのみ）
- `.workatoenv` はコミットしない（.gitignore 済み）
