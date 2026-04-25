"""Command-line interface for codex-skill-kit (entry: ``csk``)."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional, Sequence

from . import __version__
from .scaffold import scaffold_skill
from .validator import ERROR, INFO, WARN, validate_skill


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csk",
        description="Scaffold and validate Codex skills.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")

    new_parser = subparsers.add_parser("new", help="Create a new skill directory.")
    new_parser.add_argument("name", help="Skill directory name, e.g. repo-doctor.")
    new_parser.add_argument(
        "--description",
        required=True,
        help="One-sentence description for SKILL.md.",
    )
    new_parser.add_argument(
        "--dir",
        dest="target_dir",
        default=".",
        help="Directory in which to create the skill folder (default: current directory).",
    )
    new_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing skill directory.",
    )

    validate_parser = subparsers.add_parser("validate", help="Validate a skill directory.")
    validate_parser.add_argument("skill_dir", help="Path to a skill directory.")
    validate_parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Emit JSON output instead of grouped text.",
    )
    validate_parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures.",
    )

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "new":
        return _cmd_new(args)

    if args.command == "validate":
        return _cmd_validate(args)

    parser.error(f"Unknown command: {args.command}")
    return 2


def _cmd_new(args: argparse.Namespace) -> int:
    try:
        skill_path = scaffold_skill(
            args.name,
            description=args.description,
            target_dir=Path(args.target_dir),
            force=args.force,
        )
    except FileExistsError as exc:
        print(f"error: {exc}")
        return 1
    except ValueError as exc:
        print(f"error: {exc}")
        return 2

    print(f"Created skill at {skill_path}")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    result = validate_skill(args.skill_dir)

    if args.as_json:
        payload = {
            "ok": result.ok,
            "issues": [asdict(issue) for issue in result.issues],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        _print_human(result)

    has_errors = any(issue.severity == ERROR for issue in result.issues)
    has_warns = any(issue.severity == WARN for issue in result.issues)
    if has_errors or (args.strict and has_warns):
        return 1
    return 0


def _print_human(result) -> None:
    if not result.issues:
        print("ok: skill looks good")
        return

    grouped = {ERROR: [], WARN: [], INFO: []}
    for issue in result.issues:
        grouped.setdefault(issue.severity, []).append(issue)

    for severity in (ERROR, WARN, INFO):
        bucket = grouped.get(severity, [])
        if not bucket:
            continue
        print(f"{severity}:")
        for issue in bucket:
            location = f" ({issue.path})" if issue.path else ""
            print(f"  [{issue.code}] {issue.message}{location}")


if __name__ == "__main__":
    raise SystemExit(main())
