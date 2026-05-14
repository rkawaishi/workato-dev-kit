# Workspace management best practices

Guidelines for workspace layout, naming conventions, and connection management.

## Workspace layout

### Environment separation

| Environment | Purpose |
|---|---|
| Dev | Development and experimentation |
| Test | Testing and verification |
| Prod | Production operations |

Unify authentication via SSO and split workspaces per environment.

### Project hierarchy

```
Workspace/
├── Globally Shared Assets/           # Common across all teams
│   ├── Common - Connections/         # Shared connections (Slack, Email, etc.)
│   ├── Common - Functions/           # Shared Recipe Functions
│   └── Error Handler/                # Shared error handling
│
├── Team Shared Assets/               # Shared within a team
│   ├── Sales - Connections/
│   ├── Sales - Common Functions/
│   ├── Sales - Lead Enrichment/
│   ├── Sales - Sales Bell/
│   ├── Finance - Connections/
│   ├── Finance - Common Functions/
│   ├── Finance - Invoice Creator/
│   ├── Finance - Month End/
│   └── Finance - Cost Center Sync/
│
└── Project Shared Assets/            # Project-specific
    ├── Connections/
    ├── Recipes/
    └── Workbot/
```

### Three levels of sharing

| Level | Scope | Examples |
|---|---|---|
| **Globally Shared** | All teams, all projects | Shared connections, error handler, general-purpose Functions |
| **Team Shared** | All projects within a team | Team-specific connections, business logic |
| **Project** | A single project | Project-specific Recipes and connections |

### Scope management for LLM development

In coordination with the `/catalog` skill, control the set of projects an LLM can access.
Define each project's scope in `projects/CATALOG_CONFIG.yaml`:

```yaml
projects:
  Shared:
    scope: global          # Open to all teams, listed in catalog
  "Finance - Common":
    scope: team:finance    # Shared within team, listed in catalog
  "[App] IT Onboarding":
    scope: private         # Excluded from the catalog
```

| Scope | Catalog listing | LLM references |
|---|---|---|
| `global` | All assets | `/create-recipe` and `/design` suggest as shared assets |
| `team:<name>` | All assets (with team name) | Same as above (suggested with team info) |
| `private` | **Not listed** | LLM does not access via the catalog |

Projects not listed are treated as `private`.
When code duplication is detected between private projects, only **suggest** consolidation; do not expose the concrete code through the catalog.

## Asset naming conventions

### Why use a shared vocabulary

- As the number of assets grows, searching and identifying them becomes difficult
- Uniform naming makes management and auditing easier
- Consistency is preserved across teams

### Naming structure

```
<Project> <Asset Code> <Sequence> | <Description>
```

| Element | Description | Example |
|---|---|---|
| **Project** | Project abbreviation | `CBI`, `FIN`, `HR` |
| **Asset Code** | Asset type code | `REC` (Recipe), `CON` (Connection), `FNC` (Function) |
| **Sequence** | Sequential number | `D01`, `D02` |
| **Description** | Description (natural language) | `Customer 360 Data Hub` |

**Example**: `CBI REC D01 | Customer 360 Data Hub`

### Asset type codes

| Code | Type |
|---|---|
| `REC` | Recipe |
| `CON` | Connection |
| `FNC` | Recipe Function |
| `WFA` | Workflow App |
| `GNI` | Genie |
| `MCP` | MCP Server |
| `SKL` | Agentic Skill |

### Application in this toolkit

workato-dev-kit uses the following naming conventions:

| Asset | Naming pattern | Example |
|---|---|---|
| Recipe | `<descriptive name>` | `IT onboarding: manager approval, Jira ticket, Slack notification` |
| Recipe Function | `fnc: <description>` / `fnc_<snake_case>` | `fnc: Get manager from Google Sheets` |
| Connection | `<Project> \| <Provider>` | `IT Onboarding \| Jira` |
| Workflow App | `<App name>` | `IT Onboarding` |
| Skill Recipe | `Skill: <description>` | `Skill: Submit IT onboarding request` |

When adopting the official `<Project> <Code> <Seq> | <Description>` format, keep it consistent within a project.

## Connection management

### Naming convention

```
<Environment/Context> | <Provider> [- <Usage>]
```

**Examples**:
- `Shared | Slack` - company-wide shared
- `IT Onboarding | Jira` - project-specific
- `Finance | Salesforce - Sandbox` - team-specific + environment

### Deciding whether to share a connection

| Criterion | Shared | Individual |
|---|---|---|
| Authentication scope | Company-wide permissions are sufficient | Project-specific permissions required |
| Environment | References the same production environment | Uses Sandbox / test environment |
| Risk | Change impact is acceptable | Want to avoid impact on other projects |

### Environments and connections

Workato separates Dev / Test / Prod environments per workspace. You do not need to include the environment name in the connection name; in each workspace, configure the same connection name with different credentials.

When the target service itself has a Sandbox environment (e.g. Salesforce Sandbox), distinguish usage in the name:

```
IT Onboarding | Salesforce           <- production
IT Onboarding | Salesforce - Sandbox <- for testing
```

## Error handling

Place a shared error handler in Globally Shared and reference it from every project:

- Place a shared error notification Recipe inside the **Error Handler** project
- Call the error handler from each Recipe's Monitor / Error block
- Centrally manage the error notification target (Slack channel, email)
