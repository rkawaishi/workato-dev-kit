# Workato Dev Kit Guides

This toolkit supports **Claude Code**, **Cursor**, **Codex CLI**, and **Gemini CLI**. Skills (`/create-recipe`, etc.) and rules work the same way in every editor (Codex uses `$foo` instead of `/foo` syntax).

## Getting started

| Guide | Contents |
|---|---|
| [Claude Code quickstart](quickstart-claude-code.md) | Setup and first development session with Claude Code |
| [Cursor quickstart](quickstart-cursor.md) | Setup and rule synchronization for Cursor |

> **Note:** The canonical source for skills and rules is `framework/claude/` inside the kit. The kit maintainer regenerates `framework/{cursor,codex,gemini}/` and `framework/AGENTS.md` ahead of time via `python3 scripts/sync_agents.py`. Running `bash kit/setup.sh` symlinks each editor's directory into your workspace (no need to run sync yourself). See [Design and architecture](architecture.md) for details.

## Design

| Guide | Contents |
|---|---|
| [Design and architecture](architecture.md) | Dual repository layout, knowledge hierarchy, learning cycle, skill / rule structure |

## Development guides

| Guide | Contents |
|---|---|
| [Lifecycle and responsibility map](lifecycle.md) | When / who / why for every skill and doc — what gets called, written, and read |
| [Skill reference](skills-reference.md) | Purpose, options, and usage for all skills |
| [Deployment](deployment.md) | Deploying recipes, Workflow Apps, and Genies / MCP servers, plus troubleshooting |
| [Recipe patterns](recipe-patterns.md) | How the pattern catalog works and how to use it |

## Feature guides

| Guide | Contents |
|---|---|
| [Building Workflow Apps](workflow-apps.md) | Building approval workflows and other Workflow Apps via JSON |
| [Building Genies & MCP servers](genie-and-mcp.md) | Constructing AI agents (Genies) and MCP servers |
| [Custom connector development](connector-development.md) | Developing custom API connectors with the Connector SDK |

## Operations guides

| Guide | Contents |
|---|---|
| [Knowledge management](knowledge-management.md) | Learning cycle and how to grow the knowledge base |
| [Shared-asset management](shared-assets.md) | Workspace structure, naming conventions, catalog operations |
