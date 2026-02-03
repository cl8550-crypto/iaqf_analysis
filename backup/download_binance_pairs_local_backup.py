import time
import requests
import pandas as pd
from pathlib import Path

# Binance.US API
BASE_URL = "https://api.binance.us/api/v3/klines"

OUT_DIR = Path("data/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

PAIRS = ["BTCUSDT", "BTCUSDC", "BTCUSD"]
INTERVAL = "1m"
LIMIT = 1000

# Your requested window (UTC)
START_DATE = "2023-03-01T00:00:00Z"
END_DATE   = "2023-03-21T23:59:00Z"


def _get_json_with_retry(params, max_retries=8):
    for i in range(max_retries):
        r = requests.get(BASE_URL, params=params, timeout=60)
        if r.status_code == 429:
            wait = 1.5 * (2 ** i)
            print(f"429 rate limit. Sleeping {wait:.1f}s then retrying...")
            time.sleep(wait)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("Too many retries; still rate-limited or failing.")


def iter_klines(symbol: str, interval: str, start_ts: pd.Timestamp, end_ts: pd.Timestamp):
    start_ms = int(start_ts.timestamp() * 1000)
    end_ms = int(end_ts.timestamp() * 1000)

    while start_ms <= end_ms:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_ms,
            "endTime": end_ms,
            "limit": LIMIT
        }
        chunk = _get_json_with_retry(params)
        if not chunk:
            break

        yield chunk
        start_ms = chunk[-1][0] + 1
        time.sleep(0.4)


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


def download_to_csv(symbol: str, start_ts: pd.Timestamp, end_ts: pd.Timestamp, out_path: Path):
    wrote_header = False
    rows_total = 0

    for chunk in iter_klines(symbol, INTERVAL, start_ts, end_ts):
        df = chunk_to_df(chunk)
        df.to_csv(out_path, mode="a", header=not wrote_header, index=False)
        wrote_header = True
        rows_total += len(df)

    return rows_total


def main():
    start_ts = pd.to_datetime(START_DATE, utc=True)
    end_ts = pd.to_datetime(END_DATE, utc=True)

    print(f"Downloading 1m data in UTC window: {start_ts} -> {end_ts}\n")

    for sym in PAIRS:
        out_file = OUT_DIR / f"{sym}_1m_{start_ts.strftime('%Y%m%d')}_{end_ts.strftime('%Y%m%d')}.csv"
        if out_file.exists():
            out_file.unlink()

        print(f"Downloading {sym} -> {out_file}")
        n = download_to_csv(sym, start_ts, end_ts, out_file)
        print(f"  done. rows={n}\n")

    meta = pd.DataFrame({
        "pair": PAIRS,
        "interval": INTERVAL,
        "start_utc": [str(start_ts)] * len(PAIRS),
        "end_utc": [str(end_ts)] * len(PAIRS),
        "base_url": [BASE_URL] * len(PAIRS),
    })
    meta_path = OUT_DIR / "metadata_range_1m_20230301_20230321.csv"
    meta.to_csv(meta_path, index=False)
    print(f"Saved metadata: {meta_path}")


if __name__ == "__main__":
    main()

