"""TICKET-015: tests for scripts/upstream_status.sh.

Two layers:

(a) Presence/structure — env-independent, no git invoke. Asserts the
    script exists, is executable, has a bash shebang, fetches, prints the
    four severity labels, honors UPSTREAM_STATUS_REF, and that the Makefile
    target and README reference exist.

(b) Behavioral — runs the script against a self-contained local temp git
    fixture (bare "remote" + working clone built in tmp_path). No network,
    and it never touches the operator's real $CLAUDE_TRADING_SKILLS_REPO.
    Exercises ref resolution, incoming range, detached HEAD, the
    no-tracking-upstream case, override handling, severity classification,
    and the working-tree-safe guarantee.
"""
from __future__ import annotations

import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "upstream_status.sh"
MAKEFILE = REPO / "Makefile"
README = REPO / "README.md"

SEVERITY_LABELS = ["NONE", "LOW", "MEDIUM", "HIGH"]


# --- (a) presence / structure ---------------------------------------------


def test_script_exists_and_executable():
    assert SCRIPT.exists(), "scripts/upstream_status.sh missing"
    mode = SCRIPT.stat().st_mode
    assert mode & stat.S_IXUSR, "scripts/upstream_status.sh is not executable"


def test_script_has_bash_shebang():
    first = SCRIPT.read_text(encoding="utf-8").splitlines()[0]
    assert first.startswith("#!") and "bash" in first, f"bad shebang: {first!r}"


def test_script_fetches_remote_metadata():
    assert "git" in SCRIPT.read_text(encoding="utf-8")
    assert "fetch" in SCRIPT.read_text(encoding="utf-8"), "script must git fetch"


@pytest.mark.parametrize("label", SEVERITY_LABELS)
def test_script_mentions_severity_label(label: str):
    assert label in SCRIPT.read_text(encoding="utf-8"), (
        f"script missing severity label {label!r}"
    )


def test_script_honors_override_env():
    assert "UPSTREAM_STATUS_REF" in SCRIPT.read_text(encoding="utf-8")


def test_makefile_has_upstream_status_target():
    text = MAKEFILE.read_text(encoding="utf-8")
    assert "upstream-status:" in text, "Makefile missing upstream-status target"
    assert "upstream-status" in text.split(".PHONY")[1].split("\n")[0], (
        "upstream-status not in .PHONY"
    )


def test_readme_references_upstream_status():
    assert "make upstream-status" in README.read_text(encoding="utf-8")


# --- (b) behavioral against a local temp git fixture ----------------------

git = shutil.which("git")
pytestmark_behavioral = pytest.mark.skipif(git is None, reason="git not available")

GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.com",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.com",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_SYSTEM": "/dev/null",
}


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        [git, *args], cwd=str(cwd), env=GIT_ENV,
        capture_output=True, text=True, check=True,
    ).stdout


