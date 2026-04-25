"""A scaffolded skill should validate cleanly with no errors."""

from __future__ import annotations

from codex_skill_kit import scaffold_skill, validate_skill


def test_scaffolded_skill_validates(tmp_path):
    skill_path = scaffold_skill(
        "repo-doctor",
        description="Inspect repositories for agent-ready project hygiene.",
        target_dir=tmp_path,
    )

    result = validate_skill(skill_path)

    assert result.ok is True
    assert not [issue for issue in result.issues if issue.severity == "error"]
