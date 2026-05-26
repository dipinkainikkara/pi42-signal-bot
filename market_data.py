import yfinance as yf
import pandas as pd
import requests


# =========================
# FETCH CANDLES
# =========================

def get_candles(symbol="BTCUSDT"):

    try:

        # =========================
        # SYMBOL MAPPING
        # =========================

        mapping = {

            "BTCUSDT": "BTC-USD",
            "ETHUSDT": "ETH-USD",
            "SOLUSDT": "SOL-USD"
        }

        yf_symbol = mapping.get(
            symbol,
            "BTC-USD"
        )

        # =========================
        # DOWNLOAD DATA
        # =========================

        df = yf.download(

            yf_symbol,

            interval="15m",

            period="2d",

            auto_adjust=False,

            progress=False
        )

        # =========================
        # EMPTY CHECK
        # =========================

        if df.empty:

            print(
                "Yahoo returned empty dataframe",
                flush=True
            )

            return pd.DataFrame()

        # =========================
        # FLATTEN COLUMNS
        # =========================

        df.columns = [

            col[0]
            if isinstance(col, tuple)
            else col
            for col in df.columns
        ]

        # =========================
        # RENAME COLUMNS
        # =========================

        df = df.rename(columns={

            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })

        # =========================
        # KEEP ONLY REQUIRED
        # =========================

        df = df[[

            "open",
            "high",
            "low",
            "close",
            "volume"
        ]]

        # =========================
        # FORCE 1D SERIES
        # =========================

        for col in [

            "open",
            "high",
            "low",
            "close",
            "volume"
        ]:

            df[col] = pd.Series(
                df[col]
            ).astype(float)

        # =========================
        # CLEAN DATA
        # =========================

        df.dropna(inplace=True)

        print(
            f"Final candles count: {len(df)}",
            flush=True
        )

        return df

    except Exception as e:

        print(
            f"MARKET DATA ERROR: {e}",
            flush=True
        )

        return pd.DataFrame()


# =========================
# USD → INR RATE
# =========================

def get_usdtinr_rate():

    try:

        url = "https://open.er-api.com/v6/latest/USD"

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        return float(
            data["rates"]["INR"]
        )

    except Exception as e:

        print(
            f"USDINR API Error: {e}",
            flush=True
        )

        return 83.0