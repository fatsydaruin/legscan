"""
export_csv.py
Saves the computed movers DataFrame as a local CSV file whenever the
scan is run manually (or via GitHub Actions), in addition to pushing
to Supabase.

Filename format: DAY_DATEth_MONTH_YY.csv
Example: FRI_10TH_JULY_26.csv

Files are written into the `python/output/` folder.
"""

import os
import pandas as pd
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def _ordinal_suffix(day: int) -> str:
    if 11 <= day % 100 <= 13:
        return "TH"
    return {1: "ST", 2: "ND", 3: "RD"}.get(day % 10, "TH")


def _build_filename(date_obj: datetime) -> str:
    day_abbr = date_obj.strftime("%a").upper()       # FRI
    day_num = date_obj.day                           # 10
    suffix = _ordinal_suffix(day_num)                # TH
    month_name = date_obj.strftime("%B").upper()     # JULY
    year_short = date_obj.strftime("%y")             # 26
    return f"{day_abbr}_{day_num}{suffix}_{month_name}_{year_short}.csv"


def save_local_csv(movers: pd.DataFrame, trade_date: str) -> str:
    """
    movers: the DataFrame returned by compute_movers()
    trade_date: 'YYYY-MM-DD' string
    Returns the full path of the saved CSV file.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    date_obj = datetime.strptime(trade_date, "%Y-%m-%d")
    filename = _build_filename(date_obj)
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Save even if empty, so there's a record that the scan ran with 0 results
    movers.to_csv(filepath, index=False)
    print(f"Local CSV saved: {filepath}")
    return filepath


if __name__ == "__main__":
    from fetch_bhavcopy import fetch_bhavcopy
    from compute_movers import compute_movers

    test_date = datetime.now()
    raw = fetch_bhavcopy(test_date)
    if raw is not None:
        movers = compute_movers(raw, test_date.strftime("%Y-%m-%d"))
        save_local_csv(movers, test_date.strftime("%Y-%m-%d"))
    else:
        print("No data available for test date")
