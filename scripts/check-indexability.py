#!/usr/bin/env python3
"""Check live indexability; this is a repository tool only and is never deployed."""

from html.parser import HTMLParser
from http.client import HTTPException
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


URL = "https://rhettd333.github.io/"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


class RobotsParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and (attrs.get("name") or "").strip().lower() == "robots":
            if "noindex" in (attrs.get("content") or "").lower():
                self.noindex = True


def main():
    labels = ("Final HTTP status", "Meta robots", "X-Robots-Tag")
    try:
        request = Request(URL, headers={"User-Agent": USER_AGENT})
        try:
            response = urlopen(request, timeout=15)
        except HTTPError as exc:
            response = exc
        with response:
            status = response.code
            final_url = response.geturl()
            headers = response.headers.get_all("X-Robots-Tag", [])
            source = response.read().decode(
                response.headers.get_content_charset() or "utf-8", errors="replace"
            )
        page = RobotsParser()
        page.feed(source)
        page.close()
        blocked = any("noindex" in value.lower() for value in headers)
        checks = [
            (status == 200, f"{labels[0]}: {status} ({final_url})"),
            (not page.noindex, f"{labels[1]}: " +
             ("noindex found" if page.noindex else "no noindex found")),
            (not blocked, f"{labels[2]}: " +
             ("; ".join(headers) if headers else "absent")),
        ]
    except (URLError, OSError, HTTPException, ValueError, LookupError) as exc:
        checks = [(False, f"{label}: unable to check ({exc})") for label in labels]

    for passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL'}: {detail}")
    passed_count = sum(passed for passed, _ in checks)
    print(f"Summary: {passed_count}/{len(checks)} checks passed.")
    return 0 if passed_count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
