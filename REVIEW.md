# TVP Lab website refresh

A reviewable refresh of https://github.com/tvplab/tvplab.github.io, based on commit `17628dd8a9f78f011d759ea30cc64bdfdcc9aea9`.

## Current visual direction — reference update, 20 September 2026

The latest request restores the photographic hero and original homepage layout, and moves News & Events directly above Life at TVPlab. The homepage now reads: hero, introduction, research, news, lab gallery, footer.

The supplied reference inspires powder blue (`#C1CEE6`), espresso (`#402F20`) and warm ivory (`#F8F6EB`). These supersede the earlier colour choices below. The header and research section use powder blue; news and footer use espresso with ivory type; content and gallery use ivory. Original photographic colours are unchanged.

The hero returns to a full-width team photograph with a bottom-left caption and a dark gradient. Caption type is slightly smaller and lower than the first gallery version. The original mobile arrangement keeps the complete photograph above the caption. The TVPlab wordmark, bilingual pages, larger body type and swipeable galleries remain.

## Preview

Open `index.html` in a browser, or serve this folder with `python -m http.server 8000` and visit http://localhost:8000. No installation, build system or paid hosting is required.

## What changed

- Restored the homepage's links to the existing Research, People, Publications, News, Contact, About and Vacancies pages. The previous homepage contained separate placeholder copies of those pages.
- Kept the lab's photographs, logo and institutional logo strip; added compact WebP versions for normal page loads. Existing original images in the repository can stay unchanged.
- Added a consistent Cambridge blue and indigo layout with warm accents, a mobile menu, keyboard focus styles, a skip link and reduced-motion support.
- Kept old links such as `index.html#research`, `#people`, `#pi`, `#publications`, `#news` and `#contact` working by redirecting them to the existing HTML pages.
- Removed requests for absent team photographs. Members are displayed as readable name/role/biography entries until photographs are provided.
- Changed the nonfunctional contact form to an explicitly labelled email-draft workflow. It does not send, store or collect messages on a server. A configured email application is required; a direct email link is also present.
- Removed empty “Download JD” links, which did not point to any document.

## Existing content for the lab to verify

This is a presentation and navigation change, not an independent fact-check of the source repository. Existing people, publication and other content has been carried over. In particular:

1. `news.html`: confirm the six dated news items are real and correctly dated. The first three also appear on the homepage. The original source gives no supporting links for these stories.
2. `vacancies.html`: confirm that the advertised jobs/studentships, funding terms and “Open”/“Closing Soon” labels are accurate. No job-description files are present.
3. `about.html` and `antonio-vidal-puig.html`: resolve the conflicting PhD institution (Valencia in About, Granada in the PI page), and check appointments, awards and dates.
4. `people.html`: confirm current membership, roles and biographies. `images/team/` contains no portrait files in the source repository.
5. `publications.html`: check bibliographic formatting. For example, one 2015 entry uses “Proc Natl Acad Sci U S A” as its title and places the article title after the authors. Bibliometrics are copied from the old page and are not current live metrics.
6. Contact details and institutional/funder logos are preserved from the source and should be confirmed by the lab. The PI page uses `ajv22@medschl.cam.ac.uk`; Contact and Vacancies use `ajv22@cam.ac.uk`.
7. The original custom-domain site was inspected for image sources during the gallery update. This version preserves the selected Cambridge blue / indigo palette and current page structure; it is not a pixel-exact restoration of that older site.

## GitHub Pages deployment

The site is prepared for the existing `TVPlab/TVPLab.github.io` GitHub Pages deployment. Publish these static files to the repository root, preserving unrelated files and the existing Pages settings. No build step is required.

`refresh.css` contains the shared visual changes, `site.js` contains navigation and email-draft behavior, and page content remains directly editable in the HTML files. `styles.css` is included unchanged because the inner pages depend on it.

## Verification

All nine pages were checked in Chromium at 1440 px, 768 px and 390 px widths. Local navigation, image loading and horizontal overflow were checked. Mobile menu navigation, Escape-to-close, an old publication hash link, and email-draft preparation were exercised. These checks do not verify external sites, content accuracy, actual email delivery or every browser.

