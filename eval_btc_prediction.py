#!/usr/bin/env python3
"""
Compare Kronos prediction vs actual BTC price
"""

import json
import csv
import numpy as np
from datetime import datetime, timezone, timedelta

try:
    from urllib.request import urlopen, Request
except ImportError:
    import urllib2 as urllib


def fetch_btc_actual(start_date, end_date):
    """
    Fetch actual BTC/USDT daily K-line for date range.
    start_date, end_date: 'YYYY-MM-DD' format
    """
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=1000"

    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        results = {}
        start_dt = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end_dt   = datetime.strptime(end_date,   "%Y-%m-%d").replace(tzinfo=timezone.utc) + timedelta(days=1)

        for candle in data:
            open_time_ms = candle[0]
            dt = datetime.fromtimestamp(open_time_ms / 1000, tz=timezone.utc)
            if start_dt <= dt < end_dt:
                date_str    = dt.strftime("%Y-%m-%d")
                open_p     = float(candle[1])
                high_p     = float(candle[2])
                low_p      = float(candle[3])
                close_p    = float(candle[4])
                volume     = float(candle[5])
                results[date_str] = {
                    "open":  round(open_p, 2),
                    "high":  round(high_p, 2),
                    "low":   round(low_p, 2),
                    "close": round(close_p, 2),
                    "volume": int(volume),
                }

        print(f"Fetched actual data for {len(results)} days")
        return results

    except Exception as e:
        print(f"Failed to fetch actual data: {e}")
        return {}


def load_predictions(csv_path):
    """Read prediction CSV"""
    results = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("timestamps"):
                continue
            ds = row["timestamps"].strip()
            results[ds] = {
                "open":   float(row["open"]),
                "high":   float(row["high"]),
                "low":    float(row["low"]),
                "close":  float(row["close"]),
                "volume": float(row["volume"]),
            }
    print(f"Loaded {len(results)} prediction rows")
    return results


def evaluate(preds, actuals):
    """Calculate error metrics"""
    dates = sorted([d for d in preds if d in actuals])
    if not dates:
        print("No overlapping dates found!")
        return None

    print("")
    print("=" * 70)
    print(f"Comparison date count: {len(dates)}")
    print("=" * 70)

    pred_closes  = []
    actual_closes = []
    errors = []

    header = f"  {'Date':<12} {'Pred_Close':>14} {'Actual_Close':>14} {'Error':>14} {'Error%':>10}"
    print(header)
    print("-" * 70)

    for d in dates:
        p = preds[d]["close"]
        a = actuals[d]["close"]
        e = p - a
        epct = (e / a) * 100
        pred_closes.append(p)
        actual_closes.append(a)
        errors.append(e)
        print(f"  {d:<12} {p:>14.2f} {a:>14.2f} {e:>+14.2f} {epct:>+9.2f}%")

    pred_closes  = np.array(pred_closes)
    actual_closes = np.array(actual_closes)
    errors = np.array(errors)

    mae   = np.mean(np.abs(errors))
    rmse  = np.sqrt(np.mean(errors ** 2))
    mape  = np.mean(np.abs(errors) / actual_closes) * 100
    smape = np.mean(2 * np.abs(errors) / (np.abs(pred_closes) + np.abs(actual_closes))) * 100

    # Direction accuracy (up/down)
    pred_direction  = np.sign(np.diff(pred_closes))
    actual_direction = np.sign(np.diff(actual_closes))
    direction_acc = np.mean(pred_direction == actual_direction) * 100 if len(pred_direction) > 0 else 0

    print("")
    print("=" * 70)
    print("Error Metrics Summary")
    print("=" * 70)
    print(f"  MAE           : {mae:.2f}  (Mean Absolute Error)")
    print(f"  RMSE          : {rmse:.2f}  (Root Mean Square Error)")
    print(f"  MAPE          : {mape:.2f}% (Mean Absolute % Error)")
    print(f"  SMAPE         : {smape:.2f}% (Symmetric MAPE)")
    print(f"  Direction Acc : {direction_acc:.1f}% (Up/Down accuracy)")
    print("=" * 70)

    # Output comparison CSV
    output_rows = []
    for d in dates:
        output_rows.append({
            "date":         d,
            "pred_close":   round(preds[d]["close"], 2),
            "actual_close":  round(actuals[d]["close"], 2),
            "error":        round(preds[d]["close"] - actuals[d]["close"], 2),
            "error_pct":    round((preds[d]["close"] - actuals[d]["close"]) / actuals[d]["close"] * 100, 2),
        })

    out_file = "btc_pred_vs_actual.csv"
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "pred_close", "actual_close", "error", "error_pct"])
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"\nDetailed comparison saved to: {out_file}")
    return out_file


if __name__ == "__main__":
    import sys
    import glob
    import os

    # Auto-detect prediction file
    if len(sys.argv) > 1:
        pred_file = sys.argv[1]
    else:
        # Look for kronos_prediction_*.csv in current dir
        matches = sorted(glob.glob("kronos_prediction_*.csv"))
        if matches:
            pred_file = matches[-1]  # use the latest
        else:
            print("Usage: python eval_btc_prediction.py <prediction.csv>")
            print("       Or place a kronos_prediction_*.csv file in the current directory.")
            exit(1)

    if not os.path.exists(pred_file):
        print(f"File not found: {pred_file}")
        exit(1)

    print("Loading prediction file...")
    preds = load_predictions(pred_file)

    if not preds:
        print("No prediction data loaded, exit.")
        exit(1)

    dates = sorted(preds.keys())
    start_date = dates[0]
    end_date   = dates[-1]
    print(f"Prediction range: {start_date} ~ {end_date}")

    print("\nFetching actual BTC prices from Binance...")
    actuals = fetch_btc_actual(start_date, end_date)

    if not actuals:
        print("Failed to fetch actual data.")
        exit(1)

    out_file = evaluate(preds, actuals)
    print("\nDone!")
