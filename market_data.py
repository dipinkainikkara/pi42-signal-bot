import requests
import pandas as pd


# =========================
# FETCH CANDLES
# =========================

def get_candles(

    symbol="BTCUSDT",
    interval="15m",
    limit=200

):

    try:

        url = "https://api.binance.com/api/v3/klines"

        headers = {

            "User-Agent":
            "Mozilla/5.0"
        }

        params = {

            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        response = requests.get(

            url,

            params=params,

            headers=headers,

            timeout=15
        )

        print(
            f"Binance Status Code: {response.status_code}",
            flush=True
        )

        # =========================
        # INVALID RESPONSE
        # =========================

        if response.status_code != 200:

            print(
                f"Binance Error: {response.text}",
                flush=True
            )

            return pd.DataFrame()

        data = response.json()

        # =========================
        # EMPTY DATA
        # =========================

        if not data:

            print(
                "No candle data returned",
                flush=True
            )

            return pd.DataFrame()

        # =========================
        # CREATE DATAFRAME
        # =========================

        df = pd.DataFrame(

            data,

            columns=[

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
            ]
        )

        # =========================
        # CONVERT NUMBERS
        # =========================

        numeric_columns = [

            "open",
            "high",
            "low",
            "close",
            "volume"
        ]

        for col in numeric_columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        # =========================
        # DROP BAD ROWS
        # =========================

        df.dropna(inplace=True)

        print(
            f"Final candles count: {len(df)}",
            flush=True
        )

        return df

    except Exception as e:

        print(
            f"Market data error: {e}",
            flush=True
        )

        return pd.DataFrame()


# =========================
# USD → INR
# =========================

def get_usdtinr_rate():

    try:

        url = "https://api.exchangerate-api.com/v4/latest/USD"

        response = requests.get(

            url,

            timeout=10
        )

        data = response.json()

        rate = data["rates"]["INR"]

        return float(rate)

    except Exception as e:

        print(
            f"USDINR API Error: {e}",
            flush=True
        )

        return 83.0