"""``csk validate --json`` must emit machine-parseable output."""

from __future__ import annotations

import json

from codex_skill_kit import scaffold_skill
from codex_skill_kit.cli import main


def test_validate_json_output_shape(tmp_path, capsys):
    skill_path = scaffold_skill(
        "json-skill",
        description="A skill that demonstrates JSON validator output.",
        target_dir=tmp_path,
    )

    exit_code = main(["validate", str(skill_path), "--json"])

    captured = capsys.readouterr().out
    payload = json.loads(captured)

    assert exit_code == 0
    assert isinstance(payload, dict)
    assert payload["ok"] is True
    assert isinstance(payload["issues"], list)
    for issue in payload["issues"]:
        assert set(issue.keys()) == {"code", "message", "path", "severity"}


def test_validate_json_reports_missing_skill_md(tmp_path, capsys):
    exit_code = main(["validate", str(tmp_path), "--json"])

    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 1
    assert payload["ok"] is False
    codes = {issue["code"] for issue in payload["issues"]}
    assert "SKILL_MD_MISSING" in codes
