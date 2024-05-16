"""Perform the removal of custom-formatted tables from Markdown files."""

from collections.abc import Sequence

__all__: Sequence[str] = (
    "remove_custom_formatted_tables_from_all_files",
    "remove_custom_formatted_tables_from_file",
)


import shutil
from pathlib import Path
from typing import TextIO

from git import PathLike, Repo

from rcft_pymarkdown import utils


def remove_custom_formatted_tables_from_file(original_file_path: Path) -> None:
    """Remove custom-formatted tables from given path to a Markdown file."""
    temp_file_path: Path = shutil.copy2(
        original_file_path,
        original_file_path.parent / f"{original_file_path.name}.original",
    )
    new_file_path = original_file_path
    original_file_path = temp_file_path
    del temp_file_path

    original_file: TextIO
    new_file: TextIO
    with original_file_path.open("r") as original_file, new_file_path.open("w") as new_file:
        line: str
        for line in original_file:
            new_file.write(
                line.replace(
                    "<br>* ",
                    "<br> ",
                ).replace(
                    "<br/>* ",
                    "<br/> ",
                ).replace(
                    "| * ",
                    "| ",
                ),
            )


def remove_custom_formatted_tables_from_all_files() -> None:
    """Remove all custom-formatted tables within every Markdown file in this repository."""
    file_entry: tuple[str | PathLike, object]
    for file_entry in Repo(utils.PROJECT_ROOT).index.entries:
        file_path: Path = utils.PROJECT_ROOT / file_entry[0]

        if file_path.suffix != ".md":
            continue

        if not file_path.is_file() or not file_path.exists():
            continue

        original_file_path: Path = file_path.parent / f"{file_path.name}.original"
        if original_file_path.exists():
            ORIGINAL_FILE_ALREADY_EXISTS_MESSAGE: str = (
                "Cannot remove custom-formatted tables from Markdown files: "
                f"{original_file_path} already exists."
            )
            raise FileExistsError(ORIGINAL_FILE_ALREADY_EXISTS_MESSAGE)

        remove_custom_formatted_tables_from_file(file_path)
