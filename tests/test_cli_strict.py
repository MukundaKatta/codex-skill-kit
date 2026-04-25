"""--strict turns warn-level findings into a failing exit code."""

from __future__ import annotations

from codex_skill_kit.cli import main


def _write_warn_only_skill(skill_dir):
    """SKILL.md with H1 only -> TRIGGER_MISSING (warn) but no errors."""

    (skill_dir / "SKILL.md").write_text("# Just A Title\n", encoding="utf-8")
    # README + examples keep the info-level findings out of the way.
    (skill_dir / "README.md").write_text("# Just A Title\n", encoding="utf-8")
    examples = skill_dir / "examples"
    examples.mkdir()
    (examples / "basic.md").write_text("# Example\n", encoding="utf-8")


def test_validate_warn_only_default_passes(tmp_path):
    skill_dir = tmp_path / "warn-only"
    skill_dir.mkdir()
    _write_warn_only_skill(skill_dir)

    assert main(["validate", str(skill_dir)]) == 0


def test_validate_warn_only_strict_fails(tmp_path):
    skill_dir = tmp_path / "warn-only-strict"
    skill_dir.mkdir()
    _write_warn_only_skill(skill_dir)

    assert main(["validate", str(skill_dir), "--strict"]) == 1
