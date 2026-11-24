# Fact change checklist

Use this checklist to update public facts in one pass.

Repo only. Never publish this file. Keep it outside the deploy workflow allowlist.

## Fact locations

- **Name: Rhett Dawson**
  - `index.html`: title tag, meta description, `og:title`, `og:description`, `og:site_name`, `twitter:title`, `twitter:description`, JSON-LD Person `name`, personal WebSite `name`, header wordmark, Introduction headshot `alt`, footer wordmark.
  - `404.html`: title tag, header wordmark, footer wordmark.
  - `humans.txt`: heading and Site owner line.
- **Job title: Consultant**
  - `index.html`: title tag, meta description, `og:title`, `og:description`, `twitter:title`, `twitter:description`, JSON-LD Person `jobTitle`, Introduction copy.
  - Keep Consultant until the Senior Consultant promotion takes effect in June 2027, per `BRIEF.md`. Update the title tag, meta and social titles, JSON-LD `jobTitle`, and Introduction copy together, along with the descriptions listed above.
- **Employer: Deloitte**
  - `index.html`: meta description, JSON-LD Person `worksFor.name`, Introduction copy, footer disclaimer referring to the employer.
  - `404.html`: footer disclaimer referring to the employer.
- **Location: Boston and Boston, Massachusetts**
  - `index.html`: title tag, meta description, `og:title`, `og:description`, `twitter:title`, `twitter:description`, JSON-LD Person `address.addressLocality`, Introduction copy, footer identity.
  - `404.html`: footer identity.
  - `humans.txt`: Location line.
- **Work focus: corporate real estate strategy and capital planning**
  - `index.html`: title tag, meta description, `og:description`, `twitter:description`, Introduction headline and copy, Elsewhere writing description.
- **Mechanical engineering background**
  - `index.html`: meta description, `og:description`, `twitter:description`, Introduction copy, Background copy.
- **Education: Northeastern, mechanical engineering and philosophy, rugby captain**
  - `index.html`: Background copy.
- **Prior work: industrial commissioning, naval propulsion overhaul, manufacturing research**
  - `index.html`: Background copy.
- **Outside work: tenor banjo, sailing, woodworking, Brazilian jiu-jitsu**
  - `index.html`: Outside work copy.
- **Boston Capital Strategy writing: capital planning and deferred maintenance**
  - `index.html`: Elsewhere description and link `https://bostoncapitalstrategy.com`, JSON-LD authored WebSite `@id`, `url`, `name`, and `author` reference.
- **LinkedIn: `https://www.linkedin.com/in/rhett-d-318785129/`**
  - `index.html`: Elsewhere link list `href`, JSON-LD Person `sameAs`.
- **X: `@RhettDawson`, `https://x.com/RhettDawson`**
  - `index.html`: Elsewhere link list label and `href`, JSON-LD Person `sameAs`.
- **Headshot: `assets/rhett-dawson-headshot-800.jpg` and `assets/rhett-dawson-headshot-400.jpg`**
  - `index.html`: Introduction image `src` and `srcset` with version queries, image `alt` text `Rhett Dawson`, `og:image`, `twitter:image`, JSON-LD Person `image`. The metadata and JSON-LD use `https://rhettd333.github.io/assets/rhett-dawson-headshot-800.jpg`.
- **Site URL: `https://rhettd333.github.io/` and related domain URLs**
  - `index.html`: canonical link, `og:url`, `og:image`, `twitter:image`, JSON-LD Person `@id`, `url`, and `image`, personal WebSite `@id`, `url`, and `publisher` reference, authored Boston Capital Strategy WebSite `author` reference.
  - `sitemap.xml`: `loc` if the site URL changes.
  - `robots.txt`: Sitemap line if the site URL changes.
  - `404.html`: root-relative navigation, home, asset, and stylesheet links depend on the site's root path.

## Make a change

1. Update `BRIEF.md` first if the brief changes.
2. Update every listed location for the fact.
3. Update `research-notes/factual-source-ledger.md` in the same commit.
4. Run `scripts/check-metadata.py`, `scripts/check-jsonld.py`, `scripts/check-canonical.py`, and `scripts/check-links.py`, or `scripts/verify-all.py`, as applicable.
5. Search the repo for stale copies of the old fact.
6. Verify the live site after deploy.
