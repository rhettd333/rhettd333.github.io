#!/usr/bin/env python3
"""Validate structured data; this is a repository tool only and never deployed."""

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


class JsonLdParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = None
        self.blocks = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            media_type = dict(attrs).get("type") or ""
            if media_type.strip().lower() == "application/ld+json":
                self.parts = []

    def handle_data(self, data):
        if self.parts is not None:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.parts is not None:
            self.blocks.append("".join(self.parts))
            self.parts = None


def has_type(node, expected):
    types = node.get("@type")
    return types == expected or isinstance(types, list) and expected in types


def reject_constant(value):
    raise ValueError(f"Invalid JSON constant: {value}")


def main():
    results = []

    def report(label, passed, detail):
        results.append(bool(passed))
        detail = " ".join(str(detail).splitlines())
        print(f"{'PASS' if passed else 'FAIL'}: {label}: {detail}")

    document = None
    try:
        parser = JsonLdParser()
        path = Path(__file__).resolve().parent.parent / "index.html"
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
        if len(parser.blocks) != 1:
            raise ValueError(f"expected one application/ld+json block, found {len(parser.blocks)}")
        document = json.loads(parser.blocks[0], parse_constant=reject_constant)
        report("1 JSON parses", True, "one valid JSON-LD block")
    except (OSError, UnicodeError, ValueError) as exc:
        report("1 JSON parses", False, exc)

    graph = document.get("@graph") if isinstance(document, dict) else None
    valid_graph = isinstance(graph, list) and all(isinstance(node, dict) for node in graph)
    nodes = graph if valid_graph else []
    people = [node for node in nodes if has_type(node, "Person")]
    websites = [node for node in nodes if has_type(node, "WebSite")]
    report("2 Graph node types", valid_graph and len(people) == len(websites) == 1,
           f"Person={len(people)}, WebSite={len(websites)}" if valid_graph
           else "missing or invalid @graph array")

    # Check graph node definitions, not nested @id references such as publisher.
    ids = [node.get("@id") for node in nodes]
    valid_ids = valid_graph and bool(nodes) and all(isinstance(value, str) and value.strip() for value in ids)
    unique_ids = valid_ids and len(ids) == len(set(ids))
    report("3 Unique node @id values", unique_ids,
           f"{len(ids)} unique node IDs" if unique_ids else "missing, invalid, or duplicate graph node @id")

    person = people[0] if len(people) == 1 else {}
    website = websites[0] if len(websites) == 1 else {}
    person_id = person.get("@id")
    publisher = website.get("publisher")
    publisher_id = publisher.get("@id") if isinstance(publisher, dict) else None
    report("4 WebSite publisher matches Person", isinstance(person_id, str)
           and bool(person_id.strip()) and publisher_id == person_id,
           f"publisher @id={publisher_id!r}, Person @id={person_id!r}")

    image_url = person.get("image")
    try:
        parsed = urlsplit(image_url) if isinstance(image_url, str) else None
        valid_image = parsed is not None and parsed.scheme in ("http", "https") and bool(parsed.hostname)
    except ValueError:
        valid_image = False
    report("5 Person image URL", valid_image, image_url if valid_image else "missing or invalid HTTP(S) image URL")

    if not valid_image:
        report("6 Live image HTTP 200", False, "cannot fetch without a valid Person image URL")
    else:
        request = Request(image_url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        })
        try:
            with urlopen(request, timeout=30) as response:
                status = response.getcode()
                report("6 Live image HTTP 200", status == 200, f"HTTP {status}: {image_url}")
        except (HTTPError, URLError, OSError, ValueError) as exc:
            report("6 Live image HTTP 200", False, f"{image_url}: {exc}")

    print(f"Summary: {sum(results)}/{len(results)} checks passed.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
