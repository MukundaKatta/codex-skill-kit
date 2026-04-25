"""A SKILL.md with only an H1 should warn about the missing trigger sentence."""

from __future__ import annotations

from codex_skill_kit import validate_skill


def test_only_h1_warns_trigger_missing(tmp_path):
    skill_dir = tmp_path / "trigger"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("# Title Only\n", encoding="utf-8")

    result = validate_skill(skill_dir)

    warn_codes = [issue.code for issue in result.issues if issue.severity == "warn"]
    assert "TRIGGER_MISSING" in warn_codes
