from codex_skill_kit.cli import main


def test_cli_new_and_validate(tmp_path, capsys):
    assert main(["new", "repo-doctor", "--output-dir", str(tmp_path)]) == 0
    assert main(["validate", str(tmp_path / "repo-doctor")]) == 0

    output = capsys.readouterr().out
    assert "Created skill" in output
    assert "ok: skill looks good" in output


def test_cli_validate_fails_for_missing_skill(tmp_path):
    missing = tmp_path / "missing"
    missing.mkdir()

    assert main(["validate", str(missing)]) == 1

