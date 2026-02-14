import csv
import sys
from pathlib import Path

DATA_PATH = Path("data") / "students.csv"
EXPECTED_HEADER = ["id", "name", "age"]


def fail(msg: str) -> None:
    print(f"CI ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not DATA_PATH.exists():
        fail(f"Missing file: {DATA_PATH}")

    with DATA_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Header check
        if reader.fieldnames != EXPECTED_HEADER:
            fail(f"Expected header {EXPECTED_HEADER}, got {reader.fieldnames}")

        row_count = 0
        for row_num, row in enumerate(reader, start=2):  # header is line 1
            row_count += 1

            # Presence checks
            for col in EXPECTED_HEADER:
                if col not in row or row[col] is None:
                    fail(f"Row {row_num}: missing column {col}")

            age_str = (row["age"] or "").strip()
            if not age_str.isdigit():
                fail(f"Row {row_num}: age must be a non-negative integer, got {age_str!r}")

            # Optional extra checks (uncomment if you want stricter rules)
            # if int(age_str) > 120:
            #     fail(f"Row {row_num}: age seems unrealistic: {age_str}")

    if row_count == 0:
        fail("No data rows found (students.csv has only a header).")

    print("CI OK: students.csv passed validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
