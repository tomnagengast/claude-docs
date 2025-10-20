# Claude Docs Sync

Scripted mirror of the public Claude documentation that saves each page as Markdown.

## Prerequisites

- [uv](https://github.com/astral-sh/uv)

## Install

```bash
uv sync
```

## Usage

Download the docs into the default `docs/` directory:

```bash
uv run claude-docs
```

Or call the module directly and choose a custom destination:

```bash
uv run python src/sync.py --output /path/to/export
```

Re-run either command whenever you want to refresh the local copy; existing files are safely overwritten.
