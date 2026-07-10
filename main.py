"""
main.py
Daily entry point (called by GitHub Actions cron or manually).
Fetches today's (or a given date's) bhavcopy, computes movers, pushes to Supabase.

Usage:
    python main.py                 -> runs for today
    python main.py 2026-07-09      -> runs for a specific date (YYYY-MM-DD)
"""

import sys
from datetime import datetime

from fetch_bhavcopy import fetch_bhavcopy
from compute_movers import compute_movers
from push_supabase import push_movers
from export_csv import save_local_csv


def run_for_date(target_date: datetime):
    date_str = target_date.strftime("%Y-%m-%d")
    print(f"--- Running scan for {date_str} ---")

    if target_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
        print("Weekend — market closed, skipping.")
        return

    raw = fetch_bhavcopy(target_date)
    if raw is None:
        print("No bhavcopy available (holiday or not yet published). Skipping.")
        return

    movers = compute_movers(raw, date_str)
    print(f"{len(movers)} stocks moved >= 3% on {date_str}")

    push_movers(movers)
    save_local_csv(movers, date_str)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = datetime.strptime(sys.argv[1], "%Y-%m-%d")
    else:
        target = datetime.now()

    run_for_date(target)
