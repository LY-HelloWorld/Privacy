#!/usr/bin/env python3
"""Validate BeadCraft's bilingual pages, crawl paths, assets, and App Store identity."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


PUBLIC_ROOT = "https://ly-helloworld.github.io/Privacy/"
PRODUCT_ROOT = f"{PUBLIC_ROOT}BeadCraftLocal_web/"
APP_ENTITY_ID = f"{PRODUCT_ROOT}#app"
APP_STORE_ID = "6779639958"
BUNDLE_ID = "com.luoyi.beadcraftlocal"
APP_STORE_URLS = {
    "ja": "https://apps.apple.com/jp/app/beadcraft-%E3%82%A2%E3%82%A4%E3%83%AD%E3%83%B3%E3%83%93%E3%83%BC%E3%82%BA%E5%9B%B3%E6%A1%88/id6779639958",
    "en": "https://apps.apple.com/us/app/beadcraft-bead-patterns/id6779639958",
}
SLUGS = (
    "",
    "photo-to-iron-beads-pattern/",
    "bead-color-numbers-and-counts/",
    "large-pattern-making-guide/",
)
PAGE_CONTRACTS = tuple(
    (
        f"BeadCraftLocal_web/{'ja/' if language == 'ja' else ''}{slug}index.html",
        language,
        f"{PRODUCT_ROOT}{'ja/' if language == 'ja' else ''}{slug}",
        f"{PRODUCT_ROOT}ja/{slug}",
        f"{PRODUCT_ROOT}{slug}",
    )
    for slug in SLUGS
    for language in ("en", "ja")
)
CANONICAL_URLS = tuple(contract[2] for contract in PAGE_CONTRACTS)


class PageParser(HTMLParser):
    """Collect the visible and machine-readable signals used by the site contract."""

    def __init__(self) -> None:
        super().__init__()
        self.html_lang = ""
        self.canonicals: list[str] = []
        self.alternates: dict[str, str] = {}
        self.links: list[str] = []
        self.images: list[str] = []
        self.meta_names: dict[str, str] = {}
        self.meta_properties: dict[str, str] = {}
        self.json_ld: list[dict[str, object]] = []
        self.title = ""
        self.h1 = ""
        self._capture: str | None = None
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.html_lang = values.get("lang", "")
        if tag == "link":
            rel = values.get("rel", "").split()
            if "canonical" in rel:
                self.canonicals.append(values.get("href", ""))
            if "alternate" in rel and values.get("hreflang"):
                self.alternates[values["hreflang"]] = values.get("href", "")
        if tag == "a":
            self.links.append(values.get("href", ""))
        if tag == "img":
            self.images.append(values.get("src", ""))
        if tag == "meta" and values.get("name"):
            self.meta_names[values["name"]] = values.get("content", "")
        if tag == "meta" and values.get("property"):
            self.meta_properties[values["property"]] = values.get("content", "")
        if tag in {"title", "h1"}:
            self._capture = tag
            self._chunks = []
        if tag == "script" and values.get("type") == "application/ld+json":
            self._capture = "json"
            self._chunks = []

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._capture == "title" and tag == "title":
            self.title = " ".join("".join(self._chunks).split())
            self._capture = None
        elif self._capture == "h1" and tag == "h1":
            self.h1 = " ".join("".join(self._chunks).split())
            self._capture = None
        elif self._capture == "json" and tag == "script":
            try:
                payload = json.loads("".join(self._chunks))
            except json.JSONDecodeError:
                payload = None
            if isinstance(payload, dict):
                self.json_ld.append(payload)
            self._capture = None


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def json_objects(payload: object) -> list[dict[str, object]]:
    """Flatten JSON-LD graphs so each page can expose one stable app entity."""
    if isinstance(payload, dict):
        objects = [payload]
        for value in payload.values():
            objects.extend(json_objects(value))
        return objects
    if isinstance(payload, list):
        objects: list[dict[str, object]] = []
        for value in payload:
            objects.extend(json_objects(value))
        return objects
    return []


def sitemap_locations(path: Path) -> list[str]:
    root = ET.parse(path).getroot()
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    return [element.text or "" for element in root.findall(f"{namespace}url/{namespace}loc")]


def local_target(page: Path, reference: str) -> Path | None:
    parsed = urlparse(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(('#', 'mailto:', 'tel:')):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    target = (page.parent / path).resolve()
    if path.endswith("/"):
        target /= "index.html"
    return target


def validate(root: Path) -> list[str]:
    """Return every contract violation instead of stopping at the first broken page."""
    errors: list[str] = []
    titles: set[str] = set()
    descriptions: set[str] = set()

    for relative, language, canonical, japanese_url, english_url in PAGE_CONTRACTS:
        page = root / relative
        if not page.is_file():
            errors.append(f"{relative}: missing page")
            continue
        parser = parse_page(page)
        if parser.html_lang != language:
            errors.append(f"{relative}: html language mismatch")
        if parser.canonicals != [canonical]:
            errors.append(f"{relative}: canonical mismatch")
        expected_alternates = {
            "ja": japanese_url,
            "en": english_url,
            "x-default": japanese_url,
        }
        if parser.alternates != expected_alternates:
            errors.append(f"{relative}: hreflang pair mismatch")
        if not parser.title or parser.title in titles:
            errors.append(f"{relative}: title missing or duplicated")
        titles.add(parser.title)
        description = parser.meta_names.get("description", "")
        if not description or description in descriptions:
            errors.append(f"{relative}: description missing or duplicated")
        descriptions.add(description)
        if not parser.h1:
            errors.append(f"{relative}: missing h1")
        if parser.meta_names.get("robots") != "index, follow, max-image-preview:large":
            errors.append(f"{relative}: robots metadata mismatch")
        if APP_STORE_ID not in parser.meta_names.get("apple-itunes-app", ""):
            errors.append(f"{relative}: Smart App Banner missing")
        if parser.meta_properties.get("og:url") != canonical:
            errors.append(f"{relative}: Open Graph URL mismatch")

        objects = [item for block in parser.json_ld for item in json_objects(block)]
        identities = [item for item in objects if item.get("@type") == "SoftwareApplication"]
        if len(identities) != 1:
            errors.append(f"{relative}: missing SoftwareApplication identity")
        else:
            identity = identities[0]
            expected_identity = {
                "@id": APP_ENTITY_ID,
                "name": "BeadCraft",
                "identifier": APP_STORE_ID,
                "operatingSystem": "iOS 17 or later",
                "applicationCategory": "GraphicsApplication",
                "softwareVersion": "1.5.1",
                "url": PRODUCT_ROOT,
                "downloadUrl": APP_STORE_URLS[language],
                "publisher": {
                    "@type": "Person",
                    "name": "Xuemei Huang",
                    "alternateName": "雪梅 黄",
                },
            }
            for key, expected in expected_identity.items():
                if identity.get(key) != expected:
                    errors.append(f"{relative}: SoftwareApplication {key} mismatch")
            serialized = json.dumps(identity, ensure_ascii=False)
            if BUNDLE_ID not in serialized:
                errors.append(f"{relative}: bundle ID missing from identity")

        expected_store_url = APP_STORE_URLS[language]
        if not any(link.startswith(expected_store_url) for link in parser.links):
            errors.append(f"{relative}: localized App Store link missing")
        for reference in parser.links + parser.images:
            target = local_target(page, reference)
            if target is not None and not target.exists():
                label = "asset" if reference in parser.images else "link"
                errors.append(f"{relative}: missing local {label} {reference}")

    root_index = parse_page(root / "index.html")
    if not any("BeadCraftLocal_web/" in link for link in root_index.links):
        errors.append("root index must link to BeadCraft")

    robots = (root / "robots.txt").read_text(encoding="utf-8")
    if "User-agent: OAI-SearchBot\nAllow: /" not in robots:
        errors.append("root robots must allow OAI-SearchBot")

    for relative in ("sitemap.xml", "core-sitemap.xml"):
        locations = sitemap_locations(root / relative)
        missing = set(CANONICAL_URLS) - set(locations)
        duplicates = {url for url in CANONICAL_URLS if locations.count(url) > 1}
        if missing:
            errors.append(f"{relative}: missing {len(missing)} BeadCraft canonical URLs")
        if duplicates:
            errors.append(f"{relative}: duplicated BeadCraft canonical URLs")

    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("BeadCraft bilingual site validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
