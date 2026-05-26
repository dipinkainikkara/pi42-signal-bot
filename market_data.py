import requests
import pandas as pd


# =========================
# FETCH CRYPTO CANDLES
# =========================

def get_candles(symbol="ETHUSDT", interval="15m", limit=200):

    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    df = pd.DataFrame(data, columns=[

        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base",
        "taker_buy_quote",
        "ignore"
    ])

    numeric_cols = [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    for col in numeric_cols:
        df[col] = df[col].astype(float)

    return df


# =========================
# USD TO INR RATE
# =========================

def get_usdtinr_rate():

    try:

        url = "https://api.exchangerate-api.com/v4/latest/USD"

        response = requests.get(url)

        data = response.json()

        return data["rates"]["INR"]

    except:

        # fallback rate
        return 83.0