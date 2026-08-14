# Photo Vault GPT Discovery Content Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen the independent English website's answer-engine discoverability for `Photo Vault: Secure Folder` without changing app behavior.

**Architecture:** Keep the existing static GitHub Pages structure. Use the landing page for canonical product identity, two focused static guides for backup/recovery and new-iPhone migration, and the existing support page as the FAQ hub. Cross-link all product pages and register the new URLs in both sitemap files.

**Tech Stack:** Static HTML, inline CSS/JSON-LD, XML sitemaps, GitHub Pages.

## Global Constraints

- Modify only `/Users/ly/Documents/MineTest/Privacy`.
- Use `Photo Vault: Secure Folder` as the canonical public product name.
- Keep all copy in English.
- Do not change mobile app source, pricing, analytics, privacy behavior, or App Store metadata.
- State only verified behavior: local vault content, no account requirement, no server-side vault sync, encrypted ZIP export/restore, and no forgotten-PIN recovery.
- Add HTML entry/core comments to new or materially updated pages where the page flow or security/backup decision is not self-evident.

---

### Task 1: Make the landing page the canonical product entity

**Files:**
- Modify: `Privacy-Vault_web/index.html`

**Interfaces:**
- Produces the canonical product name, explicit no-account/local-storage copy, and links to the focused guides for later tasks.

- [ ] **Step 1: Replace fragmented product naming**

Use `Photo Vault: Secure Folder` for the `<title>`, meta description, Open Graph fields, JSON-LD `name`, visible brand label, H1, image alt text, and footer label. Preserve `Privacy Vault` only as an optional historical alias in prose if needed.

- [ ] **Step 2: Strengthen the factual product summary**

Add visible English statements for no account, local vault content, no cloud vault/server sync, and user-controlled encrypted ZIP backup. Remove hedged wording such as `whenever the app design supports it`.

- [ ] **Step 3: Add guide and support navigation**

Link the landing page to Support, Backup and Restore, and Move to a New iPhone pages.

- [ ] **Step 4: Check the landing page locally**

Run `rg -n "Photo Vault: Secure Folder|No account|local|cloud|backup|support|new iPhone" Privacy-Vault_web/index.html` and confirm the canonical name, concrete privacy copy, and navigation targets are present.

### Task 2: Add the backup and restore guide

**Files:**
- Create: `Privacy-Vault_web/photo-vault-backup-restore/index.html`

**Interfaces:**
- Produces a crawlable English guide answering how to back up, restore, and avoid irreversible local data loss.

- [ ] **Step 1: Create page metadata and identity**

Add an HTML entry comment, English title/meta description, canonical URL, Open Graph fields, and Article JSON-LD. Include the App Store URL and exact product name.

- [ ] **Step 2: Write the backup workflow**

Document `Settings > Data Management > Export Backup`, encrypted ZIP output, user-controlled storage, and the requirement to test a small backup before deleting originals.

- [ ] **Step 3: Write the restore and failure FAQ**

Explain restore from ZIP, password requirement, no server-side recovery, forgotten PIN behavior, app deletion risk, and keeping a second copy on a Mac/PC or external drive.

- [ ] **Step 4: Add navigation**

Link to the App Store, landing page, Support, and the new-iPhone guide. Include privacy policy and terms in the footer.

### Task 3: Add the new-iPhone migration guide

**Files:**
- Create: `Privacy-Vault_web/photo-vault-new-iphone/index.html`

**Interfaces:**
- Produces a crawlable English guide answering how to move the vault to a new iPhone without claiming unsupported automatic cloud sync.

- [ ] **Step 1: Create page metadata and identity**

Add an HTML entry comment, English title/meta description, canonical URL, Open Graph fields, and Article JSON-LD with the exact product name and App Store link.

- [ ] **Step 2: Write the migration workflow**

Tell users to export and verify an encrypted ZIP on the old iPhone, move it through Files/iCloud Drive/Mac/PC under their control, install the app on the new iPhone, restore the ZIP, and verify representative photos, videos, and documents.

- [ ] **Step 3: State limits clearly**

Explain that local-only vault content does not automatically appear on a new device, that the app team cannot recover a forgotten PIN, and that users should not delete the old vault until restore verification succeeds.

- [ ] **Step 4: Add navigation**

Link to the backup guide, Support, landing page, App Store, privacy policy, and terms.

### Task 4: Connect support and sitemap discovery

**Files:**
- Modify: `Privacy_vault/support.html`
- Modify: `sitemap.xml`
- Modify: `core-sitemap.xml`

**Interfaces:**
- Makes the guides reachable from the existing support hub and from both sitemap entry points.

- [ ] **Step 1: Add support links**

Add a `Backup and Recovery Guides` section near the FAQ and link both new pages using their published GitHub Pages paths.

- [ ] **Step 2: Add exact sitemap URLs**

Add these URLs once to each sitemap with `<lastmod>2026-08-14</lastmod>`:

`https://ly-helloworld.github.io/Privacy/Privacy-Vault_web/photo-vault-backup-restore/`

`https://ly-helloworld.github.io/Privacy/Privacy-Vault_web/photo-vault-new-iphone/`

- [ ] **Step 3: Check sitemap uniqueness**

Run `rg -n "photo-vault-backup-restore|photo-vault-new-iphone" sitemap.xml core-sitemap.xml` and confirm each URL appears exactly once per sitemap.

### Task 5: Verify the static website changes

**Files:**
- Test: `Privacy-Vault_web/index.html`
- Test: `Privacy-Vault_web/photo-vault-backup-restore/index.html`
- Test: `Privacy-Vault_web/photo-vault-new-iphone/index.html`
- Test: `Privacy_vault/support.html`
- Test: `sitemap.xml`
- Test: `core-sitemap.xml`

**Interfaces:**
- Confirms static HTML, internal links, structured data, and sitemap entries are consistent before handoff.

- [ ] **Step 1: Run repository validators or focused static checks**

Use existing site validators if a Privacy Vault-specific validator exists; otherwise check required files, canonical URLs, structured data, and local link targets with read-only shell commands.

- [ ] **Step 2: Validate public URLs after deployment**

Run `curl -L -sS -o /dev/null -w '%{http_code} %{url_effective}\\n'` against the landing page and both new guides. Expect HTTP 200; if deployment has not happened, report live verification as pending.

- [ ] **Step 3: Review the diff and status**

Run `git diff --check`, `git status --short`, and `git diff --stat`. Confirm that no files under the mobile app repository are modified.
