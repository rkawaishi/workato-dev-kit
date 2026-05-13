# Glossary

Canonical English translations for terms used throughout the workato-dev-kit documentation. Any contributor adding new docs MUST follow this glossary; reviewers should flag deviations.

> Why: this kit was originally written in Japanese. During the migration to English (see `i18n/english-migration` branch), a few terms had multiple plausible translations. This file pins the canonical choice so the docs stay consistent.

## Workato terminology (preserve as-is)

| Japanese | English | Notes |
|---|---|---|
| Workato | Workato | Proper noun |
| レシピ | **Recipe** (the Workato artifact) / **recipe** (lowercase when used as a generic noun) | Capitalise on first mention |
| Workflow App | Workflow App | Official Workato wording (do NOT expand to "Workflow Application") |
| Genie | Genie | – |
| MCP サーバー | MCP server | – |
| プロジェクト | project (in code paths and prose); **Project** when referring to a Workato Project resource | – |
| (Pre-built) コネクタ | (pre-built) connector | – |
| カスタムコネクタ | custom connector | – |
| トリガー / アクション | trigger / action | – |
| データピル | datapill | One word; matches Workato official |
| Recipe Function | Recipe Function | – |
| Data Table | Data Table | – |
| Connection | Connection | – |

## Workflow / process terminology

| Japanese | English | Notes |
|---|---|---|
| 仕様駆動ワークフロー | spec-driven workflow | NOT "specification-driven" |
| ライフサイクル | lifecycle | One word |
| 責務マップ | responsibility map | NOT "duty matrix" |
| ユーザー体験 | user experience (UX in subsequent mentions) | NOT "user journey" |
| ナレッジベース | knowledge base | – |
| docs-first | docs-first | Keep the hyphen; established term |
| 業務要件 | business requirements | – |
| ベストエフォート実装 | best-effort implementation | – |
| 不可侵の 3 原則 | three inviolable principles | – |
| 学習サイクル | learning cycle | – |
| 設計書 | design document | Use only when discussing the legacy DESIGN.md |

## Tooling / framework terminology

| Japanese | English | Notes |
|---|---|---|
| エディタ | editor (covers Claude Code, Cursor, Codex CLI, Gemini CLI as a group) | NOT "IDE" |
| ワークスペース | workspace | – |
| シンボリックリンク | symlink | One word; NOT "symbolic link" |
| Deprecated (warning + 動作維持) | deprecated | Used for skills that still run with a warning |
| 廃止済み (削除) | retired | Used for things that are removed/refused outright |
| カタログ | catalog | American spelling |
| アセット | asset | – |
| フィーチャー | feature | – |
| アーティファクト | artifact | – |
| プロバイダー | provider | – |
| メタデータ | metadata | – |

## Style notes

- Use **sentence case** in headings (e.g., "Lifecycle and responsibility map", not "Lifecycle And Responsibility Map").
- Use **imperative mood** for rules and constraints ("Do not grep other projects' Recipes", not "Other projects' Recipes should not be grepped").
- Keep the original meaning of "禁止" (prohibition) as a direct **"Do not …"** instruction.
- Preserve markdown structure (`#`, `*`, `>`, table pipes) when translating; do not reformat surrounding content.
- For skills that take user input directly (`spec`, `clarify`, `plan`, `tasks`, `create-*`, `learn-*`, `design`), end the SKILL.md `description:` field with the sentence **"Japanese prompts are also supported."** so the LLM router still picks them up when the user writes in Japanese. Orchestrator/CI skills (`analyze`, `implement`, `validate-recipe`) do NOT need this hint.
- Keep each SKILL.md `description:` field under ~200 characters for router efficiency.
