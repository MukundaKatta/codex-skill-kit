"""Scaffold a new Codex skill directory with sensible defaults."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Union


def scaffold_skill(
    name: str,
    *,
    description: str,
    target_dir: Union[str, Path] = ".",
    force: bool = False,
) -> Path:
    """Create a new skill directory at ``<target_dir>/<name>``.

    Returns the absolute :class:`Path` of the created directory. Raises
    :class:`FileExistsError` if the directory already exists and ``force``
    is ``False``.
    """

    if not name or not name.strip():
        raise ValueError("Skill name must be a non-empty string.")

    target = Path(target_dir)
    skill_path = target / name

    if skill_path.exists():
        if not force:
            raise FileExistsError(
                f"Skill directory already exists: {skill_path}. Pass force=True to overwrite."
            )
        # Force-overwrite: remove the existing tree so the scaffold starts clean.
        shutil.rmtree(skill_path)

    examples_path = skill_path / "examples"
    examples_path.mkdir(parents=True, exist_ok=False)

    (skill_path / "SKILL.md").write_text(_skill_md(name, description), encoding="utf-8")
    (skill_path / "README.md").write_text(_readme_md(name, description), encoding="utf-8")
    (examples_path / "basic.md").write_text(_example_md(name), encoding="utf-8")

    return skill_path


def _humanize(name: str) -> str:
    """Convert a kebab- or snake-cased skill name to a human-readable title."""

    cleaned = name.replace("_", " ").replace("-", " ")
    parts = [part for part in cleaned.split() if part]
    return " ".join(part[:1].upper() + part[1:] for part in parts) if parts else name


def _skill_md(name: str, description: str) -> str:
    title = _humanize(name)
    return (
        f"# {title}\n"
        "\n"
        f"{description}\n"
        "\n"
        "## When to use\n"
        "\n"
        f"Use this skill when the user asks for help related to {title.lower()}.\n"
        "\n"
        "## How it works\n"
        "\n"
        "1. Clarify the user goal and identify the smallest useful output.\n"
        "2. Inspect the relevant files or examples before changing anything.\n"
        "3. Make focused edits or recommendations.\n"
        "4. Verify the result with the lightest reliable check.\n"
        "\n"
        "## Examples\n"
        "\n"
        "See [examples/basic.md](examples/basic.md).\n"
    )


def _readme_md(name: str, description: str) -> str:
    title = _humanize(name)
    return (
        f"# {title}\n"
        "\n"
        f"{description}\n"
        "\n"
        f"Drop this directory into a Codex skills location, then ask Codex for work that matches the {title.lower()} description.\n"
    )


def _example_md(name: str) -> str:
    return (
        "# Example\n"
        "\n"
        f"Input: ask Codex to use the {name} skill on a sample request.\n"
        "Output: Codex follows the skill workflow and returns a focused result.\n"
    )
