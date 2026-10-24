# Backlog: Rhett Dawson personal site

Scoring: Priority 1 to 10, Effort 1 to 10, Rank = (P x 10) - (E x 3). Lanes: Ready Autonomous, Ready Gated, Icebox, Done. Autonomous means technical, correctness, and discoverability work inside BRIEF.md. Gated means Rhett answers first: new public claims or copy about him, positioning, contact details, photos, spending money, or anything touching the other site. Cadence note: the career coach consultation (Oct 23, 2026) advised that a personal site does not earn daily work the way Boston Capital Strategy does. Cadence is weekly unless Rhett directs daily.

## Ready Autonomous

Seeded Oct 23, 2026 for the 10-cycle overnight run Rhett directed, from a ChatGPT ideation pass through the signed-in Codex channel (deduplicated against v1, which already carries the title, meta description, canonical, basic Person JSON-LD, sitemap, robots, and stable section ids from the raw list).

- A1 Freshness and link check automation inside the weekly scrum. Add a repo script (never published) the scrum can run: checks every outbound link on the page for a live response and greps the page for stale title signals (for example the word Senior appearing before June 2027). P5 E2 Rank 44.
- A10 humans.txt. Add a small humans.txt utility file crediting the site owner and builder, linked from the head, and add it to the deploy workflow allowlist. Plain facts only, already public on the page. P4 E1 Rank 37.
- A11 Sitemap freshness. Add a lastmod date to the single sitemap URL and keep it current with each published change. P4 E1 Rank 37.
- A3 Print stylesheet so the page prints as a clean one-page bio. P3 E2 Rank 24.

## Ready Gated

- G1 Confirm the applicable Deloitte requirements for both sites, including outside activities, publishing, independence, and any impression of a separate advisory business. Rhett handles this internally. P10 E3 Rank 71.
- G3 Buy rhettdawson.com when Rhett is ready (availability and price checked first), point it at this site, and update canonical, Open Graph, and sitemap URLs in the same change. On hold by owner directive Oct 23, 2026: no domain yet. P9 E4 Rank 78.
- G2 Approve the exact v1 biography copy, public links, and this draft MISSION.md. The v1 build ships as a draft under Rhett's build direction and this item records his word-level approval or edits. P9 E2 Rank 74.
- G4 Add one natural portrait. Needs a photo Rhett likes, owns the rights to, and approves for publication. P7 E3 Rank 61.
- G6 Add an author backlink on Boston Capital Strategy, "Written by Rhett Dawson", linking here, so ownership of the expert site is plain. P6 E3 Rank 51.
- G5 Add a short Now section saying what he is working on this season, refreshed by hand. Risk of going stale is the reason this is gated. P5 E4 Rank 38.

## Icebox

- A personal blog or notes feed. Coach verdict: no. The writing lives on Boston Capital Strategy.
- A resume or CV download. Coach verdict: no. LinkedIn carries the record.
- Separate hobby pages for music, sailing, woodworking, or jiu-jitsu. Coach verdict: no inventory pages.
- A contact form or email publication on this site. LinkedIn is the contact route in v1.

## Done

- A9 404 alignment. 404.html now carries the full homepage head (theme-color and the PNG favicon set included), the same header with nav pointing at the homepage fragments, and the same footer. Root-relative paths throughout so it works at any depth, and a missing URL was screenshot-verified rendering correctly on desktop and mobile. Commit 8a4e9a2. Deploy success, homepage screenshots clean. Oct 23, 2026.
- A7 Favicon set completeness. favicon-32x32.png, icon-192x192.png, icon-512x512.png, and apple-touch-icon.png (180, opaque) generated with PIL in the favicon.svg design, referenced in the head, and added to the deploy allowlist. All four verified 200 live and the 512 icon visually matches the SVG. Commit 6f275af. Deploy success, screenshots clean. Oct 23, 2026.
- A2 Accessibility and performance pass. Contrast verified: ink 13.58 to 1 and accent 5.60 to 1 on paper, both pass WCAG AA, no color changes. Reduced motion media query added. Total published weight 8,716 bytes, no performance changes needed. Commit 4c9ec72. Deploy success, screenshots clean. Oct 23, 2026.
- A6 Structured data expansion. JSON-LD is now a graph: Person node with @id and url, plus a WebSite node naming the Person as publisher. Parses as JSON with both nodes, metadata check still 5 of 5. Commit 27089b7. Deploy success, screenshots clean. Oct 23, 2026.
- A5 Social preview completion. Twitter card tags, theme-color, and og:site_name added to the head, reusing the existing og text word for word. Commit e80e48f. Deploy success, live tags verified, metadata check still 5 of 5, screenshots clean. Oct 23, 2026.
- A8 Metadata consistency check. scripts/check-metadata.py added (repo only, verified 404 live). Five checks pass locally: name across title, og:title, and JSON-LD, jobTitle exactly Consultant, canonical equals og:url, sameAs matches the body profile links, meta description carries the name. Commit d5aca25. Deploy success, screenshots clean. Oct 23, 2026.
- A4 Identity verification links. rel="me" added to the Boston Capital Strategy, LinkedIn, and X links. Commit 62b803d. Live verified 200 with three rel="me" links, BRIEF.md 404, screenshots clean. Oct 23, 2026.
- D3 V1 built by Codex from BRIEF.md and audited by Muse. Four sections, Person JSON-LD, favicon, robots, sitemap, 404. Copy audit: zero em dashes and zero semicolons in visible copy. Rendered screenshots at 390x844 and 1280x900 read clean before the first push. Oct 23, 2026.
- D2 Career coach consultation on positioning, sections, links, and risks, via the signed-in Codex channel. Oct 23, 2026.
- D1 Repo scaffolded with BRIEF.md, MISSION.md (draft), BACKLOG.md, and a GitHub Pages deploy workflow using an allowlist dist build, matching the Boston Capital Strategy pattern. Oct 23, 2026.
