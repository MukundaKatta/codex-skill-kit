"""Local markdown references must resolve to files on disk."""

from __future__ import annotations

from codex_skill_kit import validate_skill


def _write_skill(skill_dir, link_target):
    (skill_dir / "SKILL.md").write_text(
        "# Linked Skill\n"
        "\n"
        "Use this when the user needs a documented reference. The description paragraph is long enough to satisfy the validator's length checks.\n"
        "\n"
        f"See [helper]({link_target}) for more.\n",
        encoding="utf-8",
    )


def test_missing_local_ref_reports_error(tmp_path):
    skill_dir = tmp_path / "linked-missing"
    skill_dir.mkdir()
    _write_skill(skill_dir, "missing.md")

    result = validate_skill(skill_dir)

    broken = [issue for issue in result.issues if issue.code == "BROKEN_LOCAL_REF"]
    assert broken, "expected at least one BROKEN_LOCAL_REF error"
    assert all(issue.severity == "error" for issue in broken)


def test_present_local_ref_has_no_broken_ref_error(tmp_path):
    skill_dir = tmp_path / "linked-present"
    skill_dir.mkdir()
    (skill_dir / "helper.md").write_text("# Helper\n", encoding="utf-8")
    _write_skill(skill_dir, "helper.md")

    result = validate_skill(skill_dir)

    assert not [issue for issue in result.issues if issue.code == "BROKEN_LOCAL_REF"]
