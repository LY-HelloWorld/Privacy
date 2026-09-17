import unittest
from pathlib import Path
from urllib.parse import urljoin

from tests.test_quick_content_keyboard_discovery import HeadAndLinkParser


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://ly-helloworld.github.io/Privacy/"
PRODUCT = SITE + "BorderDays_web/"
PUBLIC_URLS = {
    PRODUCT,
    PRODUCT + "how-does-schengen-90-180-rule-work/",
    PRODUCT + "when-can-i-re-enter-schengen/",
    PRODUCT + "check-a-future-schengen-trip/",
    PRODUCT + "track-tax-residency-days-across-countries/",
    PRODUCT + "us-substantial-presence-test-day-tracker/",
    PRODUCT + "uk-statutory-residence-test-day-tracker/",
    PRODUCT + "private-offline-travel-day-tracker/",
}


class StayCountDiscoveryTests(unittest.TestCase):
    # Regression entry: missing hub navigation must fail even if sitemap URLs exist.
    def test_all_formal_guides_are_reachable_from_root_hub(self):
        graph = {}
        for page in [ROOT / "index.html", *(ROOT / "BorderDays_web").rglob("index.html")]:
            relative = page.relative_to(ROOT).as_posix()
            url = SITE + relative.removesuffix("index.html")
            parser = HeadAndLinkParser()
            parser.feed(page.read_text(encoding="utf-8"))
            graph[url] = {
                urljoin(url, href).replace("/index.html", "/")
                for href in parser.links
            }

        # Follow actual anchors rather than canonical or refresh metadata:
        # only navigation edges prove that crawlers can discover a new guide.
        reached = set()
        pending = [SITE]
        while pending:
            url = pending.pop()
            if url in reached:
                continue
            reached.add(url)
            pending.extend(graph.get(url, set()) - reached)

        self.assertEqual(PUBLIC_URLS - reached, set())


if __name__ == "__main__":
    unittest.main()
