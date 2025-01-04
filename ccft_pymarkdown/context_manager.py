"""Custom context manager to clean custom-formatted tables only inside the context."""

from typing import TYPE_CHECKING

from . import utils
from .clean import clean
from .restore import restore

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence
    from pathlib import Path
    from types import TracebackType

__all__: "Sequence[str]" = ("CleanCustomFormattedTables",)


class CleanCustomFormattedTables:
    """Context manager to clean custom-formatted tables only inside the context."""

    def __init__(self, files: "Iterable[Path] | None" = None) -> None:
        """Initialise the context manager with the given selected files to clean."""
        self.files: Iterable[Path] = files if files is not None else utils.get_markdown_files()

    def __enter__(self) -> None:
        """Clean custom-formatted tables before entering the context."""
        clean(self.files)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: "TracebackType | None",  # noqa: PYI036
    ) -> None:
        """Restore Markdown files back to their original state."""
        restore(self.files)
