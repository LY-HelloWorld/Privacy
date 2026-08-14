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
    def test_missing_support_page_is_reported(self):
        """Dropping the public support destination must fail the site contract."""
        with tempfile.TemporaryDirectory() as directory:
            errors = validator.validate_required_pages(Path(directory))
        self.assertTrue(
            any("HomeInventory_web/support/index.html" in error for error in errors),
            errors,
        )

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_incomplete_support_page_reports_every_contact_destination(self):
        """A support shell without usable contact and policy links must not pass release validation."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            page = root / "HomeInventory_web" / "support" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text("<h1>Support</h1>", encoding="utf-8")
            errors = validator.validate_support_page(root)

        expected_fragments = (
            "luoyi9932@gmail.com",
            "https://ly-helloworld.github.io/Privacy/HomeInventory_web/",
            "https://ly-helloworld.github.io/Privacy/home-inventory/privacy.html",
            "https://ly-helloworld.github.io/Privacy/home-inventory/terms.html",
            "https://apps.apple.com/us/app/moving-boxes-organizer/id6766885651",
        )
        for fragment in expected_fragments:
            with self.subTest(fragment=fragment):
                self.assertTrue(any(fragment in error for error in errors), errors)

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
    def test_visible_legacy_brand_is_reported(self):
        """Legacy aliases must not appear in visible copy even when the canonical name is present."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = next(iter(validator.PAGE_SPECS))
            page = root / relative
            page.parent.mkdir(parents=True)
            page.write_text(
                '<h1>Moving Boxes Organizer</h1><p>HomeInventory keeps boxes searchable.</p>'
                '<script type="application/ld+json">'
                '{"@type":"SoftwareApplication",'
                f'"@id":"{validator.APP_ENTITY_ID}",'
                '"name":"Moving Boxes Organizer",'
                '"alternateName":["HomeInventory","Box Inventory"]}'
                "</script>",
                encoding="utf-8",
            )
            errors = validator.validate_brand_identity(root)

        self.assertTrue(any("visible legacy product name: HomeInventory" in error for error in errors), errors)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_structured_legacy_alias_is_reported(self):
        """Ambiguous aliases must not teach crawlers a second product name for the same App Store ID."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = next(iter(validator.PAGE_SPECS))
            page = root / relative
            page.parent.mkdir(parents=True)
            page.write_text(
                '<h1>Moving Boxes Organizer</h1>'
                '<script type="application/ld+json">'
                '{"@type":"SoftwareApplication",'
                f'"@id":"{validator.APP_ENTITY_ID}",'
                '"name":"Moving Boxes Organizer",'
                '"alternateName":["HomeInventory","Box Inventory"]}'
                "</script>",
                encoding="utf-8",
            )
            errors = validator.validate_brand_identity(root)

        self.assertTrue(any("structured legacy product name: HomeInventory" in error for error in errors), errors)
        self.assertTrue(any("structured legacy product name: Box Inventory" in error for error in errors), errors)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_wrong_structured_primary_name_is_reported(self):
        """The shared app entity must use the exact current App Store product name."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = next(iter(validator.PAGE_SPECS))
            page = root / relative
            page.parent.mkdir(parents=True)
            page.write_text(
                '<h1>Moving Boxes Organizer</h1>'
                '<script type="application/ld+json">'
                '{"@type":"SoftwareApplication",'
                f'"@id":"{validator.APP_ENTITY_ID}",'
                '"name":"HomeInventory"}'
                "</script>",
                encoding="utf-8",
            )
            errors = validator.validate_brand_identity(root)

        self.assertTrue(any("primary structured product name" in error for error in errors), errors)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_landing_without_purchase_and_storage_facts_is_reported(self):
        """A landing page must answer the privacy, account, sharing, and subscription filters it claims."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = "HomeInventory_web/index.html"
            page = root / relative
            page.parent.mkdir(parents=True)
            page.write_text(
                '<h1>Moving Boxes Organizer</h1>'
                '<p>Find items in moving boxes.</p>',
                encoding="utf-8",
            )
            errors = validator.validate_html_pages(root)

        self.assertTrue(any("local-by-default storage" in error for error in errors), errors)
        self.assertTrue(any("separate-account boundary" in error for error in errors), errors)
        self.assertTrue(any("one-time Pro purchase" in error for error in errors), errors)
        self.assertTrue(any("Shared Inventory boundary" in error for error in errors), errors)

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_relative_directory_navigation_is_reported(self):
        """Relative directory links must name index.html so local file previews open the page."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "HomeInventory_web" / "index.html"
            destination = root / "HomeInventory_web" / "guide" / "index.html"
            source.parent.mkdir(parents=True)
            destination.parent.mkdir(parents=True)
            source.write_text('<a href="guide/">Guide</a>', encoding="utf-8")
            destination.write_text("<h1>Guide</h1>", encoding="utf-8")

            errors = validator.validate_internal_targets(root)

        self.assertTrue(any("directory-only navigation" in error for error in errors), errors)

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
