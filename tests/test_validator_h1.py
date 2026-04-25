"""SKILL.md without a top-level heading should report H1_MISSING."""

from __future__ import annotations

from codex_skill_kit import validate_skill


def test_missing_h1_reports_error(tmp_path):
    skill_dir = tmp_path / "no-h1"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "## Subheading only\n\nBody paragraph that is long enough to not trip the description warning.\n",
        encoding="utf-8",
    )

    result = validate_skill(skill_dir)

    error_codes = [issue.code for issue in result.issues if issue.severity == "error"]
    assert "H1_MISSING" in error_codes
