# Moving Boxes Organizer Brand and Indexing P0 Design

## Goal

Improve entity consistency and discovery for App Store ID `6766885651` by making `Moving Boxes Organizer` the visible primary product name across the public website, then submitting the existing public URLs for search indexing.

## Repository Boundary

- Implementation repository: `/Users/ly/Documents/MineTest/Privacy`.
- The HomeInventory iOS repository is out of scope.
- No app binary, `Info.plist`, App Store metadata, screenshots, App ID, canonical URL, or public route changes are included.

## Brand Contract

The visible primary product name is exactly `Moving Boxes Organizer`.

Apply it consistently to:

- Header brand labels and accessible home labels.
- Page titles and social metadata where the current visible brand is `HomeInventory`.
- Product references in body copy, support copy, guide labels, screenshot alternative text, final calls to action, and footers.
- Breadcrumb labels and support-page structured data.

Keep `HomeInventory` and `Box Inventory` only as structured-data aliases on the shared `SoftwareApplication` entity. The primary JSON-LD `name` remains `Moving Boxes Organizer`; `alternateName` contains both historical aliases. Do not present `Moving Boxes Organizer by HomeInventory` as the main visible identity after this change.

## Pages In Scope

1. `https://ly-helloworld.github.io/Privacy/HomeInventory_web/`
2. `https://ly-helloworld.github.io/Privacy/HomeInventory_web/support/`
3. `https://ly-helloworld.github.io/Privacy/HomeInventory_web/how-to-keep-track-of-moving-boxes/`
4. `https://ly-helloworld.github.io/Privacy/HomeInventory_web/find-items-without-opening-boxes/`
5. `https://ly-helloworld.github.io/Privacy/HomeInventory_web/qr-labels-for-storage-boxes/`

The two existing discovery files remain:

- `https://ly-helloworld.github.io/Privacy/sitemap.xml`
- `https://ly-helloworld.github.io/Privacy/HomeInventory_web/sitemap.xml`

## Validation Design

Extend the static-site validator and its tests before changing page content. The public contract requires each in-scope page to:

- Show `Moving Boxes Organizer` as the visible product identity.
- Avoid visible standalone branding as `HomeInventory` or `Box Inventory`.
- Keep App Store ID `6766885651`, the exact App Store URL, canonical URL, and Smart App Banner.
- Reference the same shared application entity.
- Use `Moving Boxes Organizer` as the structured-data primary name and retain both historical aliases.

Run the full website test suite, static validator, whitespace checks, and desktop/mobile visual checks before publishing.

## Indexing Submission

After the website commit is pushed and live:

1. Submit the root Sitemap in Google Search Console.
2. Request indexing for the five in-scope URLs, prioritizing Support and the three guides.
3. In Bing Webmaster Tools, import the verified Google property when available; otherwise add the site through the existing account flow.
4. Submit the root Sitemap and the five URLs in Bing.

Search-platform actions may require an authenticated account and verified property. Do not create a new account, change ownership, add DNS records, or transmit credentials. If authentication or property verification blocks submission, stop at that boundary and report the exact missing prerequisite.

## Success Criteria

- All five live pages return HTTP 200 after publication.
- All five pages visibly use `Moving Boxes Organizer` as the primary product identity.
- Website tests and the static validator pass.
- Google and Bing submissions are confirmed by their respective UI, or the exact authentication/property blocker is recorded.
- Within 14 days, at least three of Support plus the three guide pages are discoverable by exact page-title search.

## Non-Goals

- Changing `CFBundleDisplayName` or shipping a new iOS version.
- Renaming the GitHub repository or `HomeInventory_web` route.
- Creating more content pages.
- Changing App Store title, subtitle, keywords, screenshots, pricing, or ratings strategy.
- Claiming guaranteed crawling, indexing, ranking, or GPT recommendation lift.
