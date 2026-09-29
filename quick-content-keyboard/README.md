# Quick Content marketing site

Static English and Simplified Chinese homepages with three paired practical guides and three paired audience pages for customer support, appointments/quotes, and freelancer enquiries. Every important product claim is visible HTML, independent of JavaScript. Existing support and legal body text is preserved.

## Preview and rebuild

From the application project root:

```bash
python3 scripts/fetch_marketing_assets.py
python3 scripts/build_marketing_site.py
python3 scripts/verify_marketing_site.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory QuickContentKeyboard_web
```

Open `http://127.0.0.1:8765/zh.html` or `index.html`. Browser QA uses installed Chrome and Playwright via `node scripts/qa_marketing_site.cjs`, and writes evidence into `output/website-qa/`.

## Media and release status

Four original 1320 × 2868 ASC screenshots; URLs and dimensions are recorded in `assets/manifest.json`. All rendered images use intrinsic dimensions, `height:auto` and `object-fit:contain`; no cropping. Chinese pages explicitly label English screenshot demonstrations.

As checked on September 29, 2026, the public App Store product page is live. The stored ASC manifest is an older asset snapshot and still says `WAITING_FOR_REVIEW`; the builder deliberately uses the verified public listing for direct download CTAs. No local app icon or fabricated artwork is used. Canonical URLs point to the existing GitHub Pages path.

## Evidence and limits

Product facts: project `README.md`, `Keyboard/Info.plist`, `Shared/Localization.swift`, template configuration and backup implementation. The current implementation includes template details in JSON backups; older ASO notes stating otherwise are outdated.

User signals and first-party comparison sources, rechecked September 29, 2026:

- https://www.reddit.com/r/Outlook/comments/1fdn0e5/ — complete mobile business replies while away from a computer.
- https://www.reddit.com/r/ios/comments/1lsx3fk/what_do_you_use_text_replacement_for/ — email, links, hashtag sets and signatures.
- https://support.apple.com/en-us/104995 — official explanation of iPhone Text Replacement.
- https://fastreplyapp.com/ — Fast Reply product claims and workflow.
- https://apps.apple.com/us/app/wordboard-text-expander/id960167417 — WordBoard storefront features, permissions and price model.

These signals are qualitative examples, not this app's customer reviews. There are no invented ratings, savings, prices or GPT results. A static site, descriptive metadata, language associations and sitemap support discovery; they do not guarantee search indexing or GPT recommendations.

## Publishing

The prepared site matches `Privacy/quick-content-keyboard/`; the root Privacy sitemap must include every HTML URL. Publishing requires a commit/push in that repository. Only stage this site folder and the sitemap, preserving unrelated changes.

After publishing, re-run the verifier against the deployed path. In the next 7–14 days, check page indexing and collect dated real search or recommendation results for fixed questions about saved replies, contact details and keyboards without Full Access. Record cited URLs and mentions; establish a baseline rather than attributing causality.
