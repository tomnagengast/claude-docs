# Claude Docs Sync

Mirror the public Claude product and Claude Code docs as Markdown.
The script walks each sitemap, fetches the `.md` representation of every page, and rebuilds the same folder structure locally.

## Sources

- https://docs.claude.com/en/docs/
- https://code.claude.com/docs/

## Setup

- Install dependencies with [uv](https://github.com/astral-sh/uv): `uv sync`

## Refresh the docs

- Default run (writes to `docs/`, with Claude Code docs nested under `docs/claude-code/`):

  ```bash
  uv run claude-docs
  ```

- Custom target folder:

  ```bash
  uv run python src/sync.py --output /path/to/export
  ```

Each run overwrites the existing Markdown files so re-running the command is the only maintenance needed.
