#!/usr/bin/env python3
"""Generate wk-lint skill packs from docs/connectors/*.md.

Emits, per connector, a directory that `wk lint --skills-path` can consume:

    skills/<provider>-recipes/
    |-- skill.yaml         # open agent skills manifest (extends: workato-recipes)
    |-- lint-rules.json    # recipe-lint rules (v0.1.0 core, optional v0.2.0 rules)
    `-- SKILL.md           # agent-facing knowledge document

The connector docs are the single source of truth. Do not hand-edit the
generated tree; regenerate it after /sync-connectors.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Connectors already shipped by workato-devs/recipe-skills. `--skills-path`
# walks a directory recursively and loads every lint-rules.json it finds, so
# emitting these alongside the official pack would register two rule sets for
# the same `connector` value. Skip them with --exclude-official.
OFFICIAL_PROVIDERS = {
    "asana",
    "gmail",
    "jira",
    "salesforce",
    "slack",
    "stripe",
    "workato_db_table",
}

PROVIDER_RE = re.compile(r"^Provider:\s*`([^`]+)`", re.M)
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)
INTERNAL_NAME_RE = re.compile(r"^`([A-Za-z0-9_]+)`$")
DEPRECATED_RE = re.compile(r"\[deprecated\]", re.I)


@dataclass
class Operation:
    name: str
    title: str
    deprecated: bool = False
    batch: bool = False
    description: str = ""


@dataclass
class Connector:
    provider: str
    title: str
    source: Path
    triggers: list[Operation] = field(default_factory=list)
    actions: list[Operation] = field(default_factory=list)
    field_details: str = ""

    @property
    def slug(self) -> str:
        return f"{self.provider.replace('_', '-')}-recipes"

    @staticmethod
    def live(ops: list[Operation]) -> list[Operation]:
        return [o for o in ops if not o.deprecated]

    @staticmethod
    def dead(ops: list[Operation]) -> list[Operation]:
        return [o for o in ops if o.deprecated]


def split_row(line: str) -> list[str]:
    """Split a markdown table row into trimmed cells."""
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [c.strip() for c in inner.split("|")]


def parse_table(lines: list[str]) -> list[Operation]:
    """Extract operations from the `| Name | Internal name | Batch | Desc |` table.

    Rows are only accepted when the second cell is a backticked identifier, so
    the two-column `| Name | Description |` prose tables that a handful of docs
    carry underneath the canonical table are ignored.
    """
    ops: list[Operation] = []
    for line in lines:
        if not line.lstrip().startswith("|"):
            continue
        cells = split_row(line)
        if len(cells) < 2:
            continue
        m = INTERNAL_NAME_RE.match(cells[1])
        if not m:
            continue
        rest = " ".join(cells[2:])
        desc = cells[3] if len(cells) > 3 else ""
        ops.append(
            Operation(
                name=m.group(1),
                title=cells[0],
                deprecated=bool(DEPRECATED_RE.search(rest)),
                batch=len(cells) > 2 and cells[2] not in ("-", ""),
                description=DEPRECATED_RE.sub("", desc).strip(),
            )
        )
    return ops


def section(text: str, heading: str) -> list[str]:
    """Return the lines under a `## <heading>` up to the next `## ` heading."""
    out: list[str] = []
    capturing = False
    for line in text.splitlines():
        if line.startswith("## "):
            if capturing:
                break
            capturing = line[3:].strip().lower() == heading.lower()
            continue
        if capturing:
            out.append(line)
    return out


def parse_connector(path: Path) -> Connector | None:
    text = path.read_text(encoding="utf-8")
    pm = PROVIDER_RE.search(text)
    if not pm:
        return None
    tm = TITLE_RE.search(text)
    title = tm.group(1).replace(" connector", "").strip() if tm else pm.group(1)
    conn = Connector(provider=pm.group(1), title=title, source=path)
    conn.triggers = parse_table(section(text, "Triggers"))
    conn.actions = parse_table(section(text, "Actions"))
    conn.field_details = "\n".join(section(text, "Field details")).strip()
    return conn


def deprecation_rules(conn: Connector) -> list[dict]:
    """A v0.2.0 declarative rule that warns on every deprecated operation.

    `assert` must evaluate true for a rule to pass, so `field_absent` on `name`
    -- a field every step carries -- fires for each step the selector matches.

    Verified against recipe-lint 1.1.0. Note that rules carried in a skill pack
    are registered twice by `--skills-path`, so each match is reported twice;
    the identical rule loaded via --config-path project rules reports once.
    That is why --deprecated=strict is the default.
    """
    names = sorted({o.name for o in conn.dead(conn.actions) + conn.dead(conn.triggers)})
    if not names:
        return []
    return [
        {
            "rule_id": f"KIT_{conn.provider.upper()}_DEPRECATED",
            "tier": 1,
            "level": "warn",
            "scope": "step",
            "message": (
                f"{conn.title}: this operation is deprecated in Workato; "
                "prefer its current replacement"
            ),
            "where": {"provider": conn.provider, "action_name": names},
            "assert": {"field_absent": {"path": "name"}},
        }
    ]


def build_lint_rules(conn: Connector, deprecated: str) -> dict:
    include_dead = deprecated != "strict"
    actions = conn.actions if include_dead else conn.live(conn.actions)
    triggers = conn.triggers if include_dead else conn.live(conn.triggers)
    doc: dict = {
        "version": "0.2.0" if deprecated == "warn" else "0.1.0",
        "connector": conn.provider,
        "connector_internals": [],
        "action_rules": [],
    }
    # `valid_*_names` drives ACTION_NAME_VALID as an allow-list. An empty array
    # would reject every operation on the provider, so leave the key out when we
    # have nothing to allow -- either the docs record no operations, or every
    # documented one is deprecated and --deprecated=strict filtered it away.
    action_names = sorted({o.name for o in actions})
    trigger_names = sorted({o.name for o in triggers})
    if action_names:
        doc["valid_action_names"] = action_names
    if trigger_names:
        doc["valid_trigger_names"] = trigger_names
    if deprecated == "warn":
        doc["rules"] = deprecation_rules(conn)
    return doc


def yaml_list(items: list[str], indent: str = "  - ") -> str:
    return "\n".join(f"{indent}{i}" for i in items)


def build_skill_yaml(conn: Connector, version: str) -> str:
    caps: list[str] = []
    for label, ops in (
        ("triggers", conn.live(conn.triggers)),
        ("actions", conn.live(conn.actions)),
    ):
        if ops:
            caps.append(f"{len(ops)} native {label}")
    if any(o.batch for o in conn.actions + conn.triggers):
        caps.append("batch operations")
    caps.append(
        "custom action via __adhoc_http_action"
        if any(o.name == "__adhoc_http_action" for o in conn.actions)
        else "recipe JSON generation"
    )

    tags = sorted({conn.provider, "workato", "recipes", "connector"})
    return f"""# {conn.title} recipes skill for Workato
