"""An empty directory should report SKILL_MD_MISSING."""

from __future__ import annotations

from codex_skill_kit import validate_skill


def test_empty_dir_reports_missing_skill_md(tmp_path):
    result = validate_skill(tmp_path)

    assert result.ok is False
    codes = [issue.code for issue in result.issues if issue.severity == "error"]
    assert "SKILL_MD_MISSING" in codes
