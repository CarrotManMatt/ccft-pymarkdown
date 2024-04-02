# RCFT-PyMarkdown

[![RCFT-PyMarkdown Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FCarrotManMatt%2Frcft-pymarkdown%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.version&label=RCFT-PyMarkdown)](https://github.com/CarrotManMatt/rcft-pymarkdown)
[![Python Version](https://img.shields.io/badge/Python-3.12-blue?&logo=Python&logoColor=white)](https://python.org/downloads/release/python-3122)
[![PyMarkdown Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FCarrotManMatt%2Frcft-pymarkdown%2Fmain%2Fpoetry.lock&query=%24.package%5B%3F%28%40.name%3D%3D%27pymarkdownlnt%27%29%5D.version&logo=Markdown&label=PyMarkdown)](https://github.com/jackdewinter/pymarkdown)
[![Tests Status](https://github.com/CarrotManMatt/rcft-pymarkdown/actions/workflows/tests.yaml/badge.svg)](https://github.com/CarrotManMatt/rcft-pymarkdown/actions/workflows/tests.yaml)
[![Mypy Status](https://img.shields.io/badge/mypy-checked-%232EBB4E&label=mypy)](https://mypy-lang.org)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://ruff.rs)
[![pre-commit.ci Status](https://results.pre-commit.ci/badge/github/CarrotManMatt/rcft-pymarkdown/main.svg)](https://results.pre-commit.ci/latest/github/CarrotManMatt/rcft-pymarkdown/main)
[![PyMarkdown Status](https://img.shields.io/badge/validated-brightgreen?logo=markdown&label=PyMarkdown)](https://github.com/jackdewinter/pymarkdown)

A Python wrapper around [jackdewinter's PyMarkdown linter](https://github.com/jackdewinter/pymarkdown) to remove custom-formatted tables in Markdown files.

When running [PyMarkdown](https://github.com/jackdewinter/pymarkdown) it may incorrectly flag errors inside a table that has correct formatting. Using this wrapper, the tables will temporarily be removed to prevent these incorrect errors.

> ⚠️ **Your tables with any Markdown files will not be linted**. This is because temporary files are created that do not include the tables, and these files are then linted.

## Usage

### Scanning All Files After Removing Custom-Formatted Tables

To perform linting using PyMarkdown, after removing custom-formatted tables, use the `scan-all` action:

```shell
rcft-pymarkdown scan-all
```

### Manually Removing Custom-Formatted Tables

To manually remove any custom-formatted tables without running PyMarkdown, use the `remove` action:

```shell
rcft-pymarkdown remove
```

### Manually Restoring Custom-Formatted Tables

To manually restore any custom-formatted tables without running PyMarkdown, use the `restore` action:

```shell
rcft-pymarkdown restore
```
