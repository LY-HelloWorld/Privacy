# WorkProofCam GPT Discovery Website Design

## Objective

Improve the public web entity for **WorkProofCam: Photo Report** so search systems and ChatGPT Search can understand what the app does, connect the website to the App Store listing, and send qualified visitors to the download page.

This work changes only the shared `Privacy` static-site repository. It does not modify or release the iOS app.

## Confirmed identifiers

- App name: `WorkProofCam: Photo Report`
- App Store ID: `6775852372`
- App Store URL: `https://apps.apple.com/us/app/workproofcam-photo-report/id6775852372`
- Official web entry: `https://ly-helloworld.github.io/Privacy/workproofcam-web/`
- Public App Store seller: `雪梅 黄`
- Site owner label: `ly-helloworld App Pages`

The website will state the publisher relationship clearly instead of presenting these labels as unrelated entities.

## Selected approach

Use the existing static HTML and shared CSS architecture. Enhance the WorkProofCam landing page and add narrowly focused supporting pages. Do not introduce a framework, build step, backend, account system, or web payment flow.

This approach provides distinct crawlable answers for high-fit user intents while preserving the maintenance model used by the shared repository.

## Information architecture

### Existing page to upgrade

- `workproofcam-web/index.html`
  - Official product identity and App Store relationship
  - Primary contractor and field-service positioning
  - Timestamp, GPS, address, notes, before/after, local-first storage, and PDF export
  - Free download and verified one-time Pro purchase messaging
  - Links to all focused pages, sample report, support, privacy, terms, and App Store

### New intent pages

- `workproofcam-web/job-site-photo-report-app/index.html`
  - Answers searches for a job-site photo report app
  - Explains the capture-to-PDF workflow and best-fit users

- `workproofcam-web/before-after-work-proof/index.html`
  - Answers searches for before/after work evidence
  - Explains photo grouping, context, and client-ready reporting

- `workproofcam-web/photo-report-without-cloud/index.html`
  - Answers searches for private or local-first photo reporting
  - Explains what stays on-device and the current absence of required accounts or cloud sync

### New sample page

- `workproofcam-web/sample-photo-report/index.html`
  - Uses fictional, clearly labelled example data
  - Shows a representative report structure with before/after records, timestamp, address, and notes
  - Does not claim that the HTML page is an exact PDF exported by the app

### New support page

- `workproofcam/support.html`
  - Provides actual support contact information already verified in the repository
  - Covers common support topics and links to privacy, terms, the product website, and App Store
  - Becomes the intended future App Store Connect Support URL

## Page content rules

- Use direct, natural English written for solo contractors, installers, cleaners, maintenance providers, inspectors, and other field-service professionals.
- Do not describe team collaboration, cloud sync, automatic uploads, or features the current app does not provide.
- Do not claim guaranteed evidentiary validity, guaranteed GPT recommendation, ranking improvements, or download lift.
- Identify the app consistently by its full name and App Store ID.
- Use the public seller name only to clarify the official App Store relationship.
- Keep primary download calls to action visible near the top and bottom of each product page.
- Use local screenshots and icons already stored in the repository.

## Structured discovery signals

The main page will expose a `SoftwareApplication` JSON-LD entity with:

- A stable `@id`
- Exact product name and alternate name
- App Store ID
- iOS operating system and business application category
- Canonical website URL
- Exact App Store `downloadUrl` and `sameAs`
- Current verified version
- Publisher relationship
- Concise feature list
- Verified offer information only

Focused pages will reference the same application `@id` and add `WebPage` plus `BreadcrumbList` data. Visible FAQ sections may use `FAQPage` data only when the structured questions and answers exactly match the page.

Every new page will include:

- Unique title and meta description
- Canonical URL
- Index/follow robots directive
- Open Graph and Twitter metadata
- Internal breadcrumb and related-page links
- Descriptive local-image alternative text

## Shared navigation and sitemap changes

- Add WorkProofCam focused-page links to the product landing page.
- Keep the shared repository root focused on app-level entries; add only a concise WorkProofCam discovery entry if needed.
- Add all new canonical URLs to `core-sitemap.xml` and `sitemap.xml`.
- Update WorkProofCam `lastmod` values to the implementation date.
- Preserve the existing wildcard crawler access in `robots.txt` unless verification finds a concrete issue.

## Visual and responsive behavior

- Reuse and extend `app-store-landing.css` rather than duplicating page-level styles.
- Preserve the existing WorkProofCam field theme and card-based layout.
- Support desktop and mobile widths without horizontal overflow.
- Keep navigation, headings, calls to action, details/FAQ controls, and links keyboard accessible.
- Respect reduced-motion preferences; no animation is required for this scope.

## Download path and measurement

The website follows the existing web-to-App-Store pattern: public page → App Store listing → app install → in-app purchase if chosen.

The implementation will retain the verified App Store URL. App Store Connect campaign attribution will not be fabricated because the required provider/campaign values are not available in the repository. Campaign parameters can be added later when supplied from App Store Connect.

## Verification

Before commit and push:

1. Parse all changed HTML files and confirm required titles, canonical links, headings, and App Store links.
2. Parse every JSON-LD block as valid JSON.
3. Parse both sitemap files as valid XML and confirm each new canonical URL appears once.
4. Check all relative internal links and local assets for missing targets.
5. Serve the repository locally and inspect the landing, focused, sample, and support pages at desktop and mobile widths.
6. Confirm no files outside the WorkProofCam surfaces, shared landing CSS, shared root entry, and sitemaps changed.
7. Review the final Git diff, commit only the scoped files, push `main`, and verify the GitHub Pages URLs return successfully after deployment.

## Non-goals

- iOS code or App Store binary changes
- App Store name, subtitle, keywords, screenshots, Marketing URL, or Support URL submission
- Paid advertising, web checkout, subscriptions, sign-in, analytics SDKs, or deep-link infrastructure
- A general blog or large collection of thin SEO pages
- Claims about internal GPT ranking logic or guaranteed recommendations

## Success criteria

- The official website, App Store ID, app name, publisher, and download URL form one consistent public entity.
- Each confirmed high-fit intent has a dedicated, useful, indexable page.
- The support destination contains real contact information.
- All new pages are reachable through internal links and both sitemaps.
- The static site passes structural, link, JSON-LD, XML, responsive, and live deployment checks.
