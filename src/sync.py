"""
Utility for backing up the Claude documentation as Markdown files.

The script pulls the public sitemap, filters for English documentation URLs,
and then mirrors the directory structure locally while saving each page's
Markdown representation (available by appending `.md` to the URL).
"""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import List
import xml.etree.ElementTree as ET

import aiohttp
from tqdm.asyncio import tqdm

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; claude-docs-backup/1.0)"}
MAX_CONCURRENT = 10  # Limit concurrent requests to avoid overwhelming the server
HIDDEN_PATHS = [
    "claude-code/claude_code_docs_map",
]


@dataclass(frozen=True)
class SiteConfig:
    name: str
    sitemap_url: str
    doc_prefixes: List[str]
    output_subdir: Path
    hidden_paths: List[str]


@dataclass(frozen=True)
class DocEntry:
    url: str
    path: str


SITES: List[SiteConfig] = [
    SiteConfig(
        name="docs.claude.com",
        sitemap_url="https://docs.claude.com/sitemap.xml",
        doc_prefixes=["https://docs.claude.com/en/docs/"],
        output_subdir=Path("."),
        hidden_paths=HIDDEN_PATHS,
    ),
    SiteConfig(
        name="code.claude.com",
        sitemap_url="https://code.claude.com/docs/sitemap.xml",
        # Support both potential URL shapes just in case:
        # - https://code.claude.com/docs/en/overview
        # - https://code.claude.com/en/overview
        doc_prefixes=[
            "https://code.claude.com/docs/en/",
            "https://code.claude.com/en/",
        ],
        output_subdir=Path("claude-code"),
        hidden_paths=[],
    ),
]


async def fetch_sitemap(
    session: aiohttp.ClientSession, sitemap_url: str
) -> str:
    async with session.get(sitemap_url, headers=HEADERS, timeout=30) as resp:
        resp.raise_for_status()
        return await resp.text()


def extract_doc_entries(sitemap_xml: str, doc_prefixes: List[str]) -> List[DocEntry]:
    root = ET.fromstring(sitemap_xml)
    # sitemap uses this namespace for urlset + url/loc entries
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    docs: List[DocEntry] = []
    for loc in root.findall(".//sm:loc", ns):
        url = (loc.text or "").strip()
        if not url:
            continue
        for prefix in doc_prefixes:
            if url.startswith(prefix):
                path = url[len(prefix) :].strip("/")
                if path:
                    docs.append(DocEntry(url=url.rstrip("/"), path=path))
                break
    docs.sort(key=lambda d: d.path)
    return docs


async def download_single_doc(
    session: aiohttp.ClientSession,
    doc: DocEntry,
    output_dir: Path,
    semaphore: asyncio.Semaphore,
) -> str | None:
    """Download a single document. Returns path on failure, None on success."""
    md_url = f"{doc.url}.md"

    async with semaphore:
        try:
            async with session.get(md_url, headers=HEADERS, timeout=30) as resp:
                if resp.status == 404:
                    return doc.path
                resp.raise_for_status()
                content = await resp.read()
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return doc.path

        destination = output_dir.joinpath(*doc.path.split("/")).with_suffix(".md")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)

    return None


async def download_markdown(docs: List[DocEntry], output_dir: Path) -> List[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    async with aiohttp.ClientSession() as session:
        tasks = [
            download_single_doc(session, doc, output_dir, semaphore)
            for doc in docs
        ]

        results = await tqdm.gather(*tasks, desc="Downloading docs", unit="doc")

    # Filter out None values (successful downloads) to get only failures
    failures = [r for r in results if r is not None]
    return failures


async def async_main(output_dir: Path) -> None:
    total_docs = 0
    total_failures = 0

    for site in SITES:
        print(f"Processing {site.name} sitemap...")
        async with aiohttp.ClientSession() as session:
            sitemap_xml = await fetch_sitemap(session, site.sitemap_url)

        docs = extract_doc_entries(sitemap_xml, site.doc_prefixes)

        if site.hidden_paths:
            default_prefix = site.doc_prefixes[0]
            for path in site.hidden_paths:
                docs.append(
                    DocEntry(
                        url=f"{default_prefix}{path}".rstrip("/"),
                        path=path,
                    )
                )

        # Deduplicate by path in case hidden paths overlap with sitemap entries
        unique_docs = {doc.path: doc for doc in docs}
        docs = sorted(unique_docs.values(), key=lambda d: d.path)

        site_output_dir = output_dir / site.output_subdir
        failures = await download_markdown(docs, site_output_dir)

        total_docs += len(docs)
        total_failures += len(failures)

        print(
            f"Downloaded {len(docs) - len(failures)} docs from {site.name} "
            f"to {site_output_dir.resolve()}"
        )
        if failures:
            print(f"Failed to download the following paths from {site.name}:")
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
