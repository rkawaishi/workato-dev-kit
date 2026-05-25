---
name: validate-recipe
description: Validate the structure of Workato recipe / Genie JSON and report issues. Takes a file path or a project name as argument.
---

# $validate-recipe

Validates the structure of Workato JSON files.

## Usage

- `$validate-recipe <file-path>` — validate a specific file
- `$validate-recipe <project-name>` — validate every file in a project
- `$validate-recipe` — no argument: validate every project

## Checks

### recipe.json

- [ ] Required top-level fields: `name`, `version`, `code`, `config`
- [ ] `code.keyword` is `"trigger"` (number: 0)
- [ ] Every step has `number`, `provider`, `name`, `keyword`, `uuid`
- [ ] `number` values are sequential
- [ ] `uuid` is a valid UUID v4
- [ ] `uuid` is 36 characters or fewer (push rejects longer values; applies to step `uuid`, `filter.conditions[].uuid`, and `input.conditions[].uuid`)
- [ ] Steps inside `block` recursively follow the same structure
- [ ] Every `provider` in `config` is actually used by the recipe
- [ ] Datapill references (`_dp`) point at a real step (`provider` + `line`)
- [ ] If `filter` is present, both `conditions` (array) and `operand` exist

### agentic_genie.json

- [ ] Required fields: `name`, `description`, `instructions`, `ai_provider`, `references`
- [ ] Each `references` entry is `type: "agentic_skill"` and its `zip_name` points to a real file
- [ ] `instructions` is not empty

### agentic_skill.json

- [ ] Required fields: `name`, `trigger_description`, `references`
- [ ] `references.recipe_id` points to a real `.recipe.json`
- [ ] The referenced recipe uses the `workato_genie` / `start_workflow` trigger

### connection.json

- [ ] Required fields: `name`, `provider`

## Output format

```
✅ file.recipe.json — OK
⚠️  file2.recipe.json — 2 warnings
  - W001: Step 3 is missing its uuid
  - W002: config contains unused provider "slack"
  - E002: Step 5 uuid exceeds 36 characters (push will fail)
❌ file3.recipe.json — 1 error
  - E001: code.keyword is not "trigger"
```

Severity: ❌ Error (likely to fail on push) > ⚠️ Warning (works but discouraged) > ℹ️ Info (informational).
