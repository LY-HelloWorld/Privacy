# BeadCraft Local Marketing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a small static marketing page at `https://ly-helloworld.github.io/Privacy/BeadCraftLocal_web/`.

**Architecture:** Add one self-contained HTML document and one copied app-icon asset in a dedicated `BeadCraftLocal_web` directory. Use the repository's shared landing-page stylesheet plus a small page-specific inline theme, with no runtime dependencies or build step.

**Tech Stack:** HTML5, CSS, Schema.org JSON-LD, GitHub Pages

## Global Constraints

- Keep existing files under `BeadCraftLocal/` unchanged.
- Do not add JavaScript, a backend, analytics, forms, frameworks, or dependencies.
- Use only claims supported by the current iOS app and legal pages.
- Make the page usable at mobile and desktop widths.

---

### Task 1: Marketing page contract test

**Files:**
- Create: `tests/test_beadcraftlocal_web.py`

**Interfaces:**
- Consumes: `BeadCraftLocal_web/index.html` and `BeadCraftLocal_web/assets/app-icon.png`
- Produces: a regression check for public metadata, navigation targets, core copy, and asset existence

- [ ] **Step 1: Write a failing unittest**

Create a Python unittest that loads the page, asserts the canonical URL, title, description, App Store link, privacy link, terms link, support email, JSON-LD application type, local-first copy, and app-icon asset.

- [ ] **Step 2: Run the test and verify failure**

Run: `python3 -m unittest tests.test_beadcraftlocal_web -v`

Expected: failure because `BeadCraftLocal_web/index.html` does not exist.

### Task 2: Static marketing page

**Files:**
- Create: `BeadCraftLocal_web/index.html`
- Create: `BeadCraftLocal_web/assets/app-icon.png`

**Interfaces:**
- Consumes: `../app-store-landing.css`, `../BeadCraftLocal/privacy.html`, `../BeadCraftLocal/terms.html`
- Produces: the public marketing route `/Privacy/BeadCraftLocal_web/`

- [ ] **Step 1: Copy the verified app icon**

Copy `BeadCraftLocal/Resources/Assets.xcassets/AppIcon.appiconset/beadcraft-app-icon.png` from the sibling iOS repository to `BeadCraftLocal_web/assets/app-icon.png`.

- [ ] **Step 2: Implement the HTML document**

Add semantic header, hero, benefit cards, workflow, local-first statement, footer, canonical/Open Graph metadata, and SoftwareApplication JSON-LD. Link legal destinations to `../BeadCraftLocal/` and email support to `luoyi9932@gmail.com`.

- [ ] **Step 3: Run the regression test**

Run: `python3 -m unittest tests.test_beadcraftlocal_web -v`

Expected: PASS.

- [ ] **Step 4: Check markup and repository diff**

Run: `python3 -m http.server 8765 --directory .` and request `/BeadCraftLocal_web/`, its icon, and both legal links; each must return HTTP 200. Run `git diff --check` and confirm no whitespace errors.

- [ ] **Step 5: Commit the implementation**

Commit only the new test, page, and icon with message `feat: add BeadCraft Local marketing page`.
