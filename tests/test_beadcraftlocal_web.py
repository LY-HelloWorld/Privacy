import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "BeadCraftLocal_web" / "index.html"


class BeadCraftLocalWebTests(unittest.TestCase):
    def test_marketing_page_has_public_contract(self):
        html = PAGE.read_text(encoding="utf-8")

        self.assertIn("<title>BeadCraft Local |", html)
        self.assertRegex(html, r'<meta name="description" content="[^"]+"')
        self.assertIn(
            '<link rel="canonical" href="https://ly-helloworld.github.io/Privacy/BeadCraftLocal_web/">',
            html,
        )
        self.assertIn("https://apps.apple.com/us/app/beadcraft-bead-patterns/id6779639958", html)
        self.assertIn("../BeadCraftLocal/privacy.html", html)
        self.assertIn("../BeadCraftLocal/terms.html", html)
        self.assertIn("mailto:luoyi9932@gmail.com", html)
        self.assertIn("processed on device", html.lower())
        self.assertIn('href="./site.css"', html)
        self.assertTrue(
            (ROOT / "BeadCraftLocal_web" / "assets" / "app-icon.png").is_file()
        )

        match = re.search(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, re.S
        )
        self.assertIsNotNone(match)
        data = json.loads(match.group(1))
        applications = [item for item in data["@graph"] if item.get("@type") == "SoftwareApplication"]
        self.assertEqual(len(applications), 1)
        self.assertEqual(applications[0]["identifier"], "6779639958")


if __name__ == "__main__":
    unittest.main()
