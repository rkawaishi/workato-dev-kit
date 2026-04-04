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
    known-patterns.md        # レシピから学んだパターン知識（自動更新）
  .claude/
    rules/                   # JSON フォーマットのリファレンス
    skills/                  # 開発用スキル
```

## Workato Platform CLI

- インストール済み: `workato` (pipx)
- プロファイル: `workato profiles list` で確認
- プロジェクト一覧: `workato projects list --source remote`
- Pull: `workato projects use "<name>" && workato pull`
- Push: `workato push`
- Init: `workato init --non-interactive --profile <profile> --project-id <id> --folder-name "<name>"`

## 開発ルール

- レシピ JSON を編集する際は `@.claude/rules/workato-recipe-format.md` を参照
- Genie/Skill を作成する際は `@.claude/rules/workato-agentic-format.md` を参照
- 新しいパターンを発見したら `docs/known-patterns.md` に追記
- `*.connection.json` に認証情報は含まれない（名前とプロバイダーのみ）
- `.workatoenv` はコミットしない（.gitignore 済み）
