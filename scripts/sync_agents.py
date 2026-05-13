#!/usr/bin/env python3
"""sync_agents.py — Generate per-agent content from canonical Claude source.

Canonical output (committed):
    framework/claude/rules/*.md       → framework/cursor/rules/*.mdc
    framework/claude/skills/*/SKILL.md → framework/cursor/skills/*/SKILL.md
    framework/claude/skills/*/SKILL.md → framework/codex/skills/*/SKILL.md
    framework/claude/skills/*/SKILL.md → framework/gemini/skills/*/SKILL.md
    framework/claude/CLAUDE.md
        + framework/claude/rules/*.md → framework/AGENTS.md

setup.sh symlinks framework/<agent>/ trees into the consumer repo, and
symlinks GEMINI.md → framework/AGENTS.md so Gemini CLI gets the same
content as Codex / Aider.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_ROOT = REPO_ROOT / "framework" / "claude"
CLAUDE_MD = CLAUDE_ROOT / "CLAUDE.md"
CLAUDE_RULES = CLAUDE_ROOT / "rules"
CLAUDE_SKILLS = CLAUDE_ROOT / "skills"

# Canonical generated output — committed, distributed via setup.sh.
CURSOR_OUT = REPO_ROOT / "framework" / "cursor"
CURSOR_RULES = CURSOR_OUT / "rules"
CURSOR_SKILLS = CURSOR_OUT / "skills"
CODEX_OUT = REPO_ROOT / "framework" / "codex"
CODEX_SKILLS = CODEX_OUT / "skills"
GEMINI_OUT = REPO_ROOT / "framework" / "gemini"
GEMINI_SKILLS = GEMINI_OUT / "skills"
AGENTS_MD = REPO_ROOT / "framework" / "AGENTS.md"


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter, body) where both exclude the '---' delimiters.

    The first '---' line opens the frontmatter; the next '---' line closes it.
    If the file does not start with '---', or no closing '---' is found, the
    entire text is treated as body.
    """
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return "", text
    for i in range(1, len(lines)):
        if lines[i] == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1 :])
    return "", text


def first_heading(body: str) -> str | None:
    """Return the first '# ...' heading text (without '# '), or None.

    Lines inside fenced code blocks (``` ... ```) are skipped so example
    headings inside code blocks do not match.
    """
    fence = False
    for line in body.splitlines():
        if line.startswith("```"):
            fence = not fence
            continue
        if not fence and line.startswith("# "):
            return line[2:]
    return None


_PATH_LINE_RE = re.compile(r'^  - "(.*)"$')


def extract_paths(fm: str) -> list[str]:
    """Extract glob entries from a Claude rule frontmatter.

    Only lines matching exactly ``  - "..."`` (two leading spaces) are
    considered, which mirrors the legacy bash script.
    """
    out: list[str] = []
    for line in fm.splitlines():
        m = _PATH_LINE_RE.match(line)
        if m:
            out.append(m.group(1))
    return out


def extract_field(fm: str, key: str) -> str | None:
    """Return the first value of ``key: ...`` in *fm*, or None."""
    pattern = re.compile(rf"^{re.escape(key)}: *(.*)$")
    for line in fm.splitlines():
        m = pattern.match(line)
        if m:
            return m.group(1)
    return None


def trim_trailing_newlines(text: str) -> str:
    """Mimic bash command-substitution: strip trailing newlines."""
    return text.rstrip("\n")


# Skill body path rewrites, applied in order. Order matters: the longer
# ".md"-suffixed patterns must run before the directory-only patterns,
# matching the legacy bash sed pipeline.
#
# The character class is ``[^.\n]`` rather than ``[^.]`` so the greedy
# quantifier cannot cross line boundaries — bash sed processes input
# line-by-line by default, and replicating that here prevents the regex
# from devouring unrelated ``.md`` references several lines away.
SKILL_PATH_REWRITES: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"@docs/"), "docs/"),
    (re.compile(r"@org/"), "org/"),
    (re.compile(r"@connectors/"), "connectors/"),
    (re.compile(r"@projects/"), "projects/"),
    (re.compile(r"@\.claude/rules/([^.\n]*)\.md"), r".cursor/rules/\1.mdc"),
    (re.compile(r"\.claude/rules/([^.\n]*)\.md"), r".cursor/rules/\1.mdc"),
    (re.compile(r"@\.claude/rules/"), ".cursor/rules/"),
    (re.compile(r"\.claude/rules/"), ".cursor/rules/"),
    (re.compile(r"@\.claude/skills/"), ".cursor/skills/"),
    (re.compile(r"\.claude/skills/"), ".cursor/skills/"),
)


