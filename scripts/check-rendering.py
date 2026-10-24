#!/usr/bin/env python3
"""Check raw HTML text; this is a repository tool only and never deployed."""

from html.parser import HTMLParser
from http.client import HTTPException
from urllib.error import URLError
from urllib.request import Request, urlopen


URL = "https://rhettd333.github.io/"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
FRAGMENTS = (
    "I work on buildings and capital decisions.",
    "I am a consultant at Deloitte in Boston.",
    "corporate real estate strategy and capital planning",
    "Background",
    "Outside work",
    "Elsewhere",
    "I write about capital planning and deferred maintenance at",
    "Personal website. Views are my own",
)


class TextParser(HTMLParser):
    """Strip tags and discard script/style content without executing anything."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.excluded_tag = None

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style") and self.excluded_tag is None:
            self.excluded_tag = tag

    def handle_endtag(self, tag):
        if tag == self.excluded_tag:
            self.excluded_tag = None

    def handle_data(self, data):
        if self.excluded_tag is None:
            self.parts.append(data)


def main():
    error = None
    visible_text = ""
    try:
        request = Request(URL, headers={"User-Agent": USER_AGENT})
        with urlopen(request, timeout=15) as response:
            source = response.read().decode(
                response.headers.get_content_charset() or "utf-8", errors="replace"
            )
        page = TextParser()
        page.feed(source)
        page.close()
        visible_text = " ".join(" ".join(page.parts).split())
    except (URLError, OSError, HTTPException, ValueError, LookupError) as exc:
        error = str(exc)

    passed_count = 0
    for fragment in FRAGMENTS:
        passed = error is None and fragment in visible_text
        passed_count += passed
        detail = f" (unable to check: {error})" if error is not None else ""
        print(f"{'PASS' if passed else 'FAIL'}: {fragment}{detail}")
    print(f"Summary: {passed_count}/{len(FRAGMENTS)} checks passed.")
    return 0 if passed_count == len(FRAGMENTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
