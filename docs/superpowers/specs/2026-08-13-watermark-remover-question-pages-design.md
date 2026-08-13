# Watermark Remover Question Pages Design

## Objective

Add three English, question-focused static pages to the existing Watermark Remover: Eraser AI companion site. The pages should make verified product capabilities easier for Google and answer engines to retrieve while giving readers a useful answer before promoting the App Store download.

The pages live in the separate Privacy repository. The iOS application repository remains unchanged.

## Evidence boundary

The content is based on the evidence recorded in the WatermarkRemoverAI project on 2026-08-13:

- Google autocomplete returned exact iPhone-oriented expressions for removing text and date stamps, plus direct watermark-remover/iPhone task expressions.
- Reddit users asked whether iPhone photo cleanup can remove text cleanly and reported pixelated cleanup failures.
- Offline/privacy and subscription concerns are supporting pain points, not claims of quantified demand.

The pages must not claim search volume, universal popularity, guaranteed rankings, guaranteed GPT recommendations, perfect removal, unlimited free use, or that every task phrase is a verbatim user question.

## URL architecture

Create three directories beneath `watermark-remover-eraser-ai-web/`, each with an `index.html`:

1. `remove-text-from-photo-iphone/`
2. `remove-watermark-from-photo-iphone/`
3. `remove-date-stamp-from-photo-iphone/`

The existing companion page remains the product hub. It links to all three question pages, and every question page links to the hub and the other two pages.

## Page structure

Each page uses the existing shared `app-store-landing.css` and official assets already stored under `watermark-remover-eraser-ai-web/assets/`. No new framework, build step, downloaded icon, or duplicate screenshot set is introduced.

Every page contains:

1. A unique title, meta description, canonical URL, Open Graph data, and Smart App Banner.
2. A concise answer at the top, before the App Store call to action.
3. A step-by-step workflow that matches the released app.
4. A section explaining when results may need a tighter selection or another pass.
5. An on-device processing explanation that distinguishes core image processing from ancillary services such as App Store purchases and analytics. It must not claim that the app never uses a network connection.
6. Accurate free and Pro boundaries: standard export and one HD export are available free; Pro includes HD, batch processing up to 30 images, smart date removal, and supported video processing up to 60 seconds where relevant.
7. A visible statement limiting use to images the user owns or has permission to edit.
8. Question-specific FAQ content with `FAQPage` JSON-LD whose visible questions and answers exactly match the structured data.
9. `SoftwareApplication` JSON-LD identifying Watermark Remover: Eraser AI, iOS, and App Store track ID `6762575551` through the official download URL.
10. Links to the existing privacy policy, terms, content policy, support page, product hub, related question pages, and official App Store listing.

## Page-specific content

### Remove text from a photo on iPhone

This is the highest-priority page. It directly answers how to erase visible text embedded in image pixels. It distinguishes embedded text from editable text layers and metadata. Examples stay within authorized uses such as removing an outdated caption from the user's own graphic, cleaning a screenshot, or removing a label from a personal photo.

The limitations section addresses letters crossing faces, hair, repeated patterns, and sharp edges. It explains that smaller selections and multiple passes can reduce visible artifacts without promising a perfect result.

### Remove a watermark from a photo on iPhone

This page explains the brush-and-preview workflow for marks on images the user owns or is authorized to edit. It covers cropping as an alternative for simple corner marks and using removal when cropping would damage composition.

It explicitly rejects removing watermarks from unpaid photographer proofs, stock previews, school photos, or other content without permission. It does not use those misuse cases as examples or acquisition copy.

### Remove a date stamp from a photo on iPhone

This page distinguishes a visible date burned into image pixels from EXIF capture-date metadata. The app page addresses visible date-stamp cleanup only and does not imply that the workflow edits EXIF metadata.

It explains why corner dates on simple backgrounds are usually easier than dates crossing subjects or textured areas. Smart date removal is identified as a Pro feature without implying that all exports are paid.

## Navigation and discovery

Add a question-guide section to the existing product hub. Use descriptive anchor text matching each page's actual topic rather than generic “learn more” links.

Add `watermark-remover-eraser-ai-web/sitemap.xml` listing the hub and three question pages with absolute canonical URLs. If the repository-level sitemap is the active GitHub Pages sitemap, add these four URLs there as well without changing unrelated entries. Do not add speculative `lastmod` dates that cannot be maintained; use the implementation date only if the existing sitemap convention requires it.

## Visual design

Follow the existing Watermark Remover theme, typography, cards, spacing, and mobile breakpoints. Reuse App Store screenshots with `object-fit: contain`; do not crop or distort them. Each page should use only the screenshot most relevant to its task to keep the page focused and fast.

The primary visual hierarchy is: direct answer, steps, evidence-based caveats, product proof, FAQ, related guides, legal links. The App Store call to action remains visible but does not precede the direct answer.

## Quality and verification

Verification includes:

- Parse every changed HTML and XML file successfully.
- Confirm one unique canonical URL and one H1 per page.
- Confirm internal links resolve locally and external legal/App Store URLs match the existing site.
- Confirm visible FAQ questions and answers match FAQ JSON-LD.
- Confirm all images have dimensions or stable layout constraints and meaningful alt text.
- Check representative desktop and mobile rendering for overflow, overlap, screenshot cropping, and tap target usability.
- Inspect `git status` before staging and stage only files created or changed for this feature.

## Out of scope

- Changes to the iOS app or App Store metadata.
- Publishing unsupported claims or invented testimonials.
- New analytics, tracking, CMS, JavaScript framework, or server-side functionality.
- Dedicated pages for video, batch removal, logos, “without uploading,” or competitor comparisons.
- Automatic GitHub push unless separately authorized after local verification.
