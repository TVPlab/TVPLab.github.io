# News migration — 21 September 2026

## Scope and provenance

- The original public blog sitemap (`https://www.tvplab-cambridge.com/blog-posts-sitemap.xml`) contains **45 post URLs**. All 45 are represented exactly once in `data/news.json` and on both news pages.
- Each record retains the original URL, structured publication timestamp, displayed publication date, title, photos and related links.
- The `why-learning-by-heart-is-important` URL actually serves **TVP Lab Christmas Party**, dated 11 December 2019. The content title is preserved; the misleading legacy slug is retained only as the stable record ID/source URL.
- Original displayed calendar dates are used for the archive. Several differ from the UTC timestamp by one day; this is intentional. Modification dates are not treated as new publications.
- Eight vague or lengthy archive headings have been clarified; their original headings are retained in `originalTitle`.
- Original English lab text is retained. Chinese entries provide edited summaries of the same stories. The CIPF–Cambridge 2021 entry paraphrases the externally syndicated Europa Press text rather than reproducing it. Original sources remain linked.
- The 2023 Monterrey post consists of an embedded seminar video, not a text article. Its original YouTube destination is retained, without inventing an abstract.
- Historical campaigns, positions and claims remain dated and carry an archive notice. No expired campaign is presented as a new appeal.

## Selected public LinkedIn updates

Eight individual public posts were read in full. Their exact publication dates were verified in the pages’ public `datePublished` metadata. URLs and timestamps are stored in each record. The complete recent-activity feed displayed a sign-in wall; this is a curated selection, not a claim of exhaustive LinkedIn coverage or an automatic live feed.

1. 19 September 2026: two CIPF PhD projects / FPU application preparation.
2. 12 September 2026: CIPF career exploration event, scheduled for 25 September, 16:30 Valencia local time.
3. 24 August 2026: EDC-MASLD / PFAS pilot-study publication.
4. 23 August 2026: BGI Tech spatial multi-omics seminar announced for 2 September, 14:00 at IMS.
5. 17 June 2026: CAMS/PUMC delegation visit and exploratory collaboration/training discussions. No signed agreement is claimed.
6. 28 May 2026: TecScience coverage of the 2026 International Obesity Research Congress.
7. 6 May 2026: invitation to give the fifth Mariano Gago Lecture, scheduled for 22 May.
8. 28 January 2026: Cambridge–Nanjing scientific network reflection.

Posts announcing events are described as announcements; attendance or successful completion is not invented. Event dates are separate from publication dates. The calendar file records the announced start only (16:30 Europe/Madrid = 14:30 UTC on 25 September); no end time has been assumed.

## Photos

64 unique photos/graphics from the original lab archive have been copied to `images/news/`, retaining their source URLs and dimensions in the data. Photos were resized to a maximum of 1200px and encoded as WebP without changing the image content.

LinkedIn image downloads returned HTTP 403. Relevant existing CIPF, Nanjing and adipocyte lab images are used with explicit archive captions, not represented as photos of the new events or figures from the new paper. Other new posts use the site’s decorative adipocyte icon. The unavailable source URLs remain in the provenance data. The seminar video thumbnail could not be downloaded; the video link is retained.

## Maintenance

- Edit `data/news.json` to add a sourced story, translation, original date and optional event date. Add local photos with their source URLs and dimensions.
- Run `python scripts/build_navigation.py` and `python scripts/build_zh.py`. The latter invokes `build_news.py`; homepage highlights are selected from the latest three publication dates.
- `build_news.py` creates both archive pages, both homepage news sections, and the small homepage translation map. No feed scraping occurs in visitors’ browsers.
- Search, topic/year filters, ordering, load-more and story deep links are progressive enhancements. All 53 stories remain available without JavaScript through native details elements.

## Cambridge visit — 22 September 2026 update
TVPlab supplied Toni’s invitation and two visit photographs (808.JPG, 816.JPG). Recap published 22 September; visit 15 September 2026 at 13:15 BST, IMS. No formal partnership agreement is claimed. LinkedIn publication dates and event display times now use Europe/London. CIPF calendar instant remains 14:30 UTC (15:30 BST); the location remains Valencia.