def rewrite_skill_body(body: str) -> str:
    out = body
    for pattern, repl in SKILL_PATH_REWRITES:
        out = pattern.sub(repl, out)
    return out


def sync_rules() -> None:
    CURSOR_RULES.mkdir(parents=True, exist_ok=True)
    for src in sorted(CLAUDE_RULES.glob("*.md")):
        text = src.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        desc = first_heading(body)
        if not desc:
            print(f"WARN: No heading found in {src.stem}, skipping")
            continue
        globs = ",".join(extract_paths(fm))
        body_trimmed = trim_trailing_newlines(body)
        out = (
            "---\n"
            f"description: {desc}\n"
            f'globs: "{globs}"\n'
            "alwaysApply: false\n"
            "---\n"
            f"{body_trimmed}\n"
        )
        dst = CURSOR_RULES / f"{src.stem}.mdc"
        dst.write_text(out, encoding="utf-8")
        print(f"  ✓ {src.stem}.mdc")


def sync_skills() -> None:
    CURSOR_SKILLS.mkdir(parents=True, exist_ok=True)
    for skill_dir in sorted(p for p in CLAUDE_SKILLS.iterdir() if p.is_dir()):
        src = skill_dir / "SKILL.md"
        if not src.is_file():
            continue
        skill_name = skill_dir.name

        text = src.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        desc = extract_field(fm, "description") or ""
        disable_model = extract_field(fm, "disable-model-invocation")

        body_rewritten = rewrite_skill_body(body)
        body_trimmed = trim_trailing_newlines(body_rewritten)

        lines = [
            "---",
            f"name: {skill_name}",
            f"description: {desc}",
        ]
        if disable_model:
            lines.append(f"disable-model-invocation: {disable_model}")
        lines.append("---")
        out = "\n".join(lines) + "\n" + body_trimmed + "\n"

        dst_dir = CURSOR_SKILLS / skill_name
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / "SKILL.md"
        dst.write_text(out, encoding="utf-8")
        print(f"  ✓ skills/{skill_name}/SKILL.md")


_HEADING_RE = re.compile(r"^(#+) ")


def demote_headings(text: str, levels: int = 1) -> str:
    """Increase the heading depth of every Markdown heading by *levels*.

    Lines inside fenced code blocks are left untouched.
    """
    out: list[str] = []
    fence = False
    for line in text.split("\n"):
        if line.startswith("```"):
            fence = not fence
            out.append(line)
            continue
        if not fence:
            m = _HEADING_RE.match(line)
            if m:
                line = ("#" * levels) + line
        out.append(line)
    return "\n".join(out)


def _known_skill_names() -> set[str]:
    """Return the set of skill directory names under framework/claude/skills/."""
    if not CLAUDE_SKILLS.is_dir():
        return set()
    return {p.name for p in CLAUDE_SKILLS.iterdir() if p.is_dir()}


def _build_codex_slash_pattern(names: set[str]) -> re.Pattern[str] | None:
    if not names:
        return None
    alts = "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True))
    # Negative lookbehind blocks word chars AND ``>`` so placeholders like
    # ``<slug>/spec.md`` don't trigger a rewrite (the ``>`` from the closing
    # angle bracket is not ``\w`` but still denotes a path context). Negative
    # lookahead blocks ``/``, ``.`` and word chars so filenames like ``/spec.md``
    # and paths like ``/spec/foo`` are left intact while ``/spec``, ``` `/spec` ```,
    # and ``/spec <args>`` still match.
    return re.compile(rf"(?<![\w>])/({alts})(?![/.\w])\b")


