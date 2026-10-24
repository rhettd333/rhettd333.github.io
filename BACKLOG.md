# Backlog: Rhett Dawson personal site

Scoring: Priority 1 to 10, Effort 1 to 10, Rank = (P x 10) - (E x 3). Lanes: Ready Autonomous, Ready Gated, Icebox, Done. Autonomous means technical, correctness, and discoverability work inside BRIEF.md. Gated means Rhett answers first: new public claims or copy about him, positioning, contact details, photos, spending money, or anything touching the other site. Cadence note: the career coach consultation (Oct 23, 2026) advised that a personal site does not earn daily work the way Boston Capital Strategy does. Cadence is weekly unless Rhett directs daily.

## Ready Autonomous

Seeded Oct 23, 2026 for the 10-cycle overnight run Rhett directed, from a ChatGPT ideation pass through the signed-in Codex channel (deduplicated against v1, which already carries the title, meta description, canonical, basic Person JSON-LD, sitemap, robots, and stable section ids from the raw list).

Round 2 seeding, Oct 23, 2026: 20 new items (A12 to A23, G7 to G14) from a second ChatGPT ideation pass through the signed-in Codex channel, deduplicated against everything Done or already queued. One raw gated idea (a Boston Capital Strategy backlink) duplicated G6 and was dropped, and one gated item (G14, analytics) was added by Muse to keep the batch at 20.

- A18 Portrait loading priority. The headshot carries the right loading hints (fetchpriority and decoding) so it arrives promptly without competing with essential resources. P6 E2 Rank 54.
- A21 Production response checks. Scripted check that deployed HTML, CSS, icons, and images return the expected content types and encoding. P6 E2 Rank 54.
- A19 Page weight budget. Set a transfer size budget for the published files and flag unexpected growth during weekly checks. P6 E3 Rank 51.
- A20 Versioned asset references. A versioning convention for stylesheet and image references so returning visitors reliably receive updated assets after a change. P5 E3 Rank 41.
- A3 Print stylesheet so the page prints as a clean one-page bio. P3 E2 Rank 24.

## Ready Gated

- G1 Confirm the applicable Deloitte requirements for both sites, including outside activities, publishing, independence, and any impression of a separate advisory business. Rhett handles this internally. P10 E3 Rank 71.
- G3 Buy rhettdawson.com when Rhett is ready (availability and price checked first), point it at this site, and update canonical, Open Graph, and sitemap URLs in the same change. On hold by owner directive Oct 23, 2026: no domain yet. P9 E4 Rank 78.
- G2 Approve the exact v1 biography copy, public links, and this draft MISSION.md. The v1 build ships as a draft under Rhett's build direction and this item records his word-level approval or edits. P9 E2 Rank 74.
- G7 Name-search introduction refinement. Rhett approves a concise opening that makes his name, Boston location, current role, and focus immediately clear. Copy change, so gated. P9 E2 Rank 74.
- G11 Search Console setup. Rhett approves ownership verification and sitemap submission so indexing and name-search visibility can be checked directly. Needs his account action. P8 E3 Rank 71.
- G8 Background specificity. Rhett approves one concrete detail about his engineering background that adds context without expanding employer claims. P7 E2 Rank 64.
- G9 Outside-work detail. Rhett approves one specific personal interest that gives new Boston contacts a natural conversation starter. P7 E2 Rank 64.
- G10 Elsewhere link descriptions. Rhett approves brief explanations distinguishing the Boston Capital Strategy writing from the LinkedIn professional record. P7 E2 Rank 64.
- G6 Add an author backlink on Boston Capital Strategy, "Written by Rhett Dawson", linking here, so ownership of the expert site is plain. P6 E3 Rank 51.
- G14 Privacy-respecting analytics. Rhett approves a lightweight, cookie-free analytics setup so name-search traffic is visible. Any vendor choice is his. P6 E3 Rank 51.
- G5 Add a short Now section saying what he is working on this season, refreshed by hand. Risk of going stale is the reason this is gated. P5 E4 Rank 38.
- G13 Personal visual identity. Rhett approves a restrained typography and color direction that makes the page feel recognizably his while preserving its simplicity. P5 E5 Rank 35.
- G12 Portrait retake. Rhett approves a replacement portrait with a clear brief for expression, framing, lighting, and background. Supersedes the studio backdrop version only if he prefers the retake. P5 E6 Rank 32.

## Icebox

