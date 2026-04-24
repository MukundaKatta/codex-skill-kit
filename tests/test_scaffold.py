from codex_skill_kit.scaffold import create_skill


def test_create_skill_scaffolds_expected_files(tmp_path):
    skill = create_skill(
        "repo-doctor",
        "Inspect repositories for agent-ready hygiene.",
        tmp_path,
    )

    assert (skill / "SKILL.md").exists()
    assert (skill / "README.md").exists()
    assert (skill / "examples" / "basic.md").exists()
    assert "Repo Doctor" in (skill / "SKILL.md").read_text(encoding="utf-8")


def test_create_skill_rejects_non_kebab_case_name(tmp_path):
    try:
        create_skill("Repo Doctor", "Bad name.", tmp_path)
    except ValueError as exc:
        assert "kebab-case" in str(exc)
    else:
        raise AssertionError("Expected ValueError")

