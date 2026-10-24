#!/usr/bin/env python3
"""Audit canonical URLs; this is a repository tool only and never deployed."""

import json
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree


class CanonicalParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonicals = []
        self.og_urls = []
        self.json_ld = []
        self.script_parts = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonicals.append(attrs.get("href", ""))
        elif tag == "meta" and attrs.get("property", "").lower() == "og:url":
            self.og_urls.append(attrs.get("content", ""))
        elif tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self.script_parts = []

    def handle_data(self, data):
        if self.script_parts is not None:
            self.script_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.script_parts is not None:
            self.json_ld.append("".join(self.script_parts))
            self.script_parts = None


def nodes(value, node_type):
    """Find typed nodes in standalone JSON-LD, arrays, or @graph documents."""
    if isinstance(value, list):
        for item in value:
            yield from nodes(item, node_type)
    elif isinstance(value, dict):
        types = value.get("@type", [])
        if types == node_type or isinstance(types, list) and node_type in types:
            yield value
        yield from nodes(value.get("@graph", []), node_type)


def main():
    root = Path(__file__).resolve().parent.parent
    expected = ["https://rhettd333.github.io/"]
    page = CanonicalParser()
    person_urls = []
    website_urls = []
    sitemap_urls = []
    page_errors = []
    sitemap_errors = []
    try:
        page.feed((root / "index.html").read_text(encoding="utf-8"))
        page.close()
        for block in page.json_ld:
            document = json.loads(block)
            person_urls.extend(node.get("url") for node in nodes(document, "Person"))
            website_urls.extend(node.get("url") for node in nodes(document, "WebSite"))
    except (OSError, UnicodeError, ValueError) as exc:
        page_errors.append(str(exc))
    try:
        sitemap = ElementTree.parse(root / "sitemap.xml")
        sitemap_urls = [node.text or "" for node in sitemap.iter()
                        if node.tag.rsplit("}", 1)[-1] == "loc"]
    except (OSError, UnicodeError, ElementTree.ParseError) as exc:
        sitemap_errors.append(str(exc))

    checks = [
        ("Canonical link href", page.canonicals, page_errors),
        ("og:url content", page.og_urls, page_errors),
        ("JSON-LD Person url", person_urls, page_errors),
        ("JSON-LD WebSite url", website_urls, page_errors),
        ("Sitemap loc URLs", sitemap_urls, sitemap_errors),
    ]
    passed_count = 0
    for label, found, errors in checks:
        passed = found == expected and not errors
        passed_count += passed
        print(f"{'PASS' if passed else 'FAIL'}: {label}: {found!r}")
    for error in page_errors + sitemap_errors:
        print(f"Error: {error}")
    print(f"Summary: {passed_count}/{len(checks)} checks passed.")
    return 0 if passed_count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
