import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-livephoto-safe-site.py"


class LivePhotoSafeSiteValidatorTests(unittest.TestCase):
    """The validator protects crawler discovery and one stable application identity."""

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="livephoto-safe-site-"))
        for relative in (
            "livephoto-safe-web",
            "livephoto-safe",
            "robots.txt",
            "sitemap.xml",
            "core-sitemap.xml",
            "index.html",
        ):
            source = ROOT / relative
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

    def test_current_site_satisfies_discovery_and_entity_contract(self) -> None:
        result = self.run_validator()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("LivePhoto Safe site validation passed", result.stdout)

    def test_missing_root_discovery_and_app_identity_fail_validation(self) -> None:
        (self.temp_dir / "index.html").write_text("<html><body>App directory</body></html>")
        (self.temp_dir / "livephoto-safe-web" / "index.html").write_text(
            '<html><head><link rel="canonical" '
            'href="https://ly-helloworld.github.io/Privacy/livephoto-safe-web/">'
            '</head><body><h1>LivePhoto Safe</h1></body></html>'
        )

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("root index must link to LivePhoto Safe", result.stdout)
        self.assertIn("missing SoftwareApplication identity", result.stdout)

    def test_download_surfaces_remain_disabled_while_storefront_is_unavailable(self) -> None:
        product_page = self.temp_dir / "livephoto-safe-web" / "index.html"
        product_page.write_text(
            product_page.read_text()
            .replace("</head>", '<meta name="apple-itunes-app" content="app-id=6805516057"></head>')
            .replace("</body>", '<a href="https://apps.apple.com/app/id6805516057">Download</a></body>')
        )

        result = self.run_validator()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("storefront download surfaces must stay disabled", result.stdout)


if __name__ == "__main__":
    unittest.main()
