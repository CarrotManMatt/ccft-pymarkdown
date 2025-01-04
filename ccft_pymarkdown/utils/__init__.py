"""Common utils made available for use throughout this project."""

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Final

from .click_logging import setup_logging

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence
    from logging import Logger
    from typing import Final

    from git import PathLike

__all__: "Sequence[str]" = (
    "PROJECT_ROOT",
    "format_exception_to_log_message",
    "get_all_markdown_files",
    "get_all_original_files",
    "setup_logging",
)


logger: "Final[Logger]" = logging.getLogger("ccft-pymarkdown")


def _get_project_root() -> "Path":
    try:
        from git import InvalidGitRepositoryError, Repo
    except ImportError:
        logger.warning("GitPython is not installed, falling back to naive file exploration")
        return _get_readme_root()

    try:
        raw_project_root: PathLike | str | None = Repo(
            Path.cwd(),
            search_parent_directories=True,
        ).working_tree_dir
    except InvalidGitRepositoryError:
        raw_project_root = None

    if raw_project_root is None:
        return _get_readme_root()

    return Path(raw_project_root)


def _get_readme_root() -> "Path":
    project_root: Path = Path.cwd().resolve()

    for _ in range(8):
        project_root = project_root.parent

        if any(path.stem == "README" for path in project_root.iterdir()):
            return project_root

    # noinspection PyFinal
    NO_ROOT_DIRECTORY_MESSAGE: Final[str] = "Could not locate project root directory."
    raise FileNotFoundError(NO_ROOT_DIRECTORY_MESSAGE)


PROJECT_ROOT: "Final[Path]" = _get_project_root()


def _naive_get_markdown_files(root: "Path") -> "Iterable[Path]":
    return (
        file_path for file_path in root.rglob("*.md") if not file_path.name.startswith(".")
    )


def get_markdown_files(
    root: "Path" = PROJECT_ROOT, *, with_git: bool = True
) -> "Iterable[Path]":
    """"""
    if not root.is_dir():
        raise NotADirectoryError(root)

    if not with_git:
        return _naive_get_markdown_files(root)

    try:
        from git import InvalidGitRepositoryError, Repo
    except ImportError:
        logger.warning("GitPython is not installed, falling back to naive file exploration")
        return _naive_get_markdown_files(root)

    try:
        repo_root: Repo = Repo(root)
    except InvalidGitRepositoryError:
        return _naive_get_markdown_files(root)

    return (
        file_path
        for file_entry in repo_root.index.entries
        if (file_path := root / file_entry[0]).suffix == ".md"
    )


def get_original_files(root: "Path" = PROJECT_ROOT) -> "Iterable[Path]":
    """"""
    if not root.is_dir():
        raise NotADirectoryError(root)

    return root.rglob("*.md.original")


def format_exception_to_log_message(exception: Exception) -> str:
    """"""
    message: str = str(exception).strip("\n\r\t -.")

    if message:
        return message

    if isinstance(exception, FileNotFoundError):
        return "File does not exist"

    if isinstance(exception, FileExistsError):
        return "File already exists"

    NO_EXCEPTION_MESSAGE: Final[str] = "Exception did not contain a loggable message."
    raise ValueError(NO_EXCEPTION_MESSAGE)
