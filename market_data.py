import yfinance as yf
import pandas as pd
import requests


# =========================
# FETCH CANDLES
# =========================

def get_candles(symbol="BTC-USD"):

    try:

        # =========================
        # SYMBOL CONVERSION
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

            progress=False
        )

        # =========================
        # EMPTY CHECK
        # =========================

        if df.empty:

            print(
                "Yahoo returned empty dataframe"
            )

            return pd.DataFrame()

        # =========================
        # CLEAN DATAFRAME
        # =========================

        df = df.rename(columns={

            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })

        df = df[[

            "open",
            "high",
            "low",
            "close",
            "volume"
        ]]

        df.dropna(inplace=True)

        return df

    except Exception as e:

        print(
            "MARKET DATA ERROR:",
            e
        )

        return pd.DataFrame()


# =========================
# USDINR RATE
# =========================

def get_usdtinr_rate():

    try:

        url = "https://open.er-api.com/v6/latest/USD"

        response = requests.get(url)

        data = response.json()

        return float(
            data["rates"]["INR"]
        )

    except:

        return 83.0