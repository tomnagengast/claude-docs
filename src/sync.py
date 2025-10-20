"""
Utility for backing up the Claude documentation as Markdown files.

The script pulls the public sitemap, filters for English documentation URLs,
and then mirrors the directory structure locally while saving each page's
Markdown representation (available by appending `.md` to the URL).
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List
import xml.etree.ElementTree as ET

import requests
from tqdm import tqdm

SITEMAP_URL = "https://docs.claude.com/sitemap.xml"
DOC_PREFIX = "https://docs.claude.com/en/docs/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; claude-docs-backup/1.0)"}


def fetch_sitemap() -> str:
    resp = requests.get(SITEMAP_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


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


def download_markdown(paths: Iterable[str], output_dir: Path) -> List[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    failures: List[str] = []

    for path in tqdm(paths, desc="Downloading docs", unit="doc"):
        md_url = f"{DOC_PREFIX}{path}.md"
        try:
            resp = requests.get(md_url, headers=HEADERS, timeout=30)
            if resp.status_code == 404:
                failures.append(path)
                continue
            resp.raise_for_status()
        except requests.RequestException:
            failures.append(path)
            continue

        destination = output_dir.joinpath(*path.split("/")).with_suffix(".md")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(resp.content)

    return failures


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

    sitemap_xml = fetch_sitemap()
    doc_paths = extract_doc_paths(sitemap_xml)
    failures = download_markdown(doc_paths, args.output)

    print(f"Downloaded {len(doc_paths) - len(failures)} docs to {args.output.resolve()}")
    if failures:
        print("Failed to download the following paths:")
        for path in failures:
            print(f" - {path}")


if __name__ == "__main__":
    main()
