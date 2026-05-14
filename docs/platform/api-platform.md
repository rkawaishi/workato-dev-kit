# API Platform

Official: https://docs.workato.com/en/api-management.html

## Overview

Enterprise-grade API management. Exposes recipe workflows as REST endpoints and safely externalizes legacy systems through API proxies.

## Core components

### API Recipes & Endpoints
Expose recipe functionality as REST endpoints. Other recipes can invoke them, and data can be shared with partners.

### API Collections
Group endpoints (recipe-based and proxy-based) into collections. Provides unified management and access control.

### API Proxies
Intermediaries that sit between clients and internal APIs. Safely expose legacy or internal systems without directly exposing them externally.

## Authentication and security

| Method | Description |
|---|---|
| OAuth 2.0 | Standard OAuth flow |
| JWT tokens | JSON Web Token-based authentication |
| OpenID Connect | ID token-based authentication |
| API Token | Authenticate via the `api-token` HTTP header |

## Access control

| Concept | Description |
|---|---|
| **Clients** | Users granted access to API collections |
| **Access Profiles** | Define which collections a client can access |
| **Access Policies** | Configure rate limits and quota management per client |

## Monitoring

- Real-time visibility into response time, error rate, and traffic patterns
- Concurrency limit tracking
- Request queuing when capacity is exceeded

## Relationship to MCP

Endpoints in API Collections can also be exposed as MCP servers.
See `@docs/platform/mcp.md` for details.
