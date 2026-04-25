"""``csk new`` should scaffold the expected files via the CLI."""

from __future__ import annotations

from codex_skill_kit.cli import main


def test_cli_new_creates_files(tmp_path, capsys):
    exit_code = main(
        [
            "new",
            "demo",
            "--description",
            "Inspect things.",
            "--dir",
            str(tmp_path),
        ]
    )

    assert exit_code == 0

    skill_dir = tmp_path / "demo"
    assert skill_dir.is_dir()
    assert (skill_dir / "SKILL.md").is_file()
    assert (skill_dir / "README.md").is_file()
    assert (skill_dir / "examples" / "basic.md").is_file()

    captured = capsys.readouterr().out
    assert "Created skill" in captured
    assert str(skill_dir) in captured
