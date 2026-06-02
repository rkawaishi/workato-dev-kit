#!/usr/bin/env python3
"""Workato Platform API helper.

Complements the official Workato Platform CLI with API calls for features
not available in the CLI (jobs, connectors metadata, recipes list as JSON).

Authentication:
  Reuses the same credentials as the Platform CLI (keyring + ~/.workato/profiles).
  Supports workspace_id-based automatic profile resolution from .workatoenv,
  so .workatoenv never needs to contain a profile name (Git-sharing safe).

Usage:
  python3 scripts/workato-api.py jobs list --recipe-id <id> [--status <status>]
  python3 scripts/workato-api.py jobs get --recipe-id <id> --job-id <id>
  python3 scripts/workato-api.py connectors list-platform [--provider <name>]
  python3 scripts/workato-api.py connectors list-custom
  python3 scripts/workato-api.py recipes list [--folder-id <id>]
  python3 scripts/workato-api.py sdk push --connector <path> [--title <t>]
    (auto-detects new vs. update by reading connector_id from
     connectors/docs/<name>.md frontmatter; saves ID back after initial create)
  python3 scripts/workato-api.py sdk pull (--connector-id <id> | --name <name>)
    (downloads connector source to connectors/<name>/connector.rb and saves
     connector_id back to connectors/docs/<name>.md frontmatter)
  python3 scripts/workato-api.py sdk edit <file> [--key <master.key>]
  python3 scripts/workato-api.py sdk decrypt <file> [--key <master.key>]
  python3 scripts/workato-api.py deploy preview --from <env> --to <env>
    [--folder-id <id>] [--from-profile <name>] [--to-profile <name>]
    (read-only preview of the manifest that would be exported; runs the
     same env-transition guards as a real deploy will. Real deploy
     execution is tracked under Issue #160 PR-2b.)
  python3 scripts/workato-api.py profile show

Global options:
  --profile <name>   Use a specific profile instead of auto-resolution

Subcommand conventions (for contributors adding new subcommands):

  Every subparser MUST set:
    - help=    one-line summary, <=50 chars (shown in the {a,b,c} list)
    - description=  2-3 sentences. State purpose AND any preconditions or
                    environment restrictions in the first sentence.
                    Use imperative voice ("Push connector...", not "Pushes...").

  Side-effect subcommands (anything that creates, updates, deletes, or
  changes state in Workato — push, deploy, recipe start/stop, oauth-profiles
  create/update/delete, etc.) additionally MUST:
    - provide --dry-run that prints the intended request without sending it
    - set epilog= with at least one --dry-run example as the first example
    - guard environment boundaries in code, not just docs:
        * deploy commands: --from and --to required; the (from, to) pair
          must be one of {(dev, test), (test, prod)} — skip-tier
          (dev -> prod), backward (test -> dev, prod -> *), and same-env
          transitions are refused
        * execution deploys with --to prod additionally require --yes
          (CI-friendly confirm); preview/read-only deploy commands do not
          require --yes since they have no side effects

  Read-only subcommands (*list, *get, jobs list/get, profile show) do not
  need --dry-run or epilog, but still need help= and description=.

  Pre-existing side-effect commands without --dry-run (sdk push,
  oauth-profiles create/update/delete) are tracked under Issue #160 for
  retrofit alongside the new feature work; new commands must comply from
  the start.

  See workato-deployment-flow.md for the dev->test->prod policy that the
  environment guards enforce at the CLI level.
"""

import argparse
import base64
import json
import os
import secrets
import subprocess
import sys
import tempfile
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path


# ---------------------------------------------------------------------------
# Profile & Auth Resolution
# ---------------------------------------------------------------------------

PROFILES_PATH = Path.home() / ".workato" / "profiles"
KEYRING_SERVICE = "workato-platform-cli"


def load_profiles() -> dict:
    """Load ~/.workato/profiles JSON."""
    if not PROFILES_PATH.exists():
        print(
            "Error: ~/.workato/profiles not found. Run 'workato init' first.",
            file=sys.stderr,
        )
        sys.exit(1)
    with open(PROFILES_PATH) as f:
        return json.load(f)


def find_workatoenv() -> dict | None:
    """Walk up from cwd to find .workatoenv and return its contents."""
    current = Path.cwd()
    while True:
        candidate = current / ".workatoenv"
        if candidate.exists():
            with open(candidate) as f:
                return json.load(f)
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def resolve_profile(explicit_profile: str | None) -> tuple[str, dict]:
    """Resolve which profile to use.

    Resolution order:
      1. --profile <name> explicitly given
      2. .workatoenv workspace_id -> match against all profiles
      3. current_profile from ~/.workato/profiles

    Returns (profile_name, profile_dict).
    """
    data = load_profiles()
    profiles = data.get("profiles", {})

    if not profiles:
        print("Error: No profiles configured. Run 'workato init'.", file=sys.stderr)
        sys.exit(1)

    # 1. Explicit profile
    if explicit_profile:
        if explicit_profile not in profiles:
            print(
                f"Error: Profile '{explicit_profile}' not found. "
                f"Available: {', '.join(profiles.keys())}",
                file=sys.stderr,
            )
            sys.exit(1)
        return explicit_profile, profiles[explicit_profile]

    # 2. workspace_id from .workatoenv
    env = find_workatoenv()
    if env and "workspace_id" in env and env["workspace_id"] is not None:
        target_ws = str(env["workspace_id"])
        for name, prof in profiles.items():
            if prof.get("workspace_id") is not None and str(prof["workspace_id"]) == target_ws:
                return name, prof
        print(
            f"Warning: workspace_id {target_ws} from .workatoenv does not match "
            f"any profile. Falling back to current_profile.",
            file=sys.stderr,
        )

    # 3. current_profile
    current = data.get("current_profile", "")
    if current and current in profiles:
        return current, profiles[current]

    # Fallback: first profile
    name = next(iter(profiles))
    return name, profiles[name]


