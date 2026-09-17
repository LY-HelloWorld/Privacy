import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


# Test entry: verify every public Quick Content Keyboard page remains reachable
# through the same discovery signals that Googlebot consumes.
ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://ly-helloworld.github.io/Privacy/quick-content-keyboard/"
PUBLIC_PAGES = {
    "index.html": BASE_URL,
    "support.html": f"{BASE_URL}support.html",
    "privacy.html": f"{BASE_URL}privacy.html",
    "terms.html": f"{BASE_URL}terms.html",
    "content.html": f"{BASE_URL}content.html",
}


class HeadAndLinkParser(HTMLParser):
    """Collect crawl-relevant links and metadata from the rendered HTML artifact."""

    def __init__(self):
        super().__init__()
        self.links = []
        self.meta = {}
        self.canonical = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"])
        elif tag == "meta" and attributes.get("name"):
            self.meta[attributes["name"]] = attributes.get("content", "")
        elif tag == "link" and attributes.get("rel") == "canonical":
            self.canonical = attributes.get("href")


def sitemap_urls(path):
    """Return the absolute URLs advertised by one XML sitemap."""

    root = ET.parse(path).getroot()
    return {
        element.text
        for element in root.iter()
        if element.tag.endswith("loc") and element.text
    }


class QuickContentKeyboardDiscoveryTests(unittest.TestCase):
    def test_public_pages_are_in_root_sitemaps(self):
        expected = set(PUBLIC_PAGES.values())

        for filename in ("sitemap.xml", "core-sitemap.xml"):
            with self.subTest(sitemap=filename):
                self.assertTrue(expected.issubset(sitemap_urls(ROOT / filename)))

    def test_root_hub_links_to_product_entry(self):
        parser = HeadAndLinkParser()
        parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))

        self.assertIn(BASE_URL, parser.links)

    def test_public_pages_have_unique_indexing_metadata(self):
        for filename, canonical in PUBLIC_PAGES.items():
            with self.subTest(page=filename):
                parser = HeadAndLinkParser()
                parser.feed(
                    (ROOT / "quick-content-keyboard" / filename).read_text(
                        encoding="utf-8"
                    )
                )

                self.assertTrue(parser.meta.get("description"))
                self.assertEqual(parser.meta.get("robots"), "index, follow")
                self.assertEqual(parser.canonical, canonical)


if __name__ == "__main__":
    unittest.main()
