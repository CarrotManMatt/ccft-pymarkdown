"""Perform the cleaning of custom-formatted tables from Markdown files."""

import logging
import shutil
from typing import TYPE_CHECKING

from ccft_pymarkdown import utils

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence
    from logging import Logger
    from pathlib import Path
    from typing import Final, Literal, TextIO


__all__: "Sequence[str]" = ("clean",)

logger: "Final[Logger]" = logging.getLogger("ccft-pymarkdown")


if TYPE_CHECKING:

    class CopiedPath(Path): ...


def _copy_file(original_file_path: "Path") -> tuple["CopiedPath", "Path"]:
    copied_path: CopiedPath = shutil.copy2(
        original_file_path,
        original_file_path.parent / f"{original_file_path.name}.original",
    )
    return copied_path, original_file_path


def _clean_single_file(original_file_path: "Path") -> None:
    """Clean custom-formatted tables within a Markdown file at a given path."""
    new_file_path: CopiedPath
    new_file_path, original_file_path = _copy_file(original_file_path)

    original_file: TextIO
    new_file: TextIO
    with original_file_path.open("r") as original_file, new_file_path.open("w") as new_file:
        line: str
        for line in original_file:
            new_file.write(
                line.replace(
                    "<br>* ",
                    "<br> ",
                )
                .replace(
                    "<br/>* ",
                    "<br/> ",
                )
                .replace(
                    "| * ",
                    "| ",
                ),
            )


def _check_file(file_path: "Path") -> "Literal[True]":
    logger.debug("Checking file '%s'", file_path)
    if file_path.suffix != ".md":
        INVALID_FILE_SUFFIX_MESSAGE: Final[str] = "File is not a markdown file."
        raise ValueError(INVALID_FILE_SUFFIX_MESSAGE)

    if not file_path.is_file():
        raise FileNotFoundError

    original_file_path: Path = file_path.parent / f"{file_path.name}.original"
    if original_file_path.exists():
        ORIGINAL_FILE_ALREADY_EXISTS_MESSAGE: str = (
            "Cannot clean custom-formatted tables from Markdown files: "
            f"{original_file_path} already exists."
        )
        raise FileExistsError(ORIGINAL_FILE_ALREADY_EXISTS_MESSAGE)

    return True


def clean(files: "Iterable[Path]", *, skip_errors: bool = False, with_git: bool = True) -> int:
    """Clean custom-formatted tables within each given Markdown file."""
    cleaned_files_count: int = 0

    file_path: Path
    for file_path in files:
        if file_path.is_dir():  # TODO: Ignore non explicit hidden files & directories
            cleaned_files_count += clean(
                utils.get_markdown_files(file_path, with_git=with_git),
                skip_errors=skip_errors,
                with_git=True,
            )
            continue

        e: Exception
        try:
            _check_file(file_path)
        except (FileNotFoundError, FileExistsError, OSError) as e:
            if not skip_errors:
                raise e from e

            logger.error(  # noqa: TRY400
                "Skipping '%s': %s", file_path, utils.format_exception_to_log_message(e)
            )
            continue

        logger.debug("File '%s' passed pre-cleaning checks", file_path)

        try:
            _clean_single_file(file_path)
        except (OSError, ValueError, RuntimeError, TypeError) as e:
            logger.error(  # noqa: TRY400
                "Error while cleaning '%s': %s",
                file_path,
                utils.format_exception_to_log_message(e),
            )
            continue

        cleaned_files_count += 1

    return cleaned_files_count
