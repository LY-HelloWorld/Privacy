#!/usr/bin/env python3
"""Validate HomeInventory's public pages, app identity, assets, and discovery files."""

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
SITE_BASE = f"{SITE_ORIGIN}{SITE_PREFIX}HomeInventory_web/"
APP_ENTITY_ID = f"{SITE_BASE}#app"
APP_STORE_ID = "6766885651"
APP_STORE_URL = "https://apps.apple.com/us/app/moving-boxes-organizer/id6766885651"
PRODUCT_NAME = "Moving Boxes Organizer by HomeInventory"

PAGE_SPECS = {
    "HomeInventory_web/index.html": SITE_BASE,
    "HomeInventory_web/how-to-keep-track-of-moving-boxes/index.html": f"{SITE_BASE}how-to-keep-track-of-moving-boxes/",
    "HomeInventory_web/find-items-without-opening-boxes/index.html": f"{SITE_BASE}find-items-without-opening-boxes/",
    "HomeInventory_web/qr-labels-for-storage-boxes/index.html": f"{SITE_BASE}qr-labels-for-storage-boxes/",
}
REQUIRED_PAGES = tuple(PAGE_SPECS)
SITEMAPS = ("sitemap.xml", "HomeInventory_web/sitemap.xml")
FORBIDDEN_VISIBLE_TERMS = (
    "reddit",
    "competitor",
    "research source",
    "gpt",
    "seo",
    "schema",
    "crawler",
    "ranking",
    "best app",
)


