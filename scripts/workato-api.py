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
  python3 scripts/workato-api.py profile show

Global options:
  --profile <name>   Use a specific profile instead of auto-resolution
"""

import argparse
import json
import os
import sys
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
    if env and "workspace_id" in env:
        target_ws = env["workspace_id"]
        for name, prof in profiles.items():
            if prof.get("workspace_id") == target_ws:
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


def get_token(profile_name: str) -> str:
    """Retrieve API token for a profile.

    Tries in order:
      1. WORKATO_API_TOKEN env var
      2. Python keyring (same as Platform CLI)
      3. ~/.workato/token_store.json
    """
    # 1. Environment variable
    env_token = os.environ.get("WORKATO_API_TOKEN")
    if env_token:
        return env_token

    # 2. Keyring
    try:
        import keyring

        token = keyring.get_password(KEYRING_SERVICE, profile_name)
        if token:
            return token
    except (ImportError, Exception) as e:
        print(f"Warning: keyring unavailable ({e}), trying fallback.", file=sys.stderr)

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

    def _request(self, path: str, params: dict | None = None) -> dict | list:
        url = f"{self.base_url}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(
                {k: v for k, v in params.items() if v is not None}
            )

        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode() if e.fp else ""
            print(
                f"Error: HTTP {e.code} {e.reason}\n"
                f"URL: {url}\n"
                f"Response: {body}",
                file=sys.stderr,
            )
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"Error: {e.reason}\nURL: {url}", file=sys.stderr)
            sys.exit(1)

    # -- Jobs --

    def jobs_list(self, recipe_id: int, status: str | None = None) -> list:
        params = {}
        if status:
            params["status"] = status
        result = self._request(f"/api/recipes/{recipe_id}/jobs", params)
        return result if isinstance(result, list) else result.get("items", [])

    def jobs_get(self, recipe_id: int, job_id: int) -> dict:
        return self._request(f"/api/recipes/{recipe_id}/jobs/{job_id}")

    # -- Connectors --

    def connectors_list_platform(self, provider: str | None = None) -> list:
        """Get Pre-built connector metadata. Paginates automatically."""
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
            all_connectors.extend(items)
            if len(items) < per_page:
                break
            page += 1

        if provider:
            all_connectors = [
                c
                for c in all_connectors
                if c.get("name", "").lower() == provider.lower()
                or c.get("provider", "").lower() == provider.lower()
            ]

        return all_connectors

    def connectors_list_custom(self) -> list:
        result = self._request("/api/custom_connectors")
        return result if isinstance(result, list) else result.get("result", [])

    # -- Recipes --

    def recipes_list(self, folder_id: int | None = None) -> list:
        params = {}
        if folder_id:
            params["folder_id"] = folder_id
        result = self._request("/api/recipes", params)
        if isinstance(result, dict):
            return result.get("items", result.get("result", []))
        return result


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
            if env and env.get("workspace_id") == profile.get("workspace_id")
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

    jobs_list_p = jobs_sub.add_parser("list", help="List jobs for a recipe")
    jobs_list_p.add_argument("--recipe-id", type=int, required=True)
    jobs_list_p.add_argument("--status", default=None, help="Filter by status")

    jobs_get_p = jobs_sub.add_parser("get", help="Get job details")
    jobs_get_p.add_argument("--recipe-id", type=int, required=True)
    jobs_get_p.add_argument("--job-id", type=int, required=True)

    # -- connectors --
    conn_parser = subparsers.add_parser("connectors", help="Manage connectors")
    conn_sub = conn_parser.add_subparsers(dest="connectors_command")

    conn_platform_p = conn_sub.add_parser(
        "list-platform", help="List Pre-built connectors"
    )
    conn_platform_p.add_argument(
        "--provider", default=None, help="Filter by provider name"
    )

    conn_sub.add_parser("list-custom", help="List custom connectors")

    # -- recipes --
    recipes_parser = subparsers.add_parser("recipes", help="Manage recipes")
    recipes_sub = recipes_parser.add_subparsers(dest="recipes_command")

    recipes_list_p = recipes_sub.add_parser("list", help="List recipes (JSON)")
    recipes_list_p.add_argument(
        "--folder-id", type=int, default=None, help="Filter by folder ID"
    )

    # -- profile --
    profile_parser = subparsers.add_parser(
        "profile", help="Show resolved profile info"
    )
    profile_sub = profile_parser.add_subparsers(dest="profile_command")
    profile_sub.add_parser("show", help="Show current profile resolution")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # profile show doesn't need API connection
    if args.command == "profile":
        if getattr(args, "profile_command", None) == "show":
            cmd_profile_show(None, args)
        else:
            profile_parser.print_help()
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
    }

    sub_cmd = getattr(args, f"{args.command}_command", None)
    handler = commands.get((args.command, sub_cmd))
    if handler:
        handler(api, args)
    else:
        # Print subcommand help
        for action in subparsers._group_actions:
            if action.choices and args.command in action.choices:
                action.choices[args.command].print_help()
                break


if __name__ == "__main__":
    main()
