from codex_skill_kit.validator import Severity, validate_skill


def test_validate_good_skill(tmp_path):
    skill = tmp_path / "good-skill"
    skill.mkdir()
    (skill / "examples").mkdir()
    (skill / "README.md").write_text("# Good Skill\n", encoding="utf-8")
    (skill / "SKILL.md").write_text(
        """# Good Skill

## Description

Use this skill when the user needs a clear repository check.

## Workflow

1. Inspect the repository.
2. Check project metadata, test commands, dependency files, and documentation.
3. Report focused findings with file paths and practical next actions.
4. Verify the result with the smallest reliable local command.
5. Keep the response concise so the user can act on it immediately.
""",
        encoding="utf-8",
    )

    assert validate_skill(skill) == []


def test_validate_missing_skill_md(tmp_path):
    skill = tmp_path / "missing"
    skill.mkdir()

    findings = validate_skill(skill)

    assert findings[0].severity == Severity.ERROR
    assert "missing SKILL.md" in findings[0].message


def test_validate_missing_local_link(tmp_path):
    skill = tmp_path / "linked"
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        """# Linked

## Description

Use this skill when the user needs linked references.

## Workflow

Read [missing](references/missing.md), then summarize the result with enough useful detail.
""",
        encoding="utf-8",
    )

    findings = validate_skill(skill)

    assert any(finding.severity == Severity.ERROR for finding in findings)
    assert any("local link target is missing" in finding.message for finding in findings)
