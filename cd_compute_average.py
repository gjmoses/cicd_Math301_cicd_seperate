# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 18:13:53 2026

@author: gm192
"""

import csv
import sys
from pathlib import Path

DATA_PATH = Path("data") / "students.csv"
OUTPUT_PATH = Path("average_age.txt")


def fail(msg: str) -> None:
    print(f"CD ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not DATA_PATH.exists():
        fail(f"Missing file: {DATA_PATH}")

    with DATA_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or "age" not in reader.fieldnames:
            fail("students.csv missing required 'age' column (run CI validation).")

        ages = []
        for row_num, row in enumerate(reader, start=2):
            age_str = (row.get("age") or "").strip()
            if not age_str.isdigit():
                fail(f"Row {row_num}: age must be a non-negative integer, got {age_str!r} (run CI validation).")
            ages.append(int(age_str))

    if not ages:
        fail("No ages found to compute an average.")

    avg = sum(ages) / len(ages)
    OUTPUT_PATH.write_text(f"Average age: {avg:.2f}\n", encoding="utf-8")
    print(f"CD OK: wrote {OUTPUT_PATH} (n={len(ages)}, avg={avg:.2f}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
