"""Validate that a skill directory is well-formed for Codex to load."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Union

# Severity tiers used by every issue. Keep these as plain strings (not an
# Enum) so JSON output is trivially serializable across stdlib boundaries.
ERROR = "error"
WARN = "warn"
INFO = "info"

# Phrases that look like a usage trigger. Matched case-insensitively as
# substrings against the description paragraph.
_TRIGGER_PHRASES = ("use this when", "use when", "trigger:", "for ")

# Markdown link with a non-remote target. Capture the target so the
# validator can resolve it relative to the skill directory.
_LINK_RE = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


@dataclass(frozen=True)
class Issue:
    """A single validator finding."""

    severity: str  # "error" | "warn" | "info"
    code: str
    message: str
    path: Optional[str] = None


@dataclass
class ValidationResult:
    """Aggregate result for a skill directory."""

    issues: List[Issue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True iff there are no error-severity issues."""

        return not any(issue.severity == ERROR for issue in self.issues)


def validate_skill(skill_dir: Union[str, Path]) -> ValidationResult:
    """Validate the skill directory at ``skill_dir`` and return a result."""

    base = Path(skill_dir)
    issues: List[Issue] = []

    skill_md = base / "SKILL.md"
    if not skill_md.is_file():
        issues.append(
            Issue(
                severity=ERROR,
                code="SKILL_MD_MISSING",
                message="SKILL.md not found in skill directory.",
                path=str(skill_md),
            )
        )
        # Without a SKILL.md the rest of the content checks cannot run, but
        # we still surface README/examples info so authors get the full list.
        _check_optional_assets(base, issues)
        return ValidationResult(issues=issues)

    content = skill_md.read_text(encoding="utf-8")
    _check_skill_md(content, skill_md, base, issues)
    _check_optional_assets(base, issues)

    return ValidationResult(issues=issues)


def _check_skill_md(content: str, skill_md: Path, base: Path, issues: List[Issue]) -> None:
    h1 = _first_h1(content)
    if h1 is None:
        issues.append(
            Issue(
                severity=ERROR,
                code="H1_MISSING",
                message="SKILL.md must start with a top-level Markdown heading (# Title).",
                path=str(skill_md),
            )
        )

    description = _first_paragraph_after_h1(content)
    desc_text = (description or "").strip()

    # Trigger / usage sentence check: rely on either an explicit trigger
    # phrase or a paragraph long enough to read as a usage description.
    has_trigger_phrase = any(p in desc_text.lower() for p in _TRIGGER_PHRASES)
    has_concise_sentence = len(desc_text) >= 20
    if not (has_trigger_phrase or has_concise_sentence):
        issues.append(
            Issue(
                severity=WARN,
                code="TRIGGER_MISSING",
                message=(
                    "SKILL.md should include a concise trigger or usage sentence "
                    "(e.g. 'Use this when ...')."
                ),
                path=str(skill_md),
            )
        )

    if desc_text and len(desc_text) < 30:
        issues.append(
            Issue(
                severity=WARN,
                code="DESCRIPTION_TOO_SHORT",
                message="SKILL.md description paragraph is shorter than 30 characters.",
                path=str(skill_md),
            )
        )

    if len(desc_text) > 1500:
        issues.append(
            Issue(
                severity=ERROR,
                code="DESCRIPTION_TOO_LONG",
                message="SKILL.md description paragraph exceeds 1500 characters; tighten it.",
                path=str(skill_md),
            )
        )

    for target in _local_link_targets(content):
        resolved = (base / target).resolve()
        if not resolved.exists():
            issues.append(
                Issue(
                    severity=ERROR,
                    code="BROKEN_LOCAL_REF",
                    message=f"Local reference '{target}' does not exist on disk.",
                    path=str(skill_md),
                )
            )


def _check_optional_assets(base: Path, issues: List[Issue]) -> None:
    if not (base / "README.md").is_file():
        issues.append(
            Issue(
                severity=INFO,
                code="README_MISSING",
                message="README.md is recommended for shared skills.",
                path=str(base / "README.md"),
            )
        )

    examples = base / "examples"
    if not examples.is_dir() or not any(examples.iterdir()):
        issues.append(
            Issue(
                severity=INFO,
                code="EXAMPLES_MISSING",
                message="examples/ directory is empty or missing; add at least one example.",
                path=str(examples),
            )
        )


def _first_h1(content: str) -> Optional[str]:
    """Return the text of the first ``# heading`` line, or ``None``."""

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            return stripped[2:].strip()
    return None


def _first_paragraph_after_h1(content: str) -> Optional[str]:
    """Return the first non-empty paragraph that is not a heading.

    The validator treats the first such paragraph as the skill description.
    """

    lines = content.splitlines()
    seen_h1 = False
    paragraph: List[str] = []
    for line in lines:
        stripped = line.strip()
        if not seen_h1:
            # Skip everything until we are past the first H1.
            if stripped.startswith("# ") and not stripped.startswith("## "):
                seen_h1 = True
            continue

        if stripped.startswith("#"):
            # We hit the next heading — stop accumulating.
            if paragraph:
                break
            continue

        if stripped == "":
            if paragraph:
                break
            continue

        paragraph.append(stripped)

    return " ".join(paragraph) if paragraph else None


def _local_link_targets(content: str) -> List[str]:
    """Return relative-link targets from the markdown content."""

    targets: List[str] = []
    for match in _LINK_RE.finditer(content):
        raw = match.group(1).strip()
        if not raw:
            continue
        lowered = raw.lower()
        if lowered.startswith(("http://", "https://", "mailto:", "#")):
            continue
        # Strip in-page anchors so '/path/to.md#section' resolves to the file.
        target = raw.split("#", 1)[0]
        if not target:
            continue
        targets.append(target)
    return targets