class PageParser(HTMLParser):
    """Collect the small set of document signals used by the release contract."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1_count = 0
        self.canonicals: list[str] = []
        self.json_ld_blocks: list[str] = []
        self.meta: dict[str, list[str]] = {}
        self.targets: list[str] = []
        self.images: list[dict[str, str]] = []
        self.visible_parts: list[str] = []
        self._hidden_depth = 0
        self._inside_json_ld = False
        self._json_ld_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value for name, value in attrs if value is not None}
        if tag == "h1":
            self.h1_count += 1
        if tag in {"script", "style"}:
            self._hidden_depth += 1
        if tag == "link":
            href = values.get("href")
            if href:
                self.targets.append(href)
            if href and "canonical" in set(values.get("rel", "").split()):
                self.canonicals.append(href)
        if tag == "a" and values.get("href"):
            self.targets.append(values["href"])
        if tag == "script" and values.get("src"):
            self.targets.append(values["src"])
        if tag == "img":
            if values.get("src"):
                self.targets.append(values["src"])
            self.images.append(values)
        if tag == "meta":
            key = values.get("name") or values.get("property")
            if key:
                self.meta.setdefault(key, []).append(values.get("content", ""))
        if tag == "script" and values.get("type") == "application/ld+json":
            self._inside_json_ld = True
            self._json_ld_parts = []

    def handle_data(self, data: str) -> None:
        if self._inside_json_ld:
            self._json_ld_parts.append(data)
        elif self._hidden_depth == 0:
            self.visible_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._inside_json_ld:
            self.json_ld_blocks.append("".join(self._json_ld_parts).strip())
            self._inside_json_ld = False
            self._json_ld_parts = []
        if tag in {"script", "style"} and self._hidden_depth:
            self._hidden_depth -= 1


def parse_page(path: Path) -> tuple[PageParser, str]:
    """Parse one UTF-8 page and retain its source for exact identity checks."""
    html = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(html)
    parser.close()
    return parser, html


def validate_required_pages(root: Path) -> list[str]:
    """Require all four crawlable HomeInventory destinations."""
    return [
        f"Missing required page: {relative}"
        for relative in REQUIRED_PAGES
        if not (root / relative).is_file()
    ]


def contains_entity_id(value: object) -> bool:
    """Find the shared app identity at any JSON-LD depth, including an @graph node."""
    if isinstance(value, dict):
        if value.get("@id") == APP_ENTITY_ID:
            return True
        return any(contains_entity_id(nested) for nested in value.values())
    if isinstance(value, list):
        return any(contains_entity_id(nested) for nested in value)
    return False


def validate_html_pages(root: Path) -> list[str]:
    """Validate page-level metadata, app handoff, identity, and restrained visible copy."""
    errors: list[str] = []
    required_meta = {
        "description",
        "robots",
        "og:title",
        "og:description",
        "og:url",
        "twitter:title",
        "twitter:description",
        "apple-itunes-app",
    }
    for relative, expected_canonical in PAGE_SPECS.items():
        path = root / relative
        if not path.is_file():
            continue
        parser, html = parse_page(path)
        if parser.h1_count != 1:
            errors.append(f"{relative} must contain exactly one h1; found {parser.h1_count}")
        if parser.canonicals != [expected_canonical]:
            errors.append(f"{relative} canonical mismatch: {parser.canonicals!r}")
        missing_meta = sorted(required_meta - set(parser.meta))
        if missing_meta:
            errors.append(f"{relative} is missing metadata: {', '.join(missing_meta)}")
        if parser.meta.get("apple-itunes-app") != [f"app-id={APP_STORE_ID}"]:
            errors.append(f"{relative} has the wrong App Store Smart App Banner identity")
        if APP_STORE_URL not in html:
            errors.append(f"{relative} is missing the exact App Store URL")
        if PRODUCT_NAME not in " ".join(parser.visible_parts):
            errors.append(f"{relative} is missing the visible product identity: {PRODUCT_NAME}")

        valid_json_values: list[object] = []
        if not parser.json_ld_blocks:
            errors.append(f"{relative} has no JSON-LD entity data")
        for index, block in enumerate(parser.json_ld_blocks, start=1):
            try:
                valid_json_values.append(json.loads(block))
            except json.JSONDecodeError as error:
                errors.append(f"{relative} JSON-LD block {index} is invalid: {error}")
        if not any(contains_entity_id(value) for value in valid_json_values):
            errors.append(f"{relative} does not reference the shared app entity {APP_ENTITY_ID}")

        visible_copy = " ".join(parser.visible_parts).lower()
        for term in FORBIDDEN_VISIBLE_TERMS:
            if term in visible_copy:
                errors.append(f"{relative} exposes forbidden process language: {term}")
    return errors


def validate_screenshot_dimensions(root: Path) -> list[str]:
    """Require intrinsic dimensions on every real App Store screenshot to prevent stretching."""
    errors: list[str] = []
    for relative in REQUIRED_PAGES:
        path = root / relative
        if not path.is_file():
            continue
        parser, _ = parse_page(path)
        for image in parser.images:
            source = image.get("src", "")
            if "assets/screenshots/" not in source:
                continue
            if image.get("width") != "1260" or image.get("height") != "2736":
                errors.append(f"{relative} screenshot {source} must declare intrinsic size 1260x2736")
    return errors


def sitemap_locations(path: Path) -> tuple[list[str], str | None]:
    """Return sitemap URLs while converting malformed XML into a validation message."""
    try:
        document = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as error:
        return [], str(error)
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    return [node.text or "" for node in document.findall(f"{namespace}url/{namespace}loc")], None


def validate_sitemaps(root: Path) -> list[str]:
    """Require both discovery files to list every canonical exactly once."""
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


def local_target(root: Path, source: Path, target: str) -> Path | None:
    """Resolve only repository-owned links; external destinations are validated separately."""
    parsed = urlparse(target)
    if parsed.scheme in {"mailto", "tel", "javascript", "data"}:
        return None
    if parsed.scheme in {"http", "https"}:
        if f"{parsed.scheme}://{parsed.netloc}" != SITE_ORIGIN or not parsed.path.startswith(SITE_PREFIX):
            return None
        candidate = root / unquote(parsed.path[len(SITE_PREFIX) :])
    elif parsed.netloc:
        return None
    else:
        if not parsed.path:
            return None
        candidate = source.parent / unquote(parsed.path)
    # GitHub Pages maps directory routes to index.html, so validate the served file rather than the folder.
    if parsed.path.endswith("/") or candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate.resolve()


def validate_internal_targets(root: Path) -> list[str]:
    """Reject broken or repository-escaping links and image/style references."""
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
    """Run every independent check and return all actionable errors in one pass."""
    errors: list[str] = []
    for validator_function in (
        validate_required_pages,
        validate_html_pages,
        validate_screenshot_dimensions,
        validate_sitemaps,
        validate_internal_targets,
    ):
        errors.extend(validator_function(root))
    return errors


# CLI entry: gate commits and deploys with one deterministic, dependency-free command.
def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the HomeInventory static-site contract.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root; defaults to the current directory.")
    errors = validate_site(Path(parser.parse_args().root).resolve())
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("HomeInventory site validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
