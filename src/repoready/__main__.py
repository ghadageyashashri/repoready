import argparse
import sys
from collections import Counter
from pathlib import Path

from .checks import run_all_checks
from .models import Status


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="repoready",
        description="Check whether a project is easy for other developers to set up.",
    )
    parser.add_argument("folder", help="Path to the project folder to check")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        print(f"Error: '{folder}' is not a folder.")
        return 2

    results = run_all_checks(folder)

    print(f"\nRepoReady report for: {folder.resolve()}\n")
    for result in results:
        label = f"[{result.status.value}]"
        print(f"{label:<10} {result.name}: {result.message}")

    counts = Counter(result.status for result in results)
    print(
        f"\nSummary: {counts[Status.PASS]} passed, "
        f"{counts[Status.WARNING]} warnings, "
        f"{counts[Status.FAIL]} failed, "
        f"{counts[Status.UNKNOWN]} unknown\n"
    )

    return 1 if counts[Status.FAIL] else 0


if __name__ == "__main__":
    sys.exit(main())