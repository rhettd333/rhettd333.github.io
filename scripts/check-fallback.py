#!/usr/bin/env python3
"""Check the page's asset fallbacks without network access (never deployed)."""

from html.parser import HTMLParser
from pathlib import Path
import re


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
FRAGMENTS = (
    "I work on buildings and capital decisions.",
    "I am a consultant at Deloitte in Boston.",
    "My background is in mechanical engineering.",
    "I studied mechanical engineering and philosophy at Northeastern",
    "industrial commissioning, naval propulsion overhaul, and manufacturing research.",
    "Outside work, I play tenor banjo, sail, make things out of wood, and train Brazilian jiu-jitsu.",
    "I write about capital planning and deferred maintenance at Boston Capital Strategy.",
    "LinkedIn", "X / @RhettDawson", "Boston, Massachusetts",
    "Personal website. Views are my own and do not represent my employer.",
)
SECTIONS = ["introduction", "background", "outside-work", "elsewhere"]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.parts = []
        self.visible_parts = []
        self.sections = []
        self.headshots = []
        self.links = []
        self.body_tags = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        style = re.sub(r"\s+", "", attrs.get("style", "").lower())
        declarations = [part.split("!", 1)[0] for part in style.split(chr(59))]
        hidden = ("hidden" in attrs or any(value in declarations for value in
                  ("display:none", "visibility:hidden", "visibility:collapse", "opacity:0")))
        hidden = hidden or any(item[1] for item in self.stack)
        in_body = tag == "body" or any(item[0] == "body" for item in self.stack)
        if in_body and tag != "body":
            self.body_tags.append((tag, attrs))
            if tag == "section":
                self.sections.append((attrs.get("id"), hidden))
            if tag == "img" and "headshot" in attrs.get("src", ""):
                self.headshots.append((attrs, hidden))
            if tag == "a":
                self.links.append((attrs.get("href"), hidden))
        if tag not in VOID:
            self.stack.append((tag, hidden))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        if (any(tag == "body" for tag, _ in self.stack) and
                not any(tag in {"script", "style", "template"} for tag, _ in self.stack)):
            self.parts.append(data)
            if not any(hidden for _, hidden in self.stack):
                self.visible_parts.append(data)


def normalized(parts):
    return " ".join("".join(parts).split())


def main():
    root = Path(__file__).resolve().parent.parent
    page = PageParser()
    errors = []
    try:
        page.feed((root / "index.html").read_text(encoding="utf-8"))
        page.close()
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(str(exc))
    text = normalized(page.parts)
    visible = normalized(page.visible_parts)
    image = page.headshots[0][0] if len(page.headshots) == 1 else {}
    checks = [
        ("Raw HTML contains all key page text", all(item in text for item in FRAGMENTS)),
        ("Key text is not hidden by markup or inline style",
         all(item in visible for item in FRAGMENTS)),
        ("Four visible sections appear in semantic order",
         page.sections == [(section, False) for section in SECTIONS]),
        ("Skip link is the first body element and targets main",
         bool(page.body_tags) and page.body_tags[0][0] == "a" and
         page.body_tags[0][1].get("href") == "#main" and
         any(tag == "main" and attrs.get("id") == "main"
             for tag, attrs in page.body_tags)),
        ("Profile and writing links remain available",
         all((url, False) in page.links for url in (
             "https://bostoncapitalstrategy.com",
             "https://www.linkedin.com/in/rhett-d-318785129/",
             "https://x.com/RhettDawson"))),
        ("Headshot has visible non-empty alt text and positive dimensions",
         len(page.headshots) == 1 and not page.headshots[0][1] and
         bool(image.get("alt", "").strip()) and
         all(re.fullmatch(r"[1-9][0-9]*", image.get(attr, ""))
             for attr in ("width", "height"))),
    ]
    for label, passed in checks:
        print(f"{'PASS' if passed and not errors else 'FAIL'}: {label}")
    for error in errors:
        print(f"Error: {error}")
    count = sum(passed for _, passed in checks) if not errors else 0
    print("Raw HTML is complete and legible without the stylesheet." if count == len(checks)
          else "Raw HTML fallback needs attention.")
    print(f"Summary: {count}/{len(checks)} checks passed.")
    return 0 if count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
