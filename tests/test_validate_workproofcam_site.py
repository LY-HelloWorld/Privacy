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


if __name__ == "__main__":
    unittest.main()
