"""Utilities for scaffolding and validating Codex skills."""

from .scaffold import scaffold_skill
from .validator import Issue, ValidationResult, validate_skill

__version__ = "0.1.0"

__all__ = [
    "Issue",
    "ValidationResult",
    "__version__",
    "scaffold_skill",
    "validate_skill",
]
