# HomeInventory Intent Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Publish three evidence-bound English problem pages that explain how Moving Boxes Organizer by HomeInventory solves common moving-box and storage-box problems, while sending every visitor and crawler to the same App Store entity.

**Architecture:** Keep the site fully static and reuse `HomeInventory_web/styles.css`. Add one validation command that parses the homepage, three intent pages, local assets, JSON-LD, App Store links, screenshot dimensions, and both sitemaps; then use that contract to drive the HTML and CSS implementation.

**Tech Stack:** HTML5, CSS3, JSON-LD, XML Sitemap, Python 3 standard library, `unittest`, headless Google Chrome.

## Global Constraints

- The visible product name is `Moving Boxes Organizer by HomeInventory`.
- Every App Store destination is `https://apps.apple.com/us/app/moving-boxes-organizer/id6766885651` and every Smart App Banner uses `app-id=6766885651`.
- Visible copy is American English and leads with the user's problem and outcome.
- Visible copy does not mention Reddit, competitors, research sources, GPT, SEO, Schema, crawlers, rankings, or unsupported performance claims.
- Only current App Store 1.3.0 screenshots in `HomeInventory_web/assets/screenshots/` may be used.
- Screenshots preserve their intrinsic `1260:2736` aspect ratio with `width: 100%`, `height: auto`, and `object-fit: contain`; intent-page screenshots are not rotated.
- The pages do not claim that QR labels contain an inventory, that all private data automatically syncs to a cloud, or that an insurer accepts exports.
- No JavaScript framework or third-party runtime dependency is added.

---

### Task 1: Encode the Static-Site Contract

**Files:**
- Create: `scripts/validate-homeinventory-site.py`
- Create: `tests/test_validate_homeinventory_site.py`

**Interfaces:**
- Produces: `validate_site(root: pathlib.Path) -> list[str]`, used by the CLI and tests.
- Produces: a CLI command returning status `0` only when the entire HomeInventory site contract passes.

- [x] **Step 1: Write failing validator tests**

  Add tests that require exactly these public files and canonicals:

  ```python
  PAGE_SPECS = {
      "HomeInventory_web/index.html": "https://ly-helloworld.github.io/Privacy/HomeInventory_web/",
      "HomeInventory_web/how-to-keep-track-of-moving-boxes/index.html": "https://ly-helloworld.github.io/Privacy/HomeInventory_web/how-to-keep-track-of-moving-boxes/",
      "HomeInventory_web/find-items-without-opening-boxes/index.html": "https://ly-helloworld.github.io/Privacy/HomeInventory_web/find-items-without-opening-boxes/",
      "HomeInventory_web/qr-labels-for-storage-boxes/index.html": "https://ly-helloworld.github.io/Privacy/HomeInventory_web/qr-labels-for-storage-boxes/",
  }
  ```

  Assert one `h1`, required social metadata, exact canonical, valid JSON-LD, the shared `#app` entity, exact App Store URL, Smart App Banner ID, existing local links/assets, both sitemap memberships, and screenshot width/height attributes of `1260` and `2736`. Add mutation tests proving a missing page, wrong identity, and wrong screenshot dimensions are rejected.

- [x] **Step 2: Run tests and verify RED**

  Run: `python3 -m unittest tests/test_validate_homeinventory_site.py -v`

  Expected: FAIL because `scripts/validate-homeinventory-site.py` and the three required pages do not exist.

- [x] **Step 3: Implement the minimal validator**

  Use only Python standard-library parsers: `html.parser.HTMLParser`, `json`, `xml.etree.ElementTree`, `urllib.parse`, and `pathlib`. Keep public entry and non-obvious URL-resolution logic documented with intent comments.

- [x] **Step 4: Run tests and confirm the remaining RED is the missing site implementation**

  Run: `python3 -m unittest tests/test_validate_homeinventory_site.py -v`

  Expected: validator unit tests pass; committed-site contract fails only for missing or not-yet-updated HomeInventory pages and metadata.

### Task 2: Unify the Homepage Product Entity

**Files:**
- Modify: `HomeInventory_web/index.html`
- Modify: `HomeInventory_web/styles.css`

**Interfaces:**
- Consumes: the exact identity and link contract from Task 1.
- Produces: canonical `SoftwareApplication` entity `https://ly-helloworld.github.io/Privacy/HomeInventory_web/#app` for all intent pages to reference.