## Colour update — 20 September 2026

The palette follows the colour references supplied by Kaida. Layout and content are unchanged by this colour update.

| Colour | Hex | Use |
| --- | --- | --- |
| Cambridge Dark Blue | #133844 | Body text, main headings and hero tint |
| Cambridge Light Blue | #D1F9F1 | Research section and inner-page mastheads |
| Cambridge Blue | #8EE8D8 | Research tile hover state |
| Cambridge Warm Blue | #00BDB6 | Link underline accents |
| Light Indigo | #EBEDFB | Navigation, footer and PI highlight |
| Warm Indigo | #B0B9F1 | Soft borders and PI accent |
| Indigo | #5366E0 | Primary buttons and keyboard focus |
| Dark Indigo | #29347A | Navigation and links |
| Apricot | #F3BB8D | News rules and hero lab name |
| Pale peach | #FFF1E6 | News background and recruitment cards |
| Terracotta | #A44D2D | Warm labels, news links and navigation underline |

Bright mint and apricot are used as accents or backgrounds. Readable dark colours are used for text on pale surfaces.

## Bilingual and larger-type update

- English pages remain at the root. Complete Simplified Chinese pages are in `zh/`.
- Each of the nine page pairs has an EN / 中文 switch linking to its counterpart. Section anchors are preserved where JavaScript is available; both language versions and the basic switch work without JavaScript.
- Chinese navigation, research descriptions, people biographies, news, recruitment, contact labels, placeholders and email-draft status are translated. Personal names, original journal titles and formal bibliographic entries remain in English for accurate citation and discovery.
- Body text is generally 19–20 px, navigation is 17–18 px, with larger headings and buttons. The mobile menu now appears below 1201 px to accommodate the larger controls and language switch.
- `scripts/build_zh.py` contains the Chinese translations. After editing English content, update its translation entries and run `python scripts/build_zh.py`; generation reports uncovered narrative text. Generated Chinese HTML is checked in so GitHub Pages needs no build step.
- The colour palette remains Cambridge blue / indigo with warm apricot and terracotta accents.

### 本地查看

解压后打开 `index.html` 查看英文版，打开 `zh/index.html` 查看中文版。每页右上角均可切换语言。文件包中的所有目录需保持原有相对位置。

### Publishing

GitHub repository access is connected. Publication uses the existing main branch and GitHub Pages workflow. Prior source-content review notes still apply.

Bilingual verification: all 18 pages checked at desktop (1440 px) and mobile (390 px), with no document overflow, missing images or page script errors. Checked paired language links, preservation of research section anchors, Chinese mobile navigation, Chinese email-draft status and language switching with JavaScript disabled. All local links and assets across both languages resolved.


## Image galleries — 20 September 2026

- Kept the page order, selected palette, larger text and all nine bilingual page pairs.
- Added a large adipocyte microscopy image alongside a four-slide research carousel.
- Added three photographs in a swipeable lab gallery, with captions, arrow navigation and a click-to-enlarge lightbox. The lightbox supports previous/next, keyboard arrows, Escape, focus restoration and native modal focus trapping.
- Carousels use native horizontal scrolling and scroll snapping. They do not auto-play. Reduced-motion preferences disable animated arrow scrolling. Photo links and horizontal scrolling work without JavaScript.
- All photos are local optimized WebP files. No images or scripts are hotlinked. The reference Wix template inspired image placement only; its assets were not copied.
- To add a photograph, add a WebP in `images/`, duplicate a `.gallery-card` link in `index.html`, update its image, alt text and caption, add translations to `scripts/build_zh.py`, then regenerate the Chinese pages. JavaScript derives the slide count automatically.
- See `IMAGE_SOURCES.md` for source assets. Original research stock previews with watermarks were not used in this update.

Gallery verification: English and Chinese homepages checked at 1440, 768 and 390 px. Confirmed arrow navigation, first/last boundaries, counters, keyboard navigation, lightbox image loading, wraparound, Escape/close, modal focus and focus restoration. A simulated native touchscreen swipe moved the mobile photo track; reduced-motion scrolling and JavaScript-disabled scrolling/photo links also passed. All local links and assets resolved.
