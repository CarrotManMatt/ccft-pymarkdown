"""Console entry point for CCFT-PyMarkdown."""

import sys
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

    from pymarkdown.api import (
        PyMarkdownApi,
        PyMarkdownPragmaError,
        PyMarkdownScanFailure,
        PyMarkdownScanPathResult,
    )


__all__: "Sequence[str]" = ("Scanner",)


class Scanner:
    @override
    def __init__(self, pymarkdown_api: "PyMarkdownApi") -> None:
        self.pymarkdown_api: PyMarkdownApi = pymarkdown_api
        self._scan_failures: list[PyMarkdownScanFailure] = []
        self._pragma_errors: list[PyMarkdownPragmaError] = []

    @property
    def encountered_failures(self) -> bool:
        return bool(self._scan_failures) or bool(self._pragma_errors)

    def log_errors(self) -> None:
        pragma_error: PyMarkdownPragmaError
        for pragma_error in self._pragma_errors:
            sys.stdout.write(
                f"{pragma_error.file_path}:"
                f"{pragma_error.line_number}: "
                "INLINE: "
                f"{pragma_error.pragma_error}\n"
            )

        scan_failure: PyMarkdownScanFailure
        for scan_failure in self._scan_failures:
            sys.stdout.write(
                f"{scan_failure.scan_file}:"
                f"{scan_failure.line_number}:"
                f"{scan_failure.column_number}: "
                f"{scan_failure.rule_id}: "
                f"{scan_failure.rule_description} "
                f"({scan_failure.rule_name})\n"
            )

    def scan_file_path(self, file_path: "Path") -> None:
        scan_result: PyMarkdownScanPathResult = self.pymarkdown_api.scan_path(str(file_path))
        self._pragma_errors.extend(scan_result.pragma_errors)
        self._scan_failures.extend(scan_result.scan_failures)
