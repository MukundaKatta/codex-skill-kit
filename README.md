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

## Why this exists

Codex skills are most useful when they are small, clear, and easy to inspect. This package makes that quality bar repeatable, so skill authors can catch rough edges before opening pull requests or sharing skills with a team.

