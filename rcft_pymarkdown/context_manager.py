from collections.abc import Sequence

__all__: Sequence[str] = ("RemoveCustomFormattedTables",)

from types import TracebackType

from rcft_pymarkdown import (
    remove_custom_formatted_tables,
    restore_custom_formatted_tables,
)


class RemoveCustomFormattedTables:
    def __enter__(self) -> None:
        remove_custom_formatted_tables.remove_custom_formatted_tables_from_all_files()

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:  # noqa: E501
        restore_custom_formatted_tables.restore_custom_formatted_tables_from_all_files()
