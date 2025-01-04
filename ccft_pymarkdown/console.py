"""Console entry point for CCFT-PyMarkdown."""

import importlib.metadata
import logging
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import click

from . import utils
from .clean import clean
from .context_manager import CleanCustomFormattedTables
from .restore import restore

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence
    from logging import Logger
    from subprocess import CompletedProcess
    from typing import Final

__all__: "Sequence[str]" = ("run",)

logger: "Final[Logger]" = logging.getLogger("ccft-pymarkdown")


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    help=f"{
        (
            importlib.metadata.metadata("CCFT-PyMarkdown").get("Summary") or "CCFT-PyMarkdown"
        ).strip(".")
    }.",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    callback=utils.setup_logging,
    expose_value=False,
)
def run() -> None:
    """Run cli entry-point."""


@run.command(name="clean", help="Clean custom-formatted tables from all Markdown files.")
@click.argument(
    "files",
    nargs=-1,
    type=click.Path(exists=True, file_okay=True, dir_okay=True, path_type=Path),
)
@click.option(
    "--with-git/--no-git",
    default=True,
)
def _clean(files: "Iterable[Path] | None", *, with_git: bool) -> None:
    clean_tables_file_exists_error: FileExistsError
    try:
        cleaned_files_count: int = clean(
            files if files is not None else utils.get_markdown_files(with_git=with_git),
            with_git=with_git,
        )

    except FileExistsError as clean_tables_file_exists_error:
        if "already exists" in str(clean_tables_file_exists_error):
            logger.error(str(clean_tables_file_exists_error).strip("\n\r\t -."))  # noqa: TRY400
            logger.info(
                "Use `%s restore` to first restore the files to their original state."  # TODO: Get prog
            )
            return

        raise clean_tables_file_exists_error from clean_tables_file_exists_error

    if cleaned_files_count == 0:
        click.echo("No files required cleaning.")
    else:
        logger.info("Successfully cleaned %d files.", cleaned_files_count)


@run.command(name="restore", help="Restore custom-formatted tables from all Markdown files.")
def _restore() -> None:
    restore(utils.get_original_files())


@run.command(
    name="scan-all", help="Lint all Markdown files after removing custom-formatted tables."
)
def _scan_all(arg_parser: "ArgumentParser") -> None:
    clean_tables_file_exists_error: FileExistsError
    try:
        with CleanCustomFormattedTables():
            parser_output: CompletedProcess[bytes] = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pymarkdown",
                    "--return-code-scheme",
                    "minimal",
                    "scan",
                    utils.PROJECT_ROOT.resolve(),
                ],
                check=True,
            )

    except FileExistsError as clean_tables_file_exists_error:
        WITH_PYMARKDOWN_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS: Final[bool] = (
            bool(clean_tables_file_exists_error.args)
            and "already exists" in clean_tables_file_exists_error.args[0]
        )
        if WITH_PYMARKDOWN_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS:
            WITH_PYMARKDOWN_CLEAN_TABLES_FILE_EXISTS_ERROR_MESSAGE: Final[str] = (
                f"{clean_tables_file_exists_error.args[0]} "
                f"Use `{arg_parser.prog} restore` to first restore the files "
                "to their original state."
            )
            raise type(clean_tables_file_exists_error)(
                WITH_PYMARKDOWN_CLEAN_TABLES_FILE_EXISTS_ERROR_MESSAGE
            ) from clean_tables_file_exists_error

        raise clean_tables_file_exists_error from clean_tables_file_exists_error

    return parser_output.returncode
