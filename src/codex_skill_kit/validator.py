from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import re


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Finding:
    severity: Severity
    message: str


LOCAL_LINK = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
TRIGGER_WORDS = ("use this skill", "when the user", "trigger", "workflow")


def validate_skill(path: Path) -> list[Finding]:
    findings: list[Finding] = []

    if not path.exists():
        return [Finding(Severity.ERROR, f"{path} does not exist")]
    if not path.is_dir():
        return [Finding(Severity.ERROR, f"{path} is not a directory")]

    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        return [Finding(Severity.ERROR, "missing SKILL.md")]

    content = skill_md.read_text(encoding="utf-8")
    stripped = content.strip()
    lower_content = content.lower()

    if not stripped:
        findings.append(Finding(Severity.ERROR, "SKILL.md is empty"))
        return findings

    if not stripped.startswith("# "):
        findings.append(Finding(Severity.ERROR, "SKILL.md should start with a top-level heading"))

    words = re.findall(r"\b[\w'-]+\b", content)
    if len(words) < 40:
        findings.append(Finding(Severity.WARNING, "SKILL.md is very short; add workflow detail"))
    if len(words) > 1200:
        findings.append(Finding(Severity.WARNING, "SKILL.md is long; consider moving detail to references"))

    if not any(word in lower_content for word in TRIGGER_WORDS):
        findings.append(
            Finding(
                Severity.WARNING,
                "SKILL.md should say when Codex should use the skill",
            )
        )

    if "## workflow" not in lower_content and "## steps" not in lower_content:
        findings.append(Finding(Severity.WARNING, "SKILL.md should include a workflow or steps section"))

    findings.extend(_missing_local_links(path, content))

    if not (path / "README.md").exists():
        findings.append(Finding(Severity.WARNING, "README.md is recommended for shared skills"))

    examples = path / "examples"
    if not examples.exists():
        findings.append(Finding(Severity.WARNING, "examples/ is recommended for reusable skills"))

    return findings


def _missing_local_links(base_path: Path, content: str) -> list[Finding]:
    findings: list[Finding] = []
    for raw_target in LOCAL_LINK.findall(content):
        target = raw_target.split("#", 1)[0].strip()
        if not target:
            continue
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        target_path = (base_path / target).resolve()
        try:
            target_path.relative_to(base_path.resolve())
        except ValueError:
            findings.append(Finding(Severity.ERROR, f"local link escapes skill directory: {raw_target}"))
            continue
        if not target_path.exists():
            findings.append(Finding(Severity.ERROR, f"local link target is missing: {raw_target}"))
    return findings

