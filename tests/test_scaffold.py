"""Tests for the scaffolding helper."""

from __future__ import annotations

import pytest

from codex_skill_kit import scaffold_skill


def test_scaffold_creates_expected_files(tmp_path):
    skill_path = scaffold_skill(
        "repo-doctor",
        description="Inspect repositories for agent-ready project hygiene.",
        target_dir=tmp_path,
    )

    assert skill_path == tmp_path / "repo-doctor"
    assert skill_path.is_dir()
    assert (skill_path / "SKILL.md").is_file()
    assert (skill_path / "README.md").is_file()
    assert (skill_path / "examples").is_dir()
    assert (skill_path / "examples" / "basic.md").is_file()

    skill_md = (skill_path / "SKILL.md").read_text(encoding="utf-8")
    assert skill_md.startswith("# Repo Doctor")
    assert "Inspect repositories for agent-ready project hygiene." in skill_md
    assert "## When to use" in skill_md
    assert "## How it works" in skill_md
    assert "## Examples" in skill_md


def test_scaffold_refuses_to_overwrite(tmp_path):
    scaffold_skill("demo", description="A demo skill.", target_dir=tmp_path)
    with pytest.raises(FileExistsError):
        scaffold_skill("demo", description="A demo skill.", target_dir=tmp_path)


def test_scaffold_force_overwrites(tmp_path):
    skill_path = scaffold_skill("demo", description="First version.", target_dir=tmp_path)
    # Drop a stray file to confirm force replaces the directory cleanly.
    (skill_path / "stray.txt").write_text("leftover", encoding="utf-8")

    scaffold_skill(
        "demo",
        description="Second version with a longer description.",
        target_dir=tmp_path,
        force=True,
    )

    assert not (skill_path / "stray.txt").exists()
    skill_md = (skill_path / "SKILL.md").read_text(encoding="utf-8")
    assert "Second version" in skill_md
