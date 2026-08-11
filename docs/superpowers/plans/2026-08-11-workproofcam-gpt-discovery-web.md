# WorkProofCam GPT Discovery Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a consistent, crawlable WorkProofCam website entity with focused intent pages, a representative report example, real support contact information, and a verified App Store download path.

**Architecture:** Extend the existing GitHub Pages repository with static HTML pages and the shared `app-store-landing.css`. Each page owns one search intent, references the same `SoftwareApplication` entity, and connects through internal links and both existing sitemaps; a standard-library Python validator enforces the resulting contract.

**Tech Stack:** HTML5, CSS3, JSON-LD/Schema.org, XML sitemaps, Python 3 standard library, GitHub Pages.

## Global Constraints

- Modify only the shared `Privacy` repository; do not modify or release the iOS app.
- Preserve the existing static-site architecture and do not add a framework, package manager, build step, backend, account system, or web payment flow.
- Identify the product as `WorkProofCam: Photo Report`, App Store ID `6775852372`, and App Store URL `https://apps.apple.com/us/app/workproofcam-photo-report/id6775852372`.
- State the App Store publisher relationship clearly: published on the App Store by `雪梅 黄`, with public pages maintained under `ly-helloworld App Pages`.
- Do not claim team collaboration, cloud sync, automatic uploads, guaranteed evidentiary validity, guaranteed GPT recommendation, ranking lift, or download lift.
- Describe job records and photos as local-first while accurately disclosing Firebase Analytics and Crashlytics for technical usage and diagnostics.
- Use `luoyi9932@gmail.com` as the verified WorkProofCam support contact.
- Reuse existing local WorkProofCam icons and screenshots.
- Add entry-point and core-logic comments to new or modified code where the intent is not self-evident.
- Keep unrelated App pages unchanged.

---

### Task 1: Strengthen the canonical WorkProofCam entity and landing page

**Files:**
- Modify: `workproofcam-web/index.html`
- Modify: `app-store-landing.css`

**Interfaces:**
- Consumes: Existing local assets under `workproofcam-web/assets/` and shared landing-page CSS classes.
- Produces: Stable application entity ID `https://ly-helloworld.github.io/Privacy/workproofcam-web/#app`, canonical product summary, and reusable WorkProofCam content styles.

- [ ] **Step 1: Run the current landing contract and verify it fails**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

html = Path("workproofcam-web/index.html").read_text()
required = [
    '"@id": "https://ly-helloworld.github.io/Privacy/workproofcam-web/#app"',
    '"identifier": "6775852372"',
    '"softwareVersion": "1.1.3"',
    'Published on the App Store by 雪梅 黄',
    'Free download',
    'one-time purchase',
]
missing = [value for value in required if value not in html]
assert not missing, missing
PY
```

Expected: FAIL with the missing entity and positioning values.

- [ ] **Step 2: Replace the main page metadata and JSON-LD**

Update the document head to include:

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "@id": "https://ly-helloworld.github.io/Privacy/workproofcam-web/#app",
  "name": "WorkProofCam: Photo Report",
  "alternateName": "WorkProofCam",
  "identifier": "6775852372",
  "operatingSystem": "iOS",
  "applicationCategory": "BusinessApplication",
  "softwareVersion": "1.1.3",
  "url": "https://ly-helloworld.github.io/Privacy/workproofcam-web/",
  "downloadUrl": "https://apps.apple.com/us/app/workproofcam-photo-report/id6775852372",
  "sameAs": ["https://apps.apple.com/us/app/workproofcam-photo-report/id6775852372"],
  "publisher": {
    "@type": "Person",
    "name": "雪梅 黄"
  },
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD",
    "description": "Free download. Optional Pro upgrade is available as a one-time in-app purchase."
  }
}
```

Include a `featureList` covering timestamped photos, optional GPS/address context, notes, before/after organization, local-first job storage, and PDF report export. Keep the visible text consistent with those properties.

- [ ] **Step 3: Rewrite the visible product positioning**

Use these page-level messages:

