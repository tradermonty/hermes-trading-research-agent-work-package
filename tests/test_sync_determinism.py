"""B-2a generator ownership / `--write` determinism tests.

Locks in these contracts:

1. `sync(..., write=True)` honors `x-generated:` on existing bundles:
   - `false`  → SKIP + WARN, file untouched.
   - missing  → SKIP + WARN (legacy unknown), file untouched.
   - `true`   → write only if rendered content differs (write-if-changed,
     mtime preserved on no-op).
2. `--force-overwrite` collapses every branch to "rewrite when the
   content actually differs".
3. New mapping entries (`skill-bundles/<slug>.yaml` absent) are
   created with `x-generated: true`.
4. `update_external_config()` is a no-op when the env entry is
   already present in `skills.external_dirs[]`.
5. The shipped repo state is the canonical second-run-no-op: two
   consecutive `sync(..., write=True)` calls leave every
   `skill-bundles/*.yaml` and `config.yaml` byte- and mtime-
   identical. This is the TICKET-004a Done-condition test.

In-process throughout — subprocess + cwd would not help here
because `ROOT` and `ENV_FILE` are derived from `__file__`.
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_FILE = REPO_ROOT / "scripts" / "sync_claude_trading_skills.py"


def _import_sync_module():
    """Import scripts/sync_claude_trading_skills.py for in-process tests.

    Register the module in sys.modules before exec_module so dataclass
    decorators on Python 3.14 can resolve __module__ correctly.
    """
    cached = sys.modules.get("b2a_syncmod")
    if cached is not None:
        return cached
    spec = importlib.util.spec_from_file_location("b2a_syncmod", SCRIPT_FILE)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["b2a_syncmod"] = mod
    spec.loader.exec_module(mod)
    return mod


# --- shared fixtures ----------------------------------------------------------


@pytest.fixture
def syncmod():
    return _import_sync_module()


@pytest.fixture
def mapping_one(tmp_path: Path):
    """Create a minimal profile root with a single mapping entry.

    Returns (profile_root, source_root, slug, mapping_skills). The source
    root is a stub directory; tests using sync() must monkeypatch
    discover_skills so the skills lookup does not require real SKILL.md
    files.
    """
    profile = tmp_path / "profile"
    (profile / "data").mkdir(parents=True)
    (profile / "skill-bundles").mkdir()
    slug = "my-test-routine"
    skills_used = ["trading-skills-navigator", "market-breadth-analyzer"]
    mapping = {
        "workflows": {
            slug: {
                "title": "My test routine",
                "category": "test",
                "cadence": "manual",
                "canonical_source": "test-fixture",
                "skills": skills_used,
                "required_outputs": ["alpha", "beta"],
            }
        }
    }
    (profile / "data" / "skill-mapping.yaml").write_text(
        yaml.safe_dump(mapping, sort_keys=False), encoding="utf-8"
    )
    source = tmp_path / "src"
    (source / "skills").mkdir(parents=True)
    return profile, source, slug, skills_used


def _stub_discover(monkeypatch: pytest.MonkeyPatch, syncmod, skill_names):
    """Avoid the upstream SKILL.md walk by returning a fixed set."""
    monkeypatch.setattr(syncmod, "discover_skills", lambda src: set(skill_names))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --- protection / skip behaviour --------------------------------------------


def test_sync_skips_protected_bundles_by_default(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    syncmod,
):
    profile, source, slug, skills = mapping_one_helper(tmp_path)
    _stub_discover(monkeypatch, syncmod, skills)
    bundle_path = profile / "skill-bundles" / f"{slug}.yaml"
    bundle_path.write_text(
        yaml.safe_dump(
            {
                "name": slug,
                "description": "hand crafted",
                "x-generated": False,
                "skills": skills,
                "instruction": "# HAND EDIT — preserve me\n",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    sha_before = _sha(bundle_path)
    mtime_before = bundle_path.stat().st_mtime_ns

    result = syncmod.sync(
        source=source,
        profile_root=profile,
        mode="external",
        write=True,
        force_overwrite=False,
    )

    assert bundle_path in result.skipped_protected
    assert bundle_path not in result.wrote
    assert _sha(bundle_path) == sha_before
    assert bundle_path.stat().st_mtime_ns == mtime_before
    captured = capsys.readouterr()
    assert "SKIP protected bundle" in captured.err
    assert slug in captured.err


def test_sync_skips_legacy_bundles_by_default(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    syncmod,
):
    profile, source, slug, skills = mapping_one_helper(tmp_path)
    _stub_discover(monkeypatch, syncmod, skills)
    bundle_path = profile / "skill-bundles" / f"{slug}.yaml"
    bundle_path.write_text(
        yaml.safe_dump(
            {
                "name": slug,
                "description": "legacy, no key",
                # NOTE: x-generated key intentionally missing
                "skills": skills,
                "instruction": "# LEGACY\n",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    sha_before = _sha(bundle_path)
    mtime_before = bundle_path.stat().st_mtime_ns

    result = syncmod.sync(
        source=source,
        profile_root=profile,
        mode="external",
        write=True,
        force_overwrite=False,
    )

    assert bundle_path in result.skipped_legacy
    assert _sha(bundle_path) == sha_before
    assert bundle_path.stat().st_mtime_ns == mtime_before
    captured = capsys.readouterr()
    assert "SKIP legacy bundle" in captured.err


def test_sync_overwrites_when_force_overwrite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    syncmod,
):
    profile, source, slug, skills = mapping_one_helper(tmp_path)
    _stub_discover(monkeypatch, syncmod, skills)
    bundle_path = profile / "skill-bundles" / f"{slug}.yaml"
    bundle_path.write_text(
        yaml.safe_dump(
            {
                "name": slug,
                "description": "hand crafted",
                "x-generated": False,
                "skills": skills,
                "instruction": "# HAND EDIT\n",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    result = syncmod.sync(
        source=source,
        profile_root=profile,
        mode="external",
        write=True,
        force_overwrite=True,
    )
    assert bundle_path in result.forced
    new_body = yaml.safe_load(bundle_path.read_text(encoding="utf-8"))
    assert new_body["x-generated"] is True
    assert "HAND EDIT" not in (new_body.get("instruction") or "")


def test_sync_write_if_changed_preserves_mtime(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    syncmod,
):
    profile, source, slug, skills = mapping_one_helper(tmp_path)
    _stub_discover(monkeypatch, syncmod, skills)
    mapping = yaml.safe_load(
        (profile / "data" / "skill-mapping.yaml").read_text(encoding="utf-8")
    )
    canonical = syncmod.render_bundle(slug, mapping["workflows"][slug])
    bundle_path = profile / "skill-bundles" / f"{slug}.yaml"
    bundle_path.write_text(syncmod.dump_yaml(canonical), encoding="utf-8")
    sha_before = _sha(bundle_path)
    mtime_before = bundle_path.stat().st_mtime_ns

    result = syncmod.sync(
        source=source,
        profile_root=profile,
        mode="external",
        write=True,
        force_overwrite=False,
    )

    assert bundle_path in result.skipped_unchanged
    assert _sha(bundle_path) == sha_before
    assert bundle_path.stat().st_mtime_ns == mtime_before


def test_sync_creates_missing_bundle_with_x_generated_true(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    syncmod,
):
    profile, source, slug, skills = mapping_one_helper(tmp_path)
    _stub_discover(monkeypatch, syncmod, skills)
    bundle_path = profile / "skill-bundles" / f"{slug}.yaml"
    assert not bundle_path.exists()
    result = syncmod.sync(
        source=source,
        profile_root=profile,
        mode="external",
        write=True,
        force_overwrite=False,
    )
    assert bundle_path in result.wrote
    body = yaml.safe_load(bundle_path.read_text(encoding="utf-8"))
    assert body["x-generated"] is True


# --- update_external_config idempotency -------------------------------------


def test_update_external_config_is_idempotent(
    tmp_path: Path,
    syncmod,
):
    profile = tmp_path / "profile"
    profile.mkdir()
    config = profile / "config.yaml"
    config.write_text(
        yaml.safe_dump(
            {"skills": {"external_dirs": ["${CLAUDE_TRADING_SKILLS_REPO}/skills"]}},
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    sha_before = _sha(config)
    mtime_before = config.stat().st_mtime_ns

    wrote = syncmod.update_external_config(profile, tmp_path / "src", True)
    assert wrote is False
    assert _sha(config) == sha_before
    assert config.stat().st_mtime_ns == mtime_before


def test_update_external_config_writes_when_entry_missing(
    tmp_path: Path,
    syncmod,
):
    profile = tmp_path / "profile"
    profile.mkdir()
    config = profile / "config.yaml"
    config.write_text(
        yaml.safe_dump({"skills": {"external_dirs": []}}, sort_keys=False),
        encoding="utf-8",
    )
    wrote_first = syncmod.update_external_config(profile, tmp_path / "src", True)
    assert wrote_first is True
    # Second call must short-circuit even after the first write added the entry.
    sha_after_first = _sha(config)
    mtime_after_first = config.stat().st_mtime_ns
    wrote_second = syncmod.update_external_config(profile, tmp_path / "src", True)
    assert wrote_second is False
    assert _sha(config) == sha_after_first
    assert config.stat().st_mtime_ns == mtime_after_first


# --- real-repo second-run-noop (TICKET-004a Done condition) ----------------


def test_sync_second_run_is_a_noop_across_all_real_artifacts(
    syncmod,
):
    upstream = os.environ.get("CLAUDE_TRADING_SKILLS_REPO")
    if not upstream:
        pytest.skip("CLAUDE_TRADING_SKILLS_REPO unset")
    src = Path(upstream).expanduser()
    if not (src / "skills").is_dir():
        pytest.skip(f"upstream skills/ missing under {src}")
    bundles_dir = REPO_ROOT / "skill-bundles"
    config_path = REPO_ROOT / "config.yaml"

    def snapshot() -> dict[str, tuple[str, int]]:
        snap: dict[str, tuple[str, int]] = {}
        for p in sorted(bundles_dir.glob("*.yaml")):
            snap[str(p.relative_to(REPO_ROOT))] = (_sha(p), p.stat().st_mtime_ns)
        snap["config.yaml"] = (_sha(config_path), config_path.stat().st_mtime_ns)
        return snap

    before = snapshot()
    syncmod.sync(
        source=src,
        profile_root=REPO_ROOT,
        mode="external",
        write=True,
        force_overwrite=False,
    )
    mid = snapshot()
    syncmod.sync(
        source=src,
        profile_root=REPO_ROOT,
        mode="external",
        write=True,
        force_overwrite=False,
    )
    after = snapshot()

    # The shipped tip should be a no-op for both calls (every bundle is
    # `x-generated: false` and config.yaml already declares the entry).
    assert before == mid, f"first sync changed something: {set(before) ^ set(mid)}"
    assert mid == after, f"second sync changed something: {set(mid) ^ set(after)}"


# --- helpers shared across tests --------------------------------------------


def mapping_one_helper(tmp_path: Path):
    """Plain helper (callable from tests). Mirrors the `mapping_one` fixture
    layout. Useful when a test also wants to mutate the layout afterwards
    without going through fixture re-binding."""
    profile = tmp_path / "profile"
    (profile / "data").mkdir(parents=True)
    (profile / "skill-bundles").mkdir()
    slug = "my-test-routine"
    skills_used = ["trading-skills-navigator", "market-breadth-analyzer"]
    mapping = {
        "workflows": {
            slug: {
                "title": "My test routine",
                "category": "test",
                "cadence": "manual",
                "canonical_source": "test-fixture",
                "skills": skills_used,
                "required_outputs": ["alpha", "beta"],
            }
        }
    }
    (profile / "data" / "skill-mapping.yaml").write_text(
        yaml.safe_dump(mapping, sort_keys=False), encoding="utf-8"
    )
    source = tmp_path / "src"
    (source / "skills").mkdir(parents=True)
    return profile, source, slug, skills_used
