#!/usr/bin/env python3
"""Regression tests for ``scripts/sync_agents.py``.

Focus is on the pure transformation functions (frontmatter parsing,
heading extraction, body rewrites). Silent regressions in these
functions would corrupt every editor's output, so we want explicit
golden tests for the trickier rewrite patterns:

- code fences must not match slash commands
- skill-name slash patterns must not catch path fragments like
  ``projects/push-project``
- ``@org/`` (newer overlay-layer references) must be stripped exactly
  like ``@docs/``
- frontmatter parsing must handle missing closing ``---``

Run with:
    python3 scripts/tests/test_sync_agents.py

Stdlib-only and importlib-based, mirroring test_sdk_push_frontmatter.py
so CI doesn't need an extra runner or sys.path manipulation.
"""

from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "sync_agents.py"

spec = importlib.util.spec_from_file_location("sync_agents", SCRIPT)
sa = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(sa)


# --- split_frontmatter ----------------------------------------------


def test_split_frontmatter_no_fm():
    fm, body = sa.split_frontmatter("# Hello\n\nbody")
    assert fm == ""
    assert body == "# Hello\n\nbody"


def test_split_frontmatter_with_fm():
    text = "---\nname: foo\ndescription: bar\n---\n# Hello\n\nbody"
    fm, body = sa.split_frontmatter(text)
    assert fm == "name: foo\ndescription: bar"
    assert body == "# Hello\n\nbody"


def test_split_frontmatter_no_close_falls_back_to_body():
    fm, body = sa.split_frontmatter("---\nfoo: bar\n# only opening")
    assert fm == ""
    assert body == "---\nfoo: bar\n# only opening"


def test_split_frontmatter_empty_body():
    fm, body = sa.split_frontmatter("---\nfoo: bar\n---\n")
    assert fm == "foo: bar"
    assert body == ""


# --- first_heading --------------------------------------------------


def test_first_heading_simple():
    assert sa.first_heading("# Title\n\nbody") == "Title"


def test_first_heading_skips_paragraph_first():
    assert sa.first_heading("intro line\n# Real Title\n") == "Real Title"


def test_first_heading_inside_fence_is_ignored():
    body = "```markdown\n# Not a heading\n```\n\n# Real Title"
    assert sa.first_heading(body) == "Real Title"


def test_first_heading_none_when_only_subheadings():
    assert sa.first_heading("## Sub\n\n### deeper\n") is None


# --- extract_paths --------------------------------------------------


def test_extract_paths_two_entries():
    fm = 'paths:\n  - "**/*.recipe.json"\n  - "**/*.lcap_page.json"\n'
    assert sa.extract_paths(fm) == ["**/*.recipe.json", "**/*.lcap_page.json"]


def test_extract_paths_ignores_non_two_space_indent():
    # Three-space indent does not match the legacy bash pattern.
    fm = 'paths:\n   - "**/*.recipe.json"\n'
    assert sa.extract_paths(fm) == []


def test_extract_paths_empty():
    assert sa.extract_paths("") == []


# --- extract_field --------------------------------------------------


def test_extract_field_simple():
    fm = "name: foo\ndescription: bar baz"
    assert sa.extract_field(fm, "description") == "bar baz"


def test_extract_field_first_match_wins():
    fm = "description: first\ndescription: second"
    assert sa.extract_field(fm, "description") == "first"


def test_extract_field_missing_returns_none():
    assert sa.extract_field("name: foo", "description") is None


# --- trim_trailing_newlines -----------------------------------------


def test_trim_trailing_newlines_strips_only_newlines():
    assert sa.trim_trailing_newlines("a\n\n\n") == "a"
    assert sa.trim_trailing_newlines("a") == "a"
    assert sa.trim_trailing_newlines("a \n") == "a "  # trailing space preserved


# --- demote_headings ------------------------------------------------


def test_demote_headings_basic():
    text = "# H1\n## H2\n### H3"
    assert sa.demote_headings(text, levels=1) == "## H1\n### H2\n#### H3"