# Codex skill body rewrites. Order matches Cursor's rewrites for the
# common cases, with Codex-specific differences:
#   * ``@.claude/rules/...`` and ``.claude/rules/...`` collapse to
#     ``AGENTS.md`` because Codex does not load per-rule files — the
#     equivalent content lives inline in framework/AGENTS.md.
#   * ``@.claude/skills/<name>`` and ``.claude/skills/<name>`` rewrite
#     to ``$<name>`` because Codex skill invocations use ``$`` not ``/``.
#   * Free-floating ``/<skill-name>`` references (in headings, code
#     spans, prose) rewrite to ``$<skill-name>`` via a separately-built
#     pattern that knows the actual skill names.
CODEX_PATH_REWRITES: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"@docs/"), "docs/"),
    (re.compile(r"@org/"), "org/"),
    (re.compile(r"@connectors/"), "connectors/"),
    (re.compile(r"@projects/"), "projects/"),
    (re.compile(r"@\.claude/CLAUDE\.md"), "AGENTS.md"),
    (re.compile(r"\.claude/CLAUDE\.md"), "AGENTS.md"),
    (re.compile(r"@\.claude/rules/[^.\n]*\.md"), "AGENTS.md"),
    (re.compile(r"\.claude/rules/[^.\n]*\.md"), "AGENTS.md"),
    (re.compile(r"@\.claude/rules/"), "AGENTS.md"),
    (re.compile(r"\.claude/rules/"), "AGENTS.md"),
    (re.compile(r"@\.claude/skills/([a-z][a-z0-9-]*)"), r"$\1"),
    (re.compile(r"\.claude/skills/([a-z][a-z0-9-]*)"), r"$\1"),
)


def rewrite_codex_body(body: str, slash_pattern: re.Pattern[str] | None) -> str:
    out = body
    for pattern, repl in CODEX_PATH_REWRITES:
        out = pattern.sub(repl, out)
    if slash_pattern is not None:
        out = slash_pattern.sub(r"$\1", out)
    return out


def sync_codex() -> None:
    """Convert Claude skills → framework/codex/skills/<name>/SKILL.md.

    Codex CLI's skills mode reads ``<workspace>/.agents/skills/<name>/
    SKILL.md`` (which setup.sh symlinks to framework/codex/skills/...).
    Slash command references are rewritten to ``$``-prefixed ones to
    match Codex's invocation syntax, and rule references collapse to
    ``AGENTS.md`` because Codex does not load per-rule files.
    """
    CODEX_SKILLS.mkdir(parents=True, exist_ok=True)
    slash_pattern = _build_codex_slash_pattern(_known_skill_names())
    for skill_dir in sorted(p for p in CLAUDE_SKILLS.iterdir() if p.is_dir()):
        src = skill_dir / "SKILL.md"
        if not src.is_file():
            continue
        skill_name = skill_dir.name

        text = src.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        desc = extract_field(fm, "description") or ""

        body_rewritten = rewrite_codex_body(body, slash_pattern)
        # Apply slash-to-dollar to the description too, since it may
        # mention sibling skills.
        if slash_pattern is not None:
            desc = slash_pattern.sub(r"$\1", desc)
        body_trimmed = trim_trailing_newlines(body_rewritten)

        lines = [
            "---",
            f"name: {skill_name}",
            f"description: {desc}",
            "---",
        ]
        out = "\n".join(lines) + "\n" + body_trimmed + "\n"

        dst_dir = CODEX_SKILLS / skill_name
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / "SKILL.md"
        dst.write_text(out, encoding="utf-8")
        print(f"  ✓ skills/{skill_name}/SKILL.md")


# Gemini skill body rewrites. Differences vs. Cursor:
#   * Rule references collapse to ``GEMINI.md`` (the agent loads a single
#     project memory file, not per-rule files).
#   * Skill cross-references stay as ``/<name>`` because Gemini uses the
#     slash invocation, just like Claude/Cursor.
GEMINI_PATH_REWRITES: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"@docs/"), "docs/"),
    (re.compile(r"@org/"), "org/"),
    (re.compile(r"@connectors/"), "connectors/"),
    (re.compile(r"@projects/"), "projects/"),
    (re.compile(r"@\.claude/CLAUDE\.md"), "GEMINI.md"),
    (re.compile(r"\.claude/CLAUDE\.md"), "GEMINI.md"),
    (re.compile(r"@\.claude/rules/[^.\n]*\.md"), "GEMINI.md"),
    (re.compile(r"\.claude/rules/[^.\n]*\.md"), "GEMINI.md"),
    (re.compile(r"@\.claude/rules/"), "GEMINI.md"),
    (re.compile(r"\.claude/rules/"), "GEMINI.md"),
    (re.compile(r"@\.claude/skills/([a-z][a-z0-9-]*)"), r"/\1"),
    (re.compile(r"\.claude/skills/([a-z][a-z0-9-]*)"), r"/\1"),
)


def rewrite_gemini_body(body: str) -> str:
    out = body
    for pattern, repl in GEMINI_PATH_REWRITES:
        out = pattern.sub(repl, out)
    return out


