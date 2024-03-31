from collections.abc import Sequence

__all__: Sequence[str] = ("run",)

import subprocess
import sys
from argparse import ArgumentParser, Namespace
from subprocess import CompletedProcess
from typing import TYPE_CHECKING, Final

from rcft_pymarkdown import (
    remove_custom_formatted_tables,
    restore_custom_formatted_tables,
    utils,
)
from rcft_pymarkdown.context_manager import RemoveCustomFormattedTables

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from argparse import _MutuallyExclusiveGroup as MutuallyExclusiveGroup


def _set_up_arg_parser() -> ArgumentParser:
    arg_parser: ArgumentParser = ArgumentParser(
        prog="rcft-pymarkdown",
        description="Lint Markdown files after removing custom-formatted tables.",
        usage="%(prog)s [--remove | --restore] ...",
        add_help=False,
    )

    remove_restore_args_group: "MutuallyExclusiveGroup" = arg_parser.add_argument_group(
        "Remove/Restore",
        "Manually remove or restore custom formatted tables from all Markdown files.",
    ).add_mutually_exclusive_group()
    remove_restore_args_group.add_argument(
        "--remove",
        action="store_true",
        help="Manually remove custom formatted tables from all Markdown files.",
    )
    remove_restore_args_group.add_argument(
        "--restore",
        action="store_true",
        help="Manually remove custom formatted tables from all Markdown files.",
    )

    return arg_parser


def run(argv: Sequence[str] | None = None) -> int:
    """Run RCFT-PyMarkdown."""
    arg_parser: ArgumentParser = _set_up_arg_parser()

    parsed_args: Namespace
    remaining_args: Sequence[str]
    parsed_args, remaining_args = arg_parser.parse_known_args(argv)

    if parsed_args.remove:
        if "-h" in remaining_args or "--help" in remaining_args:
            arg_parser.print_help()
            return 0

        if remaining_args:
            arg_parser.error(f"unrecognized arguments: {" ".join(remaining_args)}")
            raise SystemExit(2)

        remove_tables_file_exists_error: FileExistsError
        try:
            remove_custom_formatted_tables.remove_custom_formatted_tables_from_all_files()
        except FileExistsError as remove_tables_file_exists_error:
            MANUAL_REMOVE_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS: Final[bool] = (
                bool(remove_tables_file_exists_error.args)
                and "already exists" in remove_tables_file_exists_error.args[0]
            )
            if MANUAL_REMOVE_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS:
                MANUAL_REMOVE_REMOVE_TABLES_FILE_EXISTS_ERROR_MESSAGE: Final[str] = (
                    f"{remove_tables_file_exists_error.args[0]} "
                    f"Use `{arg_parser.prog} --restore` to first restore the files "
                    "to their original state."
                )
                raise type(remove_tables_file_exists_error)(
                    MANUAL_REMOVE_REMOVE_TABLES_FILE_EXISTS_ERROR_MESSAGE  # noqa: COM812
                ) from remove_tables_file_exists_error

            raise remove_tables_file_exists_error from remove_tables_file_exists_error

        return 0

    if parsed_args.restore:
        if "-h" in remaining_args or "--help" in remaining_args:
            arg_parser.print_help()
            return 0

        if remaining_args:
            arg_parser.error(f"Unrecognized arguments: {" ".join(remaining_args)}")
            raise SystemExit(2)

        restore_custom_formatted_tables.restore_custom_formatted_tables_from_all_files()
        return 0

    try:
        with RemoveCustomFormattedTables():
            parser_output: CompletedProcess[bytes] = subprocess.run(
                [sys.executable, "-m", "pymarkdown", *remaining_args],
                cwd=utils.PROJECT_ROOT,
                capture_output=True,
                check=False,
            )

    except FileExistsError as remove_tables_file_exists_error:
        WITH_PYMARKDOWN_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS: Final[bool] = (
            bool(remove_tables_file_exists_error.args)
            and "already exists" in remove_tables_file_exists_error.args[0]
        )
        if WITH_PYMARKDOWN_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS:
            WITH_PYMARKDOWN_REMOVE_TABLES_FILE_EXISTS_ERROR_MESSAGE: Final[str] = (
                f"{remove_tables_file_exists_error.args[0]} "
                f"Use `{arg_parser.prog} --restore` to first restore the files "
                "to their original state."
            )
            raise type(remove_tables_file_exists_error)(
                WITH_PYMARKDOWN_REMOVE_TABLES_FILE_EXISTS_ERROR_MESSAGE  # noqa: COM812
            ) from remove_tables_file_exists_error

        raise remove_tables_file_exists_error from remove_tables_file_exists_error

    sys.stdout.write(
        parser_output.stdout.decode("utf-8").replace(
            "__main__.py",
            arg_parser.prog,
        )  # noqa: COM812
    )
    sys.stderr.write(
        parser_output.stderr.decode("utf-8").replace(
            "__main__.py",
            arg_parser.prog,
        )  # noqa: COM812
    )

    return parser_output.returncode