```text
Eyebrow: Job-site photo reports for iPhone
Headline: Turn job-site photos into clear proof reports.
Lead: Capture timestamped before-and-after photos, keep every note tied to the right job, and export a client-ready PDF without a required account or cloud workflow.
Trust line: Official website for WorkProofCam: Photo Report · App Store ID 6775852372 · Published on the App Store by 雪梅 黄
Price line: Free download · Pro available as a one-time purchase · No subscription
Audience line: Built for solo contractors, installers, cleaners, maintenance providers, inspectors, and field-service professionals.
```

Retain the current screenshots, replace generic `field teams` language, disclose that Firebase is used for analytics/crash diagnostics but not job-content upload, and add a direct support link to the legal section.

- [ ] **Step 4: Extend the shared CSS for product proof sections**

Add scoped reusable classes for an identity line, outcome grid, workflow steps, related-page cards, report preview, support grid, breadcrumb, and bottom CTA. Keep the existing field theme and add explanatory comments at the first new shared block and at responsive layout boundaries.

- [ ] **Step 5: Re-run the landing contract and structural checks**

Run:

```bash
python3 - <<'PY'
import json
import re
from pathlib import Path

html = Path("workproofcam-web/index.html").read_text()
assert html.count('<h1') == 1
assert 'Published on the App Store by 雪梅 黄' in html
assert 'Free download' in html and 'one-time purchase' in html
blocks = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, re.S)
assert blocks
for block in blocks:
    json.loads(block)
PY
```

Expected: PASS.

- [ ] **Step 6: Commit the canonical landing improvement**

```bash
git add -- workproofcam-web/index.html app-store-landing.css
git commit -m "优化 WorkProofCam 官方落地页"
```

### Task 2: Add three focused discovery pages

**Files:**
- Create: `workproofcam-web/job-site-photo-report-app/index.html`
- Create: `workproofcam-web/before-after-work-proof/index.html`
- Create: `workproofcam-web/photo-report-without-cloud/index.html`
- Modify: `workproofcam-web/index.html`

**Interfaces:**
- Consumes: Shared app entity ID `https://ly-helloworld.github.io/Privacy/workproofcam-web/#app`, `../../app-store-landing.css`, and `../assets/` images from each new directory.
- Produces: Three canonical intent URLs linked from the main product page.

- [ ] **Step 1: Verify the intent pages are absent**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

paths = [
    Path("workproofcam-web/job-site-photo-report-app/index.html"),
    Path("workproofcam-web/before-after-work-proof/index.html"),
    Path("workproofcam-web/photo-report-without-cloud/index.html"),
]
assert all(path.exists() for path in paths), [str(path) for path in paths if not path.exists()]
PY
```

Expected: FAIL listing all three missing files.

- [ ] **Step 2: Create the job-site photo report page**

Use canonical URL `https://ly-helloworld.github.io/Privacy/workproofcam-web/job-site-photo-report-app/`, title `Job Site Photo Report App for iPhone | WorkProofCam`, and one visible H1: `Create a job-site photo report before you leave.`

The page must explain the job → capture → review → PDF workflow, identify best-fit users and poor-fit users, show a current local screenshot, link to the related before/after and local-first pages, and include top and bottom App Store calls to action.

- [ ] **Step 3: Create the before/after proof page**

Use canonical URL `https://ly-helloworld.github.io/Privacy/workproofcam-web/before-after-work-proof/`, title `Before and After Work Proof Photos | WorkProofCam`, and one visible H1: `Keep before-and-after work proof tied to the right job.`

Explain before, after, and general proof labels; job/client/site context; optional timestamp/location context; report review responsibility; and the absence of guaranteed legal or insurance validity.

- [ ] **Step 4: Create the local-first report page**

Use canonical URL `https://ly-helloworld.github.io/Privacy/workproofcam-web/photo-report-without-cloud/`, title `Photo Report App Without Required Cloud Sync | WorkProofCam`, and one visible H1: `Build photo reports without a required account or cloud sync.`

Explain that job records, photos, notes, and generated reports are designed to remain local; exports leave only when the user shares them; Firebase Analytics and Crashlytics may process technical usage and diagnostic data but not job records or proof-photo content.

- [ ] **Step 5: Add consistent structured data and breadcrumbs**

Each page must include one JSON-LD `@graph` containing a `WebPage`, a `BreadcrumbList`, and a reference to:

```json
{
  "@type": "SoftwareApplication",
  "@id": "https://ly-helloworld.github.io/Privacy/workproofcam-web/#app",
  "name": "WorkProofCam: Photo Report"
}
```

