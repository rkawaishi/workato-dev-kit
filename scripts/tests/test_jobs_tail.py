#!/usr/bin/env python3
"""Tests for `jobs list --limit` and `jobs tail` in workato-api.py.

Covers:
  - cmd_jobs_list --limit caps client-side
  - jobs_tail_loop: priming, new-job detection, max_iterations exit,
    KeyboardInterrupt exit, chronological ordering, defensive handling
    of malformed entries
  - CLI argparse types for tail

Run with:
    python3 scripts/tests/test_jobs_tail.py
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import traceback
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "workato-api.py"

spec = importlib.util.spec_from_file_location("workato_api", SCRIPT)
wa = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(wa)


def _capture_stdout(fn):
    saved = sys.stdout
    sys.stdout = io.StringIO()
    try:
        fn()
        return sys.stdout.getvalue()
    finally:
        sys.stdout = saved


# ---------------------------------------------------------------------------
# cmd_jobs_list --limit
# ---------------------------------------------------------------------------


class _ScriptedJobsAPI:
    """Returns pre-recorded pages from jobs_list calls in order."""

    def __init__(self, pages):
        self._pages = list(pages)
        self.call_count = 0

    def jobs_list(self, _recipe_id, _status=None):
        self.call_count += 1
        if not self._pages:
            return []
        if len(self._pages) == 1:
            return self._pages[0]
        return self._pages.pop(0)


def test_jobs_list_no_limit_returns_all():
    api = _ScriptedJobsAPI([[{"id": i} for i in range(5)]])
    args = SimpleNamespace(recipe_id=1, status=None, limit=None)
    out = _capture_stdout(lambda: wa.cmd_jobs_list(api, args))
    assert len(json.loads(out)) == 5


def test_jobs_list_limit_caps_client_side():
    api = _ScriptedJobsAPI([[{"id": i} for i in range(10)]])
    args = SimpleNamespace(recipe_id=1, status=None, limit=3)
    out = _capture_stdout(lambda: wa.cmd_jobs_list(api, args))
    parsed = json.loads(out)
    assert [r["id"] for r in parsed] == [0, 1, 2]


def test_jobs_list_limit_zero_returns_empty():
    api = _ScriptedJobsAPI([[{"id": 1}, {"id": 2}]])
    args = SimpleNamespace(recipe_id=1, status=None, limit=0)
    out = _capture_stdout(lambda: wa.cmd_jobs_list(api, args))
    assert json.loads(out) == []


# ---------------------------------------------------------------------------
# jobs_tail_loop
# ---------------------------------------------------------------------------


def test_tail_does_not_emit_initial_backlog():
    """The first fetch primes the seen-set; existing jobs must not print."""
    api = _ScriptedJobsAPI([
        [{"id": 1}, {"id": 2}],   # priming fetch
        [{"id": 1}, {"id": 2}],   # iter 1 — same set, no new jobs
    ])
    emitted: list = []
    iters = wa.jobs_tail_loop(
        api, recipe_id=42, status_filter=None,
        interval_seconds=0.0, max_iterations=1,
        _sleep=lambda d: None, _print=lambda line: emitted.append(line),
    )
    assert iters == 1
    assert emitted == []


def test_tail_emits_new_jobs_only():
    """New jobs that appear after the priming fetch are printed once."""
    api = _ScriptedJobsAPI([
        [{"id": 1}],                          # priming
        [{"id": 2}, {"id": 1}],               # iter 1: 2 is new
        [{"id": 3}, {"id": 2}, {"id": 1}],    # iter 2: 3 is new
    ])
    emitted: list = []
    wa.jobs_tail_loop(
        api, recipe_id=42, status_filter=None,
        interval_seconds=0.0, max_iterations=2,
        _sleep=lambda d: None, _print=lambda line: emitted.append(line),
    )
    parsed = [json.loads(line) for line in emitted]
    assert [r["id"] for r in parsed] == [2, 3]


def test_tail_emits_in_chronological_order_within_one_iter():
    """Workato returns newest-first; tail reverses so output is oldest-first."""
    api = _ScriptedJobsAPI([
        [{"id": 1}],                          # priming
        [{"id": 4}, {"id": 3}, {"id": 2}, {"id": 1}],  # iter: 4,3,2 all new
    ])
    emitted: list = []
    wa.jobs_tail_loop(
        api, recipe_id=42, status_filter=None,
        interval_seconds=0.0, max_iterations=1,
        _sleep=lambda d: None, _print=lambda line: emitted.append(line),
    )
    parsed = [json.loads(line) for line in emitted]
    # Reversed from newest-first to oldest-first
    assert [r["id"] for r in parsed] == [2, 3, 4]


def test_tail_respects_max_iterations():
    api = _ScriptedJobsAPI([
        [],   # priming
        [{"id": 1}],
        [{"id": 2}, {"id": 1}],
        [{"id": 3}, {"id": 2}, {"id": 1}],
    ])
    sleeps: list = []
    iters = wa.jobs_tail_loop(
        api, recipe_id=42, status_filter=None,
        interval_seconds=2.0, max_iterations=2,
        _sleep=lambda d: sleeps.append(d), _print=lambda _l: None,
    )
    assert iters == 2
    assert sleeps == [2.0, 2.0]


def test_tail_max_iterations_zero_does_no_polls():
    """max_iterations=0 → loop returns immediately after priming."""
    api = _ScriptedJobsAPI([[{"id": 1}]])
    emitted: list = []
    iters = wa.jobs_tail_loop(
        api, recipe_id=42, status_filter=None,
        interval_seconds=0.0, max_iterations=0,
        _sleep=lambda d: None, _print=lambda line: emitted.append(line),
    )
    assert iters == 0
    assert emitted == []
    # Only the priming call should have happened.
    assert api.call_count == 1


def test_tail_keyboardinterrupt_exits_cleanly():
    """KeyboardInterrupt during sleep returns the iteration count seen so far."""
    api = _ScriptedJobsAPI([
        [],            # priming
        [{"id": 1}],   # iter 1: 1 new
        # Sleep raises KeyboardInterrupt before iter 2 starts.
    ])

    call_count = [0]

    def sleep_then_interrupt(_d):
        call_count[0] += 1
        if call_count[0] >= 2:
            raise KeyboardInterrupt()

    emitted: list = []
    iters = wa.jobs_tail_loop(
        api, recipe_id=42, status_filter=None,
        interval_seconds=0.1, max_iterations=10,
        _sleep=sleep_then_interrupt,
        _print=lambda line: emitted.append(line),
    )
    # One full iteration before the interrupt fires on the second sleep.
    assert iters == 1
    assert len(emitted) == 1
    assert json.loads(emitted[0])["id"] == 1


def test_tail_status_filter_is_passed_to_api():
    seen_status: list = []

    class API:
        def jobs_list(self, _r, status=None):
            seen_status.append(status)
            return []

    wa.jobs_tail_loop(
        API(), recipe_id=42, status_filter="failed",
        interval_seconds=0.0, max_iterations=2,
        _sleep=lambda d: None, _print=lambda _l: None,
    )
    # Priming + 2 iterations
    assert seen_status == ["failed", "failed", "failed"]


def test_tail_skips_non_dict_entries():
    api = _ScriptedJobsAPI([
        [],
        ["not a dict", None, {"id": 7}],
    ])
    emitted: list = []
    wa.jobs_tail_loop(
        api, recipe_id=42, status_filter=None,
        interval_seconds=0.0, max_iterations=1,
        _sleep=lambda d: None, _print=lambda line: emitted.append(line),
    )
    parsed = [json.loads(line) for line in emitted]
    assert [r["id"] for r in parsed] == [7]


def test_tail_skips_entries_without_id():
    """A job dict lacking `id` cannot be deduped, so we skip it for safety."""
    api = _ScriptedJobsAPI([
        [],
        [{"id": 1}, {"status": "failed"}],  # second dict has no id
    ])
    emitted: list = []
    wa.jobs_tail_loop(
        api, recipe_id=42, status_filter=None,
        interval_seconds=0.0, max_iterations=1,
        _sleep=lambda d: None, _print=lambda line: emitted.append(line),
    )
    parsed = [json.loads(line) for line in emitted]
    assert [r["id"] for r in parsed] == [1]


# ---------------------------------------------------------------------------
# CLI argparse
# ---------------------------------------------------------------------------


def test_cli_argparse_tail_requires_recipe_id():
    import subprocess
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "jobs", "tail"],
        capture_output=True, text=True,
    )
    assert result.returncode == 2
    assert "--recipe-id" in result.stderr


def test_cli_argparse_tail_rejects_non_int_max_iterations():
    import subprocess
    result = subprocess.run(
        [
            sys.executable, str(SCRIPT),
            "jobs", "tail", "--recipe-id", "1",
            "--max-iterations", "not-an-int",
        ],
        capture_output=True, text=True,
    )
    assert result.returncode == 2


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
