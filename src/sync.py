"""
Utility for backing up the Claude documentation as Markdown files.

The script pulls the public sitemap, filters for English documentation URLs,
and then mirrors the directory structure locally while saving each page's
Markdown representation (available by appending `.md` to the URL).
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from typing import List
import xml.etree.ElementTree as ET

import aiohttp
from tqdm.asyncio import tqdm

SITEMAP_URL = "https://docs.claude.com/sitemap.xml"
DOC_PREFIX = "https://docs.claude.com/en/docs/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; claude-docs-backup/1.0)"}
MAX_CONCURRENT = 10  # Limit concurrent requests to avoid overwhelming the server
HIDDEN_PATHS = [
    "claude-code/claude_code_docs_map",
]


async def fetch_sitemap(session: aiohttp.ClientSession) -> str:
    async with session.get(SITEMAP_URL, headers=HEADERS, timeout=30) as resp:
        resp.raise_for_status()
        return await resp.text()


def extract_doc_paths(sitemap_xml: str) -> List[str]:
    root = ET.fromstring(sitemap_xml)
    # sitemap uses this namespace for urlset + url/loc entries
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    paths: List[str] = []
    for loc in root.findall(".//sm:loc", ns):
        url = loc.text or ""
        if not url.startswith(DOC_PREFIX):
            continue
        path = url[len(DOC_PREFIX) :].strip("/")
        if path:
            paths.append(path)
    paths.sort()
    return paths


async def download_single_doc(
    session: aiohttp.ClientSession,
    path: str,
    output_dir: Path,
    semaphore: asyncio.Semaphore,
) -> str | None:
    """Download a single document. Returns path on failure, None on success."""
    md_url = f"{DOC_PREFIX}{path}.md"

    async with semaphore:
        try:
            async with session.get(md_url, headers=HEADERS, timeout=30) as resp:
                if resp.status == 404:
                    return path
                resp.raise_for_status()
                content = await resp.read()
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return path

        destination = output_dir.joinpath(*path.split("/")).with_suffix(".md")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)

    return None


async def download_markdown(paths: List[str], output_dir: Path) -> List[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    async with aiohttp.ClientSession() as session:
        tasks = [
            download_single_doc(session, path, output_dir, semaphore)
            for path in paths
        ]

        results = await tqdm.gather(*tasks, desc="Downloading docs", unit="doc")

    # Filter out None values (successful downloads) to get only failures
    failures = [r for r in results if r is not None]
    return failures


async def async_main(output_dir: Path) -> None:
    async with aiohttp.ClientSession() as session:
        sitemap_xml = await fetch_sitemap(session)

    doc_paths = extract_doc_paths(sitemap_xml)
    all_paths = sorted(set(doc_paths + HIDDEN_PATHS))
    failures = await download_markdown(all_paths, output_dir)

    print(f"Downloaded {len(all_paths) - len(failures)} docs to {output_dir.resolve()}")
    if failures:
        print("Failed to download the following paths:")
        for path in failures:
            print(f" - {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backup Claude docs by fetching Markdown representations."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs"),
        help="Directory to store the downloaded Markdown files (default: docs)",
    )
    args = parser.parse_args()

    asyncio.run(async_main(args.output))


if __name__ == "__main__":
    main()
