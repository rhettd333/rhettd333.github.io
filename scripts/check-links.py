#!/usr/bin/env python3
"""Check external anchor links and title freshness; repository tool only."""

import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls = set()
        self.json_ld = []
        self.script_parts = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            href = (attrs.get("href") or "").strip()
            if href.lower().startswith(("http://", "https://")):
                self.urls.add(href)
        if tag == "script" and (attrs.get("type") or "").lower() == "application/ld+json":
            self.script_parts = []

    def handle_data(self, data):
        if self.script_parts is not None:
            self.script_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.script_parts is not None:
            self.json_ld.append("".join(self.script_parts))
            self.script_parts = None


def job_titles(value):
    """Find jobTitle values, including those in arrays and @graph nodes."""
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "jobTitle":
                yield child
            yield from job_titles(child)
    elif isinstance(value, list):
        for child in value:
            yield from job_titles(child)


def request_status(url, method):
    request = Request(url, headers={"User-Agent": USER_AGENT}, method=method)
    try:
        with urlopen(request, timeout=15) as response:
            return response.status
    except HTTPError as exc:
        status = exc.code
        exc.close()
        return status


def check_url(url):
    try:
        status = request_status(url, "HEAD")
        if status in (405, 501):
            status = request_status(url, "GET")
    except (URLError, OSError, ValueError) as exc:
        return "FAIL", f"status=N/A {url} ({exc})"
    if status in (404, 410) or 500 <= status <= 599:
        result = "FAIL"
    elif status in (403, 999):
        result = "WARN"
    else:
        result = "PASS"
    return result, f"status={status} {url}"


def main():
    counts = Counter()

    def report(result, message):
        counts[result] += 1
        print(f"{result}: {message}", flush=True)

    try:
        source = (Path(__file__).resolve().parent.parent / "index.html").read_text(
            encoding="utf-8"
        )
    except (OSError, UnicodeError) as exc:
        report("FAIL", f"Read index.html ({exc})")
    else:
        page = PageParser()
        page.feed(source)
        page.close()
        for url in sorted(page.urls):
            report(*check_url(url))
        report("FAIL" if "Senior Consultant" in source else "PASS",
               'Freshness: index.html contains no "Senior Consultant"')
        try:
            titles = [title for block in page.json_ld
                      for title in job_titles(json.loads(block))]
            valid = bool(titles) and all(title == "Consultant" for title in titles)
            report("PASS" if valid else "FAIL",
                   f'Freshness: JSON-LD jobTitle is exactly "Consultant" (found {titles!r})')
        except ValueError as exc:
            report("FAIL", f"Freshness: invalid JSON-LD ({exc})")

    print(f"Summary: {counts['PASS']} PASS, {counts['WARN']} WARN, {counts['FAIL']} FAIL")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
