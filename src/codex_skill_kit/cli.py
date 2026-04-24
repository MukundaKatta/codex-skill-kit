from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Sequence

from .scaffold import create_skill
from .validator import Severity, validate_skill


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csk",
        description="Scaffold and validate Codex skills.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new", help="Create a new skill directory.")
    new_parser.add_argument("name", help="Skill directory name, for example repo-doctor.")
    new_parser.add_argument(
        "--description",
        default="Describe when Codex should use this skill.",
        help="One-sentence description for SKILL.md.",
    )
    new_parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory where the skill folder should be created.",
    )
    new_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files when present.",
    )

    validate_parser = subparsers.add_parser("validate", help="Validate a skill directory.")
    validate_parser.add_argument("path", help="Path to a skill directory.")
    validate_parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures.",
    )

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "new":
        skill_path = create_skill(
            name=args.name,
            description=args.description,
            output_dir=Path(args.output_dir),
            force=args.force,
        )
        print(f"Created skill at {skill_path}")
        return 0

    if args.command == "validate":
        findings = validate_skill(Path(args.path))
        for finding in findings:
            print(f"{finding.severity.value}: {finding.message}")

        has_errors = any(finding.severity == Severity.ERROR for finding in findings)
        has_warnings = any(finding.severity == Severity.WARNING for finding in findings)
        if has_errors or (args.strict and has_warnings):
            return 1

        if not findings:
            print("ok: skill looks good")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
