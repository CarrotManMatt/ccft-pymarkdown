from collections.abc import Sequence

__all__: Sequence[str] = ("get_project_root",)

from pathlib import Path
from typing import Final

from git import InvalidGitRepositoryError, PathLike, Repo


def get_project_root() -> Path:
    try:
        raw_project_root: PathLike | str | None = Repo(
            Path.cwd(),
            search_parent_directories=True
        ).working_tree_dir
    except InvalidGitRepositoryError:
        raw_project_root = None

    if raw_project_root is None:
        return _get_readme_root()

    return Path(raw_project_root)


def _get_readme_root() -> Path:
    project_root: Path = Path.cwd().resolve()

    for _ in range(8):
        project_root = project_root.parent

        if any(path.stem == "README" for path in project_root.iterdir()):
            return project_root

    else:
        # noinspection PyFinal
        NO_ROOT_DIRECTORY_MESSAGE: Final[str] = "Could not locate project root directory."
        raise FileNotFoundError(NO_ROOT_DIRECTORY_MESSAGE)
