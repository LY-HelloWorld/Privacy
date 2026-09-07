# BeadCraft Local Marketing Page Design

## Goal

Create a small, publicly accessible marketing page for BeadCraft Local at:

`https://ly-helloworld.github.io/Privacy/BeadCraftLocal_web/`

The page will be suitable for the App Store Connect Marketing URL field and will leave the existing legal-document URLs unchanged.

## Scope

- Add a standalone static page at `BeadCraftLocal_web/index.html`.
- Reuse the app icon from the BeadCraft Local iOS repository.
- Present a concise English product introduction for an international App Store audience.
- Describe the verified core workflow: import an image, generate a bead pattern, review colors and quantities, track making progress, and export a PDF.
- State that image and project processing is local-first without claiming that no diagnostic data is collected.
- Link to the App Store listing, privacy policy, terms of use, and support email.
- Add responsive styling suitable for phone and desktop widths.
- Include basic title, description, canonical, Open Graph, and SoftwareApplication metadata.

## Visual Direction

Use a warm craft-table aesthetic with a restrained bead-grid motif, rounded surfaces, and colors derived from the app icon. The app icon is the primary visual asset; no generated imagery or extra screenshots are required for this first version.

## Architecture

The page remains plain static HTML and CSS within the existing GitHub Pages repository. It has no JavaScript, build step, backend, analytics, forms, or new dependency. Existing legal pages stay under `BeadCraftLocal/` and are referenced with stable relative links.

## Content Structure

1. Header with product name and legal links.
2. Hero with app icon, clear product promise, App Store action, and privacy reassurance.
3. Three concise benefit cards covering pattern generation, materials planning, and making/export.
4. A short three-step workflow.
5. Local-first privacy statement.
6. Footer with privacy, terms, and email support.

## Validation

- Confirm the page and all local assets resolve from a local HTTP server.
- Validate required links and metadata with a lightweight automated check.
- Confirm the layout has no obvious overflow at common mobile and desktop widths through responsive CSS rules.
- Verify the final public URL after the repository changes are published.

## Out of Scope

- Additional SEO question pages, localization, interactive tools, forms, analytics, or a CMS.
- Changes to the iOS application or its existing legal documents.
- App Store Connect metadata submission.
