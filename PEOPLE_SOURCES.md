# People biography sources

## Full biography migration — 10 October 2026

Re-read all 18 current-member source pages plus the individual pages for
Elizabeth Figueroa-Juarez and Eun Young Lee. `data/profile-details.json` now
retains 69 source narrative blocks and all 76 listed publication/patent records,
with original source-block text, source URLs and paragraph-by-paragraph Chinese
translations. These supersede the short summaries as the profile body; the
summaries remain directory and hero overviews. Bibliographic records stay in
English in both language versions. Original first-person voice is preserved.

Consistent sections: Research focus; Background and experience; Current research
interests; Key publications; Professional links. Only sections actually supplied
by each member are shown. Email and section-navigation links are provided.

Editorial decisions:

- Sergio: full research focus, full background, four numbered research interests,
  all five references, and `sr441@medschl.cam.ac.uk` retained.
- Katie and Martin: the source supplies a role/contact but no substantive bio.
  No biography or publication list has been invented.
- Nazuk: full three-paragraph biography retained. The source's `md215@cam.ac.uk`
  duplicates Martin's address; it is withheld pending confirmation.
- Cherub: email link corrected to match its visible source text,
  `kw619@cam.ac.uk`; the source href incorrectly pointed to `ztc22@cam.ac.uk`.
  The explicitly listed Gmail contact is also retained.
- Ruoqi: the owner's Research Associate correction still takes precedence over
  the old source's PhD-student heading. The background records the 2021 PhD start
  without inventing an end date. The truncated first-publication DOI is repaired
  to `10.21037/exrna-22-17`, checked against the publisher:
  https://exrna.amegroups.org/article/view/70128/html.
- Isabel: exactly repeated publication titles are deduplicated; source text is
  kept separately. No authors, dates or bibliographic values were guessed.
- Alumni biographies and contacts are explicitly historical. The other 18
  alumni only have directory records in the supplied source mapping; their
  existing information remains, without fabricated long biographies.
- Navigation, footer text, empty headings and the unrelated feedback widget on
  Cherub's source page are excluded from biography content.
- Explicit source URLs and checked professional links are retained; tracking
  wrappers are not copied. English citation wording is otherwise preserved,
  including incomplete references rather than invented missing information.

## Local member homepages — 10 October 2026

All 18 current members and 20 alumni now have static English and Chinese
homepages at `people/<name>.html` and `zh/people/<name>.html`. Directory portraits,
names and profile links open those local pages. Source URLs remain in the JSON
records for editorial reference. No new personal information was added.

`data/member-profiles.json` records the existing names, roles, portrait assets,
categories and stable slugs. Biographies come from `data/people-summaries.json`;
alumni content comes from `data/alumni.json`, retaining the historical-affiliation
qualification. Toni's existing longer academic biography remains accessible.

Rebuild with `python scripts/build_navigation.py` followed by
`python scripts/build_zh.py`; the latter also runs `scripts/build_profiles.py`.
For profile-data-only edits, run `python scripts/build_profiles.py` directly.
Alumni remain opt-in, and legacy directory anchors are preserved.

Validation: all 76 generated profile pages, local links and assets, fragment
targets, unique IDs, language counterparts, directory counts, menu order and
deterministic rebuild checked. Browser visual QA was unavailable in this session.

Reviewed 21 September 2026. Every linked individual page was opened and its displayed name and biography checked; copied URL slugs were not treated as identity evidence. Cards paraphrase research interests and background from those pages, in English and Chinese. The structured copy is in `data/people-summaries.json`; the translated pages are generated with `scripts/build_zh.py`.

## Limits and corrections

- Katie Fisher and Martin Dale have no substantive biography or research statement on their individual pages. Their cards give only the listed role; previously inferred duties and research specialisms have been removed.
- Ruoqi Du's old profile still calls her a PhD student. The site owner's explicit correction to Research Associate takes precedence. The old page supports her research interests and prior training.
- Sergio's old page contains different historical role descriptions. The existing website role is preserved; this summary update does not independently establish a new appointment.
- Some directory links point to the wrong person (for example the Iman name link points to Martin, while the Learn More link resolves correctly). Only pages whose visible names match the member were used.
- Contact details were not recopied: Nazuk's page repeats Martin's email, for example.
- Source descriptions were summarized without adding unpublished research from personal conversation history.

| Member ID | Checked individual profile |
| --- | --- |
| toni | [toni](https://www.tvplab-cambridge.com/tvp) |
| katie | [katie](https://www.tvplab-cambridge.com/kf) |
| mark | [mark](https://www.tvplab-cambridge.com/mc) |
| vanessa | [vanessa](https://www.tvplab-cambridge.com/vp) |
| sergio | [sergio](https://www.tvplab-cambridge.com/src) |
| sonia | [sonia](https://www.tvplab-cambridge.com/srf) |
| guillaume | [guillaume](https://www.tvplab-cambridge.com/gb) |
| ioannis | [ioannis](https://www.tvplab-cambridge.com/gk) |
| isabel | [isabel](https://www.tvplab-cambridge.com/copy-of-sonia) |
| hao | [hao](https://www.tvplab-cambridge.com/copy-of-sonia-1) |
| ruoqi | [ruoqi](https://www.tvplab-cambridge.com/copy-of-possawee-prasertsuk) |
| martin | [martin](https://www.tvplab-cambridge.com/md) |
| nazuk | [nazuk](https://www.tvplab-cambridge.com/copy-of-nazuk) |
| milidili | [milidili](https://www.tvplab-cambridge.com/copy-of-martin) |
| kaida | [kaida](https://www.tvplab-cambridge.com/copy-of-petra) |
| possawee | [possawee](https://www.tvplab-cambridge.com/copy-of-renata-risi) |
| iman | [iman](https://www.tvplab-cambridge.com/dea) |
| rodrigo | [rodrigo](https://www.tvplab-cambridge.com/copy-of-ruoqi-du) |


## Toni Vidal-Puig — author-provided CV correction (14 October 2026)

Authority: `CV - June 2025new.docx`, supplied by the user, dated June 2025.
The document is not published; public biographical content is transcribed and
translated into `data/profile-details.json`. Both academic and member biographies
now use this shared data (`scripts/build_toni.py` and `scripts/build_profiles.py`).

Corrections: Cambridge Senior Research Associate begins in 1999 (not 2000);
professorship begins October 2009. Other current appointments are not assigned
an unsupported 2009 start date. Removed the unsupported current Sanger PI claim
and stale 260-publication count. StemBAT funding is 2015–2020, not a 2020 award.
Metrics are explicitly historical: h-index 117, 48,563 citations (June 2025).
Expanded career history, education, international appointments, honours, research,
funding, service, teaching and mentoring; corrected the academic-page Scholar URL.

Source ambiguity: the CV's Education/Degrees section gives FRCP as 2008, while
Personal Fellowships and Awards gives 2007. Retain FRCP without a year pending
author clarification; do not silently choose either date. The CV groups multiple
current positions beneath October 2009–present, which is used only for the
explicitly dated Cambridge professorship. Historical training counts are dated.


## Mark Campbell — member-requested update (14 October 2026)

Title changed to Scientific Management Lead (科研管理负责人) across navigation, directory and profile sources. Three user-supplied references (Cell Reports 2023; Nature Metabolism 2022; FASEB Journal 2021) added at the top of Key publications in the requested order, retaining existing entries. Citations remain in English in both language versions; only spacing and punctuation were normalised.
