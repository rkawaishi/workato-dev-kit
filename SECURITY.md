# Security Policy

## Supported Versions

workato-dev-kit has not cut formal version tags yet.
Security fixes are applied only to the **latest commit on `main`**.
Consumers should pull the latest via `git submodule update --remote kit`.

| Version | Supported |
|---|---|
| `main` (latest) | ✅ |
| Older commits | ❌ |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it **privately** — do not open a public issue.

### Preferred: GitHub Security Advisories

1. Open the repository's [Security tab](https://github.com/rkawaishi/workato-dev-kit/security/advisories/new)
2. Choose "Report a vulnerability"
3. Fill in the details

GitHub's Private Vulnerability Reporting lets you communicate with the maintainers securely.

### Fallback: email

If GitHub Security Advisories is not available to you, email the maintainer directly.

- **Email**: kantannano@gmail.com
- **Subject prefix**: please prefix with `[SECURITY] workato-dev-kit:`

## Helpful information to include

- The affected file or component (e.g. `setup.sh`, `scripts/sync_agents.py`, or a specific skill)
- Reproduction steps (a minimal PoC)
- Expected impact (information disclosure / arbitrary code execution / privilege escalation, etc.)
- Whether you want to be credited (and if not, please say so)

## Response process

Maintainers respond as quickly as they can, but this is a volunteer-run project, so we cannot guarantee timing. As a rough guide:

| Step | Target |
|---|---|
| Acknowledgement | Within 7 days |
| Impact assessment | Within 14 days |
| Fix release | Depends on severity |

## Scope

Vulnerabilities in the code in this repository are in scope.

**Out of scope**:

- Vulnerabilities in Workato itself (report to [Workato](https://www.workato.com/legal/security))
- Misconfiguration of consumer repositories (e.g. a leaked `.workatoenv`) — that is the consumer's responsibility
- Vulnerabilities in the Workato Platform CLI itself (report to [workato-platform-cli](https://github.com/workato-devs/workato-platform-cli))
- Vulnerabilities in external services we integrate with (Claude Code, Cursor, Codex CLI, Gemini CLI, etc.)

## Disclosure policy

- Once a fix is released, we publish a GitHub Security Advisory.
- We credit reporters who want to be credited.
- We obtain a CVE for high-severity issues when appropriate.
