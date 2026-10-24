# Build brief: Rhett Dawson personal site

Owner: Rhett Dawson. No custom domain yet (owner directive Oct 23, 2026: do not buy one yet). Live placeholder: https://rhettd333.github.io/ via GitHub Pages from this repo (rhettd333/rhettd333.github.io). When a domain is bought later, first choice per the career coach consultation is rhettdawson.com, subject to availability. Do not put Boston, consulting, or capital in the personal domain.

Task: a static one-page site. Plain HTML and CSS, no build step, no framework. Repo docs (BRIEF.md, MISSION.md, BACKLOG.md, README.md) are never published. The deploy workflow copies an allowlist of site files into dist and publishes that to GitHub Pages.

## What this site is

The personal site, distinct from Boston Capital Strategy (bostoncapitalstrategy.com):

- Boston Capital Strategy establishes what Rhett knows. It is narrow and institutional and carries the capital planning writing.
- This site establishes who stands behind that work. Its one job for the partner track is to make a warm introduction easier to advance. Someone searches his name and finds a credible person with a coherent background and a life outside consulting.

Positioning and content rules below come from a ChatGPT career coach consultation on Oct 23, 2026 (full text saved in the career goal files as chatgpt-personal-site-coach-2026-10-23.txt).

## Sections (v1: ONLY these four, one page, roughly 250 words)

Header stays as site furniture: plain text wordmark "Rhett Dawson" and nav reading Introduction, Background, Outside work, Elsewhere. No monogram, no slogan, no firm-style name.

1. Introduction. Headline: "I work on buildings and capital decisions." Then: "I am a consultant at Deloitte in Boston. My work is corporate real estate strategy and capital planning, helping large building owners decide what gets funded next. My background is in mechanical engineering." Use "Consultant" as the title until the Senior Consultant promotion actually takes effect in June 2027.
2. Background. "I studied mechanical engineering and philosophy at Northeastern and captained the men's rugby team. Before consulting I worked in industrial commissioning, naval propulsion overhaul, and manufacturing research."
3. Outside work. "Outside work, I play tenor banjo, sail, make things out of wood, and train Brazilian jiu-jitsu." Keep this short and human. Do not inventory every interest. Theater and guitar gear stay out of v1 (coach call: they can come up in conversation).
4. Elsewhere. "I write about capital planning and deferred maintenance at Boston Capital Strategy." One descriptive link to https://bostoncapitalstrategy.com. Below it, text links: LinkedIn (https://www.linkedin.com/in/rhett-d-318785129/), labeled "LinkedIn", the primary professional contact route, and X (https://x.com/RhettDawson), labeled "X / @RhettDawson". No embedded feed, no sales call to action.

Footer: "Personal website. Views are my own and do not represent my employer." Plus the wordmark and Boston, Massachusetts. Nothing else.

## Never publish (hard constraints, coach consultation Oct 23, 2026)

- Client names, logos, deliverables, project economics, internal methods, or recognizable anonymized engagement stories.
- A services menu, rates, a consultation booking path, a contact or lead form, or anything that reads as a competing advisory firm.
- Deloitte branding or language implying the firm sponsors this site or Boston Capital Strategy.
- Salary, promotion expectations, partner ambitions, performance reviews, or internal relationships.
- Home address, routines, relationship details, or identifiable information about other people.
- Workplace grievances or provocative professional commentary.
- The specific $2B program or $500M a year numbers. Those stay off this site entirely.

Open compliance item (backlog G1, Rhett handles internally): check the applicable Deloitte rules on outside activities, publishing, independence, and brand use for both sites. The footer disclaimer clarifies attribution. It is not a substitute for that check.

## Voice rules (hard constraints)

- Short, dry, plain sentences. Write the way a person talks, not the way a firm brochure talks.
- Zero em dash characters anywhere in visible copy. Zero semicolons anywhere in visible copy.
- No marketing superlatives, no "world class", no "passionate", no "leverage" as a verb, no "solutions", no "strategic leader", no "engineer turned storyteller".

## Design direction

- Quiet and editorial, related to Boston Capital Strategy but clearly personal. Warm paper background, near black text, one muted accent at most, thin rules between sections.
- Serif display type for the headline (Georgia or a system serif stack), plain sans for body. No web fonts, keep page weight small.
- No portrait in v1. A single natural portrait is a gated backlog item (G4) and needs a photo Rhett actually likes and owns the rights to. The small profile reference on file is too low resolution.
- Fully responsive. No horizontal overflow on mobile. Accessible markup: skip link, landmarks, focus styles, sufficient contrast.

## Technical foundation (v1)

- Title and meta description carrying the name: "Rhett Dawson | Consultant in Boston working on buildings and capital decisions" or close to it.
- Canonical and Open Graph URLs use https://rhettd333.github.io/ until a custom domain exists. Update them in the same commit that adds a domain.
- Person JSON-LD with name, jobTitle Consultant, worksFor Deloitte, address locality Boston, and sameAs links to LinkedIn, X, and Boston Capital Strategy.
- favicon.svg, robots.txt (allow all), sitemap.xml with the single page, a simple 404.html.
- Definition of done: page renders all four sections, copy audit finds no em dash and no semicolon in visible copy, and rendered screenshots at phone (390x844) and desktop (1280x900) have been read and look clean.
