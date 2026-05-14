# Shared asset management guide

Workspace structure, naming conventions, and how to design and operate shared assets. In both Claude Code and Cursor, the `/catalog` skill generates and references the catalog.

## Workspace structure

### Environment separation

| Environment | Purpose |
|---|---|
| Dev | Development and experimentation |
| Test | Testing and validation |
| Prod | Production operations |

Separate workspaces per environment and unify authentication with SSO.

### Project hierarchy

Projects inside a workspace are organized with three levels of sharing scope:

```
Workspace/
├── Globally Shared Assets/           # Shared across all teams
│   ├── Common - Connections/         # Common connections (Slack, Email, etc.)
│   ├── Common - Functions/           # Common Recipe Functions
│   └── Error Handler/                # Shared error handling
│
├── <Team> Shared Assets/             # Shared within a team
│   ├── <Team> - Connections/
│   ├── <Team> - Common Functions/
│   └── <Team> - <App Name>/         # The team's app
│
└── <Project>/                        # Project-specific
    ├── Connections/
    ├── Recipes/
    └── ...
```

| Level | Scope | Contents |
|---|---|---|
| **Globally Shared** | All teams, all projects | Common connections, error handlers, generic Functions |
| **Team Shared** | All projects within a team | Team-specific connections and business logic |
| **Project** | A single project | Recipes specific to that project |

## Naming conventions

### Project and asset naming

```
<Project> <AssetCode> <Sequence> | <Description>
```

| Asset code | Target |
|---|---|
| `REC` | Recipe |
| `CON` | Connection |
| `FNC` | Recipe Function |
| `WFA` | Workflow App |
| `GNI` | Genie |
| `MCP` | MCP server |
| `SKL` | Agentic Skill |

**Examples:**
- `Sales Lead Enrichment REC 001 | Enrich new Salesforce lead`
- `Common FNC 001 | Get line manager from AD`

### Connection naming

```
<Environment/Context> | <Provider> [- <Purpose>]
```

**Examples:**
- `Shared | Slack`
- `Shared | Jira - Engineering`
- `Sales | Salesforce - Production`

## Designing shared assets

### When to share

| Condition | Decision |
|---|---|
| Used by three or more projects | Share it |
| Used by two or more projects within a team | Share within the team |
| Used by only one project | Do not share |
| Authentication scope differs | Use separate Connections |

### Designing Recipe Functions

Shared Recipe Functions follow the `fnc_<verb>_<noun>` naming convention:

```
fnc_get_line_manager       # Fetch line manager info
fnc_send_notification      # Send a notification
fnc_validate_input         # Validate input
```

**Design guidance:**
- Clearly define the input/output schema in `parameter_schema_json`
- Handle errors internally so they are fully contained
- Minimize side effects (make it idempotent if possible)

### Deciding whether to share a Connection

| Aspect | Share | Do not share |
|---|---|---|
| Authentication scope | Permissions common across all teams | Project-specific permissions |
| Environment | Same across all environments | Differs by environment |
| Risk | Outage impact is limited | Outage impact would be broad |

## Operating the catalog

### Generating the catalog with `/catalog`

```
/catalog
```

Outputs the following into `projects/CATALOG.md`:

- All Connections (name, provider)
- All Recipe Functions (with input/output schemas)
- All Workflow Apps
- All MCP servers

### Scope control

Configure each project's scope in `projects/CATALOG_CONFIG.yaml`:

```yaml
scopes:
  "Globally Shared Assets": global
  "Sales - Common Functions": "team:sales"
  "My Private Project": private
```

| Scope | Listed in catalog | Referenceable from other projects |
|---|---|---|
| `global` | Yes | All projects |
| `team:<name>` | Yes | Projects within the same team |
| `private` | No | Not allowed |

### Using the catalog

- `/create-recipe` references the catalog at step 2 and proposes reusing existing Connections and Recipe Functions
- `/plan` lists candidate shared assets from the catalog under `## Reused Assets` in `plan.md` during architecture design
- Before starting a new project, run `/catalog` to see the latest list of shared assets

## Workato's reference mechanism

When referencing shared assets across projects, the JSON uses the `zip_name` and `folder` fields:

```json
{
  "keyword": "share",
  "provider": "salesforce",
  "zip_name": "Shared | Salesforce",
  "folder": "Globally Shared Assets/Common - Connections"
}
```

`/create-recipe` auto-generates these references based on catalog information. There is no need to write the JSON by hand.
