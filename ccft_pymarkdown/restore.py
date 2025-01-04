"""Perform the restoration of Markdown files that had custom-formatted tables cleaned."""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence
    from logging import Logger
    from pathlib import Path
    from typing import Final, Literal

__all__: "Sequence[str]" = ("restore",)

logger: "Final[Logger]" = logging.getLogger("ccft-pymarkdown")


def _check_file(file_path: "Path") -> "Literal[True]":
    if len(file_path.suffixes) != 2:
        INVALID_FILE_SUFFIXES_COUNT_MESSAGE: Final[str] = (
            f"Invalid number of file suffixes: expected 2, got {len(file_path.suffixes)}."
        )
        raise ValueError(INVALID_FILE_SUFFIXES_COUNT_MESSAGE)

    if file_path.suffixes[0] != ".md" or file_path.suffixes[1] == ".original":
        INVALID_FILE_SUFFIXES_MESSAGE: Final[str] = (
            "File is not a previously converted markdown file."
        )
        raise ValueError(INVALID_FILE_SUFFIXES_MESSAGE)

    if not file_path.is_file():
        raise FileNotFoundError

    return True


def restore(files: "Iterable[Path]") -> None:
    """Return given Markdown files to their original state before cleaning."""
    file_path: Path
    for file_path in files:
        _check_file(file_path)

        restored_file_path: Path = file_path.parent / file_path.stem
        if restored_file_path.exists():
            logger.debug("Deleting cleaned file: '%s'", restored_file_path)
            restored_file_path.unlink()

        file_path.rename(file_path.parent / file_path.stem)