- A personal blog or notes feed. Coach verdict: no. The writing lives on Boston Capital Strategy.
- A resume or CV download. Coach verdict: no. LinkedIn carries the record.
- Separate hobby pages for music, sailing, woodworking, or jiu-jitsu. Coach verdict: no inventory pages.
- A contact form or email publication on this site. LinkedIn is the contact route in v1.

## Done

- A14 Redirect verification. scripts/check-redirects.py added (repo only, verified 404 live). The HTTP address returns a single 301 to the HTTPS homepage and the chain ends at 200 in one hop, 3 of 3 pass. Commit 5476150. Deploy success, screenshots byte-identical to the verified headshot baseline. Oct 23, 2026.
- A15 Structured data validation. scripts/check-jsonld.py added (repo only, verified 404 live). JSON-LD parses, one Person and one WebSite node, unique ids, publisher matches the Person, and the Person image URL returns 200 live, 6 of 6 pass. Commit d91c7a9. Deploy success, screenshots byte-identical to the verified headshot baseline. Oct 23, 2026.
- A22 Search crawler rendering check. scripts/check-rendering.py added (repo only, verified 404 live). All eight key text fragments are present in the raw served HTML with no scripting, 8 of 8 pass. Commit 49e08a1. Deploy success, screenshots byte-identical to the verified headshot baseline. Oct 23, 2026.
- A17 Layout shift prevention. aspect-ratio 800 / 1060 added to the headshot image rule in styles.css, so the layout space is reserved in CSS as well as by the HTML dimensions. One-line diff, no visual change. Commit 433786a. Deploy success, live CSS serves the new rule, screenshots byte-identical to the verified headshot baseline. Oct 23, 2026.
- A12 Robots guardrails audit. scripts/check-robots.py added (repo only, verified 404 live). Robots permits crawling and references the sitemap, the sitemap is well formed and lists only the homepage, 4 of 4 pass. Commit 5edd857. Deploy success, screenshots byte-identical to the verified headshot baseline. Oct 23, 2026.
- A23 Weekly verification summary. scripts/verify-all.py added (repo only, verified 404 live). Runs the four check scripts and prints a dated report. Full run: metadata 5 of 5, links 4 PASS and 1 WARN, indexability 3 of 3, canonical 5 of 5, overall PASS. One earlier run caught a transient network read error and reported FAIL correctly before the rerun passed. Commit c109748. Deploy success, screenshots byte-identical to the verified headshot baseline. Oct 23, 2026.
- A13 Canonical URL audit. scripts/check-canonical.py added (repo only, verified 404 live). Canonical link, og:url, both JSON-LD urls, and the sitemap entry all agree on https://rhettd333.github.io/, 5 of 5 pass. Commit ca832be. Deploy success, screenshots byte-identical to the verified headshot baseline. Oct 23, 2026.
- A16 Indexability smoke test. scripts/check-indexability.py added (repo only, verified 404 live). First live run passes 3 of 3: final status 200, no meta robots noindex, no X-Robots-Tag header. Commit 601d590. Deploy success, screenshots byte-identical to the verified headshot baseline. Oct 23, 2026.
- G4 Headshot published. Photo supplied and approved by Rhett Oct 23, 2026, studio backdrop version prepared from his source photo. Headshot sits in the Introduction beside the intro copy on desktop and stacks on mobile, with srcset at 400 and 800 wide, explicit dimensions, and alt text "Rhett Dawson". og:image, twitter:image, and the JSON-LD Person image point at the 800 file. Commit bb375a8. Oct 23, 2026.
- A11 Sitemap freshness. lastmod 2026-10-23 added to the single sitemap URL, XML validated, and the live sitemap serves the new element. Commit e8064e4. Deploy success, screenshots clean. Oct 23, 2026.
- A10 humans.txt. humans.txt published with owner, location, and build facts only, linked from the head with rel author, and added to the deploy allowlist. Verified 200 live with the exact content. Commit 7f44780. Deploy success, screenshots clean. Oct 23, 2026.
- A1 Freshness and link check automation. scripts/check-links.py added (repo only, verified 404 live). First full run: Boston Capital Strategy 200, X 200, LinkedIn WARN 999 (bot protection, by design), both freshness checks pass (no Senior Consultant text, JSON-LD jobTitle Consultant), exit 0. Commit 112f23f. Deploy success, screenshots clean. Oct 23, 2026.
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
