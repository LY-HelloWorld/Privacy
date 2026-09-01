#!/usr/bin/env python3
"""Validate LivePhoto Safe's crawl paths, canonical pages, and prelaunch app identity."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


PUBLIC_ROOT = "https://ly-helloworld.github.io/Privacy/"
PRODUCT_ROOT = f"{PUBLIC_ROOT}livephoto-safe-web/"
APP_ENTITY_ID = f"{PRODUCT_ROOT}#app"
APP_STORE_ID = "6805516057"
BUNDLE_ID = "com.ly.LivePhotoSafeShareApp"
PAGE_PATHS = (
    "livephoto-safe-web/index.html",
    "livephoto-safe-web/protect-live-photos-before-sharing/index.html",
    "livephoto-safe-web/remove-location-metadata-before-sharing/index.html",
    "livephoto-safe-web/blur-faces-in-live-photos/index.html",
    "livephoto-safe-web/mute-live-photo-audio-before-sharing/index.html",
    "livephoto-safe-web/share-kids-photos-without-showing-faces/index.html",
    "livephoto-safe-web/share-marketplace-photos-without-location-data/index.html",
    "livephoto-safe-web/hide-personal-information-in-id-photos/index.html",
)
CANONICAL_URLS = tuple(
    PRODUCT_ROOT if path == "livephoto-safe-web/index.html"
    else f"{PRODUCT_ROOT}{Path(path).parent.name}/"
    for path in PAGE_PATHS
)


class PageParser(HTMLParser):
    """Collect discovery metadata without depending on a browser runtime."""

    def __init__(self) -> None:
        super().__init__()
        self.canonicals: list[str] = []
        self.links: list[str] = []
        self.meta_names: dict[str, str] = {}
        self.json_ld: list[dict[str, object]] = []
        self._in_json_ld = False
        self._json_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "link" and "canonical" in values.get("rel", "").split():
            self.canonicals.append(values.get("href", ""))
        if tag == "a":
            self.links.append(values.get("href", ""))
        if tag == "meta" and values.get("name"):
            self.meta_names[values["name"]] = values.get("content", "")
        if tag == "script" and values.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._json_chunks = []

    def handle_data(self, data: str) -> None:
        if self._in_json_ld:
            self._json_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "script" or not self._in_json_ld:
            return
        self._in_json_ld = False
        try:
            payload = json.loads("".join(self._json_chunks))
        except json.JSONDecodeError:
            return
        if isinstance(payload, dict):
            self.json_ld.append(payload)


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def sitemap_locations(path: Path) -> set[str]:
    root = ET.parse(path).getroot()
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    return {element.text or "" for element in root.findall(f"{namespace}url/{namespace}loc")}


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    expected_identity = {
        "@type": "SoftwareApplication",
        "@id": APP_ENTITY_ID,
        "name": "LivePhoto Safe",
        "url": PRODUCT_ROOT,
        "operatingSystem": "iOS 17 or later",
        "applicationCategory": "UtilitiesApplication",
    }

    for relative, canonical in zip(PAGE_PATHS, CANONICAL_URLS, strict=True):
        parser = parse_page(root / relative)
        if parser.canonicals != [canonical]:
            errors.append(f"{relative}: canonical mismatch")
        identities = [item for item in parser.json_ld if item.get("@type") == "SoftwareApplication"]
        if len(identities) != 1:
            errors.append(f"{relative}: missing SoftwareApplication identity")
            continue
        identity = identities[0]
        for key, expected in expected_identity.items():
            if identity.get(key) != expected:
                errors.append(f"{relative}: SoftwareApplication {key} mismatch")
        identifiers = identity.get("identifier", [])
        serialized_identifiers = json.dumps(identifiers, ensure_ascii=False)
        if APP_STORE_ID not in serialized_identifiers or BUNDLE_ID not in serialized_identifiers:
            errors.append(f"{relative}: Apple App Store ID or bundle ID missing")
        if "downloadUrl" in identity or "sameAs" in identity:
            errors.append(f"{relative}: storefront download surfaces must stay disabled")
        if "apple-itunes-app" in parser.meta_names or any(
            "apps.apple.com" in link for link in parser.links
        ):
            errors.append(f"{relative}: storefront download surfaces must stay disabled")

    root_index = parse_page(root / "index.html")
    if not any("livephoto-safe-web/" in link for link in root_index.links):
        errors.append("root index must link to LivePhoto Safe")

    robots = (root / "robots.txt").read_text(encoding="utf-8")
    if "User-agent: OAI-SearchBot\nAllow: /" not in robots:
        errors.append("root robots must allow OAI-SearchBot")
    if f"Sitemap: {PRODUCT_ROOT}sitemap.xml" not in robots:
        errors.append("root robots must advertise the LivePhoto Safe sitemap")

    for relative in ("sitemap.xml", "core-sitemap.xml", "livephoto-safe-web/sitemap.xml"):
        locations = sitemap_locations(root / relative)
        missing = set(CANONICAL_URLS) - locations
        if missing:
            errors.append(f"{relative}: missing {len(missing)} LivePhoto Safe canonical URLs")

    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("LivePhoto Safe site validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
