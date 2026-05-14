# Learned Patterns (kit canonical)

This file is the **kit standard staging buffer** where kit maintainers place items before classifying them.
**Users of the organization must not edit this file** (it would change the kit submodule).

## Organization-side learnings go into `org/docs/learned-patterns.md`

All knowledge learned from an organization's Recipes is written to **`org/docs/` on the workspace repository side**.
For detailed routing rules, see `@.claude/rules/org-knowledge-overlay.md`.

Organization-side destinations:
- Discoveries about Recipe JSON structure -> `org/docs/learned-patterns.md` (move to the appropriate file later)
- Logic -> `org/docs/logic/<topic>.md`
- Connector-specific field information -> `org/docs/connectors/<provider>.md`
- Platform features -> `org/docs/platform/<topic>.md`
- Deployment-related -> `org/docs/patterns/deployment-guide.md`

## Kit-side canonical destinations (for kit maintainers)

General discoveries to be folded into the kit are classified via a PR to the kit repository, as follows:
- Recipe JSON structure -> `.claude/rules/workato-recipe-format.md`
- Logic -> the appropriate file under `docs/logic/`
- Connector-specific -> `docs/connectors/<name>.md`
- Platform features -> the appropriate file under `docs/platform/`
- Deployment-related -> `docs/patterns/deployment-guide.md`
