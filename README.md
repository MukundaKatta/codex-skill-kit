# codex-skill-kit

[![CI](https://github.com/MukundaKatta/codex-skill-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/MukundaKatta/codex-skill-kit/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/codex-skill-kit.svg)](https://pypi.org/project/codex-skill-kit/)
[![Python](https://img.shields.io/pypi/pyversions/codex-skill-kit.svg)](https://pypi.org/project/codex-skill-kit/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Small command-line tools for building Codex skills. `codex-skill-kit` scaffolds a fresh skill directory with the right shape, and validates skill files so they are easy for Codex to load and use.

## Install

```bash
pip install codex-skill-kit
```

The package ships two console entry points: `codex-skill-kit` (long form) and `csk` (short).

## Usage

### Create a skill

```bash
csk new repo-doctor --description "Inspect repositories for agent-ready project hygiene."
```

This creates:

```text
repo-doctor/
  SKILL.md
  README.md
  examples/
    basic.md
```

### Validate a skill

```bash
csk validate repo-doctor
```

The validator checks for:

- a `SKILL.md` file at the skill root
- a top-level Markdown heading
- a concise trigger or usage sentence
- a reasonable description length
- references to missing local files
- optional README and examples coverage

`csk validate` exits `0` unless an error-severity issue is reported. With `--strict`, warnings also fail. Pass `--json` for machine-readable output (`{"ok": bool, "issues": [...]}`).

## Use as a library

```python
from codex_skill_kit import validate_skill, scaffold_skill

result = validate_skill("path/to/skill-dir")
if not result.ok:
    for issue in result.errors:
        print(issue.code, issue.message)

scaffold_skill("new-skill", description="What this skill does and when to use it.")
```

Exposed names: `scaffold_skill`, `validate_skill`, `ValidationResult`, `Issue`.

## Validation rules

| Code | Severity | Meaning |
| --- | --- | --- |
| `SKILL_MD_MISSING` | error | The skill directory has no `SKILL.md`. |
| `H1_MISSING` | error | `SKILL.md` does not start with a `#` top-level heading. |
| `TRIGGER_MISSING` | warn | The first paragraph after the H1 has no usage trigger sentence. |
| `DESCRIPTION_TOO_SHORT` | warn | The first description paragraph is shorter than 30 characters. |
| `DESCRIPTION_TOO_LONG` | error | The first description paragraph exceeds 1500 characters. |
| `BROKEN_LOCAL_REF` | error | A local Markdown link points to a file that does not exist on disk. |
| `README_MISSING` | info | No `README.md` is present (recommended for shared skills). |
| `EXAMPLES_MISSING` | info | The `examples/` directory is missing or empty. |

## Why this exists

Codex skills are most useful when they are small, clear, and easy to inspect. This package makes that quality bar repeatable, so skill authors can catch rough edges before opening pull requests or sharing skills with a team.

## Development

```bash
pip install -e '.[dev]'
pytest
```

## License

MIT
