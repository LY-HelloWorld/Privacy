"""Entry tests for the WorkProofCam static-site validation command."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "validate-workproofcam-site.py"


def load_validator():
    """Load the real CLI module by path because its filename contains hyphens."""
    if not SCRIPT_PATH.is_file():
        return None
    specification = importlib.util.spec_from_file_location("validate_workproofcam_site", SCRIPT_PATH)
    if specification is None or specification.loader is None:
        return None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


validator = load_validator()


class WorkProofCamSiteValidatorTests(unittest.TestCase):
    def test_validator_module_exists(self):
        """Removing the shipped validator must break the site contract suite."""
        self.assertIsNotNone(validator, f"Missing validator: {SCRIPT_PATH}")

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_committed_site_is_valid(self):
        """A broken canonical, link, JSON-LD block, or sitemap must fail validation."""
        self.assertEqual([], validator.validate_site(ROOT))

    @unittest.skipIf(validator is None, "validator module is not implemented yet")
    def test_missing_required_page_is_reported(self):
        """Deleting a required public page must produce an actionable error."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            errors = validator.validate_required_pages(root)
        self.assertTrue(any("workproofcam-web/index.html" in error for error in errors), errors)

    def test_publisher_identity_validator_exists(self):
        """Removing the bilingual publisher contract must break validation."""
        self.assertTrue(hasattr(validator, "validate_publisher_identity"))

    @unittest.skipUnless(
        validator is not None and hasattr(validator, "validate_publisher_identity"),
        "publisher identity validation is not implemented yet",
    )
    def test_missing_english_publisher_identity_is_reported(self):
        """A website that exposes only the Chinese seller label must be rejected."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            page = root / "workproofcam-web" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text(
                '<p>Published on the App Store by 雪梅 黄</p>'
                '<script type="application/ld+json">'
                '{"publisher":{"@type":"Person","name":"雪梅 黄"}}'
                "</script>",
                encoding="utf-8",
            )
            errors = validator.validate_publisher_identity(root)
        self.assertTrue(any("Xuemei Huang" in error for error in errors), errors)

    def test_missing_identity_on_secondary_page_is_reported(self):
        """Dropping publisher identity from an intent page must not be hidden by a valid homepage."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            main = root / "workproofcam-web" / "index.html"
            main.parent.mkdir(parents=True)
            main.write_text(
                '<p>Published on the App Store by Xuemei Huang '
                '(listed on the App Store as 雪梅 黄)</p>'
                '<script type="application/ld+json">'
                '{"publisher":{"@type":"Person","name":"Xuemei Huang",'
                '"alternateName":"雪梅 黄"}}'
                "</script>",
                encoding="utf-8",
            )
            secondary = root / "workproofcam-web" / "job-site-photo-report-app" / "index.html"
            secondary.parent.mkdir(parents=True)
            secondary.write_text("<p>WorkProofCam job-site photo reports</p>", encoding="utf-8")
            errors = validator.validate_publisher_identity(root)
        self.assertTrue(any("job-site-photo-report-app" in error for error in errors), errors)

    @unittest.skipUnless(
        validator is not None and hasattr(validator, "validate_publisher_identity"),
        "publisher identity validation is not implemented yet",
    )
    def test_committed_site_has_bilingual_publisher_identity(self):
        """The rendered identity and JSON-LD must connect the English name to Apple's label."""
        self.assertEqual([], validator.validate_publisher_identity(ROOT))


if __name__ == "__main__":
    unittest.main()
