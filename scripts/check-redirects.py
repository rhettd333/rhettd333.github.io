#!/usr/bin/env python3
"""Verify redirects; this is a repository tool only and never deployed."""

from http.client import HTTPException
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin
from urllib.request import HTTPRedirectHandler, build_opener


START_URL = "http://rhettd333.github.io/"
EXPECTED_LOCATION = "https://rhettd333.github.io/"
MAX_HOPS = 2


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(opener, url):
    try:
        response = opener.open(url, timeout=20)
    except HTTPError as exc:
        # With automatic redirects disabled, 3xx responses arrive here too.
        response = exc
    with response:
        return response.code, response.headers.get("Location")


def main():
    opener = build_opener(NoRedirect())
    observations = []
    first_status = first_location = None
    url = START_URL
    visited = {url}
    hops = 0
    chain_ok = False
    reason = ""
    try:
        while True:
            status, location = request(opener, url)
            observations.append(
                f"{url!r}: status={status}, Location={location!r}"
            )
            if len(observations) == 1:
                first_status, first_location = status, location
            if status == 200:
                chain_ok = True
                break
            if not 300 <= status < 400:
                reason = "chain ended without HTTP 200"
                break
            if not location:
                reason = "redirect has no Location"
                break
            next_url = urldefrag(urljoin(url, location))[0]
            if next_url in visited:
                reason = f"redirect loop to {next_url!r}"
                break
            if hops >= MAX_HOPS:
                reason = f"chain exceeds {MAX_HOPS} redirect hops"
                break
            visited.add(next_url)
            url = next_url
            hops += 1
    except (URLError, OSError, ValueError, HTTPException) as exc:
        reason = f"request to {url!r} failed: {exc}"

    first_observed = (
        f"status={first_status!r}, Location={first_location!r}"
    )
    first_error = f"; {reason}" if first_status is None else ""
    checks = [
        (first_status is not None and 300 <= first_status < 400,
         f"First response is 3xx: {first_observed}{first_error}"),
        (first_location == EXPECTED_LOCATION,
         f"First Location equals {EXPECTED_LOCATION!r}: "
         f"{first_observed}{first_error}"),
        (chain_ok,
         f"Chain reaches HTTP 200 within {MAX_HOPS} hops without a loop: "
         f"hops={hops}; {'; '.join(observations) or first_observed}"
         f"{'; ' + reason if reason else ''}"),
    ]
    for passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL'}: {detail}")
    passed_count = sum(passed for passed, _ in checks)
    print(f"Summary: {passed_count}/{len(checks)} checks passed.")
    return 0 if passed_count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
