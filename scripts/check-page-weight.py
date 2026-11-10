"""Check page weight. This is a repository tool only and is never deployed."""

from pathlib import Path


FILE_BUDGETS = {
    "404.html": 3000,
    "apple-touch-icon.png": 8000,
    "assets/rhett-dawson-headshot-400.jpg": 40000,
    "assets/rhett-dawson-headshot-800.jpg": 120000,
    "favicon-32x32.png": 3000,
    "favicon.svg": 1000,
    "humans.txt": 500,
    "icon-192x192.png": 12000,
    "icon-512x512.png": 30000,
    "index.html": 10000,
    "robots.txt": 500,
    "sitemap.xml": 500,
    "styles.css": 6000,
}

INITIAL_LOAD_FILES = (
    "index.html",
    "styles.css",
    "assets/rhett-dawson-headshot-800.jpg",
)


def main():
    repo_root = Path(__file__).resolve().parent.parent
    sizes = {}
    passed_count = 0
    for name, budget in FILE_BUDGETS.items():
        try:
            size = len((repo_root / name).read_bytes())
        except OSError as exc:
            print(f"FAIL: {name} (actual unavailable, budget {budget} bytes, {exc})")
            continue
        sizes[name] = size
        passed = size <= budget
        passed_count += passed
        print(f"{'PASS' if passed else 'FAIL'}: {name} "
              f"(actual {size} bytes, budget {budget} bytes)")

    aggregates = (
        ("Total published files", FILE_BUDGETS, 200000),
        ("Initial load", INITIAL_LOAD_FILES, 120000),
    )
    for label, names, budget in aggregates:
        complete = all(name in sizes for name in names)
        total = sum(sizes[name] for name in names if name in sizes)
        passed = complete and total <= budget
        passed_count += passed
        actual = f"{total} bytes" if complete else f"unavailable, known total {total} bytes"
        print(f"{'PASS' if passed else 'FAIL'}: {label} "
              f"(actual {actual}, budget {budget} bytes)")

    print(f"Summary: {passed_count}/15 checks passed.")
    return 0 if passed_count == 15 else 1


if __name__ == "__main__":
    raise SystemExit(main())
