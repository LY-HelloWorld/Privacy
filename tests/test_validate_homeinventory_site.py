"""Entry tests for the HomeInventory static-site validation command."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "validate-homeinventory-site.py"


def load_validator():
    """Load the shipped validator by path because its filename contains hyphens."""
    if not SCRIPT_PATH.is_file():
        return None
    specification = importlib.util.spec_from_file_location("validate_homeinventory_site", SCRIPT_PATH)
    if specification is None or specification.loader is None:
        return None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


validator = load_validator()


class HomeInventorySiteValidatorTests(unittest.TestCase):
    """Protect product identity, crawlable pages, links, and screenshot proportions."""

    def test_validator_module_exists(self):
        """Removing the release gate must fail the HomeInventory site contract."""
        self.assertIsNotNone(validator, f"Missing validator: {SCRIPT_PATH}")

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_committed_site_is_valid(self):
        """The checked-in public site must satisfy the complete release contract."""
        self.assertEqual([], validator.validate_site(ROOT))

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_missing_required_page_is_reported(self):
        """A missing intent page must produce an actionable path-level error."""
        with tempfile.TemporaryDirectory() as directory:
            errors = validator.validate_required_pages(Path(directory))
        self.assertTrue(
            any("how-to-keep-track-of-moving-boxes/index.html" in error for error in errors),
            errors,
        )

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_wrong_app_identity_is_reported(self):
        """A page that points to another app must not pass entity validation."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = next(iter(validator.PAGE_SPECS))
            page = root / relative
            page.parent.mkdir(parents=True)
            page.write_text(
                '<h1>Wrong app</h1><meta name="apple-itunes-app" content="app-id=1">'
                '<script type="application/ld+json">'
                '{"@type":"SoftwareApplication","@id":"https://example.com/#wrong"}'
                "</script>",
                encoding="utf-8",
            )
            errors = validator.validate_html_pages(root)
        self.assertTrue(any("App Store" in error or "entity" in error for error in errors), errors)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_wrong_screenshot_dimensions_are_reported(self):
        """Changing intrinsic image dimensions must catch future screenshot stretching risks."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = next(iter(validator.PAGE_SPECS))
            page = root / relative
            page.parent.mkdir(parents=True)
            page.write_text(
                '<img src="assets/screenshots/example.png" width="1000" height="1000" alt="Example">',
                encoding="utf-8",
            )
            errors = validator.validate_screenshot_dimensions(root)
        self.assertTrue(any("1260x2736" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
