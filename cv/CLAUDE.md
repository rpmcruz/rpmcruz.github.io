# cv (gencv)

Turns a Ciência Vitae XML export into a webpage (HTML) and a LaTeX report. The webpage is `../index.html` (this folder lives inside the `rpmcruz.github.io` repo; it was copied from `cssgoncalves/gencv`, which is private).

## Updating the CV

1. The user exports the XML from Ciência Vitae into this folder (`3915-392E-21D4.xml`). It is committed exactly as exported (the user wants it untouched); `*.html`, `*.tex` and `browser-profile/` are gitignored.
2. Add an entry to `3915-392E-21D4.yaml` for every new output (gencv.py warns about outputs without one).
3. Run (opens a visible Chromium window; the user must press Scimago's "I am human" check, see below):
   ```
   nix-shell shell.nix --run "python3 gencv.py 3915-392E-21D4.xml"
   ```
   This writes `3915-392E-21D4.html` and `3915-392E-21D4.tex` next to the XML.
4. Publish: `cp 3915-392E-21D4.html ../index.html`, then commit and push (GitHub Pages, branch `master`).

## Files

- `gencv.py`: reads the XML and the YAML, adds `extra:*` elements (citations, impact-factor, sjr-rank, core-rank, venue, tags) to each output, adds `extra:updated` (the date of `downloaded` in the YAML) for the webpage footer, then applies both XSLTs. Preprints are removed first, from both HTML and LaTeX (the user does not want them): type P127, or a journal article whose journal is CoRR/arXiv/*Rxiv or whose DOI is arXiv's (ORCID imports arXiv papers as journal articles). Submissions under review are not preprints and stay.
- `scrap.py`: Crossref (citations), journal websites (IF), Scimago (SJR quartile, by journal ID), CORE portal (conference rank), RENATES (thesis URLs). New journals must be added to the ID dictionaries in `get_impact_factor` and `get_quartile`. The browser (Playwright Chromium, headed) keeps its cookies between runs in `browser-profile/`.
- `cienciavitae_to_html.xslt`: webpage. Header: name, links (only email and Google Scholar, per the user; Scholar URL built from the XML author identifier), biography (Ciência Vitae summary). Only papers (no supervisions), only outputs with a DOI. Sortable/filterable table with inline JS ported from `../mytable.js` (sort: Year, Citations, IF, SJR, CORE; dropdown filters: Type, Tags; clicking a tag filters by it). Footer: last update date and the source of each metric column; keep it in sync with `scrap.py` if a source changes.
- `cienciavitae_to_tex.xslt`: LaTeX report (includes supervisions and outputs without DOI).

## The YAML (`<xml name>.yaml`, next to the XML)

- No biography here: the webpage and the LaTeX report both use the Ciência Vitae summary (`resume:resume` in the XML). The user edits it in Ciência Vitae and re-exports; do not hard-code it in this repo.
- `notice:` text of the dashed box shown after the biography on the webpage (currently a call for thesis students); `{email}` becomes a link to the preferred email.
- `outputs:` keyed by DOI, or by title when there is no DOI (matching ignores case and punctuation).
  - `tags: [...]`
  - `hide: true` removes the output from both HTML and LaTeX (e.g. the erratum).
- Everything downloaded is stored at the end of the YAML (the user wants it there, not in a separate cache file), under one global timestamp:
  - `downloaded:` time of the last full download. If it is less than 30 days old (`MAX_AGE` in gencv.py), the stored values are used and nothing is downloaded, except for new papers or venues. Otherwise everything is downloaded again and the timestamp renewed; whatever fails to download or comes back n/a keeps its stored value. Delete it to force downloading.
  - `metrics:` `venue -> {impact-factor, sjr-rank, core-rank}` (journal name, or conference acronym for core-rank).
  - `papers:` `DOI -> {citations, venue, journal or conference}` from Crossref.
  - `theses:` RENATES thesis id -> URL.
- gencv.py rewrites the file with ruamel.yaml, which keeps the comments (it writes to memory first, so an error cannot empty the file).

## Tagging conventions (user preferences)

- Few tags, focused on methods. Every tag must be used by at least 2 papers shown on the webpage. The current vocabulary is listed in a comment at the top of the YAML; reuse it before inventing new tags.
- Applications only as broad areas: "medical images", "autonomous driving". No specific diseases, animals, datasets, etc.
- Tag from the abstract (OpenAlex/Crossref/Semantic Scholar APIs; Springer pages are bot-protected), not just the title. Mark entries tagged from the title only with a comment.

## Webpage style (user preferences)

Plain, old-school HTML with few CSS rules: monospace 18px, `#`/`##` heading markers, boxed table with light gray header, gray paper numbers, tags as small gray boxes. The user disliked a heavy black-and-white "blocky" design and the original brown/colored design. Type column shows only journal / conference.

## Gotchas

- The XML export is in Portuguese: use `output:output-type/@code`, never its text. Codes: P101 journal article, P122 conference paper, P103 book, P105 book chapter, P123 conference abstract, P124 conference poster, P127 preprint.
- The browser scrapers (IF of IEEE/Elsevier/MDPI/PeerJ journals, SJR) need a headed Chromium, hence a display. If the Claude session was started without `DISPLAY` (e.g. outside the desktop session), they fail ("launched a headed browser without having a XServer running") and gencv.py keeps the values stored in the YAML; setting `DISPLAY=:0` alone was not enough. Ask the user to run gencv.py from a terminal in their desktop session (`! ...` runs in the same display-less shell).
- Scimago is behind a Cloudflare "I am human" check: `get_scimago_table` waits 120 s for the user to press it in the Chromium window. Do not try to bypass it. After one failure, gencv.py stops trying that scraper for the run and keeps the stored values.
- Scimago's Cloudflare blocked the user (2026-11; it also blocks the Internet Archive's crawler) after the old scraper typed one journal URL after another (`journalsearch.php?q=<id>&tip=sid`) in a cookie-less browser. Now it browses like a person, with pauses: home page -> "Journal Rankings" -> "Download data" (a CSV with every journal: `Sourceid` -> `SJR Best Quartile`), so Scimago is visited once per refresh. The selectors were checked on archived 2024-2025 pages, but the flow was written while the user was blocked and is not yet tested on the live site. When testing offline, replace the scrapers with stubs so that no website is visited.
- The MDPI impact-factor scraper (Sensors, Mathematics) returns n/a; IEEE TAI also has no IF online.
- The live website (`../index.html`, git history) is a good source of past metric values.
