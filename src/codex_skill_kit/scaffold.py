from __future__ import annotations

import re
from pathlib import Path


VALID_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")


def create_skill(
    name: str,
    description: str,
    output_dir: Path,
    force: bool = False,
) -> Path:
    if not VALID_NAME.fullmatch(name):
        raise ValueError("Skill names should be lowercase kebab-case, for example repo-doctor.")

    skill_path = output_dir / name
    skill_path.mkdir(parents=True, exist_ok=True)
    examples_path = skill_path / "examples"
    examples_path.mkdir(exist_ok=True)

    files = {
        skill_path / "SKILL.md": _skill_md(name, description),
        skill_path / "README.md": _readme_md(name, description),
        examples_path / "basic.md": _example_md(name),
    }

    for path, content in files.items():
        if path.exists() and not force:
            continue
        path.write_text(content, encoding="utf-8")

    return skill_path


def _skill_md(name: str, description: str) -> str:
    title = name.replace("-", " ").title()
    return f"""# {title}

## Description

{description}

Use this skill when the user asks for workflows related to {name.replace("-", " ")}.

## Workflow

1. Clarify the user's goal and identify the smallest useful output.
2. Inspect the relevant files, examples, or references before changing anything.
3. Make focused edits or recommendations.
4. Verify the result with the lightest reliable check.

## Notes

- Keep output concise and actionable.
- Prefer existing project conventions over new abstractions.
"""


def _readme_md(name: str, description: str) -> str:
    title = name.replace("-", " ").title()
    return f"""# {title}

{description}

## Use

Place this directory in a Codex skills location, then ask Codex for work that matches the skill description.
"""


def _example_md(name: str) -> str:
    return f"""# Basic Example

User request:

```text
Use the {name} skill to help with this repo.
```

Expected behavior:

Codex loads the skill, follows its workflow, and verifies the result before responding.
"""

