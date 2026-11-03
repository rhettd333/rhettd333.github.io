"""Check deployment privacy. This is a repository tool only and is never deployed."""

import argparse
import os
from pathlib import Path, PurePosixPath


EXPECTED_FILES = {
    "404.html",
    "apple-touch-icon.png",
    "assets/rhett-dawson-headshot-400.jpg",
    "assets/rhett-dawson-headshot-800.jpg",
    "favicon-32x32.png",
    "favicon.svg",
    "humans.txt",
    "icon-192x192.png",
    "icon-512x512.png",
    "index.html",
    "robots.txt",
    "sitemap.xml",
    "styles.css",
}


def is_forbidden(path):
    relative = PurePosixPath(path)
    return (
        relative.name in {"BRIEF.md", "MISSION.md", "BACKLOG.md", "README.md"}
        or relative.suffix.lower() in {".md", ".markdown", ".mdown", ".mkd"}
        or any(part in {"research-notes", "scripts", ".github"} for part in relative.parts)
        or (len(relative.parts) == 1 and "notes" in relative.name.lower())
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "artifact", nargs="?", type=Path,
        default=Path(__file__).resolve().parent.parent / "dist",
    )
    artifact = parser.parse_args().artifact
    exists = artifact.is_dir()
    files = set()
    paths = set()
    errors = []
    if exists:
        for root, directories, filenames in os.walk(artifact, onerror=errors.append):
            for name in directories + filenames:
                paths.add((Path(root) / name).relative_to(artifact).as_posix())
            for name in filenames:
                files.add((Path(root) / name).relative_to(artifact).as_posix())

    missing = EXPECTED_FILES - files
    extra = files - EXPECTED_FILES
    forbidden = {path for path in paths if is_forbidden(path)}
    readable = exists and not errors
    checks = [
        (exists, "Artifact directory exists", str(artifact)),
        (readable and not missing, "No missing expected files", ", ".join(sorted(missing))),
        (readable and not extra, "No extra files", ", ".join(sorted(extra))),
        (readable and not forbidden, "No forbidden private files or paths",
         ", ".join(sorted(forbidden))),
    ]
    for passed, label, detail in checks:
        print(f"{'PASS' if passed else 'FAIL'}: {label}" + (f" ({detail})" if detail else ""))
    for error in errors:
        print(f"Artifact scan error: {error}")
    passed_count = sum(passed for passed, _, _ in checks)
    print(f"Summary: {passed_count}/{len(checks)} checks passed.")
    return 0 if passed_count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
