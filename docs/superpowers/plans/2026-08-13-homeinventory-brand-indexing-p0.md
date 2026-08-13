# Moving Boxes Organizer Brand and Indexing P0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `Moving Boxes Organizer` the consistent visible website identity and submit its five existing public pages for Google and Bing discovery.

**Architecture:** The static validator owns a machine-checkable brand contract for all five HomeInventory website pages. The HTML pages retain their routes, App Store identity, and shared JSON-LD entity while changing visible primary branding and adding both historical aliases only to structured data. Search-platform submission happens only after the tested website commit is live.

**Tech Stack:** HTML5, JSON-LD, Python 3 standard library, `unittest`, GitHub Pages, Google Search Console, Bing Webmaster Tools.

## Global Constraints

- Repository is exactly `/Users/ly/Documents/MineTest/Privacy`; do not modify the HomeInventory iOS repository.
- Visible primary product name is exactly `Moving Boxes Organizer`.
- `HomeInventory` and `Box Inventory` remain only as structured-data aliases.
- App Store ID remains `6766885651` and App Store URL remains `https://apps.apple.com/us/app/moving-boxes-organizer/id6766885651`.
- Keep all five current canonical routes, both Sitemaps, screenshots, feature claims, policy URLs, and Support email unchanged.
- Do not create accounts, alter site ownership, add DNS records, or expose credentials during search-platform submission.

---

### Task 1: Enforce and Publish the Public Brand Contract

**Files:**
- Modify: `tests/test_validate_homeinventory_site.py`
- Modify: `scripts/validate-homeinventory-site.py`
- Modify: `HomeInventory_web/index.html`
- Modify: `HomeInventory_web/support/index.html`
- Modify: `HomeInventory_web/how-to-keep-track-of-moving-boxes/index.html`
- Modify: `HomeInventory_web/find-items-without-opening-boxes/index.html`
- Modify: `HomeInventory_web/qr-labels-for-storage-boxes/index.html`
- Create: `docs/superpowers/plans/2026-08-13-homeinventory-brand-indexing-p0.md`

**Interfaces:**
- `validate_brand_identity(root: pathlib.Path) -> list[str]` validates visible identity and the shared `SoftwareApplication` primary name/aliases.
- `validate_site(root)` includes `validate_brand_identity` in the release gate.

- [ ] **Step 1: Write failing brand-contract tests**

  Add behavior tests that reject a page whose visible copy uses `HomeInventory` as the product brand and reject a shared application entity without primary name `Moving Boxes Organizer` and aliases `HomeInventory`, `Box Inventory`.

- [ ] **Step 2: Verify RED**

  Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests/test_validate_homeinventory_site.py -v`

  Expected: FAIL because `validate_brand_identity` does not exist and the committed pages still expose the old visible brand.

- [ ] **Step 3: Implement the validator contract**

  Add `PRIMARY_PRODUCT_NAME`, `PRODUCT_ALIASES`, a JSON-LD application entity finder, and `validate_brand_identity`. Visible text must contain the primary name and must not contain `HomeInventory` or `Box Inventory`; JSON-LD must use the exact primary name and both aliases.

- [ ] **Step 4: Verify the remaining RED**

  Run the focused tests again. Validator behavior tests must pass; the committed-site test must still fail against existing page copy.

- [ ] **Step 5: Update all five pages**

  Replace visible old-brand references in titles, social metadata, navigation, body copy, alt text, labels, final calls to action, and footers. Keep `HomeInventory` and add `Box Inventory` only in each `SoftwareApplication.alternateName` list. Keep the shared `@id`, App Store URL, canonical, and Smart App Banner unchanged.

- [ ] **Step 6: Verify GREEN and visual behavior**

  Run:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate-homeinventory-site.py .
  git diff --check
  ```

  Render the homepage and Support page at `1440x1100` and `390x844`. Require document width to equal viewport width and visually inspect headings, navigation, buttons, and footers.

- [ ] **Step 7: Commit and publish**

  Stage only the plan, validator, tests, and five HTML pages. Commit in Chinese, push `main`, then verify each of the five live pages returns HTTP 200 and exposes the new visible primary identity.

### Task 2: Submit Existing Discovery Surfaces

**External surfaces:**
- Google Search Console
- Bing Webmaster Tools

**Inputs:**
- Root Sitemap: `https://ly-helloworld.github.io/Privacy/sitemap.xml`
- Product Sitemap: `https://ly-helloworld.github.io/Privacy/HomeInventory_web/sitemap.xml`
- Five canonical page URLs listed in the approved design.

- [ ] **Step 1: Verify public discovery inputs**

  Require HTTP 200 for `robots.txt`, both Sitemaps, and all five pages. Verify the root `robots.txt` references the root Sitemap and each Sitemap lists all five canonical URLs exactly once where applicable.

- [ ] **Step 2: Submit to Google Search Console**

  Use an existing authenticated and verified property. Submit the root Sitemap and use URL Inspection to request indexing for the homepage, Support page, and three guides. Record UI confirmation for each accepted request.

- [ ] **Step 3: Submit to Bing Webmaster Tools**

  Use the existing authenticated property or import the verified Google property. Submit the root Sitemap and the five canonical URLs. Record UI confirmation for each accepted request.

- [ ] **Step 4: Handle external blockers without expanding authority**

  If login, CAPTCHA, or unverified ownership blocks either platform, stop on that platform. Do not create an account, change ownership, add DNS records, or enter credentials. Report the exact UI state and the smallest user action required.

### Task 3: Final Verification and Handoff

- [ ] **Step 1: Re-run fresh website evidence**

  Run the full tests, static validator, `git diff --check`, live HTTP checks, and confirm website `HEAD` equals `origin/main`.

- [ ] **Step 2: Report indexing status accurately**

  Distinguish `submitted`, `pending`, `blocked`, and `indexed`. Do not equate a successful request with completed indexing or guaranteed recommendation lift.

- [ ] **Step 3: Preserve App repository state**

  Confirm no files or commits were created in `/Users/ly/Documents/MineTest/HomeInventory` during this implementation.
