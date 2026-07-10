"""
backfill.py
One-time script to backfill the last N days of data.
Run this once after setup to populate history, e.g.:

    python backfill.py 30

Skips weekends automatically; holidays are skipped silently since
fetch_bhavcopy returns None for dates with no published data.
"""

import sys
import time
from datetime import datetime, timedelta

from main import run_for_date

DEFAULT_DAYS = 30


def backfill(days: int):
    today = datetime.now()
    print(f"Backfilling last {days} calendar days...")

    for i in range(days, -1, -1):
        target = today - timedelta(days=i)
        run_for_date(target)
        time.sleep(1)  # be polite to NSE servers, avoid rate limiting

    print("Backfill complete.")


if __name__ == "__main__":
    n_days = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DAYS
    backfill(n_days)
