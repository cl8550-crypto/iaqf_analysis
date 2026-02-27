# IAQF 2026 — Analysis Repository

This repository contains the data and code supporting our IAQF 2026 paper on stablecoin market structure. The paper is organized into four main sections; the folders below map directly to those sections.

---

## Paper Structure & Folder Map

| Paper Section | Folder | Description |
|---|---|---|
| 2. Cross-Currency Basis | `cross_currency_basis/` | Computes and analyzes the cross-currency basis |
| 3. Stablecoin Dynamics | `stablecoin_dynamics/` | Core stablecoin basis analysis (also supplies data for Section 2) |
| 4. Liquidity and Fragmentation | `liquidity/` | Exchange-level liquidity and market fragmentation |

---

## Repository Structure

```
iaqf_analysis/
├── data/
│   ├── binance/raw/          # Binance.US 1-min spot OHLCV data
│   └── kraken/raw/           # Kraken 1-min spot OHLCV data
├── scripts/
│   └── download_binance_pairs.py
├── stablecoin_dynamics/
│   └── code/
│       ├── binance_code.ipynb
│       ├── kraken_code.ipynb
│       └── comparison_analysis_code.ipynb
├── cross_currency_basis/     # Section 2 code
└── liquidity/                # Section 4 code
```

---

## Data (`data/`)

Raw 1-minute spot OHLCV data for three BTC trading pairs across two exchanges, covering the Silicon Valley Bank / USDC depeg stress period.

### Binance.US (`data/binance/raw/`)

| File | Pair | Date Range (UTC) |
|---|---|---|
| `btcusdt_1m_20230301_20230321.csv` | BTC/USDT | 2023-03-01 to 2023-03-21 |
| `btcusdc_1m_20230301_20230321.csv` | BTC/USDC | 2023-03-01 to 2023-03-21 |
| `btcusd_1m_20230301_20230321.csv` | BTC/USD | 2023-03-01 to 2023-03-21 |
| `metadata_range_1m_20230301_20230321.csv` | — | Dataset metadata (pairs, interval, exchange) |

Columns: `open_time, open, high, low, close, volume`

### Kraken (`data/kraken/raw/`)

| File | Pair | Date Range (UTC) |
|---|---|---|
| `btcusdt_1m_20230301_20230321.csv` | BTC/USDT | 2023-01-01 to 2023-03-31 |
| `btcusdc_1m_20230301_20230321.csv` | BTC/USDC | 2023-01-01 to 2023-03-31 |
| `btcusd_1m_20230301_20230321.csv` | BTC/USD | 2023-01-01 to 2023-03-31 |

Kraken files have no header row. Columns (by position): `timestamp, open, high, low, close, volume, count`

> **Note:** Raw data files should not be modified directly.

---

## Scripts (`scripts/`)

### `download_binance_pairs.py`

Downloads 1-minute kline data from the Binance.US REST API for BTC/USDT, BTC/USDC, and BTC/USD. Handles rate limiting (HTTP 429) and server errors with exponential backoff. Saves one CSV per pair plus a metadata file to `data/binance/raw/`.

---

## Section 2 — Cross-Currency Basis (`cross_currency_basis/`)

Code for the **Cross-Currency Basis** section of the paper. Uses the same 1-minute spot price data from `data/` (also used by Section 3) to construct and analyze the cross-currency basis between stablecoin and fiat BTC markets.

---

## Section 3 — Stablecoin Dynamics (`stablecoin_dynamics/`)

Code and figures for the **Stablecoin Dynamics** section. The data in `data/` was collected for this section and is shared with Section 2.

### `stablecoin_dynamics/code/binance_code.ipynb`

Processes and analyzes **Binance.US** data. Runs the full stablecoin basis pipeline for the Binance exchange:

- **Data cleaning** — timestamp parsing, deduplication, alignment of BTC/USDT, BTC/USDC, BTC/USD into a balanced panel
- **1.1 Stablecoin basis** — computes USDT and USDC basis relative to USD benchmark
- **1.2 Cross-stablecoin spread** — USDT-minus-USDC spread isolating relative confidence between the two stablecoins
- **1.3 Absolute deviation magnitude** — MAD and tail percentiles (95th, 99th) in basis points
- **2.1 Rolling volatility** — rolling standard deviation of basis at 1h, 6h, and 1d windows
- **2.2 Mean reversion speed** — AR(1) half-life estimation; measures how quickly basis deviations correct
- **2.3 Stress persistence** — fraction of time above 20 bps threshold and excursion duration statistics
- **3.1 Calm vs stress regimes** — conditional basis statistics split by BTC realized volatility and max drawdown
- **3.2 Asymmetry** — discount vs premium magnitude and frequency

### `stablecoin_dynamics/code/kraken_code.ipynb`

Same pipeline as `binance_code.ipynb` applied to **Kraken** data. Covers the identical sequence of analyses (Sections 1.1–3.2) for the Kraken exchange, enabling direct comparison of results.

### `stablecoin_dynamics/code/comparison_analysis_code.ipynb`

**Cross-exchange comparison** notebook. Imports outputs from both `binance_code.ipynb` and `kraken_code.ipynb` and runs:

- **4.1 Cross-exchange basis gap** — `Δ_s(t) = Basis_{s,Binance}(t) − Basis_{s,Kraken}(t)` for USDT and USDC; summary statistics (mean, std, p95, p99, max in bps); time-series plot saved as `fig_gap_timeseries.png`
- **4.2 Lead–lag analysis** — cross-correlation at lags −60 to +60 minutes to determine which exchange prices stablecoin risk first; plot saved as `fig_leadlag_crosscorr.png`
- **5.1 Stability ranking** — ranks all four market/exchange combinations (USDT-Binance, USDC-Binance, USDT-Kraken, USDC-Kraken) by worst 1% absolute deviation
- **5.2 Recovery time** — average, median, and 95th percentile of excursion durations above 5 bps per market

---

## Section 4 — Liquidity and Fragmentation (`liquidity/`)

Code for the **Liquidity and Fragmentation** section of the paper. Analyzes exchange-level liquidity conditions and market fragmentation across stablecoin trading pairs.

> **Note:** The data used for this section is **not included in this repository** because the file sizes are too large to push to GitHub.
