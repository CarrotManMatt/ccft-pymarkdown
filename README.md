# RCFT-PyMarkdown

[![RCFT-PyMarkdown Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FCarrotManMatt%2rcft-pymarkdown%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.version&label=RCFT-PyMarkdown)](https://github.com/CarrotManMatt/rcft-pymarkdown)

A Python wrapper around [jackdewinter's PyMarkdown linter](https://github.com/jackdewinter/pymarkdown) to remove custom-formatted tables in Markdown files.

When running [PyMarkdown](https://github.com/jackdewinter/pymarkdown) it may incorrectly flag errors inside a table that has correct formatting. Using this wrapper, the tables will temporarily be removed to prevent these incorrect errors.

> ⚠️ **Your tables with any Markdown files will not be linted**. This is because temporary files are created that do not include the tables, and these files are then linted.

## Usage

To perform linting and remove custom-formatted tables, replace `pymarkdown` with `rcft-pymarkdown` in any commands you wish to run.

```shell
rcft-pymarkdown {...}
```

* Replace `{...}` with the rest of the `pymarkdown` command you wish to run

For example:

```shell
rcft-pymarkdown scan .
```

### Manually Removing Custom-Formatted Tables

To manually remove any custom-formatted tables without running PyMarkdown, use the `--remove` flag:

```shell
rcft-pymarkdown --remove
```

### Manually Restoring Custom-Formatted Tables

To manually restore any custom-formatted tables without running PyMarkdown, use the `--restore` flag:

```shell
rcft-pymarkdown --restore
```
