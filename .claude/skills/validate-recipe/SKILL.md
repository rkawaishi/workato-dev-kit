---
description: Workato レシピ/Genie JSON の構造を検証し、問題を報告する。引数にファイルパスまたはプロジェクト名を指定。
allowed-tools: Read, Glob, Grep, Bash
---

# /validate-recipe

Workato JSON ファイルの構造を検証するスキル。

## 使い方

- `/validate-recipe <file-path>` — 特定ファイルを検証
- `/validate-recipe <project-name>` — プロジェクト内の全ファイルを検証
- `/validate-recipe` — 引数なしで全プロジェクトを検証

## 検証項目

### recipe.json

- [ ] トップレベル必須フィールド: `name`, `version`, `code`, `config`
- [ ] `code.keyword` が `"trigger"` であること（number: 0）
- [ ] 全ステップに `number`, `provider`, `name`, `keyword`, `uuid` があること
- [ ] `number` が連番であること
- [ ] `uuid` が有効な UUID v4 形式であること
- [ ] `block` 内のステップが再帰的に正しい構造であること
- [ ] `config` 内の全 `provider` がレシピ内で使用されていること
- [ ] datapill 参照 (`_dp`) の `provider` と `line` が実在するステップを指していること
- [ ] `filter` がある場合、`conditions` 配列と `operand` が存在すること

### agentic_genie.json

- [ ] 必須フィールド: `name`, `description`, `instructions`, `ai_provider`, `references`
- [ ] `references` の各エントリが `type: "agentic_skill"` で `zip_name` が実在するファイルを指していること
- [ ] `instructions` が空でないこと

### agentic_skill.json

- [ ] 必須フィールド: `name`, `trigger_description`, `references`
- [ ] `references.recipe_id` が実在する `.recipe.json` を指していること
- [ ] 参照先レシピが `workato_genie` / `start_workflow` トリガーを使用していること

### connection.json

- [ ] 必須フィールド: `name`, `provider`

## 出力形式

```
✅ file.recipe.json — OK
⚠️  file2.recipe.json — 2 warnings
  - W001: Step 3 の uuid が未設定
  - W002: config に未使用の provider "slack" あり
❌ file3.recipe.json — 1 error
  - E001: code.keyword が "trigger" ではない
```

重要度: ❌ Error（push 時に失敗する可能性）> ⚠️ Warning（動作はするが推奨されない）> ℹ️ Info（参考情報）
