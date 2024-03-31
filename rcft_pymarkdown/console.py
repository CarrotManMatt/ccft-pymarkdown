"""
Console script wrapper for Minecraft Mod Downloader.

This script performs argument parsing & sends a return code back to the console.
"""

from collections.abc import Sequence

__all__: Sequence[str] = ("run",)

from argparse import ArgumentParser


def set_up_arg_parser() -> ArgumentParser:
    raise NotImplementedError


def run(argv: Sequence[str] | None = None) -> int:
    """Run the Minecraft Mod Downloader tool as a CLI tool with argument parsing."""
    arg_parser: ArgumentParser = set_up_arg_parser()

    arg_parser.parse_args(argv)

    raise NotImplementedError
