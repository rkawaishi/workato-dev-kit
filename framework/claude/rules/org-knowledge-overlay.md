# Org Knowledge Overlay

A convention for accumulating organization-specific knowledge separately from the kit's knowledge base (`docs/`).
This guarantees that updating the kit does not lose or overwrite the organization's learning.

## Layout

```
<workspace-root>/
├── docs/                       ← symlink to kit/docs/ (read-only)
│   ├── connectors/<name>.md
│   ├── logic/<topic>.md
│   ├── platform/<topic>.md
│   ├── patterns/<...>
│   └── learned-patterns.md
└── org/                        ← organization knowledge. The kit never touches this.
    └── docs/                   ← mirrors the docs/ tree
        ├── connectors/<name>.md
        ├── logic/<topic>.md
        ├── platform/<topic>.md
        ├── patterns/<...>
        └── learned-patterns.md
```

`org/` is managed in the workspace repository (outside the kit submodule).
You may create directories under `org/docs/` on demand; you do not need to pre-create empty ones.

## Responsibilities

| Type of knowledge | Where it lives | Skill that writes it |
|---|---|---|
| Workato official spec and API info for every connector | `docs/` (kit) | `/sync-connectors`, `/auto-learn` |
| Field info and operational know-how for what the org actually uses | `org/docs/` | `/learn-recipe`, `/learn-pattern` |
| Corrections or addenda to kit docs | `org/docs/<same-relative-path>` | Edited manually by the user |
| Org-specific connectors, logic, patterns | `org/docs/<...>` | Edited manually by the user |

**Do not edit the kit's `docs/` directly** — that would commit into the kit submodule.
If you find an error, write a correction at `org/docs/<same-relative-path>`.
If you later want to upstream it into the kit, open a separate PR (out of scope here).

## Read convention

When a skill or recipe-creation process references `@docs/<path>`, it must also check the matching `@org/docs/<path>`:

1. Read `@docs/<path>`.
2. If `@org/docs/<path>` exists, read it as well.
3. When the two conflict, **the org version wins** (org overrides kit defaults).
4. Non-overlapping information from each is additive.

Examples:
- Referencing `@docs/connectors/clearbit.md` → also check `@org/docs/connectors/clearbit.md`.
- Referencing `@docs/logic/data-pills.md` → also check `@org/docs/logic/data-pills.md`.
- For org-only resources like `@org/docs/connectors/<internal>.md` (no kit equivalent), read just the org file.

## Write convention

### Learning skills (`/learn-recipe` and friends)

All knowledge obtained from the org's own recipes / projects goes to `org/docs/<relative-path>`.

| Type of finding | Destination |
|---|---|
| Connector field info (input/output) | `org/docs/connectors/<provider>.md` |
| New provider / action discoveries | `org/docs/connectors/<provider>.md` |
| Workato-internal providers | `org/docs/platform/<topic>.md` |
| Logic step specifics | `org/docs/logic/<topic>.md` |
| Datapill patterns | `org/docs/logic/data-pills.md` |
| Deployment findings | `org/docs/patterns/deployment-guide.md` |
| Recipe construction patterns (`/learn-pattern`) | `org/docs/patterns/recipe-patterns/<name>.md` |
| Unclassifiable findings | `org/docs/learned-patterns.md` |

**Legacy**: an older convention used `projects/docs/patterns/` for org-domain patterns.
The read side still consults `projects/docs/patterns/` when it exists, but **all new writes go to `org/docs/patterns/recipe-patterns/`**.
Distinguish "generic" vs "org-domain" within the pattern body (e.g. a "Scope" section), not by path.

Before writing, read the matching `docs/<same-relative-path>` and skip anything the kit already documents. Only write **differences, corrections, and org-specific additions** to `org/docs/`.

### Sync skills (`/sync-connectors`, `/auto-learn`)

These write information obtained from Workato official sources into the kit canonical `docs/`. They continue to target `kit/docs/connectors/<name>.md` (commits inside the kit submodule). They do not touch `org/docs/connectors/<name>.md`.

## Git management

Changes under `org/docs/` are committed in the workspace repository:

```bash
cd <workspace-root>
git add org/docs/
git commit -m "docs(org): learn from <project-name> recipes"
```

Do not commit to the kit submodule (`kit/`).

## Directory initialization

`org/docs/` doesn't exist initially. Skills like `/learn-recipe` create it on first write:

```bash
mkdir -p org/docs/connectors org/docs/logic org/docs/platform org/docs/patterns
```

The user does not need to pre-create these — skills will create them on demand when calling `Write`.