def sync_gemini() -> None:
    """Convert Claude skills → framework/gemini/skills/<name>/SKILL.md.

    Gemini CLI's skills mode reads ``<workspace>/.gemini/skills/<name>/
    SKILL.md`` (which setup.sh symlinks to framework/gemini/skills/...).
    Body rewrites collapse rule references to ``GEMINI.md`` because
    Gemini reads a single project memory file rather than per-rule
    files; setup.sh symlinks GEMINI.md to framework/AGENTS.md so the
    content is shared with Codex / Aider.
    """
    GEMINI_SKILLS.mkdir(parents=True, exist_ok=True)
    for skill_dir in sorted(p for p in CLAUDE_SKILLS.iterdir() if p.is_dir()):
        src = skill_dir / "SKILL.md"
        if not src.is_file():
            continue
        skill_name = skill_dir.name

        text = src.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        desc = extract_field(fm, "description") or ""

        body_rewritten = rewrite_gemini_body(body)
        body_trimmed = trim_trailing_newlines(body_rewritten)

        lines = [
            "---",
            f"name: {skill_name}",
            f"description: {desc}",
            "---",
        ]
        out = "\n".join(lines) + "\n" + body_trimmed + "\n"

        dst_dir = GEMINI_SKILLS / skill_name
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / "SKILL.md"
        dst.write_text(out, encoding="utf-8")
        print(f"  ✓ skills/{skill_name}/SKILL.md")


def sync_agents_md() -> None:
    """Generate framework/AGENTS.md by aggregating CLAUDE.md and the rules.

    AGENTS.md is the agent-neutral counterpart to CLAUDE.md — it is
    consumed by Codex CLI, Gemini CLI fallback (via GEMINI.md copy),
    Aider, and any agent that follows the AGENTS.md convention. Because
    these agents do not load per-rule files separately the way Claude
    Code does, every rule body is appended inline so AGENTS.md is
    self-contained.
    """
    claude_md_text = CLAUDE_MD.read_text(encoding="utf-8").rstrip()

    parts: list[str] = [
        "<!-- AUTO-GENERATED by scripts/sync_agents.py — DO NOT EDIT MANUALLY.",
        "     Source: framework/claude/CLAUDE.md + framework/claude/rules/*.md -->",
        "",
        claude_md_text,
        "",
        "---",
        "",
        "# File format rules",
        "",
        "When using Claude Code, the content of this section is referenced "
        "individually as `@.claude/rules/<name>.md`. For agents that do not "
        "load per-rule files — AGENTS.md / GEMINI.md / Codex CLI — the same "
        "content is consolidated below.",
        "",
    ]

    for rule_file in sorted(CLAUDE_RULES.glob("*.md")):
        text = rule_file.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        rule_name = rule_file.stem
        globs = extract_paths(fm)

        # Demote H1→H2, H2→H3, etc., so the rule's top-level heading
        # nests under our "File format rules" section.
        body_demoted = demote_headings(body.lstrip("\n"), levels=1).rstrip()

        # Insert applicability annotation right after the (now H2)
        # top-level heading.
        if globs:
            globs_line = "*Applies to: " + ", ".join(f"`{g}`" for g in globs) + "*"
            lines = body_demoted.split("\n")
            for i, ln in enumerate(lines):
                if ln.startswith("## "):
                    lines.insert(i + 1, "")
                    lines.insert(i + 2, globs_line)
                    break
            body_demoted = "\n".join(lines)

        parts.append(f"<!-- source: framework/claude/rules/{rule_name}.md -->")
        parts.append(body_demoted)
        parts.append("")

    out = "\n".join(parts).rstrip() + "\n"
    AGENTS_MD.write_text(out, encoding="utf-8")
    print(f"  ✓ framework/AGENTS.md ({len(out.splitlines())} lines)")


def main() -> int:
    if not CLAUDE_RULES.is_dir() or not CLAUDE_SKILLS.is_dir():
        print(
            f"Skipped: framework/claude/{{rules,skills}} not found at {REPO_ROOT} "
            "(consumer repo or non-kit context)."
        )
        return 0

    print("=== Syncing rules → framework/cursor/rules/ ===")
    sync_rules()
    print()
    print("=== Syncing skills → framework/cursor/skills/ ===")
    sync_skills()
    print()
    print("=== Syncing skills → framework/codex/skills/ ===")
    sync_codex()
    print()
    print("=== Syncing skills → framework/gemini/skills/ ===")
    sync_gemini()
    print()
    print("=== Generating framework/AGENTS.md ===")
    sync_agents_md()
    print()
    print(
        "Done. framework/cursor/rules/workato-project.mdc and hooks.json "
        "are hand-maintained and untouched by sync."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
