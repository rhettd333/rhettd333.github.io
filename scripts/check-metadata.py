#!/usr/bin/env python3
"""Check identity metadata in the repository's index.html (never deployed)."""

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.in_body = False
        self.in_title = False
        self.script_parts = None
        self.titles = []
        self.meta = {}
        self.canonicals = []
        self.json_ld = []
        self.profile_links = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "head":
            self.in_head = True
        elif tag == "body":
            self.in_body = True
        if self.in_head:
            if tag == "title":
                self.in_title = True
                self.titles.append("")
            elif tag == "meta":
                key = (attrs.get("property") or attrs.get("name") or "").lower()
                self.meta.setdefault(key, []).append(attrs.get("content", ""))
            elif tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
                self.canonicals.append(attrs.get("href", ""))
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self.script_parts = []
        if self.in_body and tag == "a":
            href = attrs.get("href", "")
            try:
                host = (urlsplit(href).hostname or "").lower().removeprefix("www.")
            except ValueError:
                return
            if host in {"bostoncapitalstrategy.com", "linkedin.com", "x.com"}:
                self.profile_links.add(href)

    def handle_data(self, data):
        if self.in_title:
            self.titles[-1] += data
        if self.script_parts is not None:
            self.script_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        elif tag == "body":
            self.in_body = False
        elif tag == "title":
            self.in_title = False
        elif tag == "script" and self.script_parts is not None:
            self.json_ld.append("".join(self.script_parts))
            self.script_parts = None


def people(value):
    """Find Person nodes in standalone JSON-LD, arrays, or @graph documents."""
    if isinstance(value, list):
        for item in value:
            yield from people(item)
    elif isinstance(value, dict):
        types = value.get("@type", [])
        if types == "Person" or isinstance(types, list) and "Person" in types:
            yield value
        yield from people(value.get("@graph", []))


def main():
    page = MetadataParser()
    persons = []
    errors = []
    try:
        page.feed((Path(__file__).resolve().parent.parent / "index.html").read_text(encoding="utf-8"))
        page.close()
        for block in page.json_ld:
            persons.extend(people(json.loads(block)))
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(str(exc))

    person = persons[0] if len(persons) == 1 and not errors else {}
    name = "Rhett Dawson"
    same_as = person.get("sameAs")
    checks = [
        ("Title, og:title, and Person name carry Rhett Dawson",
         len(page.titles) == 1 and name in page.titles[0]
         and len(page.meta.get("og:title", [])) == 1
         and name in page.meta["og:title"][0]
         and name in str(person.get("name", ""))),
        ("Person jobTitle is exactly Consultant", person.get("jobTitle") == "Consultant"),
        ("Canonical link and og:url are identical",
         len(page.canonicals) == 1 and bool(page.canonicals[0])
         and page.canonicals == page.meta.get("og:url", [])),
        ("Person sameAs matches the three body profile URLs as sets",
         isinstance(same_as, list) and all(isinstance(url, str) for url in same_as)
         and len(page.profile_links) == 3 and set(same_as) == page.profile_links),
        ("Meta description exists and contains Rhett Dawson",
         len(page.meta.get("description", [])) == 1
         and name in page.meta["description"][0]),
    ]
    for label, passed in checks:
        print(f"{'PASS' if passed and not errors else 'FAIL'}: {label}")
    for error in errors:
        print(f"Error: {error}")
    passed_count = sum(passed for _, passed in checks) if not errors else 0
    print(f"Summary: {passed_count}/{len(checks)} checks passed.")
    return 0 if passed_count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
