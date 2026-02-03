# File Description
## Binance Spot Data (1m)

- **[BTCUSDT_1m_20230301_20230321.csv](data/binance/raw/BTCUSDT_1m_20230301_20230321.csv)**  
  Exchange: Binance.US  
  Frequency: 1 minute  
  Date Range (UTC): 2023-03-01 to 2023-03-21  

- **[BTCUSDC_1m_20230301_20230321.csv](data/binance/raw/BTCUSDC_1m_20230301_20230321.csv)**  
  Exchange: Binance.US  
  Frequency: 1 minute  
  Date Range (UTC): 2023-03-01 to 2023-03-21  

- **[BTCUSD_1m_20230301_20230321.csv](data/binance/raw/BTCUSD_1m_20230301_20230321.csv)**  
  Exchange: Binance.US  
  Frequency: 1 minute  
  Date Range (UTC): 2023-03-01 to 2023-03-21  

- **[Metadata file](data/binance/raw/metadata_range_1m_20230301_20230321.csv)**  
  Describes dataset scope, frequency, time window, and exchange.

## Kraken Spot Data (1m)

- **[BTCUSDT_1m_20230301_20230321.csv](data/kraken/raw/BTCUSDT_1m_20230301_20230321.csv)**  
  Exchange: Kraken  
  Trading Pair: BTC/USDT  
  Frequency: 1 minute  
  Date Range (UTC): 2023-03-01 to 2023-03-21  

- **[BTCUSDC_1m_20230301_20230321.csv](data/kraken/raw/BTCUSDC_1m_20230301_20230321.csv)**  
  Exchange: Kraken  
  Trading Pair: BTC/USDC  
  Frequency: 1 minute  
  Date Range (UTC): 2023-03-01 to 2023-03-21  

- **[BTCUSD_1m_20230301_20230321.csv](data/kraken/raw/BTCUSD_1m_20230301_20230321.csv)**  
  Exchange: Kraken  
  Trading Pair: BTC/USD  
  Frequency: 1 minute  
  Date Range (UTC): 2023-03-01 to 2023-03-21  

### Notes

- data files from Kraken following this pattern (since there's no column name written down above each column)--> columns = ["timestamp","open","high","low","close","volume","count"]
- Raw data files should not be modified directly.
