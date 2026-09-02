import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "BorderDays_web"
BASE = "https://ly-helloworld.github.io/Privacy/BorderDays_web/"
APP_STORE = "https://apps.apple.com/app/id6803141319"
ROUTES = [
    "",
    "how-does-schengen-90-180-rule-work/",
    "when-can-i-re-enter-schengen/",
    "check-a-future-schengen-trip/",
    "track-tax-residency-days-across-countries/",
    "us-substantial-presence-test-day-tracker/",
    "uk-statutory-residence-test-day-tracker/",
    "private-offline-travel-day-tracker/",
]
LEGACY = {
    "schengen-90-180-calculator/": "how-does-schengen-90-180-rule-work/",
    "tax-residency-day-tracker/": "track-tax-residency-days-across-countries/",
    "private-travel-day-ledger/": "private-offline-travel-day-tracker/",
}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.links = []
        self.meta = []
        self.canonicals = []
        self.scripts = []
        self._script = None
        self._script_parts = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])
        if tag == "meta":
            self.meta.append(values)
        if tag == "link" and values.get("rel") == "canonical":
            self.canonicals.append(values.get("href"))
        if tag == "script" and values.get("type") == "application/ld+json":
            self._script = values
            self._script_parts = []

    def handle_data(self, data):
        if self._script is not None:
            self._script_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._script is not None:
            self.scripts.append(json.loads("".join(self._script_parts)))
            self._script = None


def read_page(route):
    path = SITE / route / "index.html" if route else SITE / "index.html"
    text = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)
    return path, text, parser


def schema_types(value):
    if isinstance(value, dict):
        found = {value.get("@type")} if value.get("@type") else set()
        for child in value.values():
            found |= schema_types(child)
        return found
    if isinstance(value, list):
        result = set()
        for child in value:
            result |= schema_types(child)
        return result
    return set()


class BorderDaysWebTests(unittest.TestCase):
    def test_all_canonical_pages_have_unique_metadata(self):
        titles, descriptions = set(), set()
        for route in ROUTES:
            path, text, page = read_page(route)
            self.assertEqual(page.h1, 1, path)
            title = re.search(r"<title>(.*?)</title>", text, re.S).group(1)
            description = next(m["content"] for m in page.meta if m.get("name") == "description")
            self.assertNotIn(title, titles)
            self.assertNotIn(description, descriptions)
            titles.add(title)
            descriptions.add(description)
            self.assertEqual(page.canonicals, [BASE + route])
            banner = next(m["content"] for m in page.meta if m.get("name") == "apple-itunes-app")
            self.assertIn("app-id=6803141319", banner)
            self.assertIn(APP_STORE, page.links)

    def test_homepage_contract(self):
        _, text, page = read_page("")
        for phrase in ["StayCount: Schengen &amp; Tax", "No account", "No location permission",
                       "Schengen 90/180", "US Substantial Presence", "UK Visitor",
                       "UK Statutory Residence Test"]:
            self.assertIn(phrase, text)
        for route in ROUTES[1:]:
            self.assertIn(route, text)
        self.assertGreaterEqual(page.links.count(APP_STORE), 2)
        self.assertEqual(len(re.findall(r'class="app-screenshot"', text)), 3)
        self.assertIn("../BorderDays/privacy.html", page.links)
        self.assertIn("../BorderDays/terms.html", page.links)
        self.assertIn("../BorderDays/support.html", page.links)
        types = set().union(*(schema_types(script) for script in page.scripts))
        self.assertIn("SoftwareApplication", types)
        self.assertIn("com.ly.find.borderdays", text)

    def test_pain_page_contracts(self):
        for route in ROUTES[1:]:
            path, text, page = read_page(route)
            for section_id in ["direct-answer", "worked-example", "checklist", "mistakes",
                               "staycount", "official-references", "faq", "boundary"]:
                self.assertIn(f'id="{section_id}"', text, f"{path}: {section_id}")
            self.assertRegex(text.lower(), r"simplified|fictional")
            self.assertGreaterEqual(page.links.count(APP_STORE), 3)
            types = set().union(*(schema_types(script) for script in page.scripts))
            self.assertTrue({"Article", "FAQPage", "BreadcrumbList"}.issubset(types), path)
            self.assertGreaterEqual(len(re.findall(r'<details', text)), 3, path)
            self.assertLessEqual(len(re.findall(r'<details', text)), 5, path)

    def test_internal_links_resolve(self):
        for route in ROUTES:
            path, _, page = read_page(route)
            for href in page.links:
                parsed = urlparse(href)
                if parsed.scheme or href.startswith(("#", "mailto:")):
                    continue
                target = (path.parent / parsed.path).resolve()
                if parsed.path.endswith("/"):
                    target /= "index.html"
                self.assertTrue(target.exists(), f"{path}: broken {href}")

    def test_release_contract(self):
        for old, new in LEGACY.items():
            _, text, page = read_page(old)
            self.assertIn('name="robots" content="noindex,follow"', text)
            self.assertEqual(page.canonicals, [BASE + new])
            self.assertIn("url=../" + new, text)
            self.assertIn("../" + new, page.links)
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for route in ROUTES:
            self.assertEqual(sitemap.count(f"<loc>{BASE + route}</loc>"), 1)
        for old in LEGACY:
            self.assertNotIn(f"<loc>{BASE + old}</loc>", sitemap)
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("User-agent: *\nAllow: /", robots)
        self.assertIn("https://ly-helloworld.github.io/Privacy/sitemap.xml", robots)
        benchmark = json.loads((SITE / "research/gpt-visibility-benchmark.json").read_text())
        self.assertEqual(benchmark["target_entity_id"], "6803141319")
        self.assertGreaterEqual(len(benchmark["prompts"]), 3)
        self.assertLessEqual(len(benchmark["prompts"]), 5)


if __name__ == "__main__":
    unittest.main()
