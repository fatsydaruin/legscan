"""
compute_movers.py
Takes a bhavcopy DataFrame, filters to NIFTY 500 watchlist symbols,
computes % change, and returns gainers/losers with abs(pct_change) >= threshold.
"""

import json
import pandas as pd

THRESHOLD_PCT = 3.0
WATCHLIST_PATH = "watchlist.json"


def load_watchlist() -> set:
    with open(WATCHLIST_PATH, "r") as f:
        return set(json.load(f))


def compute_movers(df: pd.DataFrame, trade_date: str) -> pd.DataFrame:
    """
    df: cleaned bhavcopy DataFrame (from fetch_bhavcopy)
    trade_date: 'YYYY-MM-DD' string
    Returns a DataFrame ready to push to Supabase: 
    columns = [trade_date, symbol, close_price, prev_close, pct_change, volume, category]
    """
    watchlist = load_watchlist()

    filtered = df[df["SYMBOL"].isin(watchlist)].copy()

    # Avoid division by zero / bad rows
    filtered = filtered[(filtered["PREV_CLOSE"].notna()) & (filtered["PREV_CLOSE"] != 0)]

    filtered["pct_change"] = (
        (filtered["CLOSE_PRICE"] - filtered["PREV_CLOSE"]) / filtered["PREV_CLOSE"]
    ) * 100

    movers = filtered[filtered["pct_change"].abs() >= THRESHOLD_PCT].copy()

    movers["category"] = movers["pct_change"].apply(lambda x: "gainer" if x > 0 else "loser")
    movers["trade_date"] = trade_date

    result = movers.rename(columns={
        "SYMBOL": "symbol",
        "CLOSE_PRICE": "close_price",
        "PREV_CLOSE": "prev_close",
        "TTL_TRD_QNTY": "volume",
    })[["trade_date", "symbol", "close_price", "prev_close", "pct_change", "volume", "category"]]

    result["pct_change"] = result["pct_change"].round(2)

    return result.sort_values("pct_change", ascending=False).reset_index(drop=True)


if __name__ == "__main__":
    from fetch_bhavcopy import fetch_bhavcopy
    from datetime import datetime

    test_date = datetime.now()
    raw = fetch_bhavcopy(test_date)
    if raw is not None:
        movers = compute_movers(raw, test_date.strftime("%Y-%m-%d"))
        print(f"Found {len(movers)} movers >= {THRESHOLD_PCT}%")
        print(movers)
    else:
        print("No data available for test date")
