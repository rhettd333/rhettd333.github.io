#!/usr/bin/env python3
"""Audit robots guardrails; this is a repository tool only and never deployed."""

from pathlib import Path
from xml.etree import ElementTree


def parse_robots(source):
    groups = []
    agents = []
    rules = []
    sitemaps = []
    for line in source.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        name, value = (part.strip() for part in line.split(":", 1))
        name = name.lower()
        if name == "sitemap":
            sitemaps.append(value)
        elif name == "user-agent":
            if rules:
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(value)
        elif agents:
            rules.append((name, value))
    if agents:
        groups.append((agents, rules))
    return groups, sitemaps


def main():
    root = Path(__file__).resolve().parent.parent
    expected_sitemap = "https://rhettd333.github.io/sitemap.xml"
    expected_urls = ["https://rhettd333.github.io/"]
    try:
        groups, sitemaps = parse_robots(
            (root / "robots.txt").read_text(encoding="utf-8")
        )
        wildcard_rules = [rule for agents, rules in groups if "*" in agents
                          for rule in rules]
        crawl_allowed = (("allow", "/") in wildcard_rules and
                         ("disallow", "/") not in wildcard_rules)
        checks = [
            (crawl_allowed, f"User-agent: * crawling rules: {wildcard_rules!r}"),
            (expected_sitemap in sitemaps, f"Robots Sitemap: {sitemaps!r}; "
             f"expected {expected_sitemap!r}"),
        ]
    except (OSError, UnicodeError) as exc:
        checks = [(False, f"{label}: unable to read robots.txt ({exc})")
                  for label in ("User-agent: * crawling rules", "Robots Sitemap")]

    try:
        sitemap = ElementTree.parse(root / "sitemap.xml")
        checks.append((True, "Sitemap XML: well-formed"))
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        document = sitemap.getroot()
        entries = document.findall(f"{namespace}url")
        urls = [node.text or "" for node in document.iter(f"{namespace}loc")]
        valid_urls = (document.tag == f"{namespace}urlset" and
                      len(entries) == 1 and
                      len(entries[0].findall(f"{namespace}loc")) == 1 and
                      urls == expected_urls)
        checks.append((valid_urls, f"Sitemap URLs: {urls!r}; "
                       f"{len(entries)} URL entries; expected {expected_urls!r}"))
    except (OSError, UnicodeError, ElementTree.ParseError) as exc:
        checks.extend((False, f"{label}: unable to parse sitemap.xml ({exc})")
                      for label in ("Sitemap XML", "Sitemap URLs"))

    for passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL'}: {detail}")
    passed_count = sum(passed for passed, _ in checks)
    print(f"Summary: {passed_count}/{len(checks)} checks passed.")
    return 0 if passed_count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
