"""
push_supabase.py
Uploads computed movers DataFrame to Supabase `daily_movers` table.
Uses upsert on (trade_date, symbol) so re-running for same date is safe.
"""

import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL / SUPABASE_KEY not set. Check your .env file.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def push_movers(movers: pd.DataFrame) -> int:
    """Upserts rows into daily_movers table. Returns number of rows pushed."""
    if movers.empty:
        print("No movers to push.")
        return 0

    client = get_client()
    records = movers.to_dict(orient="records")

    # Supabase python client needs plain python types, not numpy types
    for r in records:
        for k, v in r.items():
            if pd.isna(v):
                r[k] = None
            elif hasattr(v, "item"):  # numpy int64/float64 -> python native
                r[k] = v.item()

    client.table("daily_movers").upsert(records, on_conflict="trade_date,symbol").execute()
    print(f"Pushed {len(records)} rows to Supabase.")
    return len(records)


if __name__ == "__main__":
    from fetch_bhavcopy import fetch_bhavcopy
    from compute_movers import compute_movers
    from datetime import datetime

    test_date = datetime.now()
    raw = fetch_bhavcopy(test_date)
    if raw is not None:
        movers = compute_movers(raw, test_date.strftime("%Y-%m-%d"))
        push_movers(movers)
    else:
        print("No data available for test date")