def test_demote_headings_inside_fence_untouched():
    text = "# Real\n```\n# Looks like H1 but inside fence\n```\n## After"
    out = sa.demote_headings(text, levels=1)
    assert out == "## Real\n```\n# Looks like H1 but inside fence\n```\n### After"


def test_demote_headings_zero_levels_is_noop():
    text = "# H1\n## H2"
    assert sa.demote_headings(text, levels=0) == text


# --- Cursor body rewrites (rewrite_skill_body) ----------------------


def test_cursor_strips_at_docs():
    assert sa.rewrite_skill_body("see @docs/connectors/foo.md") == "see docs/connectors/foo.md"


def test_cursor_strips_at_org():
    # @org/ is the newer overlay-layer prefix; must be stripped just
    # like @docs/.
    assert sa.rewrite_skill_body("併読 @org/docs/connectors/foo.md") == "併読 org/docs/connectors/foo.md"


def test_cursor_rewrites_at_claude_rules_md_to_mdc():
    body = "詳細は @.claude/rules/workato-recipe-format.md 参照"
    assert sa.rewrite_skill_body(body) == "詳細は .cursor/rules/workato-recipe-format.mdc 参照"


def test_cursor_rewrites_unprefixed_claude_rules_md_to_mdc():
    body = ".claude/rules/workato-cli.md を読む"
    assert sa.rewrite_skill_body(body) == ".cursor/rules/workato-cli.mdc を読む"


def test_cursor_rewrites_at_claude_skills_to_cursor_skills():
    body = "see @.claude/skills/create-recipe/SKILL.md"
    assert sa.rewrite_skill_body(body) == "see .cursor/skills/create-recipe/SKILL.md"


def test_cursor_rewrite_does_not_cross_lines():
    # The character class [^.\n] prevents the regex from devouring
    # multiple lines when looking for ".md".
    body = "@.claude/rules/foo\n\n... unrelated .md mention later"
    out = sa.rewrite_skill_body(body)
    # The first part collapses to .cursor/rules/ (directory-only rewrite)
    # because there is no ".md" on the same line.
    assert out.startswith(".cursor/rules/foo\n")
    assert "unrelated .md mention" in out


# --- Codex body rewrites (rewrite_codex_body) -----------------------


def test_codex_collapses_rules_md_to_agents_md():
    body = "詳細は @.claude/rules/workato-cli.md"
    assert sa.rewrite_codex_body(body, None) == "詳細は AGENTS.md"


def test_codex_collapses_unprefixed_rules_to_agents_md():
    body = ".claude/rules/workato-recipe-format.md 参照"
    assert sa.rewrite_codex_body(body, None) == "AGENTS.md 参照"


def test_codex_skill_dir_to_dollar():
    body = "実行は @.claude/skills/create-recipe で"
    assert sa.rewrite_codex_body(body, None) == "実行は $create-recipe で"


def test_codex_strips_at_org():
    # Overlay layer prefix must collapse for Codex too.
    assert sa.rewrite_codex_body("@org/docs/foo.md", None) == "org/docs/foo.md"


# --- Codex slash pattern ---------------------------------------------


def test_codex_slash_pattern_returns_none_for_empty_set():
    assert sa._build_codex_slash_pattern(set()) is None


def test_codex_slash_pattern_matches_known_skill():
    pat = sa._build_codex_slash_pattern({"create-recipe", "push-project"})
    assert pat is not None
    out = pat.sub(r"$\1", "次は /create-recipe を呼ぶ")
    assert out == "次は $create-recipe を呼ぶ"


def test_codex_slash_pattern_skips_unknown_skill():
    pat = sa._build_codex_slash_pattern({"create-recipe"})
    assert pat is not None
    # /unknown-skill is not in the known set — must NOT be rewritten.
    assert pat.sub(r"$\1", "/unknown-skill") == "/unknown-skill"


