# Workbot

Official: https://docs.workato.com/en/workbot/overview.html

## Overview

Workato's chatbot framework. Runs on Slack, Microsoft Teams, and Facebook Workplace, integrating business applications into a chat interface.

## Supported platforms

| Platform | Documentation | provider |
|---|---|---|
| Slack | https://docs.workato.com/en/workbot/workbot.html | `slack_bot` |
| Microsoft Teams | https://docs.workato.com/en/workbot-for-teams/workbot.html | `teams_bot` |

## Key capabilities

### Monitoring & notifications
Notify channels of business events (customer tickets, form submissions, DevOps alerts, etc.). Supports smart notifications with user-defined filters.

### Data operations
Retrieve, create, and update business application data from chat. Operate without switching apps.

### Request automation
Run internal-resource provisioning workflows from chat.

## How it works

- Workbot must be invited to a channel
- In channels, mention `@workbot` (not needed in DMs)
- Everyone in the channel can use Workbot commands
- Automatically detects the Workato account's latest app Connections at install time

## Relationship to recipes

Workbot triggers / actions are used in recipes:
- **Trigger**: Detect Slack / Teams events or commands
- **Action**: Post messages, render Block Kit, handle button interactions

Full list of triggers / actions:
- Slack: `@docs/connectors/workbot-for-slack.md`
- Teams: `@docs/connectors/workbot-for-teams.md`

## Custom OAuth Profile

When events not covered by the standard connector (`reaction_added`, etc.) or extra scopes (`channels.history`, etc.) are required, configure a Custom OAuth Profile to obtain additional Slack / Teams scopes.

Details: see the "slack vs slack_bot" section of `@docs/learned-patterns.md`

## Notes

- Not available in CN data centers
- Prebuilt recipes are available, enabling minimal-setup adoption
- Can also be used as the chat interface for a Genie (AI agent)
