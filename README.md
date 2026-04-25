# codex-skill-kit

Small command-line tools for building Codex skills.

`codex-skill-kit` helps you scaffold a skill directory and validate the files that make a skill easy for Codex to load, understand, and use.

## Install for development

```bash
python -m pip install -e .
```

## Create a skill

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

## Validate a skill

```bash
csk validate repo-doctor
```

The validator checks for:

- a `SKILL.md` file
- a top-level Markdown heading
- a concise trigger or usage sentence
- a reasonable description length
- references to missing local files
- optional README and examples coverage

### Validation rules

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

`csk validate` exits 0 unless an error-severity issue is reported. With `--strict`, warnings also fail. Pass `--json` for machine-readable output (`{"ok": bool, "issues": [...]}`).

## Why this exists

Codex skills are most useful when they are small, clear, and easy to inspect. This package makes that quality bar repeatable, so skill authors can catch rough edges before opening pull requests or sharing skills with a team.