# Generated by scripts/gen_lint_rules.py from docs/connectors/{conn.source.name}
# Do not hand-edit -- regenerate after /sync-connectors.

name: {conn.slug}
version: {version}
description: >
  {conn.title} knowledge for Workato recipe generation. Enumerates the connector's
  valid trigger and action internal names so coding agents cannot hallucinate
  operations, and feeds `wk lint` connector-name validation.

author: workato-dev-kit (community)
license: MIT

extends: workato-recipes

capabilities:
{yaml_list(caps)}

entry_point: SKILL.md

platforms:
  - workato
  - {conn.provider}

tags:
{yaml_list(tags)}

source:
  provider: {conn.provider}
  doc: docs/connectors/{conn.source.name}
"""


def ops_table(ops: list[Operation]) -> str:
    if not ops:
        return "_None._\n"
    rows = ["| Internal name | Title | Batch |", "|---|---|---|"]
    for o in sorted(ops, key=lambda x: x.name):
        rows.append(f"| `{o.name}` | {o.title} | {'yes' if o.batch else '-'} |")
    return "\n".join(rows) + "\n"


def build_skill_md(conn: Connector) -> str:
    live_t, live_a = conn.live(conn.triggers), conn.live(conn.actions)
    dead_t, dead_a = conn.dead(conn.triggers), conn.dead(conn.actions)
    has_adhoc = any(o.name == "__adhoc_http_action" for o in conn.actions)

    parts = [
        f"# {conn.title} recipes\n",
        f"Provider value to use in every step: `{conn.provider}`\n",
        "This skill extends the base `workato-recipes` skill. Read that first for "
        "recipe JSON structure, datapill syntax, and control flow; this document "
        "only covers what is specific to this connector.\n",
        "## Before you generate\n",
        f'- Set `"provider": "{conn.provider}"` on every step that uses this connector.',
        "- Use only the internal names listed below. They are the same list "
        "`lint-rules.json` enforces, so anything else fails `wk lint`.",
        (
            "- Reach for `__adhoc_http_action` only when no native operation covers "
            "the call.\n"
            if has_adhoc
            else "- This connector has no custom-action escape hatch; if no native "
            "operation fits, use the HTTP connector instead.\n"
        ),
        f"## Triggers ({len(live_t)})\n",
        ops_table(live_t),
        f"\n## Actions ({len(live_a)})\n",
        ops_table(live_a),
    ]

    if dead_t or dead_a:
        parts.append(
            "\n## Deprecated -- do not generate\n\n"
            "Workato still executes these in existing recipes, but new recipes must "
            "not use them. They are excluded from `valid_action_names`.\n"
        )
        if dead_t:
            parts.append("\n### Triggers\n\n" + ops_table(dead_t))
        if dead_a:
            parts.append("\n### Actions\n\n" + ops_table(dead_a))

    if conn.field_details:
        parts.append(
            "\n## Field details\n\n"
            "Input/output field definitions observed from the Workato UI. The "
            "Workato API does not expose these, so treat them as the authoritative "
            "source for required fields and types.\n\n" + conn.field_details + "\n"
        )

    parts.append(
        "\n## Validation\n\n"
        "```bash\n"
        "wk lint <recipe>.recipe.json --skills-path <path-to>/skills\n"
        "```\n"
    )
    return "\n".join(parts)


def write(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--docs-dir", type=Path, default=Path("docs/connectors"))
    ap.add_argument("--out-dir", type=Path, default=Path("skills"))
    ap.add_argument("--only", nargs="*", metavar="PROVIDER", help="generate just these providers")
    ap.add_argument(
        "--exclude-official",
        action="store_true",
        help="skip the 7 connectors workato-devs/recipe-skills already ships",
    )
    ap.add_argument(
        "--deprecated",
        choices=["strict", "warn"],
        default="strict",
        help="strict: omit deprecated names, so using one is an ACTION_NAME_VALID "
        "error (matches the official pack). warn: keep them valid and emit a "
        "v0.2.0 warn rule instead -- better for linting recipes pulled from an "
        "existing workspace, but recipe-lint 1.1.0 reports skill-pack rules twice.",
    )
    ap.add_argument("--version", default="0.1.0", help="version stamped into skill.yaml")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    docs = sorted(p for p in args.docs_dir.glob("*.md") if not p.name.startswith("_"))
    if not docs:
        print(f"no connector docs under {args.docs_dir}", file=sys.stderr)
        return 1

    written = skipped = 0
    undocumented: list[str] = []
    for path in docs:
        conn = parse_connector(path)
        if conn is None:
            print(f"skip {path.name}: no Provider line", file=sys.stderr)
            skipped += 1
            continue
        if args.only and conn.provider not in args.only:
            continue
        if args.exclude_official and conn.provider in OFFICIAL_PROVIDERS:
            skipped += 1
            continue
        if not conn.actions and not conn.triggers:
            # The docs record no operations at all (the platform API returned
            # none). A skill here would teach an agent nothing and constrain
            # nothing -- surface it as a /sync-connectors gap instead.
            undocumented.append(conn.provider)
            skipped += 1
            continue

        out = args.out_dir / conn.slug
        rules = build_lint_rules(conn, args.deprecated)
        write(out / "lint-rules.json", json.dumps(rules, indent=2, ensure_ascii=False) + "\n", args.dry_run)
        write(out / "skill.yaml", build_skill_yaml(conn, args.version), args.dry_run)
        write(out / "SKILL.md", build_skill_md(conn), args.dry_run)
        written += 1
        if args.only or args.dry_run:
            print(
                f"{conn.slug}: {len(rules['valid_trigger_names'])} triggers, "
                f"{len(rules['valid_action_names'])} actions"
            )

    print(
        f"{'would write' if args.dry_run else 'wrote'} {written} skill(s), skipped {skipped}",
        file=sys.stderr,
    )
    if undocumented:
        print(
            f"no operations documented for {len(undocumented)} connector(s) -- "
            f"run /sync-connectors on them: {' '.join(sorted(undocumented))}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
