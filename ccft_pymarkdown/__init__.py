"""Suppress custom-formatted table errors when linting using PyMarkdown in Markdown files."""

from typing import TYPE_CHECKING

from .clean import clean
from .console import run
from .context_manager import CleanCustomFormattedTables
from .restore import restore

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__: "Sequence[str]" = (
    "CleanCustomFormattedTables",
    "clean",
    "restore",
    "run",
)
