#!/usr/bin/env python3
"""Workato Platform API helper.

Complements the official Workato Platform CLI with API calls for features
not available in the CLI (jobs, connectors metadata, recipes list as JSON).

Authentication:
  Reuses the same credentials as the Platform CLI (keyring + ~/.workato/profiles).
  Supports workspace_id-based automatic profile resolution from .workatoenv,
  so .workatoenv never needs to contain a profile name (Git-sharing safe).

Usage:
  python3 scripts/workato-api.py jobs list --recipe-id <id>
    [--status <status>] [--limit <N>]
  python3 scripts/workato-api.py jobs get --recipe-id <id> --job-id <id>
  python3 scripts/workato-api.py jobs tail --recipe-id <id>
    [--status <status>] [--interval <sec>] [--max-iterations <N>]
  python3 scripts/workato-api.py connectors list-platform [--provider <name>]
  python3 scripts/workato-api.py connectors list-custom
  python3 scripts/workato-api.py recipes list [--folder-id <id>]
    [--status running|stopped]
  python3 scripts/workato-api.py recipes start <id> [--dry-run]
    (PUT /api/recipes/:id/start; requires <org>-dev profile)
  python3 scripts/workato-api.py recipes stop <id> [--dry-run]
    (PUT /api/recipes/:id/stop; requires <org>-dev profile)
  python3 scripts/workato-api.py sdk push --connector <path> [--title <t>]
    (auto-detects new vs. update by reading connector_id from
     connectors/docs/<name>.md frontmatter; saves ID back after initial create)
  python3 scripts/workato-api.py sdk pull (--connector-id <id> | --name <name>)
    (downloads connector source to connectors/<name>/connector.rb and saves
     connector_id back to connectors/docs/<name>.md frontmatter)
  python3 scripts/workato-api.py sdk pull-project [--project-dir <path>]
    (wraps `workato pull` in the project directory)
  python3 scripts/workato-api.py sdk diff-project [--project-dir <path>]
    (pulls to a temp dir and diffs against the project directory)
  python3 scripts/workato-api.py sdk edit <file> [--key <master.key>]
  python3 scripts/workato-api.py sdk decrypt <file> [--key <master.key>]
  python3 scripts/workato-api.py deploy preview --to <test|prod>
    [--project-id <id> | --folder-id <id>]
    (read-only preview: same env guard as deploy run, but no API write)
  python3 scripts/workato-api.py deploy run --to <test|prod>
    [--project-id <id> | --folder-id <id>] [--description <text>]
    [--yes] [--wait] [--timeout <sec>]
    (--yes required when --to prod; --wait polls until success/failed)
  python3 scripts/workato-api.py deploy status <deployment-id>
  python3 scripts/workato-api.py deploy list [--project-id <id>]
    [--environment-type <test|prod>] [--state <state>] [--limit <N>]
    [--from-date <iso>] [--to-date <iso>]
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
      (or ship a sibling `preview` subcommand that fulfills the same role —
      see deploy preview)
    - set epilog= with at least one --dry-run / preview example
    - guard environment boundaries in code, not just docs:
        * deploy commands: --to is the only env flag; the source
          environment is inferred from the resolved profile's
          `<org>-<env>` suffix. The (source, --to) pair must be one of
          {(dev, test), (test, prod)} — skip-tier (dev->prod), backward
          (test->dev, prod->*), and same-env transitions are refused
          before any API call.
        * execution deploys with --to prod additionally require --yes
          (CI-friendly confirm); preview commands do not require --yes
          since they have no side effects.
        * Non-deploy state-mutation commands that target a workspace
          (recipes start/stop, and the sdk push / oauth-profiles
          create-update-delete retrofits) refuse unless the resolved
          profile is `<org>-dev`. Direct mutations against test/prod
          workspaces violate the deploy-only promotion policy — those
          changes must arrive via `deploy run`. See
          workato-deployment-flow.md.

  Read-only subcommands (*list, *get, jobs list/get, profile show) do not
  need --dry-run or epilog, but still need help= and description=.

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


def find_workatoenv(start_dir: Path | None = None) -> dict | None:
    """Walk up from `start_dir` (default cwd) to find .workatoenv.

    `start_dir` lets project-aware commands like `sdk pull-project
    --project-dir <path>` resolve the workspace from the *target*
    project, not from the shell's cwd.
    """
    current = start_dir if start_dir is not None else Path.cwd()
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


def resolve_profile(
    explicit_profile: str | None,
    start_dir: Path | None = None,
) -> tuple[str, dict]:
    """Resolve which profile to use.

    Resolution order:
      1. --profile <name> explicitly given
      2. .workatoenv workspace_id (walking up from `start_dir`, default cwd)
         -> match against all profiles
      3. current_profile from ~/.workato/profiles

    `start_dir` is forwarded to find_workatoenv() so callers that
    operate on a specific project directory (e.g. sdk pull-project
    --project-dir) resolve relative to that directory, not cwd.

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
    env = find_workatoenv(start_dir)
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

    def recipe_start(self, recipe_id: int) -> dict:
        """PUT /api/recipes/:id/start — start a recipe.

        State-changing; the caller must enforce the dev-profile
        constraint (require_dev_profile_for_mutation) before invoking.
        """
        result = self._request(
            f"/api/recipes/{recipe_id}/start", method="PUT",
        )
        if isinstance(result, dict):
            return result.get("data", result.get("result", result))
        return result  # type: ignore[return-value]

    def recipe_stop(self, recipe_id: int) -> dict:
        """PUT /api/recipes/:id/stop — stop a recipe.

        State-changing; the caller must enforce the dev-profile
        constraint (require_dev_profile_for_mutation) before invoking.
        """
        result = self._request(
            f"/api/recipes/{recipe_id}/stop", method="PUT",
        )
        if isinstance(result, dict):
            return result.get("data", result.get("result", result))
        return result  # type: ignore[return-value]

    # -- Projects API: deploy --

    def project_deploy(
        self,
        project_ref: str,
        environment_type: str,
        description: str | None = None,
    ) -> dict:
        """Deploy a project to test or prod via the Projects API.

        POST /api/projects/:id/deploy?environment_type=test|prod
        :id accepts either a numeric project_id or `f{folder_id}` (per
        the Workato docs). Returns the Deployment object; state will
        typically be `pending` and require polling via deployment_get().
        """
        body: dict = {}
        if description is not None:
            body["description"] = description
        result = self._request(
            f"/api/projects/{project_ref}/deploy",
            params={"environment_type": environment_type},
            method="POST",
            body=body if body else None,
        )
        if isinstance(result, dict):
            return result.get("data", result.get("result", result))
        return result  # type: ignore[return-value]

    def deployment_get(self, deployment_id: int | str) -> dict:
        """GET /api/deployments/:id — fetch a single deployment record."""
        result = self._request(f"/api/deployments/{deployment_id}")
        if isinstance(result, dict):
            return result.get("data", result.get("result", result))
        return result  # type: ignore[return-value]

    def deployments_list(
        self,
        project_id: int | None = None,
        folder_id: int | None = None,
        environment_type: str | None = None,
        state: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> list:
        """GET /api/deployments — list deployment records with filters.

        Filter values are passed through to the API as-is. `from`/`to`
        are date filters per the docs; their CLI flag names are
        `--from-date` / `--to-date` to avoid clashing with the Python
        keyword `from`.
        """
        params: dict = {}
        if project_id is not None:
            params["project_id"] = project_id
        if folder_id is not None:
            params["folder_id"] = folder_id
        if environment_type is not None:
            params["environment_type"] = environment_type
        if state is not None:
            params["state"] = state
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        result = self._request("/api/deployments", params=params or None)
        if isinstance(result, dict):
            items = result.get("items", result.get("result", result.get("data", [])))
            return items if isinstance(items, list) else []
        return result if isinstance(result, list) else []


# ---------------------------------------------------------------------------
# Deploy helpers (env guard + profile env inference + polling)
# ---------------------------------------------------------------------------


DEPLOY_SOURCE_ENVS = ("dev", "test")
DEPLOY_TARGET_ENVS = ("test", "prod")
ALLOWED_DEPLOY_TRANSITIONS = {("dev", "test"), ("test", "prod")}
DEPLOYMENT_TERMINAL_STATES = {"success", "failed", "succeeded", "failure"}


def infer_profile_env(profile_name: str) -> str | None:
    """Return `dev`, `test`, or `prod` if profile_name ends with `-<env>`.

    Used to derive the source environment from the resolved profile, since
    the Projects deploy API does not take a `--from` flag. Profile names
    that do not follow the `<org>-<env>` convention return None and force
    the caller to explain the constraint.
    """
    for env in ("dev", "test", "prod"):
        suffix = f"-{env}"
        if profile_name.endswith(suffix) and len(profile_name) > len(suffix):
            return env
    return None


def require_dev_profile_for_mutation(profile_name: str, operation: str) -> None:
    """Refuse a non-deploy state mutation unless the profile is <org>-dev.

    Used by commands like `recipes start` / `recipes stop` that mutate
    Workato state directly. The deploy-only promotion policy in
    workato-deployment-flow.md forbids such mutations against
    test/prod workspaces — those changes must arrive via `deploy run`.

    Refuses with a clear message when:
      - the profile name does not follow `<org>-<env>` (cannot prove dev), or
      - the inferred env is anything other than `dev`.
    """
    env = infer_profile_env(profile_name)
    if env == "dev":
        return
    if env is None:
        print(
            f"Error: refusing to {operation} — cannot prove the resolved "
            f"profile '{profile_name}' targets a dev workspace. The "
            f"safety guard requires `<org>-dev` naming (e.g. acme-dev). "
            f"Rename the profile or pass --profile <name> to select one "
            f"that follows the convention.",
            file=sys.stderr,
        )
        sys.exit(1)
    print(
        f"Error: refusing to {operation} against `{env}` workspace "
        f"(profile '{profile_name}'). Direct state mutations are "
        f"allowed only on `<org>-dev` profiles; promote changes to "
        f"test/prod via `deploy run` instead. See "
        f"workato-deployment-flow.md.",
        file=sys.stderr,
    )
    sys.exit(1)


def check_deploy_transition(source_env: str | None, target_env: str) -> None:
    """Refuse invalid (source, target) pairs before any API call.

    Allowed: (dev, test), (test, prod). source_env=None means the profile
    name did not follow the `<org>-<env>` convention; in that case we
    cannot prove the transition is safe, so refuse with a clear message
    about the naming requirement.
    """
    if source_env is None:
        print(
            "Error: cannot infer source environment from the resolved "
            "profile name. The deploy guard requires the profile to "
            "follow `<org>-<env>` (e.g. acme-dev, acme-test) so the "
            "(source, --to) pair can be validated. Rename the profile "
            "or use --profile <name> to select one that follows the "
            "convention.",
            file=sys.stderr,
        )
        sys.exit(1)
    if source_env == target_env:
        print(
            f"Error: source profile is `{source_env}` and --to is "
            f"`{target_env}`. Deploy requires distinct source and target "
            f"environments.",
            file=sys.stderr,
        )
        sys.exit(1)
    if (source_env, target_env) not in ALLOWED_DEPLOY_TRANSITIONS:
        allowed = ", ".join(
            f"{a}->{b}" for a, b in sorted(ALLOWED_DEPLOY_TRANSITIONS)
        )
        print(
            f"Error: deploy {source_env}->{target_env} is not allowed. "
            f"Allowed transitions: {allowed}. Skip-tier (dev->prod), "
            f"backward, and same-env transitions are refused (see "
            f"workato-deployment-flow.md).",
            file=sys.stderr,
        )
        sys.exit(1)


def resolve_project_ref(
    explicit_project_id: int | None,
    explicit_folder_id: int | None,
) -> str:
    """Return the `:id` path segment for /api/projects/:id/deploy.

    Workato accepts either a numeric project_id or `f{folder_id}`.
    Resolution order:
      1. --project-id <int>
      2. --folder-id <int>
      3. .workatoenv folder_id (walking up from cwd)
    Exits with a clear error if none of these resolves, or if both
    --project-id and --folder-id are passed (the CLI also enforces the
    mutex via argparse, but a defense-in-depth check here keeps the
    helper safe for direct callers).
    """
    if explicit_project_id is not None and explicit_folder_id is not None:
        print(
            "Error: --project-id and --folder-id are mutually exclusive; "
            "pass exactly one.",
            file=sys.stderr,
        )
        sys.exit(1)
    if explicit_project_id is not None:
        return str(explicit_project_id)
    if explicit_folder_id is not None:
        return f"f{explicit_folder_id}"
    env_data = find_workatoenv()
    if env_data is not None:
        folder_id = env_data.get("folder_id")
        if isinstance(folder_id, int):
            return f"f{folder_id}"
    print(
        "Error: no --project-id or --folder-id given and no usable "
        "folder_id found in .workatoenv. Run from inside a project, "
        "or pass one of --project-id <id> / --folder-id <id>.",
        file=sys.stderr,
    )
    sys.exit(1)


def poll_deployment(
    api: "WorkatoAPI",
    deployment_id: int | str,
    timeout_seconds: int,
    poll_interval_seconds: float = 2.0,
    _sleep=None,
    _now=None,
) -> dict:
    """Poll GET /api/deployments/:id until state is terminal or timeout hits.

    Returns the final deployment dict. Exits with a clear error if the
    timeout expires before a terminal state is observed. _sleep and _now
    are injection points for tests.
    """
    import time
    sleep = _sleep if _sleep is not None else time.sleep
    now = _now if _now is not None else time.monotonic

    deadline = now() + timeout_seconds
    while True:
        record = api.deployment_get(deployment_id)
        state = (record.get("state") or "").lower() if isinstance(record, dict) else ""
        if state in DEPLOYMENT_TERMINAL_STATES:
            return record
        if now() >= deadline:
            print(
                f"Error: deployment {deployment_id} did not reach a "
                f"terminal state within {timeout_seconds}s "
                f"(last state: {state or 'unknown'}). The deployment "
                f"may still complete server-side; check "
                f"`deploy status {deployment_id}` later.",
                file=sys.stderr,
            )
            sys.exit(1)
        sleep(poll_interval_seconds)


# ---------------------------------------------------------------------------
# CLI Commands
# ---------------------------------------------------------------------------


def cmd_jobs_list(api: WorkatoAPI, args: argparse.Namespace):
    jobs = api.jobs_list(args.recipe_id, args.status)
    if args.limit is not None and args.limit >= 0:
        jobs = jobs[: args.limit]
    print(json.dumps(jobs, indent=2, ensure_ascii=False))


def cmd_jobs_get(api: WorkatoAPI, args: argparse.Namespace):
    job = api.jobs_get(args.recipe_id, args.job_id)
    print(json.dumps(job, indent=2, ensure_ascii=False))


def jobs_tail_loop(
    api: WorkatoAPI,
    recipe_id: int,
    status_filter: str | None,
    interval_seconds: float,
    max_iterations: int | None,
    _sleep=None,
    _print=print,
) -> int:
    """Poll `jobs_list` and print only newly-seen jobs each iteration.

    Returns the number of poll iterations completed (after the priming
    fetch). max_iterations=None means run until KeyboardInterrupt;
    tests pass a finite value plus an injected `_sleep` so the suite
    does not actually wait.

    `_print` is injected so tests can capture per-iteration emissions.
    """
    import time
    sleep = _sleep if _sleep is not None else time.sleep

    # Prime the seen-set with whatever exists right now — we only want
    # to stream NEW jobs from this point forward, not the backlog.
    initial = api.jobs_list(recipe_id, status_filter)
    seen: set = {
        j.get("id") for j in initial
        if isinstance(j, dict) and j.get("id") is not None
    }

    iterations = 0
    try:
        while True:
            if max_iterations is not None and iterations >= max_iterations:
                return iterations
            sleep(interval_seconds)
            iterations += 1
            page = api.jobs_list(recipe_id, status_filter)
            new_jobs = []
            for j in page:
                if not isinstance(j, dict):
                    continue
                jid = j.get("id")
                if jid is None or jid in seen:
                    continue
                seen.add(jid)
                new_jobs.append(j)
            # Workato returns jobs newest-first; reverse so the tail
            # reads top-to-bottom by time, matching `tail -f` semantics.
            for j in reversed(new_jobs):
                _print(json.dumps(j, ensure_ascii=False))
    except KeyboardInterrupt:
        return iterations


def cmd_jobs_tail(api: WorkatoAPI, args: argparse.Namespace):
    """Stream new jobs for a recipe, one JSON object per line.

    Read-only; no env or dev-profile guard. Polling interval defaults
    to 5 seconds. Without --max-iterations, runs until Ctrl+C.
    """
    jobs_tail_loop(
        api,
        recipe_id=args.recipe_id,
        status_filter=args.status,
        interval_seconds=args.interval,
        max_iterations=args.max_iterations,
    )


def cmd_connectors_list_platform(api: WorkatoAPI, args: argparse.Namespace):
    connectors = api.connectors_list_platform(args.provider)
    print(json.dumps(connectors, indent=2, ensure_ascii=False))


def cmd_connectors_list_custom(api: WorkatoAPI, args: argparse.Namespace):
    connectors = api.connectors_list_custom()
    print(json.dumps(connectors, indent=2, ensure_ascii=False))


def cmd_recipes_list(api: WorkatoAPI, args: argparse.Namespace):
    recipes = api.recipes_list(args.folder_id)
    if args.status is not None:
        want_running = (args.status == "running")
        recipes = [
            r for r in recipes
            if isinstance(r, dict) and bool(r.get("running")) is want_running
        ]
    print(json.dumps(recipes, indent=2, ensure_ascii=False))


def cmd_recipes_start(api: WorkatoAPI, args: argparse.Namespace):
    """Start a recipe by ID. Refuses against non-`<org>-dev` profiles."""
    require_dev_profile_for_mutation(
        args._resolved_profile_name, f"start recipe {args.recipe_id}",
    )
    if args.dry_run:
        url = f"{api.base_url}/api/recipes/{args.recipe_id}/start"
        print(json.dumps({
            "mode": "dry-run",
            "would_call": {"method": "PUT", "url": url, "body": None},
            "profile": args._resolved_profile_name,
        }, indent=2, ensure_ascii=False))
        return
    result = api.recipe_start(args.recipe_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_recipes_stop(api: WorkatoAPI, args: argparse.Namespace):
    """Stop a recipe by ID. Refuses against non-`<org>-dev` profiles."""
    require_dev_profile_for_mutation(
        args._resolved_profile_name, f"stop recipe {args.recipe_id}",
    )
    if args.dry_run:
        url = f"{api.base_url}/api/recipes/{args.recipe_id}/stop"
        print(json.dumps({
            "mode": "dry-run",
            "would_call": {"method": "PUT", "url": url, "body": None},
            "profile": args._resolved_profile_name,
        }, indent=2, ensure_ascii=False))
        return
    result = api.recipe_stop(args.recipe_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# deploy preview / run / status (Projects API)
# ---------------------------------------------------------------------------


def _deploy_resolve_profile_and_api(args: argparse.Namespace) -> tuple[str, dict, WorkatoAPI]:
    """Resolve the single source profile, build a WorkatoAPI client.

    Used by all deploy subcommands. Returns (profile_name, profile,
    api). The same workspace token that authenticates the API call is
    the source workspace for the deploy.
    """
    profile_name, profile = resolve_profile(args.profile)
    region_url = profile.get("region_url", "")
    if not region_url:
        print(
            f"Error: profile '{profile_name}' has no region_url.",
            file=sys.stderr,
        )
        sys.exit(1)
    token = get_token(profile_name)
    return profile_name, profile, WorkatoAPI(region_url, token)


def cmd_deploy_preview(_unused: WorkatoAPI | None, args: argparse.Namespace):
    """Print what `deploy run` would call against, without writing.

    Same env-transition guard as `deploy run`. The Projects API has no
    dedicated preview endpoint, so the preview is a planning summary:
    resolved profile, source/target env, project reference, target URL,
    and (when a folder_id is in play) the recipes currently in that
    folder via the read-only /api/recipes endpoint.
    """
    profile_name, profile, api = _deploy_resolve_profile_and_api(args)
    source_env = infer_profile_env(profile_name)
    check_deploy_transition(source_env, args.to_env)

    project_ref = resolve_project_ref(args.project_id, args.folder_id)

    folder_id_for_listing: int | None = None
    if args.folder_id is not None:
        folder_id_for_listing = args.folder_id
    elif args.project_id is None:
        env_data = find_workatoenv()
        if env_data is not None and isinstance(env_data.get("folder_id"), int):
            folder_id_for_listing = env_data["folder_id"]

    recipes_preview: list = []
    if folder_id_for_listing is not None:
        recipes_preview = api.recipes_list(folder_id_for_listing)

    region_url = profile.get("region_url", "")
    target_url = (
        f"{region_url.rstrip('/')}/api/projects/{project_ref}/deploy"
        f"?environment_type={args.to_env}"
    )
    output = {
        "mode": "preview",
        "profile": profile_name,
        "workspace_url": region_url,
        "source_env": source_env,
        "target_env": args.to_env,
        "project_ref": project_ref,
        "would_call": {
            "method": "POST",
            "url": target_url,
            "body": {"description": args.description} if args.description else {},
        },
        "recipes_in_folder": [
            {"id": r.get("id"), "name": r.get("name"), "running": r.get("running")}
            for r in recipes_preview
            if isinstance(r, dict)
        ],
        "notes": [
            "No API writes were performed.",
            "Run `deploy run` with the same arguments to execute (requires "
            "--yes when --to prod).",
        ],
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


def cmd_deploy_run(_unused: WorkatoAPI | None, args: argparse.Namespace):
    """Execute a deploy via POST /api/projects/:id/deploy.

    Runs the same env guard as preview, refuses --to prod without
    --yes, then POSTs the deploy. With --wait, polls
    GET /api/deployments/:id until state is terminal or --timeout
    seconds elapse. Without --wait, returns immediately with the
    pending Deployment record.
    """
    profile_name, _profile, api = _deploy_resolve_profile_and_api(args)
    source_env = infer_profile_env(profile_name)
    check_deploy_transition(source_env, args.to_env)

    if args.to_env == "prod" and not args.yes:
        print(
            "Error: `deploy run --to prod` is destructive and requires "
            "--yes to confirm. Re-run with --yes (typically after a "
            "successful test deploy and release-manager sign-off).",
            file=sys.stderr,
        )
        sys.exit(1)

    project_ref = resolve_project_ref(args.project_id, args.folder_id)

    record = api.project_deploy(
        project_ref=project_ref,
        environment_type=args.to_env,
        description=args.description,
    )

    if not args.wait:
        print(json.dumps(record, indent=2, ensure_ascii=False))
        return

    deployment_id = record.get("id") if isinstance(record, dict) else None
    if deployment_id is None:
        print(
            "Error: deploy POST succeeded but the response did not "
            "include a deployment id; cannot poll.",
            file=sys.stderr,
        )
        print(json.dumps(record, indent=2, ensure_ascii=False))
        sys.exit(1)

    final = poll_deployment(api, deployment_id, args.timeout)
    print(json.dumps(final, indent=2, ensure_ascii=False))
    state = (final.get("state") or "").lower() if isinstance(final, dict) else ""
    if state not in ("success", "succeeded"):
        sys.exit(1)


def cmd_deploy_status(_unused: WorkatoAPI | None, args: argparse.Namespace):
    """Fetch a single deployment record by id (read-only)."""
    _, _, api = _deploy_resolve_profile_and_api(args)
    record = api.deployment_get(args.deployment_id)
    print(json.dumps(record, indent=2, ensure_ascii=False))


def cmd_deploy_list(_unused: WorkatoAPI | None, args: argparse.Namespace):
    """List deployment records with optional filter passthrough.

    Read-only; no env-transition guard. The resolved profile determines
    which workspace's deployments are listed.
    """
    _, _, api = _deploy_resolve_profile_and_api(args)
    items = api.deployments_list(
        project_id=args.project_id,
        folder_id=args.folder_id,
        environment_type=args.environment_type,
        state=args.state,
        from_date=args.from_date,
        to_date=args.to_date,
    )
    if args.limit is not None and args.limit >= 0:
        items = items[: args.limit]
    print(json.dumps(items, indent=2, ensure_ascii=False))


def cmd_oauth_profiles_list(api: WorkatoAPI, args: argparse.Namespace):
    profiles = api.oauth_profiles_list()
    print(json.dumps(profiles, indent=2, ensure_ascii=False))


def cmd_oauth_profiles_get(api: WorkatoAPI, args: argparse.Namespace):
    profile = api.oauth_profiles_get(args.id)
    print(json.dumps(profile, indent=2, ensure_ascii=False))


def _redact_oauth_body(body: dict) -> dict:
    """Return a deep-copied body with secrets masked for dry-run output.

    --dry-run writes to stdout, which CI logs and `tee` will capture.
    The CLI already accepted the secret in argv, so we are not creating
    a new exposure, but emitting the secret a second time in pipeline
    logs is unnecessary. Mask `data.client_secret` and `data.token`.
    """
    safe = json.loads(json.dumps(body))
    data = safe.get("data") if isinstance(safe, dict) else None
    if isinstance(data, dict):
        for key in ("client_secret", "token"):
            if key in data and data[key] is not None:
                data[key] = "***REDACTED***"
    return safe


def _oauth_dry_run_output(method: str, path: str, body: dict | None,
                           profile_name: str, base_url: str) -> dict:
    payload = {
        "mode": "dry-run",
        "would_call": {
            "method": method,
            "url": f"{base_url.rstrip('/')}{path}",
            "body": _redact_oauth_body(body) if body is not None else None,
        },
        "profile": profile_name,
    }
    return payload


def cmd_oauth_profiles_create(api: WorkatoAPI, args: argparse.Namespace):
    require_dev_profile_for_mutation(
        args._resolved_profile_name, f"create OAuth profile '{args.name}'",
    )
    body: dict = {
        "name": args.name, "provider": args.provider,
        "data": {"client_id": args.client_id, "client_secret": args.client_secret},
    }
    if args.token is not None:
        body["data"]["token"] = args.token
    if args.dry_run:
        print(json.dumps(_oauth_dry_run_output(
            "POST", "/api/custom_oauth_profiles", body,
            args._resolved_profile_name, api.base_url,
        ), indent=2, ensure_ascii=False))
        return
    result = api.oauth_profiles_create(
        name=args.name, provider=args.provider,
        client_id=args.client_id, client_secret=args.client_secret,
        token=args.token,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nCreated OAuth profile: {result.get('name', args.name)}", file=sys.stderr)


def cmd_oauth_profiles_update(api: WorkatoAPI, args: argparse.Namespace):
    require_dev_profile_for_mutation(
        args._resolved_profile_name, f"update OAuth profile id={args.id}",
    )
    body: dict = {
        "name": args.name, "provider": args.provider,
        "data": {"client_id": args.client_id, "client_secret": args.client_secret},
    }
    if args.token is not None:
        body["data"]["token"] = args.token
    if args.dry_run:
        print(json.dumps(_oauth_dry_run_output(
            "PUT", f"/api/custom_oauth_profiles/{args.id}", body,
            args._resolved_profile_name, api.base_url,
        ), indent=2, ensure_ascii=False))
        return
    result = api.oauth_profiles_update(
        profile_id=args.id, name=args.name, provider=args.provider,
        client_id=args.client_id, client_secret=args.client_secret,
        token=args.token,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nUpdated OAuth profile: {result.get('name', args.name)}", file=sys.stderr)


def cmd_oauth_profiles_delete(api: WorkatoAPI, args: argparse.Namespace):
    require_dev_profile_for_mutation(
        args._resolved_profile_name, f"delete OAuth profile id={args.id}",
    )
    if args.dry_run:
        print(json.dumps(_oauth_dry_run_output(
            "DELETE", f"/api/custom_oauth_profiles/{args.id}", None,
            args._resolved_profile_name, api.base_url,
        ), indent=2, ensure_ascii=False))
        return
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


def _invoke_workato_pull(
    profile_name: str, cwd: Path,
    _runner=None,
) -> tuple[int, str, str]:
    """Invoke `workato --profile <name> pull` in `cwd`.

    Returns (returncode, stdout, stderr). Never raises; callers decide
    how to surface failures. `_runner` is an injection point for tests
    (a callable taking (cmd_list, cwd) and returning (rc, stdout, stderr)).
    """
    if _runner is not None:
        return _runner(["workato", "--profile", profile_name, "pull"], cwd)
    result = subprocess.run(
        ["workato", "--profile", profile_name, "pull"],
        cwd=str(cwd),
        capture_output=True, text=True,
    )
    return result.returncode, result.stdout, result.stderr


def _validate_project_dir(project_dir: Path) -> None:
    """Refuse if project_dir lacks .workatoenv (workato pull would fail)."""
    if not project_dir.is_dir():
        print(
            f"Error: project dir '{project_dir}' does not exist.",
            file=sys.stderr,
        )
        sys.exit(1)
    if not (project_dir / ".workatoenv").exists():
        print(
            f"Error: '{project_dir}' has no .workatoenv. `workato pull` "
            f"reads the workspace/folder from .workatoenv, so it must "
            f"be run from inside a project directory.",
            file=sys.stderr,
        )
        sys.exit(1)


PROJECT_EXCLUDE_PATTERNS = (".git", ".venv", "node_modules", "__pycache__")


def _resolve_project_profile(
    explicit_profile: str | None, project_dir: Path,
) -> str:
    """Resolve the profile name from the *target* project directory.

    `args._resolved_profile_name` is set by main() from cwd's
    .workatoenv; when --project-dir points elsewhere, that name can
    select the wrong workspace. Re-resolve relative to project_dir so
    the workspace matches the project being pulled / diffed.
    """
    name, _ = resolve_profile(explicit_profile, start_dir=project_dir)
    return name


def cmd_sdk_pull_project(_api: WorkatoAPI | None, args: argparse.Namespace):
    """Pull project assets from the resolved Workato workspace.

    Thin wrapper around `workato --profile <name> pull` that adds
    profile auto-resolution from the target project's .workatoenv.
    Read-only against Workato (only modifies local files in
    `--project-dir`, default cwd). No env-transition guard — pull is
    allowed against any profile per workato-deployment-flow.md.
    """
    project_dir = Path(args.project_dir).resolve() if args.project_dir else Path.cwd()
    _validate_project_dir(project_dir)
    profile_name = _resolve_project_profile(args.profile, project_dir)
    rc, out, err = _invoke_workato_pull(profile_name, project_dir)
    if out:
        sys.stdout.write(out)
        if not out.endswith("\n"):
            sys.stdout.write("\n")
    if err:
        sys.stderr.write(err)
        if not err.endswith("\n"):
            sys.stderr.write("\n")
    sys.exit(rc)


def _diff_argv(local: Path, pulled: Path) -> list[str]:
    """Build the `diff -ru` argv with exclusions matching copytree's ignore set.

    The exclude list MUST mirror PROJECT_EXCLUDE_PATTERNS so the temp
    copy and the local tree are compared on the same surface; otherwise
    a local-only `.venv` would always register as "only in local" and
    diff-project would exit 1 even when Workato-managed assets are
    identical.
    """
    argv = ["diff", "-ru"]
    for pattern in PROJECT_EXCLUDE_PATTERNS:
        argv.extend(["--exclude", pattern])
    argv.extend([str(local), str(pulled)])
    return argv


def _run_diff(local: Path, pulled: Path, _runner=None) -> tuple[int, str, str]:
    """Invoke `diff -ru` between two directories. Returns (rc, stdout, stderr).

    diff's exit codes: 0 = identical, 1 = differ, 2 = error.
    """
    argv = _diff_argv(local, pulled)
    if _runner is not None:
        return _runner(argv, None)
    result = subprocess.run(argv, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def cmd_sdk_diff_project(_api: WorkatoAPI | None, args: argparse.Namespace):
    """Show diff between local project and dev workspace state.

    Copies the project directory to a temp dir (excluding bulky local
    dirs like .git / .venv / node_modules / __pycache__), runs
    `workato pull` in the copy so the temp tree reflects the remote
    state, then runs `diff -ru` between the local project and the
    pulled copy using the same exclude set. Read-only — the original
    project directory is never modified.

    Exit codes mirror diff(1): 0 = identical, 1 = differences printed,
    2 = the pull or the diff itself failed.
    """
    import shutil
    project_dir = Path(args.project_dir).resolve() if args.project_dir else Path.cwd()
    _validate_project_dir(project_dir)
    profile_name = _resolve_project_profile(args.profile, project_dir)

    with tempfile.TemporaryDirectory(prefix="kit-sdk-diff-") as tmp:
        pulled_root = Path(tmp) / "pulled"
        # Copy the project to a temp dir; exclude VCS and bulky local
        # directories so the pull does not waste time on irrelevant
        # files. The same exclude set is passed to `diff -ru` below
        # (see _diff_argv) so the comparison surface matches.
        ignore = shutil.ignore_patterns(*PROJECT_EXCLUDE_PATTERNS)
        shutil.copytree(project_dir, pulled_root, ignore=ignore)

        rc, _out, err = _invoke_workato_pull(profile_name, pulled_root)
        if rc != 0:
            sys.stderr.write(
                f"Error: `workato pull` failed in temp copy "
                f"(exit {rc}). stderr:\n{err}"
            )
            sys.exit(2)

        diff_rc, diff_out, diff_err = _run_diff(project_dir, pulled_root)
        if diff_out:
            sys.stdout.write(diff_out)
            if not diff_out.endswith("\n"):
                sys.stdout.write("\n")
        if diff_rc == 2:
            sys.stderr.write(
                f"Error: `diff -ru` failed (exit 2). stderr:\n{diff_err}"
            )
            sys.exit(2)
        sys.exit(diff_rc)


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
    require_dev_profile_for_mutation(
        args._resolved_profile_name, f"push connector {args.connector}",
    )

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

    if args.dry_run:
        # Show what would be sent without calling the API. The source
        # code can be large, so emit a summary (length + title) rather
        # than the full body. The release follow-up is reported
        # explicitly so users know what they're authorizing.
        if is_update:
            method, path = "PUT", f"/api/custom_connectors/{resolved_id}"
        else:
            method, path = "POST", "/api/custom_connectors"
        print(json.dumps({
            "mode": "dry-run",
            "would_call": {
                "method": method,
                "url": f"{api.base_url.rstrip('/')}{path}",
                "body_summary": {
                    "code_length": len(source_code),
                    "title": title,
                    "description_set": bool(args.description),
                    "notes_set": bool(args.notes),
                },
            },
            "would_release": not args.no_release,
            "profile": args._resolved_profile_name,
            "docs_path": str(docs_path),
            "is_update": is_update,
        }, indent=2, ensure_ascii=False))
        return

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
            "Optionally filter by status (e.g. failed, success). "
            "--limit caps the output client-side. Read-only."
        ),
    )
    jobs_list_p.add_argument("--recipe-id", type=int, required=True)
    jobs_list_p.add_argument("--status", default=None, help="Filter by status")
    jobs_list_p.add_argument(
        "--limit", type=int, default=None,
        help="Cap the number of jobs returned (client-side)",
    )

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

    jobs_tail_p = jobs_sub.add_parser(
        "tail",
        help="Stream new jobs as they appear",
        description=(
            "Poll the jobs endpoint and print only newly-seen jobs each "
            "iteration, one JSON object per line. Read-only. The initial "
            "fetch is used to prime the seen-set, so existing jobs are "
            "NOT printed — only ones that appear after the command starts. "
            "Default interval is 5 seconds; without --max-iterations the "
            "command runs until Ctrl+C."
        ),
        epilog=(
            "Examples:\n"
            "  # Tail failed jobs for a recipe, refreshing every 10s\n"
            "  python3 scripts/workato-api.py jobs tail --recipe-id 12345 \\\n"
            "      --status failed --interval 10\n\n"
            "  # Tail for at most 6 polling iterations (e.g. ~30s at 5s interval)\n"
            "  python3 scripts/workato-api.py jobs tail --recipe-id 12345 \\\n"
            "      --max-iterations 6\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    jobs_tail_p.add_argument("--recipe-id", type=int, required=True)
    jobs_tail_p.add_argument(
        "--status", default=None, help="Filter by status (e.g. failed)",
    )
    jobs_tail_p.add_argument(
        "--interval", type=float, default=5.0,
        help="Polling interval in seconds (default: 5.0)",
    )
    jobs_tail_p.add_argument(
        "--max-iterations", dest="max_iterations", type=int, default=None,
        help="Stop after N polling iterations (default: run until Ctrl+C)",
    )

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
            "pagination. Optionally filter by folder, and by run state "
            "(running/stopped, filtered client-side on the `running` "
            "field). Read-only."
        ),
    )
    recipes_list_p.add_argument(
        "--folder-id", type=int, default=None, help="Filter by folder ID"
    )
    recipes_list_p.add_argument(
        "--status", choices=("running", "stopped"), default=None,
        help="Filter by run state (client-side filter on the `running` field)",
    )

    recipes_start_p = recipes_sub.add_parser(
        "start",
        help="Start a recipe (PUT /api/recipes/:id/start)",
        description=(
            "Start a recipe by numeric ID. Refuses unless the resolved "
            "profile is `<org>-dev` — direct mutations against test/prod "
            "violate the deploy-only promotion policy. Use --dry-run to "
            "print the intended request without sending it."
        ),
        epilog=(
            "Examples:\n"
            "  # Dry run: print the URL that would be called\n"
            "  python3 scripts/workato-api.py recipes start 12345 --dry-run\n\n"
            "  # Start a recipe in the dev workspace\n"
            "  python3 scripts/workato-api.py recipes start 12345\n\n"
            "  # Refused: profile is not `<org>-dev`\n"
            "  python3 scripts/workato-api.py recipes start 12345 --profile acme-prod\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    recipes_start_p.add_argument("recipe_id", type=int, help="Recipe ID")
    recipes_start_p.add_argument(
        "--dry-run", action="store_true",
        help="Print the intended PUT request without sending it",
    )

    recipes_stop_p = recipes_sub.add_parser(
        "stop",
        help="Stop a recipe (PUT /api/recipes/:id/stop)",
        description=(
            "Stop a recipe by numeric ID. Refuses unless the resolved "
            "profile is `<org>-dev` — direct mutations against test/prod "
            "violate the deploy-only promotion policy. Use --dry-run to "
            "print the intended request without sending it."
        ),
        epilog=(
            "Examples:\n"
            "  python3 scripts/workato-api.py recipes stop 12345 --dry-run\n"
            "  python3 scripts/workato-api.py recipes stop 12345\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    recipes_stop_p.add_argument("recipe_id", type=int, help="Recipe ID")
    recipes_stop_p.add_argument(
        "--dry-run", action="store_true",
        help="Print the intended PUT request without sending it",
    )

    # -- deploy (Projects API) --
    deploy_parser = subparsers.add_parser(
        "deploy",
        help="Promote a project from dev->test or test->prod",
    )
    deploy_sub = deploy_parser.add_subparsers(dest="deploy_command")

    def _add_deploy_common(p: argparse.ArgumentParser, with_description: bool):
        p.add_argument(
            "--to", dest="to_env", choices=DEPLOY_TARGET_ENVS, required=True,
            help="Target environment (test or prod)",
        )
        # --project-id and --folder-id are alternate ways to name the
        # deploy target; passing both at once is an error (argparse
        # enforces this — silent precedence would be a footgun for a
        # state-changing command).
        target_group = p.add_mutually_exclusive_group()
        target_group.add_argument(
            "--project-id", type=int, default=None,
            help="Project ID (mutually exclusive with --folder-id)",
        )
        target_group.add_argument(
            "--folder-id", type=int, default=None,
            help="Folder ID (becomes `f<id>` in the deploy URL; "
                 "mutually exclusive with --project-id). "
                 "Default: folder_id from .workatoenv in cwd.",
        )
        if with_description:
            p.add_argument(
                "--description", default=None,
                help="Optional deployment description (for audit log)",
            )

    deploy_preview_p = deploy_sub.add_parser(
        "preview",
        help="Preview what `deploy run` would call",
        description=(
            "Print what `deploy run` would call against, without writing "
            "to the workspace. Runs the same env-transition guard as "
            "`deploy run`: the source environment is inferred from the "
            "resolved profile's `<org>-<env>` suffix, and only "
            "(dev, test) and (test, prod) are allowed. Lists recipes in "
            "the resolved folder for context when a folder_id is in play."
        ),
        epilog=(
            "Examples:\n"
            "  # Preview a dev -> test deploy (folder_id from .workatoenv)\n"
            "  python3 scripts/workato-api.py deploy preview --to test\n\n"
            "  # Preview a test -> prod deploy with an explicit folder\n"
            "  python3 scripts/workato-api.py deploy preview --to prod \\\n"
            "      --folder-id 12345 --profile acme-test\n\n"
            "  # Skip-tier (dev profile -> --to prod) is refused before any API call.\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _add_deploy_common(deploy_preview_p, with_description=True)

    deploy_run_p = deploy_sub.add_parser(
        "run",
        help="Execute a deploy (POST /api/projects/:id/deploy)",
        description=(
            "Execute a deploy from the connected workspace to the --to "
            "environment via the Projects API. Refuses unsafe transitions "
            "(only dev->test and test->prod are allowed). --to prod also "
            "requires --yes. With --wait, polls the deployment until "
            "state becomes terminal or --timeout seconds elapse."
        ),
        epilog=(
            "Examples:\n"
            "  # Preview first (read-only, no API write):\n"
            "  python3 scripts/workato-api.py deploy preview --to test\n\n"
            "  # Execute a dev -> test deploy and wait for it to finish:\n"
            "  python3 scripts/workato-api.py deploy run --to test --wait\n\n"
            "  # Execute a test -> prod deploy (--yes is required):\n"
            "  python3 scripts/workato-api.py deploy run --to prod --yes --wait \\\n"
            "      --description \"Release 2026-06-02\" --profile acme-test\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _add_deploy_common(deploy_run_p, with_description=True)
    deploy_run_p.add_argument(
        "--yes", action="store_true",
        help="Required confirmation when --to prod (CI-friendly)",
    )
    deploy_run_p.add_argument(
        "--wait", action="store_true",
        help="Poll until the deployment reaches a terminal state",
    )
    deploy_run_p.add_argument(
        "--timeout", type=int, default=300,
        help="Polling timeout in seconds (default: 300)",
    )

    deploy_status_p = deploy_sub.add_parser(
        "status",
        help="Get a single deployment's state",
        description=(
            "Fetch and print a single deployment record by ID "
            "(GET /api/deployments/:id). Read-only. The profile must "
            "point at the workspace that owns the deployment "
            "(typically the target workspace, e.g. test for a "
            "dev->test deploy)."
        ),
    )
    deploy_status_p.add_argument(
        "deployment_id", type=int,
        help="Deployment ID returned by `deploy run`",
    )

    deploy_list_p = deploy_sub.add_parser(
        "list",
        help="List deployments with filters",
        description=(
            "List deployment records from the workspace the resolved "
            "profile points at (GET /api/deployments). Read-only. All "
            "filters are optional; the API returns the items array as "
            "JSON, with --limit applied client-side."
        ),
        epilog=(
            "Examples:\n"
            "  # Latest 5 deployments to test from the connected workspace\n"
            "  python3 scripts/workato-api.py deploy list \\\n"
            "      --environment-type test --limit 5\n\n"
            "  # All failed prod deployments for one project\n"
            "  python3 scripts/workato-api.py deploy list \\\n"
            "      --project-id 42 --environment-type prod --state failed\n\n"
            "  # Deployments since a specific date\n"
            "  python3 scripts/workato-api.py deploy list \\\n"
            "      --from-date 2026-06-01 --to-date 2026-06-30\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    deploy_list_target_group = deploy_list_p.add_mutually_exclusive_group()
    deploy_list_target_group.add_argument(
        "--project-id", type=int, default=None,
        help="Filter by project ID (mutually exclusive with --folder-id)",
    )
    deploy_list_target_group.add_argument(
        "--folder-id", type=int, default=None,
        help="Filter by folder ID (mutually exclusive with --project-id)",
    )
    deploy_list_p.add_argument(
        "--environment-type", choices=DEPLOY_TARGET_ENVS, default=None,
        help="Filter by target environment (test or prod)",
    )
    deploy_list_p.add_argument(
        "--state", default=None,
        help="Filter by deployment state (e.g. pending, success, failed)",
    )
    deploy_list_p.add_argument(
        "--from-date", dest="from_date", default=None,
        help="Filter by deployment created_at >= this ISO date",
    )
    deploy_list_p.add_argument(
        "--to-date", dest="to_date", default=None,
        help="Filter by deployment created_at <= this ISO date",
    )
    deploy_list_p.add_argument(
        "--limit", type=int, default=None,
        help="Cap the number of items returned (client-side)",
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
            "after an initial create. Refuses unless the resolved profile is "
            "`<org>-dev` — direct mutations against test/prod must go via "
            "`deploy run` instead."
        ),
        epilog=(
            "Examples:\n"
            "  # Dry run: print intended URL + body summary, no API call\n"
            "  python3 scripts/workato-api.py sdk push --connector connectors/foo/connector.rb --dry-run\n\n"
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
    sdk_push_p.add_argument(
        "--dry-run", action="store_true",
        help="Print intended POST/PUT (and release follow-up) without sending",
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

    sdk_pull_project_p = sdk_sub.add_parser(
        "pull-project",
        help="Pull all project assets via `workato pull`",
        description=(
            "Pull project assets (recipes, connections, lookup tables, "
            "etc.) from the resolved Workato workspace by invoking "
            "`workato --profile <name> pull` in the project directory. "
            "Thin wrapper: profile is auto-resolved from .workatoenv. "
            "Read-only against Workato; only local files are modified."
        ),
        epilog=(
            "Examples:\n"
            "  # Pull into the current project directory\n"
            "  python3 scripts/workato-api.py sdk pull-project\n\n"
            "  # Pull into an explicit project directory\n"
            "  python3 scripts/workato-api.py sdk pull-project --project-dir projects/my-app\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sdk_pull_project_p.add_argument(
        "--project-dir", default=None,
        help="Project directory to pull into (default: cwd). Must contain .workatoenv.",
    )

    sdk_diff_project_p = sdk_sub.add_parser(
        "diff-project",
        help="Diff local project against dev workspace",
        description=(
            "Show differences between the local project and the "
            "resolved Workato workspace. Copies the project to a temp "
            "dir, runs `workato pull` in the copy so it reflects the "
            "remote state, then `diff -ru` between local and pulled. "
            "Read-only — does not modify the original project directory. "
            "Exit code: 0 = identical, 1 = differences printed, 2 = error."
        ),
        epilog=(
            "Examples:\n"
            "  # Diff the current project against dev\n"
            "  python3 scripts/workato-api.py sdk diff-project\n\n"
            "  # Diff an explicit project directory\n"
            "  python3 scripts/workato-api.py sdk diff-project --project-dir projects/my-app\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sdk_diff_project_p.add_argument(
        "--project-dir", default=None,
        help="Project directory to diff (default: cwd). Must contain .workatoenv.",
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
            "Refuses unless the resolved profile is `<org>-dev` — direct "
            "mutations against test/prod must go via `deploy run` instead. "
            "Writes to Workato."
        ),
        epilog=(
            "Examples:\n"
            "  # Dry run: print intended POST with secrets redacted\n"
            "  python3 scripts/workato-api.py oauth-profiles create --dry-run \\\n"
            "      --name \"My App\" --provider slack \\\n"
            "      --client-id <id> --client-secret <secret>\n\n"
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
    oauth_create_p.add_argument(
        "--dry-run", action="store_true",
        help="Print intended POST (secrets redacted) without sending it",
    )

    oauth_update_p = oauth_sub.add_parser(
        "update",
        help="Update OAuth profile",
        description=(
            "Update a custom OAuth profile by ID. All identifying fields are "
            "required (name, provider, client_id, client_secret). Refuses "
            "unless the resolved profile is `<org>-dev` — direct mutations "
            "against test/prod must go via `deploy run` instead. Writes to "
            "Workato."
        ),
        epilog=(
            "Examples:\n"
            "  # Dry run: print intended PUT with secrets redacted\n"
            "  python3 scripts/workato-api.py oauth-profiles update --id 123 --dry-run \\\n"
            "      --name \"My App\" --provider slack \\\n"
            "      --client-id <id> --client-secret <secret>\n\n"
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
    oauth_update_p.add_argument(
        "--dry-run", action="store_true",
        help="Print intended PUT (secrets redacted) without sending it",
    )

    oauth_delete_p = oauth_sub.add_parser(
        "delete",
        help="Delete OAuth profile",
        description=(
            "Delete a custom OAuth profile by ID. Destructive; the profile "
            "is removed from the connected workspace. Refuses unless the "
            "resolved profile is `<org>-dev`."
        ),
        epilog=(
            "Examples:\n"
            "  # Dry run: print the DELETE that would be sent\n"
            "  python3 scripts/workato-api.py oauth-profiles delete --id 123 --dry-run\n\n"
            "  python3 scripts/workato-api.py oauth-profiles delete --id 123\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    oauth_delete_p.add_argument("--id", type=int, required=True)
    oauth_delete_p.add_argument(
        "--dry-run", action="store_true",
        help="Print the intended DELETE request without sending it",
    )

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

    # These sdk subcommands do not touch the Workato API directly:
    # decrypt/edit operate on local .enc files, and pull-project/diff-project
    # shell out to `workato pull`. Dispatch before the main() profile-and-token
    # bootstrap so keyring problems do not block workflows that don't need a
    # Python-side token.
    _sdk_pre_api = {
        "decrypt": cmd_sdk_decrypt,
        "edit": cmd_sdk_edit,
        "pull-project": cmd_sdk_pull_project,
        "diff-project": cmd_sdk_diff_project,
    }
    if args.command == "sdk" and getattr(args, "sdk_command", None) in _sdk_pre_api:
        _sdk_pre_api[args.sdk_command](None, args)
        return

    # deploy handlers manage their own profile/token resolution so they
    # can run the env-transition guard before any API client is built.
    if args.command == "deploy":
        deploy_handlers = {
            "preview": cmd_deploy_preview,
            "run": cmd_deploy_run,
            "status": cmd_deploy_status,
            "list": cmd_deploy_list,
        }
        sub = getattr(args, "deploy_command", None)
        if sub in deploy_handlers:
            deploy_handlers[sub](None, args)
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
    # Make the resolved profile name visible to handlers that need to
    # apply env-aware guards (e.g. recipes start/stop's dev-only check).
    args._resolved_profile_name = profile_name

    # Dispatch
    commands = {
        ("jobs", "list"): cmd_jobs_list,
        ("jobs", "get"): cmd_jobs_get,
        ("jobs", "tail"): cmd_jobs_tail,
        ("connectors", "list-platform"): cmd_connectors_list_platform,
        ("connectors", "list-custom"): cmd_connectors_list_custom,
        ("recipes", "list"): cmd_recipes_list,
        ("recipes", "start"): cmd_recipes_start,
        ("recipes", "stop"): cmd_recipes_stop,
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
