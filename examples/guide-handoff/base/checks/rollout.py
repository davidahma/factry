"""Running the previous reader against a real, mixed receipt stream."""

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_RECEIPT = '{"total_pence": 75}\n'


def previous_total(records):
    """Frozen behavior of the previous reader."""
    return sum(json.loads(line)["total_pence"] for line in records)


def main():
    written = subprocess.check_output(
        [sys.executable, "-B", "ledger.py", "write", "125"], cwd=ROOT, text=True,
    )
    try:
        observed = previous_total((HISTORICAL_RECEIPT + written).splitlines())
    except KeyError:
        sys.exit("Rollback reader could not read the current row: missing total_pence")
    if observed != 200:
        sys.exit(f"Rollback reader returned {observed}. Expected 200.")
    print("Rollback reader accepted old and current rows: 200")


if __name__ == "__main__":
    main()
