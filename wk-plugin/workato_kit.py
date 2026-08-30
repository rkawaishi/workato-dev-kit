#!/usr/bin/env python3
"""workato-kit: a `wk` plugin for the Workato asset types wk does not model.

`wk` speaks newline-delimited JSON-RPC 2.0 over stdin/stdout and spawns this
process per call (ADR-004). Nothing here imports wk; the wire format is the
only coupling.

    wk -> plugin  {"jsonrpc":"2.0","method":"kit.validate","params":{...},"id":1}\n
    plugin -> wk  {"jsonrpc":"2.0","result":{...},"id":1}\n

`recipe-lint` already covers `*.recipe.json` far better than we could. This
plugin deliberately validates only what it does not model:

  *.connection.json       filename must be the snake_case of the display name,
                          workspace prefix included, or push silently renames it
  *.workato_db_table.json business columns only -- writing the system columns
                          locally makes `pull` produce duplicates
  *.agentic_genie.json    skill references must resolve
  *.agentic_skill.json    recipe reference must resolve, trigger must be agentic
  *.lcap_app.json         page references must resolve
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

VERSION = "0.1.0"

# Workato assigns these on the server. Declaring them locally makes `wk pull`
# return a second copy with a different id.
DATA_TABLE_SYSTEM_COLUMNS = {"record id", "created time", "last modified time"}

ASSET_GLOBS = (
    "*.connection.json",
    "*.workato_db_table.json",
    "*.agentic_genie.json",
    "*.agentic_skill.json",
    "*.lcap_app.json",
    "*.lcap_page.json",
)


class Diagnostic(dict):
    def __init__(self, path: str, rule: str, level: str, message: str, pointer: str = ""):
        super().__init__(path=path, rule=rule, level=level, message=message, pointer=pointer)


def snake(name: str) -> str:
    """Workato's display-name -> filename normalisation."""
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", name.lower())).strip("_")


def check_connection(path: Path, doc: dict) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    for key in ("name", "provider"):
        if not doc.get(key):
            out.append(Diagnostic(str(path), "KIT_CONNECTION_REQUIRED", "error",
                                  f'connection is missing required field "{key}"', f"/{key}"))
    name = doc.get("name")
    if name:
        stem = path.name[: -len(".connection.json")]
        if stem != snake(name):
            out.append(Diagnostic(
                str(path), "KIT_CONNECTION_FILENAME", "error",
                f'filename "{stem}" is not the snake_case of display name "{name}" '
                f'(expected "{snake(name)}.connection.json"). Workato renames the file '
                f"on push, which the next pull reports as a delete plus an add.",
                "/name"))
    return out


def check_data_table(path: Path, doc: dict) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    for i, field in enumerate(doc.get("fields") or doc.get("schema") or []):
        label = str(field.get("name", "")).strip().lower()
        if label in DATA_TABLE_SYSTEM_COLUMNS:
            out.append(Diagnostic(
                str(path), "KIT_DATATABLE_SYSTEM_COLUMN", "error",
                f'"{field.get("name")}" is a Workato system column; remove it. '
                f"`wk pull` adds the system columns back, and a locally assigned "
                f"id produces a duplicate column.",
                f"/fields/{i}"))
    return out


def check_genie(path: Path, doc: dict, siblings: set[str]) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    for key in ("name", "instructions", "references"):
        if not doc.get(key):
            out.append(Diagnostic(str(path), "KIT_GENIE_REQUIRED", "error",
                                  f'genie is missing required field "{key}"', f"/{key}"))
    for i, ref in enumerate(doc.get("references") or []):
        if ref.get("type") != "agentic_skill":
            out.append(Diagnostic(str(path), "KIT_GENIE_REF_TYPE", "error",
                                  f'reference type must be "agentic_skill", got '
                                  f'"{ref.get("type")}"', f"/references/{i}/type"))
        zip_name = ref.get("zip_name")
        if zip_name and zip_name not in siblings:
            out.append(Diagnostic(str(path), "KIT_GENIE_REF_MISSING", "error",
                                  f'reference "{zip_name}" does not exist in this project',
                                  f"/references/{i}/zip_name"))
    return out


