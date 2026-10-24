#!/usr/bin/env python3
"""Check production responses; this is a repository tool only and never deployed."""

from http.client import HTTPException
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = "https://rhettd333.github.io"
RESPONSES = (
    ("/", "text/html"),
    ("/styles.css", "text/css"),
    ("/favicon.svg", "image/svg"),
    ("/favicon-32x32.png", "image/png"),
    ("/assets/rhett-dawson-headshot-800.jpg", "image/jpeg"),
    ("/robots.txt", "text/plain"),
    ("/sitemap.xml", "xml"),
)
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)


def main():
    passed_count = 0
    for path, expected in RESPONSES:
        url = BASE_URL + path
        status = None
        content_type = ""
        error = ""
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})
            try:
                response = urlopen(request, timeout=20)
            except HTTPError as exc:
                response = exc
            with response:
                status = response.code
                content_type = response.headers.get("Content-Type", "")
        except (URLError, OSError, ValueError, HTTPException) as exc:
            error = f"; error={exc}"
        passed = not error and status == 200 and expected in content_type.lower()
        passed_count += bool(passed)
        print(
            f"{'PASS' if passed else 'FAIL'}: {url} "
            f"status={status!r}, Content-Type={content_type!r}; "
            f"expected status=200, Content-Type contains {expected!r}{error}"
        )
    print(f"Summary: {passed_count}/{len(RESPONSES)} checks passed.")
    return 0 if passed_count == len(RESPONSES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
