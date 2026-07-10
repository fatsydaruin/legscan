"""
fetch_bhavcopy.py
Downloads NSE's daily "sec_bhavdata_full" bhavcopy CSV for a given date
and returns a cleaned pandas DataFrame.

NSE blocks requests without proper browser-like headers + cookies, so we
first hit the homepage to grab session cookies, then request the archive file.
"""

import io
import requests
import pandas as pd
from datetime import datetime

BASE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def _get_session() -> requests.Session:
    """Create a session with NSE cookies set (required to avoid 403)."""
    session = requests.Session()
    session.headers.update(BASE_HEADERS)
    # Hitting homepage first sets the necessary cookies for archives access
    session.get("https://www.nseindia.com", timeout=10)
    session.get("https://www.nseindia.com/market-data/securities-available-for-trading", timeout=10)
    return session


def fetch_bhavcopy(date: datetime) -> pd.DataFrame | None:
    """
    Fetch bhavcopy for a single date.
    Returns a DataFrame with cleaned columns, or None if not available
    (weekend / market holiday / data not yet published).
    """
    date_str = date.strftime("%d%m%Y")
    url = f"https://archives.nseindia.com/products/content/sec_bhavdata_full_{date_str}.csv"

    session = _get_session()
    resp = session.get(url, timeout=15)

    if resp.status_code != 200 or len(resp.content) < 500:
        return None  # likely a holiday / weekend / no data

    df = pd.read_csv(io.StringIO(resp.text))

    # NSE CSV has stray whitespace in column names and string values
    df.columns = [c.strip() for c in df.columns]
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # Keep only EQ series (regular equity, excludes BE/BZ/etc.)
    df = df[df["SERIES"] == "EQ"].copy()

    # Numeric conversions
    numeric_cols = ["PREV_CLOSE", "OPEN_PRICE", "HIGH_PRICE", "LOW_PRICE",
                     "LAST_PRICE", "CLOSE_PRICE", "AVG_PRICE",
                     "TTL_TRD_QNTY", "TURNOVER_LACS", "NO_OF_TRADES"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


if __name__ == "__main__":
    # quick manual test: fetch today's data
    test_date = datetime.now()
    result = fetch_bhavcopy(test_date)
    if result is None:
        print(f"No data for {test_date.date()} (holiday/weekend/not published yet)")
    else:
        print(f"Fetched {len(result)} rows for {test_date.date()}")
        print(result.head())