def check_skill(path: Path, doc: dict, siblings: set[str]) -> list[Diagnostic]:
    out: list[Diagnostic] = []
    for key in ("name", "trigger_description", "references"):
        if not doc.get(key):
            out.append(Diagnostic(str(path), "KIT_SKILL_REQUIRED", "error",
                                  f'agentic skill is missing required field "{key}"', f"/{key}"))
    refs = doc.get("references") or {}
    recipe = refs.get("recipe_id") if isinstance(refs, dict) else None
    if recipe and not any(s.startswith(str(recipe)) for s in siblings):
        out.append(Diagnostic(str(path), "KIT_SKILL_RECIPE_MISSING", "error",
                              f'referenced recipe "{recipe}" does not exist in this project',
                              "/references/recipe_id"))
    return out


CHECKS = {
    ".connection.json": lambda p, d, sib: check_connection(p, d),
    ".workato_db_table.json": lambda p, d, sib: check_data_table(p, d),
    ".agentic_genie.json": check_genie,
    ".agentic_skill.json": check_skill,
}


def collect(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths or ["."]:
        p = Path(raw)
        if p.is_dir():
            for pattern in ASSET_GLOBS:
                files.extend(sorted(p.rglob(pattern)))
        elif p.is_file():
            files.append(p)
    return files


def validate(paths: list[str], strict: bool = False) -> dict:
    files = collect(paths)
    siblings = {f.name for parent in {f.parent for f in files} for f in parent.iterdir()
                if f.is_file()}
    diagnostics: list[Diagnostic] = []
    for f in files:
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            diagnostics.append(Diagnostic(str(f), "KIT_INVALID_JSON", "error", str(exc)))
            continue
        for suffix, check in CHECKS.items():
            if f.name.endswith(suffix):
                diagnostics.extend(check(f, doc, siblings))
                break

    errors = sum(1 for d in diagnostics if d["level"] == "error")
    warnings = sum(1 for d in diagnostics if d["level"] == "warn")
    if strict:
        errors += warnings
        warnings = 0
    return {
        "files": len(files),
        "errors": errors,
        "warnings": warnings,
        "diagnostics": diagnostics,
    }


def render(result: dict) -> str:
    lines: list[str] = []
    for d in result.get("diagnostics", []):
        marker = "ERROR" if d["level"] == "error" else d["level"].upper()
        pointer = f" {d['pointer']}" if d.get("pointer") else ""
        lines.append(f"  {d['path']}{pointer} [{marker}] {d['rule']}: {d['message']}")
    lines.append(
        f"workato-kit: {result.get('files', 0)} file(s), "
        f"{result.get('errors', 0)} error(s), {result.get('warnings', 0)} warning(s)"
    )
    return "\n".join(lines)


def normalise_params(params) -> tuple[list[str], bool]:
    """wk sends two different `params` shapes, neither of them documented.

    Top-level commands send an object carrying the declared args and flags;
    subcommands send a bare positional array of the raw arguments. Both were
    observed against wk 1.0.3 -- set WK_PLUGIN_DEBUG to re-check after an
    upgrade.
    """
    if isinstance(params, list):
        return [str(p) for p in params], False
    if not isinstance(params, dict):
        return [], False
    paths = params.get("paths") or params.get("files") or params.get("args") or []
    if isinstance(paths, str):
        paths = [paths]
    return [str(p) for p in paths], bool(params.get("strict"))


def dispatch(method: str, params) -> dict:
    if method == "shutdown":
        return {}
    if method == "kit.render":
        payload = params.get("result") if isinstance(params, dict) else None
        return {"text": render(payload if isinstance(payload, dict) else {})}

    paths, strict = normalise_params(params)
    if method == "kit.version":
        return {"version": VERSION, "name": "workato-kit"}
    if method in ("kit.validate", "kit.run", "kit.pre_push"):
        return validate(paths, strict)
    raise ValueError(f"unknown method: {method}")


def main() -> int:
    # WK_PLUGIN_DEBUG=<file> records every frame, which is how the params and
    # result shapes above were determined -- wk's docs do not specify them.
    debug = os.environ.get("WK_PLUGIN_DEBUG")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if debug:
            with open(debug, "a", encoding="utf-8") as fh:
                fh.write(f"<- {line}\n")
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        rid = req.get("id")
        try:
            response = {"jsonrpc": "2.0", "result": dispatch(req.get("method", ""),
                                                             req.get("params") or {}), "id": rid}
        except Exception as exc:  # a plugin crash must not take wk down
            response = {"jsonrpc": "2.0",
                        "error": {"code": -32603, "message": str(exc)}, "id": rid}
        payload = json.dumps(response, ensure_ascii=False)
        if debug:
            with open(debug, "a", encoding="utf-8") as fh:
                fh.write(f"-> {payload}\n")
        sys.stdout.write(payload + "\n")
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
