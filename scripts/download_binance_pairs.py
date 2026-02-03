import time
import requests
import pandas as pd
from pathlib import Path

# =========================
# Configuration
# =========================

BASE_URL = "https://api.binance.us/api/v3/klines"
SESSION = requests.Session()

PAIRS = ["BTCUSDT", "BTCUSDC", "BTCUSD"]
INTERVAL = "1m"
LIMIT = 1000

# Requested window (UTC)
START_DATE = "2023-03-01T00:00:00Z"
END_DATE   = "2023-03-21T23:59:00Z"

OUT_DIR = Path("data_binance/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# Robust request helper
# =========================

def _get_json_with_retry(params, max_retries=12):
    for i in range(max_retries):
        try:
            r = SESSION.get(BASE_URL, params=params, timeout=60)

            # Rate limit
            if r.status_code == 429:
                wait = min(60, 2 * (2 ** i))
                print(f"429 rate limit. Sleeping {wait}s then retrying...")
                time.sleep(wait)
                continue

            # Server-side issues
            if r.status_code in (418, 500, 502, 503, 504):
                wait = min(60, 2 * (2 ** i))
                print(f"Server error {r.status_code}. Sleeping {wait}s then retrying...")
                time.sleep(wait)
                continue

            r.raise_for_status()
            return r.json()

        except (
            requests.exceptions.ConnectTimeout,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
        ) as e:
            wait = min(60, 2 * (2 ** i))
            print(f"Network timeout/error: {e}. Sleeping {wait}s then retrying...")
            time.sleep(wait)

    raise RuntimeError("Too many retries; still failing.")

# =========================
# Data download helpers
# =========================

def iter_klines(symbol, start_ts, end_ts):
    start_ms = int(start_ts.timestamp() * 1000)
    end_ms = int(end_ts.timestamp() * 1000)

    while start_ms <= end_ms:
        params = {
            "symbol": symbol,
            "interval": INTERVAL,
            "startTime": start_ms,
            "endTime": end_ms,
            "limit": LIMIT,
        }

        chunk = _get_json_with_retry(params)
        if not chunk:
            break

        yield chunk
        start_ms = chunk[-1][0] + 1
        time.sleep(0.3)


def chunk_to_df(chunk):
    df = pd.DataFrame(chunk, columns=[
        "open_time","open","high","low","close","volume",
        "close_time","quote_volume","trades",
        "taker_base","taker_quote","ignore"
    ])

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df = df[["open_time","open","high","low","close","volume"]]

    for c in ["open","high","low","close","volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    return df


def download_pair(symbol, start_ts, end_ts):
    out_file = OUT_DIR / f"{symbol}_1m_20230301_20230321.csv"
    if out_file.exists():
        out_file.unlink()

    rows = 0
    wrote_header = False

    for chunk in iter_klines(symbol, start_ts, end_ts):
        df = chunk_to_df(chunk)
        df.to_csv(out_file, mode="a", header=not wrote_header, index=False)
        wrote_header = True
        rows += len(df)

    print(f"{symbol}: saved {rows} rows")

# =========================
# Main
# =========================

def main():
    start_ts = pd.to_datetime(START_DATE, utc=True)
    end_ts = pd.to_datetime(END_DATE, utc=True)

    print(f"Downloading 1m data from {start_ts} to {end_ts}\n")

    for pair in PAIRS:
        print(f"Starting {pair}...")
        download_pair(pair, start_ts, end_ts)

    meta = pd.DataFrame({
        "pair": PAIRS,
        "interval": INTERVAL,
        "start_utc": START_DATE,
        "end_utc": END_DATE,
        "exchange": "Binance.US"
    })

    meta_path = OUT_DIR / "metadata_range_1m_20230301_20230321.csv"
    meta.to_csv(meta_path, index=False)
    print(f"\nSaved metadata: {meta_path}")


if __name__ == "__main__":
    main()
