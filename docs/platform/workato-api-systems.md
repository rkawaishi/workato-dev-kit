# Workato API systems (Developer API / API Platform / OEM)

> Last verified: 2026-04-19

Workato has **four similar-but-different APIs all named "API Client"** (Developer API / API Platform v1 / API Platform v2 / OEM). Among them, API Platform v1 is being retired.

Read this document before starting any design work, and decide up front which system you will use. Conflating them forces you to redo the design from scratch (early-stage failure of the `workato-key-broker` project).

## Decision flow

```
Do you want to operate Workato itself via API? (recipe CRUD, connection management, API client issuance, etc.)
  └─ YES → Developer API
  └─ NO  → Do you need authentication for calling APIs you have published externally? (you already publish endpoints on your own API Platform)
             └─ YES → API Platform Clients (v1 = Access Profiles is being retired; v2 = API Keys is current)
             └─ NO  → Do you want to manage customer Workato tenants as a partner? (SaaS embed)
                        └─ YES → OEM / Embedded API
                        └─ NO  → If you ended up here the question is unclear. Reformulate the use case
```

## Comparison table

| Item | Developer API | API Platform Clients (v1 / Access Profiles) | API Platform Clients (v2 / API Keys) | OEM / Embedded API |
|---|---|---|---|---|
| **Purpose** | Operate Workato itself | Caller-side authentication for externally published APIs (legacy) | Caller-side authentication for externally published APIs (current) | Partner manages customer tenants |
| **Typical actor** | CLI / MCP / Dev Kit / internal automation | External system (legacy) | External system (new) | ISV / SaaS vendor |
| **Endpoint base** | `/api/*` (e.g., `/api/recipes`, `/api/developer_api_clients/*`) | `/api/api_clients/*` ⚠️ Not in official docs, slated for retirement | `/api/v2/api_clients/*` ⚠️ Not in official docs | `/oem/oem-api/*` (e.g., `/oem/oem-api/adapters`) |
| **Scope unit** | Project / Folder (attach project scope to the role) | Per Access Profile (= the linked API Collections) | Per Client + API Key (with IP restrictions and mTLS) | Per customer tenant |
| **Auth header** | `Authorization: Bearer <token>` / legacy `x-user-token` + `x-user-email` was retired on 2025-07-14 | `api-token` header | `api-token` header | Admin Console / JWT |
| **Status** | Current | **Being retired** (no new creation / changes from 2025-12-01; fully retired and tokens invalidated on 2026-07-01) | Current (recommended) | Current |
| **UI admin screen** | Workspace admin > API clients | API platform > Clients (Access Profiles tab) | API platform > Clients (API Keys tab) | Admin Console |
| **Official docs** | [workato-api.html](https://docs.workato.com/en/workato-api.html) / [api-clients.html](https://docs.workato.com/workato-api/api-clients.html) | [api-client-mgmt.html](https://docs.workato.com/en/api-mgmt/api-client-mgmt.html) | Same (API Keys section) | [oem.html](https://docs.workato.com/en/oem.html) / [oem-api.html](https://docs.workato.com/en/oem/oem-api.html) |

> **Note on "v1 / v2" naming and endpoint paths**
> The official docs do not use v1 / v2; they call them "Access Profiles (legacy)" and "API Keys (modern)". The v1 / v2 labels here are an informal convention for the empirically observed paths used when manipulating API Platform clients via the Developer API (`/api/api_clients/*` vs `/api/v2/api_clients/*`).
>
> ⚠️ **`/api/api_clients/*` and `/api/v2/api_clients/*` are undocumented endpoints not listed in the official documentation** and may change without notice. For new designs, first check whether the API Platform UI or an official SDK can meet your requirements; hitting these endpoints directly is a last resort.

## Details per system

### 1. Developer API

**In one line**: the API for "operating Workato from outside Workato".

- This is what powers the CLI (`workato` command), the MCP server, and the local Dev Kit behind the scenes
- Where API Clients are issued: **Workspace admin > API clients**
- Attach a Project scope to the role to limit which projects the API Client can touch
- The legacy authentication (`x-user-token` + `x-user-email`) was retired on 2025-07-14. Any code written from now on must use `Authorization: Bearer`

Typical use cases:
- Run `workato push` / `workato pull` from CI
- Hit `/api/recipes` from MCP to list recipes
- Export job history from `/api/jobs` for auditing

### 2. API Platform Clients (v1 / Access Profiles) — being retired

**In one line**: the **legacy** authentication for "letting external systems call APIs I have published on Workato".

- Concept: a three-layer model of **Client** → **Access Profile** → **API Collections**
- An Access Profile decides "which collections can be called", and an API Token is linked to it
- The external system calls with the `api-token` header
- An Access Policy sets rate limits / quotas per Access Profile

Retirement schedule:
- **2025-12-01**: Existing Access Profiles can no longer be modified or newly created
- **2026-07-01**: Fully retired. Issued API Tokens become invalid

Existing systems must migrate to v2 (API Keys) by 2026-07-01.

### 3. API Platform Clients (v2 / API Keys) — current

**In one line**: the successor to v1. Attaches 1 to 20 API Keys directly to a Client without going through an Access Profile.

Main differences (vs. v1):
- **API Key is a first-class resource**: up to 20 per Client, individually rotatable
- **IP restrictions**: allow / block list per Key
- **mTLS**: mutual TLS can be made mandatory on a custom domain
- **Auth method expansion**: Auth Token / OAuth 2.0 / JWT / OpenID Connect
- **Portal**: A self-service Portal where clients manage their own Keys can be provided

All new builds should use this one.

### 4. OEM / Embedded API

**In one line**: an API for ISVs / SaaS vendors who embed Workato inside their own product and "manage end-customer Workato tenants" on their behalf.

- A multi-tenant Admin Console structure
- End customers operate from within the partner product via iframe + JWT authentication
- A separate world from the Developer API. The partner side can create recipes / connections / adapters in the customer tenants
- Typical actor: an ISV with a Workato Embedded contract

Not used in ordinary recipe development. Consider only when building a platform product.

## Design-time checklist

Before starting the design of a new integration, state the following explicitly:

- [ ] Which system (Developer API / API Platform v1 / v2 / OEM)
- [ ] Who is the caller (internal CLI / MCP / external system / partner product)
- [ ] What is the scope unit (Project / Folder / Access Profile / Client+Key / tenant)
- [ ] What is the auth header (`Authorization: Bearer` / `api-token` / JWT)
- [ ] Are you trying to newly use v1 Access Profile (retired)?

## References

- Developer API: https://docs.workato.com/en/workato-api.html
- Developer API Clients management: https://docs.workato.com/workato-api/api-clients.html
- Migration FAQ from legacy auth: https://docs.workato.com/workato-api/moving-to-api-client-authentication-faq.html
- API Platform overview: https://docs.workato.com/en/api-management.html
- API Platform Client management (Access Profiles / API Keys): https://docs.workato.com/en/api-mgmt/api-client-mgmt.html
- OEM / Embedded: https://docs.workato.com/en/oem.html
- OEM API: https://docs.workato.com/en/oem/oem-api.html