Add a visible breadcrumb back to the WorkProofCam main page. Add a `Related WorkProofCam guides` section linking all sibling intent pages.

- [ ] **Step 6: Link the new pages from the canonical landing page**

Add a `Choose the workflow you need` section to `workproofcam-web/index.html` with direct links and plain-language descriptions for all three canonical URLs.

- [ ] **Step 7: Validate the focused-page contract**

Run:

```bash
python3 - <<'PY'
import json
import re
from pathlib import Path

slugs = ["job-site-photo-report-app", "before-after-work-proof", "photo-report-without-cloud"]
main = Path("workproofcam-web/index.html").read_text()
for slug in slugs:
    path = Path("workproofcam-web") / slug / "index.html"
    html = path.read_text()
    assert html.count("<h1") == 1, slug
    assert f"/Privacy/workproofcam-web/{slug}/" in html, slug
    assert "https://ly-helloworld.github.io/Privacy/workproofcam-web/#app" in html, slug
    assert "id6775852372" in html, slug
    assert f"./{slug}/" in main, slug
    for block in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, re.S):
        json.loads(block)
PY
```

Expected: PASS.

- [ ] **Step 8: Commit the focused discovery pages**

```bash
git add -- workproofcam-web/index.html workproofcam-web/job-site-photo-report-app/index.html workproofcam-web/before-after-work-proof/index.html workproofcam-web/photo-report-without-cloud/index.html
git commit -m "新增 WorkProofCam 精准需求页面"
```

### Task 3: Add a representative report example and real support destination

**Files:**
- Create: `workproofcam-web/sample-photo-report/index.html`
- Create: `workproofcam/support.html`
- Modify: `workproofcam-web/index.html`
- Modify: `workproofcam-web/job-site-photo-report-app/index.html`
- Modify: `workproofcam-web/before-after-work-proof/index.html`
- Modify: `workproofcam-web/photo-report-without-cloud/index.html`

**Interfaces:**
- Consumes: Existing WorkProofCam legal documents, verified support email, shared landing CSS, and local screenshots.
- Produces: Crawlable example output and stable support URL `https://ly-helloworld.github.io/Privacy/workproofcam/support.html`.

- [ ] **Step 1: Verify the sample and support pages are absent**

Run:

```bash
test -f workproofcam-web/sample-photo-report/index.html && test -f workproofcam/support.html
```

Expected: FAIL.

- [ ] **Step 2: Create the representative sample report page**

Use canonical URL `https://ly-helloworld.github.io/Privacy/workproofcam-web/sample-photo-report/`, title `Sample Job Site Photo Report | WorkProofCam`, and H1 `See the structure of a clear job photo report.`

Use this explicitly fictional record:

```text
Example only — not a real customer job or an exact exported PDF
Job: Kitchen Sink Supply-Line Replacement
Client: Example Property Services
Site: 125 Example Street, Austin, TX
Before: 9:14 AM · Corroded supply line visible below sink
After: 10:02 AM · New supply line installed; area dried and checked
Technician note: Water restored. Connections visually checked after five minutes.
```

Show the structure as accessible HTML, explain which fields are optional, and link to the App Store and all three intent pages. Do not present the sample as legally verified evidence.

- [ ] **Step 3: Create the support page**

Use a standalone legal-document style consistent with `workproofcam/privacy.html`. Add an entry comment explaining that the page is the public support destination. Include:

```text
Support email: luoyi9932@gmail.com
App: WorkProofCam: Photo Report
App Store ID: 6775852372
Common topics: camera permission, location permission, local job records, PDF export, Pro purchase restore, privacy and diagnostics
```

Link to the product landing page, App Store listing, privacy policy, terms, and content policy. For purchase support, direct users to Apple purchase history/refund support without promising developer-side billing changes.

- [ ] **Step 4: Add sample and support links across WorkProofCam pages**

Add `Sample report` and `Support` links to the main header/footer and focused-page related links. Use the same canonical destinations everywhere.

- [ ] **Step 5: Validate support and sample accuracy**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

