"""Logging setup for use in combination with the click framework."""

import logging
from typing import TYPE_CHECKING, override

import click

if TYPE_CHECKING:
    from collections.abc import Sequence
    from logging import Logger
    from typing import Final

__all__: "Sequence[str]" = ("setup_logging",)


logger: "Final[Logger]" = logging.getLogger("ccft-pymarkdown")


class ColorFormatter(logging.Formatter):
    @override
    def format(self, record: logging.LogRecord) -> str:
        if not record.exc_info:
            PREFIX: Final[str] = click.style(
                f"{record.levelname.upper()}: ",
                fg=(
                    "red"
                    if record.levelno >= logging.ERROR
                    else "yellow"
                    if record.levelno >= logging.WARNING
                    else "blue"
                ),
            )
            return "\n".join(f"{PREFIX}{line}" for line in super().format(record).splitlines())

        return super().format(record)


class ClickHandler(logging.Handler):
    @override
    def emit(self, record: logging.LogRecord) -> None:
        try:
            click.echo(self.format(record), err=record.levelno >= logging.WARNING)
        except Exception:  # noqa: BLE001
            self.handleError(record)
            return


def setup_logging(_ctx: click.Context, _param: click.Parameter, value: object) -> None:
    """"""
    if not isinstance(value, int):
        raise TypeError(f"Expected int, got {type(value)} for 'verbose' value.")

    logger.setLevel(logging.DEBUG if value > 0 else logging.INFO)
    logger.propagate = False
    click_handler: logging.Handler = ClickHandler()
    click_handler.formatter = ColorFormatter()
    logger.handlers = [click_handler]