- [x] **Step 1: Update homepage metadata and JSON-LD**

  Set the application entity to:

  ```json
  {
    "@id": "https://ly-helloworld.github.io/Privacy/HomeInventory_web/#app",
    "@type": "SoftwareApplication",
    "name": "Moving Boxes Organizer",
    "alternateName": "HomeInventory",
    "identifier": "6766885651",
    "downloadUrl": "https://apps.apple.com/us/app/moving-boxes-organizer/id6766885651",
    "publisher": {"@type": "Person", "name": "雪梅 黄"}
  }
  ```

  Replace short App Store links, update the visible identity, and add a guide navigation block linking all three intent pages. Preserve the homepage's existing problem-first copy and six real screenshots.

- [x] **Step 2: Add shared guide styles**

  Add reusable `.guide-*`, `.related-guides`, `.fit-list`, and `.product-identity` rules to `styles.css`. Keep the existing global intrinsic-image rule and explicitly define intent screenshots with `width: 100%; height: auto; object-fit: contain; transform: none`.

- [x] **Step 3: Run the validator**

  Run: `python3 scripts/validate-homeinventory-site.py .`

  Expected: homepage identity errors disappear; missing intent-page and sitemap errors remain.

### Task 3: Build the Three Problem Pages

**Files:**
- Create: `HomeInventory_web/how-to-keep-track-of-moving-boxes/index.html`
- Create: `HomeInventory_web/find-items-without-opening-boxes/index.html`
- Create: `HomeInventory_web/qr-labels-for-storage-boxes/index.html`

**Interfaces:**
- Consumes: shared CSS and `#app` entity from Task 2.
- Produces: three independently indexable answers with reciprocal guide links and exact App Store handoff.

- [x] **Step 1: Create the moving-box tracking answer**

  Use the title `How to Keep Track of What Is Inside Moving Boxes`. Explain why memory, scattered notes, and room-only labels fail; give five concrete recording steps; show screenshots `02_record_box_in_seconds_1260x2736.png` and `06_unpack_what_matters_first_1260x2736.png`.

- [x] **Step 2: Create the item-finding answer**

  Use the title `How to Find an Item Without Opening Every Box`. Explain the gap between knowing an item was packed and knowing its exact box; give four search-and-locate steps; show screenshots `01_find_without_opening_1260x2736.png` and `03_print_stick_scan_1260x2736.png`.

- [x] **Step 3: Create the storage-label answer**

  Use the title `How to Label Storage Boxes So You Can Find Things Later`. Explain why small paper labels become incomplete or stale; give four readable-label and linked-record steps; show screenshots `03_print_stick_scan_1260x2736.png` and `02_record_box_in_seconds_1260x2736.png`.

- [x] **Step 4: Validate copy and markup**

  Run:

  ```bash
  python3 scripts/validate-homeinventory-site.py .
  rg -ni "reddit|competitor|research source|gpt|seo|schema|crawler|ranking|best app|downloads|save [0-9]+" HomeInventory_web/*/index.html
  ```

  Expected: validator reports only pending sitemap errors; forbidden-term scan returns no matches.

### Task 4: Publish Discovery Entries and Verify Rendering

**Files:**
- Modify: `sitemap.xml`
- Modify: `HomeInventory_web/sitemap.xml`

**Interfaces:**
- Consumes: four canonical page URLs from Tasks 2 and 3.
- Produces: root and product sitemaps with all four URLs and `lastmod` `2026-08-12`.

- [x] **Step 1: Update both sitemaps**

  Set homepage priority to `0.9` in the root sitemap and `1.0` in the product sitemap. Add each intent page with `changefreq` `monthly`, priority `0.8`, and no duplicate URL.

- [x] **Step 2: Run the complete automated suite**

  Run:

  ```bash
  python3 -m unittest tests/test_validate_homeinventory_site.py tests/test_validate_workproofcam_site.py -v
  python3 scripts/validate-homeinventory-site.py .
  git diff --check
  ```

  Expected: all tests pass, the validator prints `HomeInventory site validation passed.`, and Git reports no whitespace errors.

- [x] **Step 3: Render desktop and mobile pages**

  Start `python3 -m http.server 8765` at the repository root. Use headless Chrome to save each page at `1440x1100` and `390x844`. Inspect the eight renders for clipping, overflow, illegible navigation, wrong content order, or transformed screenshots.

- [x] **Step 4: Measure rendered screenshot ratios**

  In headless Chrome, read each intent screenshot's `naturalWidth`, `naturalHeight`, `getBoundingClientRect().width`, and `getBoundingClientRect().height`. Require `abs(rendered_width / rendered_height - 1260 / 2736) <= 0.001` for every screenshot at both viewport sizes.

- [x] **Step 5: Review, commit, and push**

  Review `git diff --stat`, `git diff`, and `git status`. Stage only the plan, validator/tests, HomeInventory pages/styles, and two sitemaps. Commit in Chinese with a scoped message, push `main` with `git push origin main`, then verify the four live URLs return HTTP 200.