sample = Path("workproofcam-web/sample-photo-report/index.html").read_text()
support = Path("workproofcam/support.html").read_text()
assert "Example only" in sample
assert "not a real customer job" in sample
assert "exact exported PDF" in sample
assert "luoyi9932@gmail.com" in support
assert "6775852372" in support
for path in ["privacy.html", "terms.html", "content.html"]:
    assert path in support
PY
```

Expected: PASS.

- [ ] **Step 6: Commit the sample and support destinations**

```bash
git add -- workproofcam-web workproofcam/support.html
git commit -m "补充 WorkProofCam 示例报告和支持页"
```

### Task 4: Connect the discovery graph through sitemaps and the shared hub

**Files:**
- Modify: `index.html`
- Modify: `core-sitemap.xml`
- Modify: `sitemap.xml`

**Interfaces:**
- Consumes: Five new WorkProofCam canonical URLs.
- Produces: Root-hub crawl path and sitemap discovery for every WorkProofCam page.

- [ ] **Step 1: Run the sitemap contract and verify it fails**

Run:

```bash
python3 - <<'PY'
import xml.etree.ElementTree as ET

urls = [
    "https://ly-helloworld.github.io/Privacy/workproofcam-web/job-site-photo-report-app/",
    "https://ly-helloworld.github.io/Privacy/workproofcam-web/before-after-work-proof/",
    "https://ly-helloworld.github.io/Privacy/workproofcam-web/photo-report-without-cloud/",
    "https://ly-helloworld.github.io/Privacy/workproofcam-web/sample-photo-report/",
    "https://ly-helloworld.github.io/Privacy/workproofcam/support.html",
]
for sitemap in ["core-sitemap.xml", "sitemap.xml"]:
    root = ET.parse(sitemap).getroot()
    values = [node.text for node in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    assert all(value in values for value in urls), (sitemap, [value for value in urls if value not in values])
PY
```

Expected: FAIL listing the missing URLs.

- [ ] **Step 2: Update both sitemap files**

Add each new canonical URL exactly once, use `<lastmod>2026-08-11</lastmod>`, use weekly change frequency for the four product content pages, monthly change frequency for support, and keep existing non-WorkProofCam entries unchanged. Update the existing WorkProofCam landing-page `lastmod` to `2026-08-11`.

- [ ] **Step 3: Extend the existing WorkProofCam root-hub card**

Keep the current WorkProofCam app-level card and add a compact list containing `Product page`, `Sample report`, and `Support`. Do not add separate root-level cards for each intent page.

- [ ] **Step 4: Re-run XML and root-link validation**

Run the Step 1 command again, then run:

```bash
python3 - <<'PY'
from pathlib import Path

html = Path("index.html").read_text()
assert "workproofcam-web/sample-photo-report/" in html
assert "workproofcam/support.html" in html
PY
```

Expected: PASS.

- [ ] **Step 5: Commit the crawl-path updates**

```bash
git add -- index.html core-sitemap.xml sitemap.xml
git commit -m "完善 WorkProofCam 站点收录入口"
```

### Task 5: Add a permanent static-site validator

**Files:**
- Create: `scripts/validate-workproofcam-site.py`
- Create: `tests/test_validate_workproofcam_site.py`

**Interfaces:**
- Consumes: Repository root path and the committed WorkProofCam HTML/XML contract.
- Produces: `validate_site(root: pathlib.Path) -> list[str]` and a command-line exit status of zero only when no errors are found.

- [ ] **Step 1: Write the failing validator tests**

Create `tests/test_validate_workproofcam_site.py` using `unittest`. It must load the validator module by file path and contain:

```python
def test_committed_site_is_valid(self):
    self.assertEqual([], validator.validate_site(ROOT))

def test_missing_required_page_is_reported(self):
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        errors = validator.validate_required_pages(root)
    self.assertTrue(any("workproofcam-web/index.html" in error for error in errors))
```

- [ ] **Step 2: Run the tests and verify they fail**

Run:

```bash
python3 -m unittest tests/test_validate_workproofcam_site.py -v
```

Expected: FAIL because `scripts/validate-workproofcam-site.py` does not exist.

- [ ] **Step 3: Implement the validator**

Create `scripts/validate-workproofcam-site.py` with:

```python
REQUIRED_PAGES = (
    "workproofcam-web/index.html",
    "workproofcam-web/job-site-photo-report-app/index.html",
    "workproofcam-web/before-after-work-proof/index.html",
    "workproofcam-web/photo-report-without-cloud/index.html",
    "workproofcam-web/sample-photo-report/index.html",
    "workproofcam/support.html",
)


def validate_required_pages(root: Path) -> list[str]:
    return [f"Missing required page: {relative}" for relative in REQUIRED_PAGES if not (root / relative).is_file()]


def validate_site(root: Path) -> list[str]:
    errors: list[str] = []
    for validator_function in (
        validate_required_pages,
        validate_html_pages,
        validate_sitemaps,
        validate_internal_targets,
    ):
        errors.extend(validator_function(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the WorkProofCam static-site contract.")
    parser.add_argument("root", nargs="?", default=".")
    errors = validate_site(Path(parser.parse_args().root).resolve())
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("WorkProofCam site validation passed.")
    return 0
```

Implement `validate_html_pages` by parsing every file in `REQUIRED_PAGES`, counting H1 start tags, collecting canonical links, loading every `application/ld+json` block with `json.loads`, and checking the exact canonical URL and App Store ID from the page specification. Implement `validate_sitemaps` by parsing both sitemap files with `ElementTree`, rejecting duplicate `<loc>` values, and requiring all six WorkProofCam canonical URLs. Implement `validate_internal_targets` by resolving relative links against the current HTML file and `https://ly-helloworld.github.io/Privacy/` links against the repository root, ignoring fragments, `mailto:`, and external hosts. Use only `argparse`, `html.parser`, `json`, `pathlib`, `re`, `sys`, `urllib.parse`, and `xml.etree.ElementTree`. Add an entry comment above `main` and comments explaining JSON-LD extraction and URL-to-file conversion.

- [ ] **Step 4: Run unit and CLI validation**

Run:

```bash
python3 -m unittest tests/test_validate_workproofcam_site.py -v
python3 scripts/validate-workproofcam-site.py .
```

Expected: all tests PASS and CLI prints `WorkProofCam site validation passed.`

- [ ] **Step 5: Commit the validator**

```bash
git add -- scripts/validate-workproofcam-site.py tests/test_validate_workproofcam_site.py
git commit -m "增加 WorkProofCam 静态站验证"
```

### Task 6: Perform visual QA, final review, push, and live verification

**Files:**
- Verify only; modify scoped files only if validation finds a defect.

**Interfaces:**
- Consumes: Completed static pages and validator.
- Produces: Pushed `main` branch and live GitHub Pages verification evidence.

- [ ] **Step 1: Run the full structural verification**

```bash
git diff --check origin/main..HEAD
python3 -m unittest tests/test_validate_workproofcam_site.py -v
python3 scripts/validate-workproofcam-site.py .
```

Expected: no whitespace errors, all tests PASS, validator PASS.

- [ ] **Step 2: Serve the site locally**

Run from the repository root:

```bash
python3 -m http.server 8765
```

Open and inspect these URLs at 1440×1000 and 390×844:

```text
http://127.0.0.1:8765/workproofcam-web/
http://127.0.0.1:8765/workproofcam-web/job-site-photo-report-app/
http://127.0.0.1:8765/workproofcam-web/before-after-work-proof/
http://127.0.0.1:8765/workproofcam-web/photo-report-without-cloud/
http://127.0.0.1:8765/workproofcam-web/sample-photo-report/
http://127.0.0.1:8765/workproofcam/support.html
```

Confirm no horizontal overflow, readable text, visible primary CTA, working header/footer navigation, loaded images, and a clear example-data disclaimer.

- [ ] **Step 3: Review the exact push scope**

```bash
git status --short --branch
git diff --stat origin/main..HEAD
git log --oneline origin/main..HEAD
```

Expected: only the approved design/plan, WorkProofCam pages, shared landing CSS, shared hub, two sitemaps, and validator/test files differ from `origin/main`.

- [ ] **Step 4: Push the unified repository**

```bash
git push origin main
```

Expected: the remote `main` advances to the local HEAD.

- [ ] **Step 5: Verify GitHub Pages deployment**

After deployment, request each canonical URL and confirm HTTP 200, the expected H1, the App Store ID, and the canonical link. Re-run the same checks for `core-sitemap.xml` and `sitemap.xml`, and report any Pages delay as deployment pending rather than claiming completion.
