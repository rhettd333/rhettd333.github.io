"""Check asset versions. This repository tool is never deployed.

Local asset references carry ?v=1 initially, using a plain positive integer.
Anyone changing styles.css, a favicon or icon file, or a headshot file must
bump the token to the next integer on every local asset reference in the
same change.
"""

from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import parse_qs, urlsplit


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.assets = []
        self.og_images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        references = []
        if tag == "link":
            rel = attrs.get("rel", "").lower().split()
            if any(value in rel for value in ("stylesheet", "icon", "apple-touch-icon")):
                references.append(attrs.get("href", ""))
        elif tag == "img" and "headshot" in attrs.get("src", ""):
            references.append(attrs.get("src", ""))
            references.extend(entry.strip().split()[0]
                              for entry in attrs.get("srcset", "").split(",")
                              if entry.strip())
        elif tag == "meta" and attrs.get("property", "").lower() == "og:image":
            self.og_images.append(attrs.get("content", ""))
        for reference in references:
            url = urlsplit(reference)
            if not url.scheme and not url.netloc:
                self.assets.append(reference)


def main():
    root = Path(__file__).resolve().parent.parent
    checks = []
    references = []
    pages = {}
    for name in ("index.html", "404.html"):
        page = AssetParser()
        try:
            page.feed((root / name).read_text(encoding="utf-8"))
            page.close()
            passed = bool(page.assets)
        except (OSError, UnicodeError, ValueError):
            passed = False
        checks.append((f"{name} local asset references parsed", passed))
        pages[name] = page
        references.extend(page.assets)

    urls = [urlsplit(reference) for reference in references]
    versions = [parse_qs(url.query, keep_blank_values=True).get("v", []) for url in urls]
    checks.extend([
        ("Every local asset has a ?v= token",
         bool(urls) and all(url.query.startswith("v=") and len(tokens) == 1
                            for url, tokens in zip(urls, versions))),
        ("All version tokens are identical across both pages",
         bool(versions) and all(tokens == versions[0] for tokens in versions)),
        ("Every version token is a positive integer",
         bool(versions) and all(len(tokens) == 1 and
                                re.fullmatch(r"[0-9]+", tokens[0]) is not None and
                                int(tokens[0]) > 0 for tokens in versions)),
        ("Every referenced asset exists on disk",
         bool(urls) and all((root / url.path.lstrip("/")).is_file() for url in urls)),
        ("Absolute og:image URL has no query string",
         len(pages["index.html"].og_images) == 1 and
         all(urlsplit(value).scheme in ("http", "https") and
             bool(urlsplit(value).netloc) and "?" not in value
             for value in pages["index.html"].og_images)),
    ])
    passed_count = 0
    for label, passed in checks:
        passed_count += passed
        print(f"{'PASS' if passed else 'FAIL'}: {label}")
    print(f"Summary: {passed_count}/{len(checks)} checks passed.")
    return 0 if passed_count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
