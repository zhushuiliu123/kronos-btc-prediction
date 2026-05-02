#!/usr/bin/env python3
"""
Fetch recent Bitcoin historical K-line (OHLC) data
Data source: Binance public API (free, no API key required, very reliable)
"""

import json
import csv
from datetime import datetime, timezone

try:
    from urllib.request import urlopen, Request
except ImportError:
    import urllib2 as urllib


def fetch_btc_binance(limit=90):
    """
    Fetch BTC/USDT daily K-line data from Binance public API.
    - limit: number of daily candles (max 1000)
    Returns list of dicts with OHLC + volume.
    """
    print(f"Fetching BTC/USDT daily K-line from Binance (last {limit} days)...")

    # Binance public klines API
    # symbol=BTCUSDT, interval=1d (daily), limit=N
    url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit={limit}"

    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        if not data:
            print("No data received from Binance")
            return None

        # Binance kline format:
        # [
        #   [
        #     1499040000000,      // Open time (ms)
        #     "0.01657200",       // Open
        #     "0.80000000",       // High
        #     "0.01575800",       // Low
        #     "0.01577100",       // Close
        #     "148976.11427815",  // Volume
        #     1499644799999,      // Close time
        #     "2434.19055334",    // Quote asset volume
        #     308,                // Number of trades
        #     "1756.87402335",    // Taker buy base volume
        #     "23.24143524",      // Taker buy quote volume
        #     "0"                 // Ignore
        #   ],
        #   ...
        # ]

        rows = []
        for candle in data:
            open_time_ms = candle[0]
            open_p   = float(candle[1])
            high_p   = float(candle[2])
            low_p    = float(candle[3])
            close_p  = float(candle[4])
            volume   = float(candle[5])

            date_str = datetime.fromtimestamp(open_time_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")

            rows.append({
                "timestamp": date_str,
                "open":  round(open_p, 2),
                "high":  round(high_p, 2),
                "low":   round(low_p, 2),
                "close": round(close_p, 2),
                "volume": int(volume),
            })

        print(f"Successfully fetched {len(rows)} daily candles")
        return rows

    except Exception as e:
        print(f"Failed to fetch data from Binance: {e}")
        return None


def save_csv(rows, filename="btc_history.csv"):
    """Save data to CSV file."""
    if not rows:
        print("No data to save")
        return False

    fieldnames = ["timestamp", "open", "high", "low", "close", "volume"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Data saved to: {filename}")
    print(f"Total rows: {len(rows)}")
    print(f"Date range: {rows[0]['timestamp']} to {rows[-1]['timestamp']}")
    return True


def print_sample(rows, n=8):
    """Print first/last N rows as preview."""
    print("\nData preview (first {} rows):".format(n))
    print(f"{'timestamp':<12} {'open':>12} {'high':>12} {'low':>12} {'close':>12} {'volume':>15}")
    print("-" * 80)
    for row in rows[:n]:
        print(f"{row['timestamp']:<12} {row['open']:>12.2f} {row['high']:>12.2f} {row['low']:>12.2f} {row['close']:>12.2f} {row['volume']:>15}")

    if len(rows) > n:
        print("...")
        print(f"Last row: {rows[-1]['timestamp']}  close={rows[-1]['close']:.2f}")


if __name__ == "__main__":
    # Fetch last 500 daily candles from Binance (enough for lookback=200 + pred_len=30)
    rows = fetch_btc_binance(limit=500)

    if rows:
        print_sample(rows, n=8)
        save_csv(rows, filename="btc_history_500days.csv")
        print("\nDone! CSV file is ready to upload to Kronos dashboard!")
        print("Columns: timestamp, open, high, low, close, volume")
    else:
        print("Failed to fetch data. Trying CoinGecko as fallback...")
