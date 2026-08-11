#!/usr/bin/env python3
"""Validate WorkProofCam's public HTML, entity metadata, links, and sitemaps."""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


SITE_ORIGIN = "https://ly-helloworld.github.io"
SITE_PREFIX = "/Privacy/"
APP_STORE_ID = "6775852372"
APP_STORE_URL = "https://apps.apple.com/us/app/workproofcam-photo-report/id6775852372"

PAGE_SPECS = {
    "workproofcam-web/index.html": "https://ly-helloworld.github.io/Privacy/workproofcam-web/",
    "workproofcam-web/job-site-photo-report-app/index.html": "https://ly-helloworld.github.io/Privacy/workproofcam-web/job-site-photo-report-app/",
    "workproofcam-web/before-after-work-proof/index.html": "https://ly-helloworld.github.io/Privacy/workproofcam-web/before-after-work-proof/",
    "workproofcam-web/photo-report-without-cloud/index.html": "https://ly-helloworld.github.io/Privacy/workproofcam-web/photo-report-without-cloud/",
    "workproofcam-web/sample-photo-report/index.html": "https://ly-helloworld.github.io/Privacy/workproofcam-web/sample-photo-report/",
    "workproofcam/support.html": "https://ly-helloworld.github.io/Privacy/workproofcam/support.html",
}
REQUIRED_PAGES = tuple(PAGE_SPECS)
SITEMAPS = ("core-sitemap.xml", "sitemap.xml")


class PageParser(HTMLParser):
    """Collect only the document signals the static-site contract depends on."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1_count = 0
        self.canonicals: list[str] = []
        self.json_ld_blocks: list[str] = []
        self.targets: list[str] = []
        self.meta_keys: set[str] = set()
        self._inside_json_ld = False
        self._json_ld_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value for name, value in attrs if value is not None}
        if tag == "h1":
            self.h1_count += 1
        if tag == "link":
            href = values.get("href")
            rel_values = set(values.get("rel", "").split())
            if href and "canonical" in rel_values:
                self.canonicals.append(href)
            if href:
                self.targets.append(href)
        if tag in {"a", "img", "script"}:
            attribute = "href" if tag == "a" else "src"
            target = values.get(attribute)
            if target:
                self.targets.append(target)
        if tag == "meta":
            key = values.get("name") or values.get("property")
            if key:
                self.meta_keys.add(key)
        if tag == "script" and values.get("type") == "application/ld+json":
            self._inside_json_ld = True
            self._json_ld_parts = []

    def handle_data(self, data: str) -> None:
        # JSON-LD can arrive in multiple parser chunks, so preserve all parts until the script closes.
        if self._inside_json_ld:
            self._json_ld_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._inside_json_ld:
            self.json_ld_blocks.append("".join(self._json_ld_parts).strip())
            self._inside_json_ld = False
            self._json_ld_parts = []


def parse_page(path: Path) -> tuple[PageParser, str]:
    html = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(html)
    parser.close()
    return parser, html


def validate_required_pages(root: Path) -> list[str]:
    return [
        f"Missing required page: {relative}"
        for relative in REQUIRED_PAGES
        if not (root / relative).is_file()
    ]


def validate_html_pages(root: Path) -> list[str]:
    errors: list[str] = []
    required_meta = {"description", "robots", "og:title", "og:description", "og:url", "twitter:title", "twitter:description"}

    for relative, expected_canonical in PAGE_SPECS.items():
        path = root / relative
        if not path.is_file():
            continue
        try:
            parser, html = parse_page(path)
        except (OSError, UnicodeError) as error:
            errors.append(f"Unable to read {relative}: {error}")
            continue

        if parser.h1_count != 1:
            errors.append(f"{relative} must contain exactly one h1; found {parser.h1_count}")
        if parser.canonicals != [expected_canonical]:
            errors.append(f"{relative} canonical mismatch: {parser.canonicals!r}")
        if APP_STORE_ID not in html:
            errors.append(f"{relative} does not identify App Store ID {APP_STORE_ID}")
        if not parser.json_ld_blocks:
            errors.append(f"{relative} has no JSON-LD entity data")
        for index, block in enumerate(parser.json_ld_blocks, start=1):
            try:
                json.loads(block)
            except json.JSONDecodeError as error:
                errors.append(f"{relative} JSON-LD block {index} is invalid: {error}")
        missing_meta = sorted(required_meta - parser.meta_keys)
        if missing_meta:
            errors.append(f"{relative} is missing metadata: {', '.join(missing_meta)}")
        if relative == "workproofcam/support.html" and "luoyi9932@gmail.com" not in html:
            errors.append(f"{relative} is missing the verified support email")
        if APP_STORE_URL not in html:
            errors.append(f"{relative} is missing the exact App Store URL")

    return errors


def sitemap_locations(path: Path) -> tuple[list[str], str | None]:
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as error:
        return [], str(error)
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    return [node.text or "" for node in root.findall(f"{namespace}url/{namespace}loc")], None


def validate_sitemaps(root: Path) -> list[str]:
    errors: list[str] = []
    required_urls = set(PAGE_SPECS.values())

    for relative in SITEMAPS:
        locations, parse_error = sitemap_locations(root / relative)
        if parse_error:
            errors.append(f"Unable to parse {relative}: {parse_error}")
            continue
        duplicates = sorted(url for url, count in Counter(locations).items() if count > 1)
        if duplicates:
            errors.append(f"{relative} contains duplicate URLs: {', '.join(duplicates)}")
        missing = sorted(required_urls - set(locations))
        if missing:
            errors.append(f"{relative} is missing URLs: {', '.join(missing)}")

    return errors


def validate_publisher_identity(root: Path) -> list[str]:
    """Require one readable overseas name while preserving Apple's exact seller label."""
    relative = "workproofcam-web/index.html"
    path = root / relative
    if not path.is_file():
        return [f"Missing publisher identity page: {relative}"]

    parser, html = parse_page(path)
    errors: list[str] = []
    visible_identity = "Published on the App Store by Xuemei Huang (listed on the App Store as 雪梅 黄)"
    if visible_identity not in html:
        errors.append(f"{relative} must display Xuemei Huang with the App Store alias 雪梅 黄")

    publisher_matches = []
    for block in parser.json_ld_blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and isinstance(data.get("publisher"), dict):
            publisher_matches.append(data["publisher"])

    # Entity matching depends on retaining both the overseas display name and Apple's exact public label.
    if not any(
        publisher.get("name") == "Xuemei Huang" and publisher.get("alternateName") == "雪梅 黄"
        for publisher in publisher_matches
    ):
        errors.append(f"{relative} JSON-LD publisher must name Xuemei Huang with alternateName 雪梅 黄")
    return errors


