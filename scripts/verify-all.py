#!/usr/bin/env python3
"""Weekly verification: a repository tool only and never deployed.

The weekly scrum runs it to summarize all repository checks.
"""

from datetime import date
from pathlib import Path
import subprocess
import sys


SCRIPTS = (
    "check-metadata.py",
    "check-links.py",
    "check-indexability.py",
    "check-canonical.py",
)


def main():
    scripts_dir = Path(__file__).resolve().parent
    print(f"Weekly verification report: {date.today().isoformat()}", flush=True)
    all_passed = True
    for name in SCRIPTS:
        script = scripts_dir / name
        if not script.is_file():
            print(f"FAIL: {name} (exit code 1) — missing script")
            all_passed = False
            continue
        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                cwd=scripts_dir.parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors="replace",
                check=False,
            )
        except OSError as exc:
            print(f"FAIL: {name} (exit code 1) — unable to run: {exc}")
            all_passed = False
            continue
        passed = result.returncode == 0
        all_passed = all_passed and passed
        summaries = [line.strip() for line in result.stdout.splitlines()
                     if line.strip().lower().startswith("summary:")]
        summary = f" — {summaries[-1]}" if summaries else ""
        print(f"{'PASS' if passed else 'FAIL'}: {name} "
              f"(exit code {result.returncode}){summary}")
    print(f"overall {'PASS' if all_passed else 'FAIL'}")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