def _run_status(repo: Path, ref: str | None = None) -> str:
    env = {**GIT_ENV, "CLAUDE_TRADING_SKILLS_REPO": str(repo)}
    if ref is not None:
        env["UPSTREAM_STATUS_REF"] = ref
    proc = subprocess.run(
        ["bash", str(SCRIPT)], env=env, capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"script failed: {proc.stderr}"
    return proc.stdout


def _risk(out: str) -> str:
    for line in out.splitlines():
        if line.startswith("Local-edit risk:"):
            return line.split(":", 1)[1].strip()
    raise AssertionError("no risk line in output")


@pytest.fixture()
def upstream_pair(tmp_path: Path):
    """Bare 'remote' + a working clone one commit behind it.

    Returns (clone_path, c2_subject). The clone's `main` tracks
    `origin/main`; `origin/main` is one commit (C2) ahead of the clone's
    HEAD (C1), so the script should report C2 as incoming.
    """
    if git is None:
        pytest.skip("git not available")
    remote = tmp_path / "remote.git"
    _git(tmp_path, "init", "--bare", "--initial-branch=main", str(remote))

    seed = tmp_path / "seed"
    _git(tmp_path, "clone", str(remote), str(seed))
    (seed / "skills" / "foo").mkdir(parents=True)
    (seed / "skills" / "foo" / "SKILL.md").write_text("v1\n", encoding="utf-8")
    (seed / "workflows").mkdir()
    (seed / "workflows" / "bar.yaml").write_text("name: bar\n", encoding="utf-8")
    _git(seed, "add", "-A")
    _git(seed, "commit", "-m", "C1 seed")
    _git(seed, "push", "origin", "main")
    # C2 — the incoming commit.
    (seed / "skills" / "foo" / "SKILL.md").write_text("v2\n", encoding="utf-8")
    (seed / "workflows" / "baz.yaml").write_text("name: baz\n", encoding="utf-8")
    _git(seed, "add", "-A")
    _git(seed, "commit", "-m", "C2 incoming change")
    _git(seed, "push", "origin", "main")

    clone = tmp_path / "clone"
    _git(tmp_path, "clone", str(remote), str(clone))
    _git(clone, "reset", "--hard", "HEAD~1")  # one behind → C2 is incoming
    return clone, "C2 incoming change"


@pytestmark_behavioral
def test_clean_clone_reports_none_and_incoming(upstream_pair):
    clone, c2 = upstream_pair
    out = _run_status(clone)
    assert _risk(out) == "NONE", out
    assert c2 in out, "incoming commit subject not shown"
    assert "baz.yaml" in out, "incoming workflows/ file not listed"
    assert "skills/foo/SKILL.md" in out, "incoming skills/ file not listed"


@pytestmark_behavioral
def test_dirty_skills_reports_high(upstream_pair):
    clone, _ = upstream_pair
    (clone / "skills" / "foo" / "SKILL.md").write_text("hand edit\n", encoding="utf-8")
    assert _risk(_run_status(clone)) == "HIGH"


@pytestmark_behavioral
def test_dirty_workflows_reports_high(upstream_pair):
    clone, _ = upstream_pair
    (clone / "workflows" / "bar.yaml").write_text("name: bar\nedit: 1\n", encoding="utf-8")
    assert _risk(_run_status(clone)) == "HIGH"


@pytestmark_behavioral
def test_local_commit_ahead_reports_high(upstream_pair):
    clone, _ = upstream_pair
    (clone / "skills" / "foo" / "local.md").write_text("x\n", encoding="utf-8")
    _git(clone, "add", "-A")
    _git(clone, "commit", "-m", "local ahead")
    assert _risk(_run_status(clone)) == "HIGH"


@pytestmark_behavioral
def test_detached_head_reports_high_with_incoming(upstream_pair):
    clone, c2 = upstream_pair
    _git(clone, "checkout", "--detach")
    out = _run_status(clone)
    assert _risk(out) == "HIGH", out
    # origin/HEAD still resolves, so the incoming section still renders.
    assert c2 in out, "incoming should still render via origin/HEAD on detached HEAD"
    assert "UNRESOLVED" not in out.split("Incoming")[1].split("Local-edit risk")[0]


@pytestmark_behavioral
def test_no_remote_reports_unresolved_and_at_least_medium(upstream_pair):
    clone, _ = upstream_pair
    _git(clone, "remote", "remove", "origin")
    out = _run_status(clone)
    assert "UNRESOLVED" in out
    assert _risk(out) in {"MEDIUM", "HIGH"}
    assert "skipped" in out.lower()


@pytestmark_behavioral
def test_no_tracking_upstream_but_origin_head_is_not_none(upstream_pair):
    clone, c2 = upstream_pair
    _git(clone, "branch", "--unset-upstream")
    out = _run_status(clone)
    # tracking_upstream=false → must NOT be NONE even though the tree is clean.
    assert _risk(out) != "NONE", out
    assert _risk(out) in {"MEDIUM", "HIGH"}
    assert c2 in out, "incoming should still render via origin/HEAD fallback"


@pytestmark_behavioral
def test_override_remote_tracking_ref_selects_ref(upstream_pair):
    clone, c2 = upstream_pair
    out = _run_status(clone, ref="origin/main")
    assert "origin/main" in out
    assert c2 in out
    assert _risk(out) == "NONE", out


@pytestmark_behavioral
def test_override_non_remote_ref_skips_fetch_and_at_least_medium(upstream_pair):
    clone, _ = upstream_pair
    sha = _git(clone, "rev-parse", "HEAD").strip()
    out = _run_status(clone, ref=sha)
    assert _risk(out) in {"MEDIUM", "HIGH"}
    assert "fetch skipped" in out.lower()


@pytestmark_behavioral
def test_working_tree_unchanged_after_run(upstream_pair):
    clone, _ = upstream_pair
    before = _git(clone, "status", "--porcelain")
    _run_status(clone)
    after = _git(clone, "status", "--porcelain")
    assert before == after, "script must not modify the working tree"