def test_codex_slash_pattern_avoids_path_false_positive():
    # The (?<!\w) lookbehind must prevent matches inside paths like
    # "projects/push-project" so a casual file path is not corrupted
    # into "projects$push-project".
    pat = sa._build_codex_slash_pattern({"push-project", "create-recipe"})
    assert pat is not None
    assert pat.sub(r"$\1", "projects/push-project") == "projects/push-project"
    assert pat.sub(r"$\1", "see /push-project skill") == "see $push-project skill"


def test_codex_slash_pattern_word_boundary_stops_partial_match():
    # \b after the name prevents partial rewrites inside longer words
    # that happen to start with the skill name.
    pat = sa._build_codex_slash_pattern({"design"})
    assert pat is not None
    assert pat.sub(r"$\1", "/design") == "$design"
    assert pat.sub(r"$\1", "/designer") == "/designer"


def test_codex_longer_names_match_first():
    # When two skills share a prefix (e.g. "create" and "create-recipe"),
    # the longer alternation wins so /create-recipe is fully captured.
    pat = sa._build_codex_slash_pattern({"create", "create-recipe"})
    assert pat is not None
    assert pat.sub(r"$\1", "/create-recipe") == "$create-recipe"


def test_codex_slash_pattern_preserves_placeholder_path():
    # ``<NNN>-<slug>/spec.md`` is a template file path. The ``>`` of the
    # closing angle bracket is not ``\w`` but still signals a path context,
    # so the rewrite must leave ``/spec`` intact.
    pat = sa._build_codex_slash_pattern({"spec", "plan", "tasks"})
    assert pat is not None
    assert (
        pat.sub(r"$\1", "projects/<project>/specs/<NNN>-<slug>/spec.md")
        == "projects/<project>/specs/<NNN>-<slug>/spec.md"
    )


def test_codex_slash_pattern_preserves_filename_reference():
    # ``/spec.md`` mid-sentence is a filename, not a command — keep as is.
    pat = sa._build_codex_slash_pattern({"spec"})
    assert pat is not None
    assert pat.sub(r"$\1", "see /spec.md for details") == "see /spec.md for details"


def test_codex_slash_pattern_preserves_path_segment():
    # ``/spec/foo`` uses the skill name as a directory segment — keep as is.
    pat = sa._build_codex_slash_pattern({"spec"})
    assert pat is not None
    assert pat.sub(r"$\1", "look at /spec/foo for context") == "look at /spec/foo for context"


# --- Gemini body rewrites (rewrite_gemini_body) ---------------------


def test_gemini_collapses_rules_to_gemini_md():
    body = "詳細は @.claude/rules/workato-cli.md"
    assert sa.rewrite_gemini_body(body) == "詳細は GEMINI.md"


def test_gemini_skill_dir_keeps_slash():
    # Gemini uses the / invocation syntax, so cross-references stay /.
    body = "実行は @.claude/skills/create-recipe"
    assert sa.rewrite_gemini_body(body) == "実行は /create-recipe"


def test_gemini_strips_at_org():
    assert sa.rewrite_gemini_body("@org/docs/foo.md") == "org/docs/foo.md"


# --- main() smoke ---------------------------------------------------


def test_main_no_op_when_claude_tree_missing(monkey_paths=None):
    # Saving / restoring constants is OK because tests run sequentially.
    saved_rules = sa.CLAUDE_RULES
    saved_skills = sa.CLAUDE_SKILLS
    sa.CLAUDE_RULES = Path("/nonexistent/rules")
    sa.CLAUDE_SKILLS = Path("/nonexistent/skills")
    try:
        rc = sa.main()
    finally:
        sa.CLAUDE_RULES = saved_rules
        sa.CLAUDE_SKILLS = saved_skills
    assert rc == 0


def main() -> int:
    tests = [(name, obj) for name, obj in sorted(globals().items())
             if name.startswith("test_") and callable(obj)]
    failures: list[tuple[str, str]] = []
    for name, fn in tests:
        try:
            fn()
            print(f"  ok  {name}")
        except Exception:
            failures.append((name, traceback.format_exc()))
            print(f"  FAIL {name}")

    print(f"\n{len(tests) - len(failures)}/{len(tests)} passed")
    for name, tb in failures:
        print(f"\n--- {name} ---\n{tb}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