def _get_token_from_os_keychain(profile_name: str) -> str | None:
    """Read token directly from OS keychain without the keyring Python package.

    On macOS, uses the ``security`` CLI to read from Keychain.
    On Linux, tries ``secret-tool`` (libsecret / GNOME Keyring).
    Returns None if the token cannot be retrieved.
    """
    if sys.platform == "darwin":
        try:
            result = subprocess.run(
                [
                    "security",
                    "find-generic-password",
                    "-s", KEYRING_SERVICE,
                    "-a", profile_name,
                    "-w",
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except FileNotFoundError:
            pass
    elif sys.platform.startswith("linux"):
        try:
            result = subprocess.run(
                [
                    "secret-tool",
                    "lookup",
                    "service", KEYRING_SERVICE,
                    "username", profile_name,
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except FileNotFoundError:
            pass
    return None


def get_token(profile_name: str) -> str:
    """Retrieve API token for a profile.

    Tries in order:
      1. WORKATO_API_TOKEN env var
      2. Python keyring package (same as Platform CLI)
      2b. OS keychain CLI (macOS security / Linux secret-tool) — when
          keyring package is unavailable (e.g. pipx isolated env)
      3. ~/.workato/token_store.json
    """
    # 1. Environment variable
    env_token = os.environ.get("WORKATO_API_TOKEN")
    if env_token:
        return env_token

    # 2. Keyring (Python package)
    try:
        import keyring

        token = keyring.get_password(KEYRING_SERVICE, profile_name)
        if token:
            return token
    except ImportError:
        # keyring not installed in this Python (e.g. pipx isolated env).
        # Try OS-level keychain directly.
        token = _get_token_from_os_keychain(profile_name)
        if token:
            return token
    except Exception as e:
        print(f"Warning: keyring error ({e}), trying fallback.", file=sys.stderr)
        token = _get_token_from_os_keychain(profile_name)
        if token:
            return token

    # 3. Token store file
    token_store = Path.home() / ".workato" / "token_store.json"
    if token_store.exists():
        with open(token_store) as f:
            store = json.load(f)
        token = store.get(profile_name)
        if token:
            return token

    print(
        f"Error: No API token found for profile '{profile_name}'.\n"
        "Set WORKATO_API_TOKEN env var, or run 'workato init' to store in keyring.",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# API Client
# ---------------------------------------------------------------------------


class WorkatoAPI:
    """Simple Workato Platform API client."""

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _request(
        self, path: str, params: dict | None = None, method: str = "GET",
        body: dict | list | None = None,
    ) -> dict | list:
        url = f"{self.base_url}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(
                {k: v for k, v in params.items() if v is not None}
            )

        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            method=method,
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            err_body = e.read().decode() if e.fp else ""
            safe_url = url.split("?")[0]
            print(
                f"Error: HTTP {e.code} {e.reason}\n"
                f"URL: {safe_url}\n"
                f"Response: {err_body}",
                file=sys.stderr,
            )
            sys.exit(1)
        except urllib.error.URLError as e:
            safe_url = url.split("?")[0]
            print(f"Error: {e.reason}\nURL: {safe_url}", file=sys.stderr)
            sys.exit(1)

    # -- Jobs --

    def jobs_list(self, recipe_id: int, status: str | None = None) -> list:
        params = {}
        if status:
            params["status"] = status
        result = self._request(f"/api/recipes/{recipe_id}/jobs", params)
        return result if isinstance(result, list) else result.get("items", [])

    def jobs_get(self, recipe_id: int, job_id: str) -> dict:
        return self._request(f"/api/recipes/{recipe_id}/jobs/{job_id}")

    # -- Connectors --

    def connectors_list_platform(self, provider: str | None = None) -> list:
        """Get Pre-built connector metadata. Paginates automatically.

        When --provider is given, checks each page for a match and returns
        early to avoid fetching all 1000+ connectors.
        """
        all_connectors = []
        page = 1
        per_page = 100
        while True:
            result = self._request(
                "/api/integrations/all",
                {"page": page, "per_page": per_page},
            )
            items = (
                result.get("items", [])
                if isinstance(result, dict)
                else result
            )
            if not items:
                break

            if provider:
                matched = [
                    c for c in items
                    if c.get("name", "").lower() == provider.lower()
                    or c.get("provider", "").lower() == provider.lower()
                ]
                if matched:
                    return matched
                if len(items) < per_page:
                    break
                page += 1
                continue

            all_connectors.extend(items)
            if len(items) < per_page:
                break
            page += 1

        if provider:
            return []
        return all_connectors

    def connectors_list_custom(self) -> list:
        result = self._request("/api/custom_connectors")
        return result if isinstance(result, list) else result.get("result", [])

    def connectors_get_custom(self, connector_id: int) -> dict:
        """Fetch a single custom connector record (id, name, title, code, ...).

        The Platform API has historically returned the source under several
        shapes — `code`, `result.code`, `latest_released_version.code`, or
        within `released_versions[]`. The caller is expected to use
        `_extract_connector_source` to handle whichever shape comes back.
        """
        result = self._request(f"/api/custom_connectors/{connector_id}")
        if isinstance(result, dict):
            return result.get("data", result.get("result", result))
        return result  # type: ignore[return-value]

    # -- SDK (Custom Connectors) --

    def sdk_push(
        self,
        source_code: str,
        title: str,
        connector_id: int | None = None,
        description: str | None = None,
        notes: str | None = None,
        no_release: bool = False,
    ) -> dict:
        """Push connector source code to Workato.

        The create/update call uploads the code. A separate release call
        publishes the latest uploaded version.
        """
        payload: dict = {"code": source_code}
        if description:
            payload["description"] = description
        if notes:
            payload["note"] = notes

        if connector_id is not None:
            result = self._request(
                f"/api/custom_connectors/{connector_id}",
                method="PUT", body=payload,
            )
        else:
            payload["title"] = title
            result = self._request(
                "/api/custom_connectors",
                method="POST", body=payload,
            )

        data = result.get("data", result) if isinstance(result, dict) else result

        # Release unless explicitly skipped
        if not no_release:
            cid = connector_id if connector_id is not None else (data.get("id") if isinstance(data, dict) else None)
            if cid is not None:
                rel = self._request(
                    f"/api/custom_connectors/{cid}/release",
                    method="POST",
                )
                rel_data = rel.get("data", rel) if isinstance(rel, dict) else rel
                if isinstance(rel_data, dict):
                    data = rel_data

        return data

    # -- OAuth Profiles --

    def oauth_profiles_list(self) -> list:
        result = self._request("/api/custom_oauth_profiles")
        if isinstance(result, dict):
            return result.get("result", result.get("items", []))
        return result

    def oauth_profiles_get(self, profile_id: int) -> dict:
        return self._request(f"/api/custom_oauth_profiles/{profile_id}")

    def oauth_profiles_create(
        self, name: str, provider: str, client_id: str, client_secret: str,
        token: str | None = None,
    ) -> dict:
        body: dict = {
            "name": name,
            "provider": provider,
            "data": {"client_id": client_id, "client_secret": client_secret},
        }
        if token is not None:
            body["data"]["token"] = token
        result = self._request(
            "/api/custom_oauth_profiles", method="POST", body=body,
        )
        return result.get("data", result) if isinstance(result, dict) else result

    def oauth_profiles_update(
        self, profile_id: int, name: str, provider: str,
        client_id: str, client_secret: str, token: str | None = None,
    ) -> dict:
        body: dict = {
            "name": name,
            "provider": provider,
            "data": {"client_id": client_id, "client_secret": client_secret},
        }
        if token is not None:
            body["data"]["token"] = token
        result = self._request(
            f"/api/custom_oauth_profiles/{profile_id}", method="PUT", body=body,
        )
        return result.get("data", result) if isinstance(result, dict) else result

    def oauth_profiles_delete(self, profile_id: int) -> dict:
        return self._request(
            f"/api/custom_oauth_profiles/{profile_id}", method="DELETE",
        )

    # -- SDK Generate Schema --

    def sdk_generate_schema_json(self, raw_json: str) -> dict:
        return self._request(
            "/api/sdk/generate_schema/json", method="POST",
            body={"sample": raw_json},
        )

    def sdk_generate_schema_csv(self, csv_content: str, col_sep: str = ",") -> dict:
        return self._request(
            "/api/sdk/generate_schema/csv", method="POST",
            body={"sample": csv_content, "col_sep": col_sep},
        )

    # -- Recipes --

    def recipes_list(self, folder_id: int | None = None) -> list:
        """List recipes with pagination."""
        all_recipes = []
        page = 1
        per_page = 100
        while True:
            params: dict = {"page": page, "per_page": per_page}
            if folder_id is not None:
                params["folder_id"] = folder_id
            result = self._request("/api/recipes", params)
            if isinstance(result, dict):
                items = result.get("items", result.get("result", []))
            else:
                items = result
            if not items:
                break
            all_recipes.extend(items)
            if len(items) < per_page:
                break
            page += 1
        return all_recipes

    # -- Deploy (Recipe Lifecycle Management) --

    def deploy_folder_assets(self, folder_id: int) -> list:
        """List assets in a folder that would be included in an export manifest.

        Calls the read-only `GET /api/export_manifests/folder_assets`
        endpoint. Returns the asset list as Workato reports it (each entry
        carries id, type, name, and folder context). This drives the
        preview output for `deploy preview`; the same data feeds the
        manifest body used by `deploy run` (PR-2b).
        """
        result = self._request(
            "/api/export_manifests/folder_assets",
            params={"folder_id": folder_id},
        )
        if isinstance(result, dict):
            data = result.get("result", result.get("data", result))
            if isinstance(data, dict):
                return data.get("assets", [])
            if isinstance(data, list):
                return data
        return result if isinstance(result, list) else []


# ---------------------------------------------------------------------------
# Deploy helpers (environment guard + profile pair resolution)
# ---------------------------------------------------------------------------


DEPLOY_ENVS = ("dev", "test", "prod")
ALLOWED_DEPLOY_TRANSITIONS = {("dev", "test"), ("test", "prod")}


def check_deploy_transition(from_env: str, to_env: str) -> None:
    """Refuse invalid (from, to) pairs before any API call or profile work.

    Allowed: (dev, test), (test, prod). Everything else — skip-tier
    (dev -> prod), backward (test -> dev, prod -> *), and same-env —
    is rejected. See workato-deployment-flow.md.
    """
    if from_env == to_env:
        print(
            f"Error: --from and --to are both '{from_env}'. "
            f"Deploy requires distinct source and target environments.",
            file=sys.stderr,
        )
        sys.exit(1)
    if (from_env, to_env) not in ALLOWED_DEPLOY_TRANSITIONS:
        allowed = ", ".join(f"{a}->{b}" for a, b in sorted(ALLOWED_DEPLOY_TRANSITIONS))
        print(
            f"Error: deploy {from_env}->{to_env} is not allowed. "
            f"Allowed transitions: {allowed}. "
            f"Skip-tier (dev->prod), backward, and same-env transitions are "
            f"refused (see workato-deployment-flow.md).",
            file=sys.stderr,
        )
        sys.exit(1)


def _strip_env_suffix(profile_name: str) -> str | None:
    """Return the org prefix if profile_name follows `<org>-<env>`."""
    for env in DEPLOY_ENVS:
        suffix = f"-{env}"
        if profile_name.endswith(suffix) and len(profile_name) > len(suffix):
            return profile_name[: -len(suffix)]
    return None


def derive_sibling_profile(source_name: str, target_env: str) -> str | None:
    """Given `<org>-<env>`, return `<org>-<target_env>` if pattern matches."""
    org = _strip_env_suffix(source_name)
    if org is None:
        return None
    return f"{org}-{target_env}"


def resolve_deploy_profiles(
    from_env: str,
    to_env: str,
    explicit_from: str | None,
    explicit_to: str | None,
    explicit_default: str | None,
) -> tuple[tuple[str, dict], tuple[str, dict]]:
    """Resolve source and target profiles for a deploy.

    Resolution order:
      Source: explicit --from-profile, else current resolved profile
              (must follow `<org>-<from_env>` so the target can be derived).
      Target: explicit --to-profile, else `<org>-<to_env>` derived from
              the source profile name.

    Exits with a clear error if any required profile cannot be resolved.
    """
    profiles_data = load_profiles()
    profiles = profiles_data.get("profiles", {})

    # Source profile
    if explicit_from:
        source_name = explicit_from
    else:
        source_name, _ = resolve_profile(explicit_default)
    if source_name not in profiles:
        print(
            f"Error: source profile '{source_name}' not found in "
            f"~/.workato/profiles.",
            file=sys.stderr,
        )
        sys.exit(1)
    source_profile = profiles[source_name]

    # Target profile
    if explicit_to:
        target_name = explicit_to
    else:
        derived = derive_sibling_profile(source_name, to_env)
        if derived is None:
            print(
                f"Error: cannot derive target profile from "
                f"'{source_name}'. Expected `<org>-{from_env}` naming so "
                f"the target can be inferred as `<org>-{to_env}`. Pass "
                f"--to-profile <name> to override.",
                file=sys.stderr,
            )
            sys.exit(1)
        target_name = derived
    if target_name not in profiles:
        print(
            f"Error: target profile '{target_name}' not found in "
            f"~/.workato/profiles. Configure it with `workato init` or "
            f"pass --to-profile <name>.",
            file=sys.stderr,
        )
        sys.exit(1)
    target_profile = profiles[target_name]

    return (source_name, source_profile), (target_name, target_profile)


def resolve_deploy_folder_id(explicit_folder_id: int | None) -> int:
    """Resolve folder_id from --folder-id or .workatoenv. Exit if neither."""
    if explicit_folder_id is not None:
        return explicit_folder_id
    env_data = find_workatoenv()
    if env_data is None:
        print(
            "Error: no --folder-id given and no .workatoenv found by "
            "walking up from the current directory. Run from inside a "
            "project, or pass --folder-id <id>.",
            file=sys.stderr,
        )
        sys.exit(1)
    folder_id = env_data.get("folder_id")
    if not isinstance(folder_id, int):
        print(
            "Error: .workatoenv was found but does not contain an "
            "integer folder_id. Pass --folder-id <id> explicitly.",
            file=sys.stderr,
        )
        sys.exit(1)
    return folder_id


# ---------------------------------------------------------------------------
# CLI Commands
# ---------------------------------------------------------------------------


def cmd_jobs_list(api: WorkatoAPI, args: argparse.Namespace):
    jobs = api.jobs_list(args.recipe_id, args.status)
    print(json.dumps(jobs, indent=2, ensure_ascii=False))


def cmd_jobs_get(api: WorkatoAPI, args: argparse.Namespace):
    job = api.jobs_get(args.recipe_id, args.job_id)
    print(json.dumps(job, indent=2, ensure_ascii=False))


def cmd_connectors_list_platform(api: WorkatoAPI, args: argparse.Namespace):
    connectors = api.connectors_list_platform(args.provider)
    print(json.dumps(connectors, indent=2, ensure_ascii=False))


def cmd_connectors_list_custom(api: WorkatoAPI, args: argparse.Namespace):
    connectors = api.connectors_list_custom()
    print(json.dumps(connectors, indent=2, ensure_ascii=False))


def cmd_recipes_list(api: WorkatoAPI, args: argparse.Namespace):
    recipes = api.recipes_list(args.folder_id)
    print(json.dumps(recipes, indent=2, ensure_ascii=False))


def _summarize_assets(assets: list) -> dict:
    """Group assets by `type` and return {type: count}."""
    counts: dict = {}
    for a in assets:
        if not isinstance(a, dict):
            continue
        kind = a.get("type") or a.get("asset_type") or "unknown"
        counts[kind] = counts.get(kind, 0) + 1
    return counts


def cmd_deploy_preview(_api: WorkatoAPI, args: argparse.Namespace):
    """Read-only preview of what `deploy run` (PR-2b) would export.

    Runs the env-transition guard, resolves source and target profiles,
    resolves folder_id, then calls the source workspace's read-only
    folder_assets endpoint and prints what would be packaged. Makes no
    writes to either workspace.
    """
    check_deploy_transition(args.from_env, args.to_env)

    (source_name, source_profile), (target_name, target_profile) = \
        resolve_deploy_profiles(
            args.from_env, args.to_env,
            args.from_profile, args.to_profile,
            args.profile,
        )

    folder_id = resolve_deploy_folder_id(args.folder_id)

    source_region = source_profile.get("region_url", "")
    if not source_region:
        print(
            f"Error: source profile '{source_name}' has no region_url.",
            file=sys.stderr,
        )
        sys.exit(1)
    source_token = get_token(source_name)
    source_api = WorkatoAPI(source_region, source_token)

    assets = source_api.deploy_folder_assets(folder_id)
    summary = _summarize_assets(assets)

    output = {
        "mode": "preview",
        "source": {
            "profile": source_name,
            "workspace_url": source_region,
            "env": args.from_env,
        },
        "target": {
            "profile": target_name,
            "workspace_url": target_profile.get("region_url", ""),
            "env": args.to_env,
        },
        "folder_id": folder_id,
        "asset_summary": summary,
        "assets": assets,
        "notes": [
            "No API writes were performed; only the read-only "
            "/api/export_manifests/folder_assets endpoint was called on the "
            "source workspace.",
            "Real deploy execution is tracked under Issue #160 PR-2b.",
        ],
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


def cmd_oauth_profiles_list(api: WorkatoAPI, args: argparse.Namespace):
    profiles = api.oauth_profiles_list()
    print(json.dumps(profiles, indent=2, ensure_ascii=False))


def cmd_oauth_profiles_get(api: WorkatoAPI, args: argparse.Namespace):
    profile = api.oauth_profiles_get(args.id)
    print(json.dumps(profile, indent=2, ensure_ascii=False))


def cmd_oauth_profiles_create(api: WorkatoAPI, args: argparse.Namespace):
    result = api.oauth_profiles_create(
        name=args.name, provider=args.provider,
        client_id=args.client_id, client_secret=args.client_secret,
        token=args.token,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nCreated OAuth profile: {result.get('name', args.name)}", file=sys.stderr)


def cmd_oauth_profiles_update(api: WorkatoAPI, args: argparse.Namespace):
    result = api.oauth_profiles_update(
        profile_id=args.id, name=args.name, provider=args.provider,
        client_id=args.client_id, client_secret=args.client_secret,
        token=args.token,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nUpdated OAuth profile: {result.get('name', args.name)}", file=sys.stderr)


def cmd_oauth_profiles_delete(api: WorkatoAPI, args: argparse.Namespace):
    result = api.oauth_profiles_delete(args.id)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nDeleted OAuth profile id={args.id}", file=sys.stderr)


def cmd_sdk_generate_schema(api: WorkatoAPI, args: argparse.Namespace):
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    content = file_path.read_text()
    if file_path.suffix == ".csv":
        result = api.sdk_generate_schema_csv(content)
    else:
        # API expects raw JSON string, not parsed object
        result = api.sdk_generate_schema_json(content)

    print(json.dumps(result, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Encrypted File Support (aes-128-gcm, compatible with fork CLI)
# Format: base64(ciphertext)--base64(iv)--base64(auth_tag)
# ---------------------------------------------------------------------------


def _enc_decrypt(encrypted_data: bytes, key_hex: str) -> bytes:
    """Decrypt data encrypted with aes-128-gcm."""
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        print(
            "Error: 'cryptography' package required for .enc file support.\n"
            "Install: pip install cryptography",
            file=sys.stderr,
        )
        sys.exit(1)

    parts = encrypted_data.split(b"--")
    if len(parts) != 3:
        print(
            "Error: Invalid .enc file format. "
            "Expected: base64(ciphertext)--base64(iv)--base64(auth_tag)",
            file=sys.stderr,
        )
        sys.exit(1)

    ciphertext = base64.b64decode(parts[0])
    iv = base64.b64decode(parts[1])
    auth_tag = base64.b64decode(parts[2])

    key = bytes.fromhex(key_hex)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(iv, ciphertext + auth_tag, None)


def _enc_encrypt(plaintext: bytes, key_hex: str) -> bytes:
    """Encrypt data using aes-128-gcm."""
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        print(
            "Error: 'cryptography' package required for .enc file support.\n"
            "Install: pip install cryptography",
            file=sys.stderr,
        )
        sys.exit(1)

    key = bytes.fromhex(key_hex)
    iv = os.urandom(12)
    aesgcm = AESGCM(key)
    ct_and_tag = aesgcm.encrypt(iv, plaintext, None)
    ciphertext = ct_and_tag[:-16]
    auth_tag = ct_and_tag[-16:]

    return (
        base64.b64encode(ciphertext)
        + b"--"
        + base64.b64encode(iv)
        + b"--"
        + base64.b64encode(auth_tag)
    )


def _resolve_key_path(key_arg: str | None, enc_file: Path) -> Path:
    """Resolve master.key path: explicit arg, or same directory as .enc file."""
    if key_arg:
        return Path(key_arg)
    return enc_file.parent / "master.key"


# ---------------------------------------------------------------------------
# Connector docs frontmatter (for connector_id persistence)
#
# `connectors/docs/<name>.md` holds a YAML-ish frontmatter block that records
# the Workato connector ID after a successful push. Subsequent pushes read
# it back so the user does not need to remember `--connector-id`.
# Only flat `key: value` pairs are supported (no nested structures).
# ---------------------------------------------------------------------------


def _connector_docs_path(connector_rb_path: Path) -> Path:
    """Return `connectors/docs/<name>.md` derived from the connector.rb path.

    `<name>` is the basename of the connector.rb's parent directory, and the
    docs dir is a sibling of that parent (i.e. `connectors/docs/`).
    """
    connector_dir = connector_rb_path.resolve().parent
    name = connector_dir.name
    docs_dir = connector_dir.parent / "docs"
    return docs_dir / f"{name}.md"


def _read_frontmatter(md_path: Path) -> tuple[dict, str]:
    """Parse top-of-file YAML-ish frontmatter. Returns (fm_dict, body)."""
    if not md_path.exists():
        return {}, ""
    text = md_path.read_text()
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_text = text[4:end]
    body = text[end + len("\n---\n"):]

    fm: dict = {}
    for line in fm_text.splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    return fm, body


def _write_frontmatter(md_path: Path, fm: dict, connector_name: str | None = None):
    """Write/update frontmatter at top of `md_path`.

    Creates a minimal stub body if the file doesn't exist yet so the
    frontmatter has somewhere to live.
    """
    md_path.parent.mkdir(parents=True, exist_ok=True)

    if md_path.exists():
        _existing_fm, body = _read_frontmatter(md_path)
    else:
        name = connector_name or md_path.stem
        body = (
            f"# {name} connector\n\n"
            f"Provider: `{name}`\n"
            f"Source: Custom (Connector SDK)\n\n"
            f"> Run `/sync-connectors --custom {name}` to populate "
            f"trigger / action / field metadata.\n"
        )

    fm_lines = "\n".join(f"{k}: {v}" for k, v in fm.items())
    md_path.write_text(f"---\n{fm_lines}\n---\n\n{body.lstrip()}")


def _resolve_connector_id(
    connector_rb_path: Path, explicit_id: int | None
) -> tuple[int | None, Path]:
    """Decide which connector ID to use for this push.

    Returns `(id_or_None, docs_path)`. Explicit `--connector-id` wins;
    otherwise the frontmatter of `connectors/docs/<name>.md` is consulted.
    """
    docs_path = _connector_docs_path(connector_rb_path)
    if explicit_id is not None:
        return explicit_id, docs_path

    fm, _ = _read_frontmatter(docs_path)
    raw = fm.get("connector_id")
    if not raw:
        return None, docs_path
    try:
        return int(raw), docs_path
    except ValueError:
        print(
            f"Warning: connector_id in {docs_path} is not an integer ('{raw}'); "
            "treating as new connector.",
            file=sys.stderr,
        )
        return None, docs_path


def _extract_connector_source(record: dict) -> str | None:
    """Best-effort extraction of the Ruby source from a custom-connector record.

    The Platform API has used several shapes over time; check in order:
      1. `code` (current).
      2. `source_code` (some older deployments).
      3. `latest_released_version.code` (when released-version is nested).
      4. The newest entry in `released_versions[]` by version number.
    """
    if not isinstance(record, dict):
        return None

    for key in ("code", "source_code"):
        value = record.get(key)
        if isinstance(value, str) and value:
            return value

    latest = record.get("latest_released_version")
    if isinstance(latest, dict):
        for key in ("code", "source_code"):
            value = latest.get(key)
            if isinstance(value, str) and value:
                return value

    versions = record.get("released_versions")
    if isinstance(versions, list) and versions:
        def _ver_key(v: dict) -> int:
            try:
                return int(v.get("version", 0))
            except (TypeError, ValueError):
                return 0
        candidates = [v for v in versions if isinstance(v, dict)]
        for v in sorted(candidates, key=_ver_key, reverse=True):
            for key in ("code", "source_code"):
                value = v.get(key)
                if isinstance(value, str) and value:
                    return value

    return None


def _connector_slug(record: dict, fallback: str | None = None) -> str:
    """Pick the directory-name slug for a fetched custom connector.

    Prefers `name` (which is typically a slug), then `title` lowered with
    non-alnum chars replaced. Falls back to `fallback` (usually the CLI arg)
    or the connector ID stringified.
    """
    import re

    raw = record.get("name") if isinstance(record, dict) else None
    if not raw:
        raw = record.get("title") if isinstance(record, dict) else None
    if not raw:
        raw = fallback or ""
    raw = str(raw).strip()
    slug = re.sub(r"[^a-z0-9]+", "_", raw.lower()).strip("_")
    return slug or (str(record.get("id")) if isinstance(record, dict) else "connector")


def cmd_sdk_pull(api: WorkatoAPI, args: argparse.Namespace):
    """Pull a custom connector's source from Workato to the local filesystem."""
    if args.connector_id is None and not args.name:
        print(
            "Error: provide --connector-id <id> or --name <connector-name>.",
            file=sys.stderr,
        )
        sys.exit(1)

    connector_id = args.connector_id
    record: dict | None = None

    if connector_id is None:
        # Resolve name -> id via the list endpoint
        listed = api.connectors_list_custom()
        target = args.name.lower()
        matches = [
            c for c in listed
            if isinstance(c, dict) and (
                str(c.get("name", "")).lower() == target
                or str(c.get("title", "")).lower() == target
            )
        ]
        if not matches:
            print(
                f"Error: no custom connector with name/title '{args.name}'. "
                f"Run 'connectors list-custom' to see available connectors.",
                file=sys.stderr,
            )
            sys.exit(1)
        if len(matches) > 1:
            ids = ", ".join(str(c.get("id")) for c in matches)
            print(
                f"Error: name '{args.name}' is ambiguous (matches ids: {ids}). "
                f"Re-run with --connector-id.",
                file=sys.stderr,
            )
            sys.exit(1)
        record = matches[0]
        connector_id = int(record["id"])
        # The list response sometimes already contains the code; only re-fetch
        # if it doesn't.
        if _extract_connector_source(record) is None:
            record = api.connectors_get_custom(connector_id)
    else:
        record = api.connectors_get_custom(connector_id)

    source = _extract_connector_source(record or {})
    if source is None:
        print(
            f"Error: connector id={connector_id} has no source code in the "
            f"API response. (It may have no released version yet.)",
            file=sys.stderr,
        )
        sys.exit(1)

    slug = _connector_slug(record or {}, fallback=args.name)
    target_dir = Path(args.output_dir) if args.output_dir else Path("connectors") / slug
    target_file = target_dir / "connector.rb"

    if target_file.exists() and not args.force:
        print(
            f"Error: {target_file} already exists. Re-run with --force to overwrite.",
            file=sys.stderr,
        )
        sys.exit(1)

    target_dir.mkdir(parents=True, exist_ok=True)
    target_file.write_text(source)

    try:
        display_target = target_file.relative_to(Path.cwd())
    except ValueError:
        display_target = target_file

    title = record.get("title") if isinstance(record, dict) else None
    print(
        f"Pulled connector id={connector_id} "
        f"({title or slug}) -> {display_target}",
        file=sys.stderr,
    )

    # Persist connector_id to docs frontmatter (mirrors sdk push behavior).
    # The docs-frontmatter convention is tied to the canonical
    # connectors/<slug>/ layout, where docs live in a sibling connectors/docs/.
    # With --output-dir we cannot assume that layout, so skip the save rather
    # than writing an unexpected docs/ directory next to an arbitrary path.
    if args.skip_save_id:
        pass
    elif args.output_dir:
        print(
            "Note: connector_id not saved to docs frontmatter "
            "(--output-dir bypasses the canonical connectors/ layout). "
            f"Pass --connector-id {connector_id} when running sdk push.",
            file=sys.stderr,
        )
    else:
        docs_path = _connector_docs_path(target_file)
        fm, _ = _read_frontmatter(docs_path)
        existing = fm.get("connector_id")
        if existing != str(connector_id):
            fm["connector_id"] = str(connector_id)
            _write_frontmatter(docs_path, fm, connector_name=slug)
            try:
                display_docs = docs_path.relative_to(Path.cwd())
            except ValueError:
                display_docs = docs_path
            if existing is None:
                print(
                    f"Saved connector_id={connector_id} to {display_docs}",
                    file=sys.stderr,
                )
            else:
                print(
                    f"Updated connector_id in {display_docs} "
                    f"({existing} -> {connector_id})",
                    file=sys.stderr,
                )


def cmd_sdk_push(api: WorkatoAPI, args: argparse.Namespace):
    connector_path = Path(args.connector)
    if not connector_path.exists():
        print(f"Error: File not found: {connector_path}", file=sys.stderr)
        sys.exit(1)

    source_code = connector_path.read_text()

    title = args.title
    if not title:
        import re
        match = re.search(r"title:\s*['\"](.+?)['\"]", source_code)
        title = match.group(1) if match else connector_path.parent.name

    resolved_id, docs_path = _resolve_connector_id(connector_path, args.connector_id)
    is_update = resolved_id is not None

    try:
        display_docs = docs_path.relative_to(Path.cwd())
    except ValueError:
        display_docs = docs_path

    if is_update:
        if args.connector_id is not None:
            print(f"Updating connector id={resolved_id} (--connector-id)", file=sys.stderr)
        else:
            print(
                f"Updating connector id={resolved_id} "
                f"(from {display_docs} frontmatter)",
                file=sys.stderr,
            )
    else:
        print(
            f"Creating new connector '{title}' "
            f"(no connector_id found in {display_docs})",
            file=sys.stderr,
        )

    result = api.sdk_push(
        source_code=source_code,
        title=title,
        connector_id=resolved_id,
        description=args.description,
        notes=args.notes,
        no_release=args.no_release,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))

    returned_id = result.get("id") if isinstance(result, dict) else None
    final_id = resolved_id if resolved_id is not None else returned_id

    action = "Updated" if is_update else "Created"
    print(
        f"\n{action} connector: {result.get('title', title)} (id={final_id or '?'})",
        file=sys.stderr,
    )

    # Persist connector_id to docs frontmatter on first successful push
    # (or if the docs file did not yet record the ID for some reason).
    if final_id is not None and not args.skip_save_id:
        fm, _ = _read_frontmatter(docs_path)
        existing = fm.get("connector_id")
        if existing != str(final_id):
            fm["connector_id"] = str(final_id)
            _write_frontmatter(docs_path, fm, connector_name=connector_path.parent.name)
            if existing is None:
                print(
                    f"Saved connector_id={final_id} to "
                    f"{docs_path} (next push will update in place)",
                    file=sys.stderr,
                )
            else:
                print(
                    f"Updated connector_id in {docs_path} "
                    f"({existing} -> {final_id})",
                    file=sys.stderr,
                )


def cmd_sdk_decrypt(_api: WorkatoAPI, args: argparse.Namespace):
    """Decrypt a .enc file and print to stdout."""
    enc_path = Path(args.file)
    if not enc_path.exists():
        print(f"Error: File not found: {enc_path}", file=sys.stderr)
        sys.exit(1)

    key_path = _resolve_key_path(args.key, enc_path)
    if not key_path.exists():
        print(f"Error: Key file not found: {key_path}", file=sys.stderr)
        sys.exit(1)

    key_hex = key_path.read_text().strip()
    decrypted = _enc_decrypt(enc_path.read_bytes(), key_hex)
    print(decrypted.decode("utf-8"))


def cmd_sdk_edit(_api: WorkatoAPI, args: argparse.Namespace):
    """Decrypt a .enc file, open in $EDITOR, re-encrypt on save."""
    enc_path = Path(args.file)
    key_path = _resolve_key_path(args.key, enc_path)

    if not key_path.exists():
        if not enc_path.exists():
            # New file: generate key
            key_hex = secrets.token_hex(16)
            key_path.write_text(key_hex + "\n")
            print(f"Generated new key: {key_path}", file=sys.stderr)
            original = ""
        else:
            print(f"Error: Key file not found: {key_path}", file=sys.stderr)
            sys.exit(1)
    else:
        key_hex = key_path.read_text().strip()
        if enc_path.exists():
            original = _enc_decrypt(enc_path.read_bytes(), key_hex).decode("utf-8")
        else:
            original = ""

    editor = os.environ.get("EDITOR", "vi")

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(original)
        tmp_path = tmp.name

    try:
        import shlex
        result = subprocess.run(shlex.split(editor) + [tmp_path])
        if result.returncode != 0:
            print("Editor exited with error. File not saved.", file=sys.stderr)
            sys.exit(1)

        edited = Path(tmp_path).read_text(encoding="utf-8")
        if edited == original:
            print("No changes made.", file=sys.stderr)
            return

        encrypted = _enc_encrypt(edited.encode("utf-8"), key_hex)
        enc_path.write_bytes(encrypted)
        print(f"Encrypted and saved: {enc_path}", file=sys.stderr)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def cmd_profile_show(_api: WorkatoAPI, args: argparse.Namespace):
    """Show resolved profile info (without token)."""
    profile_name, profile = resolve_profile(args.profile)
    env = find_workatoenv()
    info = {
        "resolved_profile": profile_name,
        "region_url": profile.get("region_url", ""),
        "workspace_id": profile.get("workspace_id"),
        "workatoenv": env,
        "resolution_method": (
            "explicit --profile"
            if args.profile
            else "workspace_id from .workatoenv"
            if env
            and "workspace_id" in env
            and env["workspace_id"] is not None
            and profile.get("workspace_id") is not None
            and str(env["workspace_id"]) == str(profile.get("workspace_id"))
            else "current_profile"
        ),
    }
    print(json.dumps(info, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Workato Platform API helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--profile",
        default=None,
        help="Profile name (default: auto-resolve from .workatoenv workspace_id)",
    )

    subparsers = parser.add_subparsers(dest="command", help="API command group")

    # -- jobs --
    jobs_parser = subparsers.add_parser("jobs", help="Manage recipe jobs")
    jobs_sub = jobs_parser.add_subparsers(dest="jobs_command")

    jobs_list_p = jobs_sub.add_parser(
        "list",
        help="List jobs for a recipe",
        description=(
            "List jobs for a recipe in reverse-chronological order. "
            "Optionally filter by status (e.g. failed, success). Read-only."
        ),
    )
    jobs_list_p.add_argument("--recipe-id", type=int, required=True)
    jobs_list_p.add_argument("--status", default=None, help="Filter by status")

    jobs_get_p = jobs_sub.add_parser(
        "get",
        help="Get job details",
        description=(
            "Show the full input/output payload, error, and metadata for a "
            "single job. Read-only."
        ),
    )
    jobs_get_p.add_argument("--recipe-id", type=int, required=True)
    jobs_get_p.add_argument("--job-id", type=str, required=True)

    # -- connectors --
    conn_parser = subparsers.add_parser("connectors", help="Manage connectors")
    conn_sub = conn_parser.add_subparsers(dest="connectors_command")

    conn_platform_p = conn_sub.add_parser(
        "list-platform",
        help="List Pre-built connectors",
        description=(
            "List Workato's Pre-built (platform) connectors with pagination. "
            "When --provider is given, returns early on the first matching "
            "page. Read-only."
        ),
    )
    conn_platform_p.add_argument(
        "--provider", default=None, help="Filter by provider name"
    )

    conn_sub.add_parser(
        "list-custom",
        help="List custom connectors",
        description=(
            "List custom connectors in the connected workspace. Read-only."
        ),
    )

    # -- recipes --
    recipes_parser = subparsers.add_parser("recipes", help="Manage recipes")
    recipes_sub = recipes_parser.add_subparsers(dest="recipes_command")

    recipes_list_p = recipes_sub.add_parser(
        "list",
        help="List recipes (JSON)",
        description=(
            "List recipes in the connected workspace as JSON, with "
            "pagination. Optionally filter by folder. Read-only."
        ),
    )
    recipes_list_p.add_argument(
        "--folder-id", type=int, default=None, help="Filter by folder ID"
    )

    # -- deploy --
    deploy_parser = subparsers.add_parser(
        "deploy", help="Promote a project between environments (Recipe Lifecycle)"
    )
    deploy_sub = deploy_parser.add_subparsers(dest="deploy_command")

    deploy_preview_p = deploy_sub.add_parser(
        "preview",
        help="Preview the manifest that would be exported",
        description=(
            "Preview what would be packaged for a deploy from --from to "
            "--to, without writing to either workspace. Runs the same "
            "(from, to) transition guards as a real deploy: only "
            "dev->test and test->prod are allowed. Calls only the "
            "read-only /api/export_manifests/folder_assets endpoint on "
            "the source workspace."
        ),
        epilog=(
            "Examples:\n"
            "  # Preview a dev -> test deploy of the current project\n"
            "  python3 scripts/workato-api.py deploy preview --from dev --to test\n\n"
            "  # Preview a test -> prod deploy with explicit folder and profiles\n"
            "  python3 scripts/workato-api.py deploy preview --from test --to prod \\\n"
            "      --folder-id 12345 --from-profile acme-test --to-profile acme-prod\n\n"
            "  # Skip-tier (dev -> prod) is refused before any API call:\n"
            "  python3 scripts/workato-api.py deploy preview --from dev --to prod\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    deploy_preview_p.add_argument(
        "--from", dest="from_env", choices=DEPLOY_ENVS, required=True,
        help="Source environment (dev/test/prod)",
    )
    deploy_preview_p.add_argument(
        "--to", dest="to_env", choices=DEPLOY_ENVS, required=True,
        help="Target environment (dev/test/prod)",
    )
    deploy_preview_p.add_argument(
        "--folder-id", type=int, default=None,
        help="Folder ID to export (default: from .workatoenv in cwd)",
    )
    deploy_preview_p.add_argument(
        "--from-profile", default=None,
        help="Source profile name (default: current resolved profile)",
    )
    deploy_preview_p.add_argument(
        "--to-profile", default=None,
        help="Target profile name (default: derive `<org>-<to>` from source)",
    )

    # -- sdk --
    sdk_parser = subparsers.add_parser(
        "sdk", help="Connector SDK commands (uses Platform API token)"
    )
    sdk_sub = sdk_parser.add_subparsers(dest="sdk_command")

    sdk_push_p = sdk_sub.add_parser(
        "push",
        help="Push connector source code to Workato",
        description=(
            "Push connector source to Workato as a new version and release "
            "it. Auto-detects create vs. update from the connector_id stored "
            "in connectors/docs/<name>.md frontmatter, and saves the ID back "
            "after an initial create. Writes to the connected workspace."
        ),
        epilog=(
            "Examples:\n"
            "  # Update an existing connector (ID auto-resolved from docs frontmatter)\n"
            "  python3 scripts/workato-api.py sdk push --connector connectors/foo/connector.rb\n\n"
            "  # First-time push (creates the connector, then saves the new ID)\n"
            "  python3 scripts/workato-api.py sdk push --connector connectors/foo/connector.rb --title \"Foo\"\n\n"
            "  # Upload without releasing\n"
            "  python3 scripts/workato-api.py sdk push --connector connectors/foo/connector.rb --no-release\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sdk_push_p.add_argument(
        "--connector", required=True, help="Path to connector.rb file"
    )
    sdk_push_p.add_argument(
        "--title", default=None, help="Connector title (auto-detected from source)"
    )
    sdk_push_p.add_argument(
        "--connector-id", type=int, default=None,
        help="Existing connector ID (for updates)"
    )
    sdk_push_p.add_argument("--description", default=None, help="Description (markdown)")
    sdk_push_p.add_argument("--notes", default=None, help="Release notes")
    sdk_push_p.add_argument(
        "--no-release", action="store_true", help="Upload without releasing"
    )
    sdk_push_p.add_argument(
        "--skip-save-id", action="store_true",
        help="Don't persist the returned connector_id to "
             "connectors/docs/<name>.md frontmatter",
    )

    sdk_pull_p = sdk_sub.add_parser(
        "pull",
        help="Pull a custom connector's source from Workato",
        description=(
            "Download a custom connector's source to "
            "connectors/<name>/connector.rb. Resolves the connector by --id "
            "or by --name (via list-custom), and writes connector_id back to "
            "connectors/docs/<name>.md frontmatter. Writes local files only."
        ),
        epilog=(
            "Examples:\n"
            "  python3 scripts/workato-api.py sdk pull --connector-id 12345\n"
            "  python3 scripts/workato-api.py sdk pull --name slack_custom\n"
            "  python3 scripts/workato-api.py sdk pull --name foo --output-dir tmp/ --force\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sdk_pull_p.add_argument(
        "--connector-id", type=int, default=None,
        help="Workato custom connector ID to pull",
    )
    sdk_pull_p.add_argument(
        "--name", default=None,
        help="Connector name or title (resolved via list-custom)",
    )
    sdk_pull_p.add_argument(
        "--output-dir", default=None,
        help="Override the output directory (default: connectors/<name>/). "
             "When set, connector_id is not saved to docs frontmatter.",
    )
    sdk_pull_p.add_argument(
        "--force", action="store_true",
        help="Overwrite connector.rb if it already exists",
    )
    sdk_pull_p.add_argument(
        "--skip-save-id", action="store_true",
        help="Don't persist connector_id to connectors/docs/<name>.md frontmatter",
    )

    sdk_decrypt_p = sdk_sub.add_parser(
        "decrypt",
        help="Decrypt a .enc file and print to stdout",
        description=(
            "Decrypt a Workato CLI master.key-encrypted file and print the "
            "plaintext to stdout. Read-only; does not modify the .enc file."
        ),
    )
    sdk_decrypt_p.add_argument("file", help="Path to .enc file")
    sdk_decrypt_p.add_argument(
        "--key", default=None, help="Path to master.key (default: same dir as .enc)"
    )

    sdk_edit_p = sdk_sub.add_parser(
        "edit",
        help="Decrypt .enc file, open in $EDITOR, re-encrypt on save",
        description=(
            "Decrypt a .enc file to a temp file, open it in $EDITOR, and "
            "re-encrypt on save. Creates a new .enc file if the path does "
            "not exist. Writes the local .enc file only; no Workato calls."
        ),
        epilog=(
            "Examples:\n"
            "  python3 scripts/workato-api.py sdk edit connectors/foo/connection.enc\n"
            "  python3 scripts/workato-api.py sdk edit connectors/foo/connection.enc --key path/to/master.key\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sdk_edit_p.add_argument("file", help="Path to .enc file (created if not exists)")
    sdk_edit_p.add_argument(
        "--key", default=None, help="Path to master.key (default: same dir as .enc)"
    )

    sdk_gen_p = sdk_sub.add_parser(
        "generate-schema",
        help="Generate Workato schema from JSON/CSV sample",
        description=(
            "Generate a Workato connector schema from a sample JSON or CSV "
            "file by calling the Platform schema-generation API. Read-only; "
            "prints the resulting schema to stdout."
        ),
    )
    sdk_gen_p.add_argument("file", help="Path to JSON or CSV sample file")

    # -- oauth-profiles --
    oauth_parser = subparsers.add_parser(
        "oauth-profiles", help="Manage custom OAuth profiles"
    )
    oauth_sub = oauth_parser.add_subparsers(dest="oauth_profiles_command")

    oauth_sub.add_parser(
        "list",
        help="List custom OAuth profiles",
        description=(
            "List custom OAuth profiles in the connected workspace. Read-only."
        ),
    )

    oauth_get_p = oauth_sub.add_parser(
        "get",
        help="Get OAuth profile by ID",
        description=(
            "Show a single custom OAuth profile (id, name, provider, data) "
            "by its numeric ID. Read-only."
        ),
    )
    oauth_get_p.add_argument("--id", type=int, required=True)

    oauth_create_p = oauth_sub.add_parser(
        "create",
        help="Create OAuth profile",
        description=(
            "Create a new custom OAuth profile in the connected workspace. "
            "Writes to Workato."
        ),
        epilog=(
            "Examples:\n"
            "  python3 scripts/workato-api.py oauth-profiles create \\\n"
            "      --name \"My App\" --provider slack \\\n"
            "      --client-id <id> --client-secret <secret>\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    oauth_create_p.add_argument("--name", required=True)
    oauth_create_p.add_argument("--provider", required=True)
    oauth_create_p.add_argument("--client-id", required=True)
    oauth_create_p.add_argument("--client-secret", required=True)
    oauth_create_p.add_argument("--token", default=None, help="Token (Slack only)")

    oauth_update_p = oauth_sub.add_parser(
        "update",
        help="Update OAuth profile",
        description=(
            "Update a custom OAuth profile by ID. All identifying fields are "
            "required (name, provider, client_id, client_secret). Writes to "
            "Workato."
        ),
        epilog=(
            "Examples:\n"
            "  python3 scripts/workato-api.py oauth-profiles update --id 123 \\\n"
            "      --name \"My App\" --provider slack \\\n"
            "      --client-id <id> --client-secret <secret>\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    oauth_update_p.add_argument("--id", type=int, required=True)
    oauth_update_p.add_argument("--name", required=True)
    oauth_update_p.add_argument("--provider", required=True)
    oauth_update_p.add_argument("--client-id", required=True)
    oauth_update_p.add_argument("--client-secret", required=True)
    oauth_update_p.add_argument("--token", default=None, help="Token (Slack only)")

    oauth_delete_p = oauth_sub.add_parser(
        "delete",
        help="Delete OAuth profile",
        description=(
            "Delete a custom OAuth profile by ID. Destructive; the profile "
            "is removed from the connected workspace."
        ),
        epilog=(
            "Examples:\n"
            "  python3 scripts/workato-api.py oauth-profiles delete --id 123\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    oauth_delete_p.add_argument("--id", type=int, required=True)

    # -- profile --
    profile_parser = subparsers.add_parser(
        "profile", help="Show resolved profile info"
    )
    profile_sub = profile_parser.add_subparsers(dest="profile_command")
    profile_sub.add_parser(
        "show",
        help="Show current profile resolution",
        description=(
            "Show which profile is currently resolved and how (explicit "
            "--profile, .workatoenv workspace_id match, or current_profile "
            "fallback). Read-only; no Workato API call."
        ),
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Commands that don't need API connection
    if args.command == "profile":
        if getattr(args, "profile_command", None) == "show":
            cmd_profile_show(None, args)
        else:
            profile_parser.print_help()
        return

    if args.command == "sdk" and getattr(args, "sdk_command", None) in ("decrypt", "edit"):
        handler = {"decrypt": cmd_sdk_decrypt, "edit": cmd_sdk_edit}[args.sdk_command]
        handler(None, args)
        return

    # deploy resolves source/target profiles independently of the global
    # --profile flag, so it dispatches before the single-profile setup.
    if args.command == "deploy":
        if getattr(args, "deploy_command", None) == "preview":
            cmd_deploy_preview(None, args)  # type: ignore[arg-type]
        else:
            deploy_parser.print_help()
        return

    # Resolve profile and create API client
    profile_name, profile = resolve_profile(args.profile)
    region_url = profile.get("region_url", "")
    if not region_url:
        print(
            f"Error: No region_url in profile '{profile_name}'.", file=sys.stderr
        )
        sys.exit(1)

    token = get_token(profile_name)
    api = WorkatoAPI(region_url, token)

    # Dispatch
    commands = {
        ("jobs", "list"): cmd_jobs_list,
        ("jobs", "get"): cmd_jobs_get,
        ("connectors", "list-platform"): cmd_connectors_list_platform,
        ("connectors", "list-custom"): cmd_connectors_list_custom,
        ("recipes", "list"): cmd_recipes_list,
        ("sdk", "push"): cmd_sdk_push,
        ("sdk", "pull"): cmd_sdk_pull,
        ("sdk", "generate-schema"): cmd_sdk_generate_schema,
        ("oauth-profiles", "list"): cmd_oauth_profiles_list,
        ("oauth-profiles", "get"): cmd_oauth_profiles_get,
        ("oauth-profiles", "create"): cmd_oauth_profiles_create,
        ("oauth-profiles", "update"): cmd_oauth_profiles_update,
        ("oauth-profiles", "delete"): cmd_oauth_profiles_delete,
    }

    cmd_key = args.command.replace("-", "_")
    sub_cmd = getattr(args, f"{cmd_key}_command", None)
    handler = commands.get((args.command, sub_cmd))
    if handler:
        handler(api, args)
    else:
        # Print subcommand help
        if hasattr(subparsers, "choices") and args.command in subparsers.choices:
            subparsers.choices[args.command].print_help()
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
