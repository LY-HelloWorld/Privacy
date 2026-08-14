# Photo Vault GPT Discovery Content Design

## Goal

Improve the public English evidence surface for the iOS app so ChatGPT and other answer engines can identify one consistent product and match it to user questions about local storage, no account, backup/recovery, and moving to a new iPhone.

## Scope

- Modify the independent marketing repository at `/Users/ly/Documents/MineTest/Privacy` only.
- Use `Photo Vault: Secure Folder` as the canonical public product name, matching the App Store listing.
- Keep `Privacy Vault` and `Pic Safe` only as historical aliases where clarification is useful.
- Update the existing landing page and support page.
- Add two focused English question pages:
  - `photo-vault-backup-restore/`
  - `photo-vault-new-iphone/`
- Update both existing sitemap files.
- Do not change the mobile app source code, privacy behavior, analytics, or pricing.

## Content requirements

The public pages must state plainly, and consistently:

- No account is required for the vault.
- Vault content is stored locally on the device.
- The app does not operate a cloud vault or sync vault media to its servers.
- Users can create and restore an encrypted ZIP backup under their control.
- Forgetting the main PIN cannot be recovered by the app team.
- Users should verify a backup before deleting originals or changing devices.
- Photos, videos, PDFs, documents, and ZIP files are supported where the current app supports them.
- Face ID/PIN, decoy PIN, and intruder capture claims must preserve the current Pro limitations.

## SEO and entity requirements

- Each page gets an English title, meta description, canonical URL, Open Graph title/description, and `SoftwareApplication` or `Article` JSON-LD appropriate to the page.
- The canonical product name and App Store URL/ID must be present on each page.
- The landing page links to Support, backup/restore, and new-iPhone pages.
- The support page links to the two focused pages.
- New pages are included in `sitemap.xml` and `core-sitemap.xml` with the 2026-08-14 last-modified date.
- Existing legal pages remain unchanged except for links if needed.

## Design decisions

### Canonical identity

The current public materials use `Hide Photos: Private Vault`, `Privacy Vault`, and `Pic Safe`, while the App Store uses `Photo Vault: Secure Folder`. This fragments entity resolution. All main headings, metadata, structured data, and navigation labels will use `Photo Vault: Secure Folder`.

### Page structure

The landing page remains the product overview. The backup/restore page answers disaster-recovery questions step by step. The new-iPhone page answers migration questions and points users back to the backup guide. The support page remains the operational FAQ and links to both guides.

### Truthfulness boundary

The copy will say vault media is local-only and that backups are user-exported encrypted ZIP files. It will not claim that the app is entirely offline, that every feature is free, or that forgotten PINs can be recovered. Existing analytics and App Store purchase processing remain covered by the privacy policy.

## Verification

- Check all new and changed pages contain the expected canonical URL, product name, App Store link, and visible English headings.
- Check all internal links resolve to files in the repository.
- Check both sitemap files contain the new URLs exactly once.
- Run the repository's existing validation tests if applicable and perform a live HTTP 200 check for the published GitHub Pages URLs after deployment.
