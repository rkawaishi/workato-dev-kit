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
  python3 scripts/workato-api.py sdk edit <file> [--key <master.key>]
  python3 scripts/workato-api.py sdk decrypt <file> [--key <master.key>]
  python3 scripts/workato-api.py profile show

Global options:
  --profile <name>   Use a specific profile instead of auto-resolution
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

    def _request(
        self, path: str, params: dict | None = None, method: str = "GET",
        body: dict | list | None = None,
    ) -> dict | list:
        url = f"{self.base_url}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(
                {k: v for k, v in params.items() if v is not None}
            )

        data = json.dumps(body).encode() if body else None
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
            body = e.read().decode() if e.fp else ""
            safe_url = url.split("?")[0]
            print(
                f"Error: HTTP {e.code} {e.reason}\n"
                f"URL: {safe_url}\n"
                f"Response: {body}",
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
        """Push connector source code to Workato."""
        payload: dict = {"source_code": source_code}
        if description:
            payload["description"] = description
        if notes:
            payload["notes"] = notes
        if no_release:
            payload["release"] = False

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

        return result.get("data", result) if isinstance(result, dict) else result

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

    result = api.sdk_push(
        source_code=source_code,
        title=title,
        connector_id=args.connector_id,
        description=args.description,
        notes=args.notes,
        no_release=args.no_release,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))

    action = "Updated" if args.connector_id else "Created"
    cid = result.get("id", "?")
    print(f"\n{action} connector: {result.get('title', title)} (id={cid})", file=sys.stderr)


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

    jobs_list_p = jobs_sub.add_parser("list", help="List jobs for a recipe")
    jobs_list_p.add_argument("--recipe-id", type=int, required=True)
    jobs_list_p.add_argument("--status", default=None, help="Filter by status")

    jobs_get_p = jobs_sub.add_parser("get", help="Get job details")
    jobs_get_p.add_argument("--recipe-id", type=int, required=True)
    jobs_get_p.add_argument("--job-id", type=str, required=True)

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

    # -- sdk --
    sdk_parser = subparsers.add_parser(
        "sdk", help="Connector SDK commands (uses Platform API token)"
    )
    sdk_sub = sdk_parser.add_subparsers(dest="sdk_command")

    sdk_push_p = sdk_sub.add_parser(
        "push", help="Push connector source code to Workato"
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

    sdk_decrypt_p = sdk_sub.add_parser(
        "decrypt", help="Decrypt a .enc file and print to stdout"
    )
    sdk_decrypt_p.add_argument("file", help="Path to .enc file")
    sdk_decrypt_p.add_argument(
        "--key", default=None, help="Path to master.key (default: same dir as .enc)"
    )

    sdk_edit_p = sdk_sub.add_parser(
        "edit", help="Decrypt .enc file, open in $EDITOR, re-encrypt on save"
    )
    sdk_edit_p.add_argument("file", help="Path to .enc file (created if not exists)")
    sdk_edit_p.add_argument(
        "--key", default=None, help="Path to master.key (default: same dir as .enc)"
    )

    sdk_gen_p = sdk_sub.add_parser(
        "generate-schema", help="Generate Workato schema from JSON/CSV sample"
    )
    sdk_gen_p.add_argument("file", help="Path to JSON or CSV sample file")

    # -- oauth-profiles --
    oauth_parser = subparsers.add_parser(
        "oauth-profiles", help="Manage custom OAuth profiles"
    )
    oauth_sub = oauth_parser.add_subparsers(dest="oauth_profiles_command")

    oauth_sub.add_parser("list", help="List custom OAuth profiles")

    oauth_get_p = oauth_sub.add_parser("get", help="Get OAuth profile by ID")
    oauth_get_p.add_argument("--id", type=int, required=True)

    oauth_create_p = oauth_sub.add_parser("create", help="Create OAuth profile")
    oauth_create_p.add_argument("--name", required=True)
    oauth_create_p.add_argument("--provider", required=True)
    oauth_create_p.add_argument("--client-id", required=True)
    oauth_create_p.add_argument("--client-secret", required=True)
    oauth_create_p.add_argument("--token", default=None, help="Token (Slack only)")

    oauth_update_p = oauth_sub.add_parser("update", help="Update OAuth profile")
    oauth_update_p.add_argument("--id", type=int, required=True)
    oauth_update_p.add_argument("--name", required=True)
    oauth_update_p.add_argument("--provider", required=True)
    oauth_update_p.add_argument("--client-id", required=True)
    oauth_update_p.add_argument("--client-secret", required=True)
    oauth_update_p.add_argument("--token", default=None, help="Token (Slack only)")

    oauth_delete_p = oauth_sub.add_parser("delete", help="Delete OAuth profile")
    oauth_delete_p.add_argument("--id", type=int, required=True)

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
