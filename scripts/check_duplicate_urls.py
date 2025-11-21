#!/usr/bin/env python3
"""Scan the sitemap for duplicate URLs.

This script reads a sitemap XML file (default: sitemap.xml at the repo root),
collects every <loc> entry, and reports any duplicates that could create SEO
or crawling issues. The script exits with a non-zero status code when
duplicates are found so it can be used as a CI check.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


def parse_sitemap(path: Path) -> list[str]:
    """Return every URL found in the <loc> nodes of the sitemap."""
    tree = ET.parse(path)
    root = tree.getroot()

    namespace = ""
    if root.tag.startswith("{"):
        namespace = root.tag.split("}")[0].strip("{")

    loc_tag = "loc" if not namespace else f"{{{namespace}}}loc"
    urls: list[str] = []

    for loc in root.iter(loc_tag):
        url = (loc.text or "").strip()
        if url:
            urls.append(url)

    return urls


def find_duplicates(urls: list[str]) -> dict[str, int]:
    """Return a mapping of URLs to their count when they appear more than once."""
    counts = Counter(urls)
    return {url: count for url, count in counts.items() if count > 1}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check sitemap for duplicate URLs")
    parser.add_argument(
        "sitemap",
        type=Path,
        nargs="?",
        default=Path("sitemap.xml"),
        help="Path to the sitemap file (default: sitemap.xml)",
    )
    args = parser.parse_args()

    if not args.sitemap.exists():
        print(f"Error: {args.sitemap} does not exist", file=sys.stderr)
        return 2

    urls = parse_sitemap(args.sitemap)
    duplicates = find_duplicates(urls)

    if not duplicates:
        print("No duplicate URLs detected.")
        return 0

    print("Duplicate URLs found:")
    for url, count in sorted(duplicates.items()):
        print(f"- {url} (appears {count} times)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