def local_target(root: Path, source: Path, target: str) -> Path | None:
    parsed = urlparse(target)
    if parsed.scheme in {"mailto", "tel", "javascript", "data"}:
        return None
    if parsed.scheme in {"http", "https"}:
        if f"{parsed.scheme}://{parsed.netloc}" != SITE_ORIGIN or not parsed.path.startswith(SITE_PREFIX):
            return None
        relative = unquote(parsed.path[len(SITE_PREFIX) :])
        candidate = root / relative
    elif parsed.netloc:
        return None
    else:
        relative = unquote(parsed.path)
        if not relative:
            return None
        candidate = source.parent / relative

    # GitHub Pages serves a directory URL from its index.html file.
    if parsed.path.endswith("/") or candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate.resolve()


def validate_internal_targets(root: Path) -> list[str]:
    errors: list[str] = []
    resolved_root = root.resolve()

    for relative in REQUIRED_PAGES:
        source = root / relative
        if not source.is_file():
            continue
        parser, _ = parse_page(source)
        for target in parser.targets:
            candidate = local_target(resolved_root, source, target)
            if candidate is None:
                continue
            try:
                candidate.relative_to(resolved_root)
            except ValueError:
                errors.append(f"{relative} points outside the repository: {target}")
                continue
            if not candidate.is_file():
                errors.append(f"{relative} has missing local target: {target}")

    return errors


def validate_site(root: Path) -> list[str]:
    errors: list[str] = []
    for validator_function in (
        validate_required_pages,
        validate_html_pages,
        validate_sitemaps,
        validate_publisher_identity,
        validate_internal_targets,
    ):
        errors.extend(validator_function(root))
    return errors


# CLI entry: return a non-zero status with every actionable error so Pages changes can be gated before push.
def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the WorkProofCam static-site contract.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root; defaults to the current directory.")
    errors = validate_site(Path(parser.parse_args().root).resolve())
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("WorkProofCam site validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
