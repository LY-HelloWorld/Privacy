import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-beadcraft-site.py"


class BeadCraftSiteValidatorTests(unittest.TestCase):
    """The site contract keeps every Japanese page paired with one English equivalent."""

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="beadcraft-site-"))
        for relative in (
            "BeadCraftLocal_web",
            "BeadCraftLocal",
            "robots.txt",
            "sitemap.xml",
            "core-sitemap.xml",
            "index.html",
        ):
            source = ROOT / relative
            if not source.exists():
                continue
            target = self.temp_dir / relative
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def run_validator(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(self.temp_dir)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_current_site_satisfies_bilingual_discovery_contract(self) -> None:
        result = self.run_validator()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("BeadCraft bilingual site validation passed", result.stdout)

    def test_missing_language_pair_and_store_identity_fail_validation(self) -> None:
        japanese_page = self.temp_dir / "BeadCraftLocal_web" / "ja" / "index.html"
        if not japanese_page.exists():
            self.skipTest("production pages are created during the GREEN phase")
        japanese_page.unlink()
        english_page = self.temp_dir / "BeadCraftLocal_web" / "index.html"
        english_page.write_text(
            '<!doctype html><html lang="en"><head><link rel="canonical" '
            'href="https://ly-helloworld.github.io/Privacy/BeadCraftLocal_web/en/">'
            '</head><body><h1>BeadCraft</h1></body></html>',
            encoding="utf-8",
        )

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing page", result.stdout)
        self.assertIn("canonical mismatch", result.stdout)
        self.assertIn("missing SoftwareApplication identity", result.stdout)

    def test_broken_internal_asset_and_sitemap_entry_fail_validation(self) -> None:
        product_page = self.temp_dir / "BeadCraftLocal_web" / "index.html"
        if not product_page.exists():
            self.skipTest("production pages are created during the GREEN phase")
        product_page.write_text(
            product_page.read_text(encoding="utf-8").replace(
                "./assets/app-icon.png", "./assets/missing-icon.png"
            ),
            encoding="utf-8",
        )
        sitemap = self.temp_dir / "core-sitemap.xml"
        sitemap.write_text(
            sitemap.read_text(encoding="utf-8").replace(
                "https://ly-helloworld.github.io/Privacy/BeadCraftLocal_web/", ""
            ),
            encoding="utf-8",
        )

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing local asset", result.stdout)
        self.assertIn("core-sitemap.xml: missing", result.stdout)


if __name__ == "__main__":
    unittest.main()
