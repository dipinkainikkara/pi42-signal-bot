from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

import random


def analyze(df):

    # =========================
    # INDICATORS
    # =========================

    df['ema50'] = EMAIndicator(
        close=df['close'],
        window=50
    ).ema_indicator()

    df['ema200'] = EMAIndicator(
        close=df['close'],
        window=200
    ).ema_indicator()

    df['rsi'] = RSIIndicator(
        close=df['close'],
        window=14
    ).rsi()

    df['atr'] = AverageTrueRange(
        high=df['high'],
        low=df['low'],
        close=df['close'],
        window=14
    ).average_true_range()

    latest = df.iloc[-1]

    # =========================
    # BASIC VALUES
    # =========================

    current_price = float(
        latest['close']
    )

    atr = float(
        latest['atr']
    )

    rsi = float(
        latest['rsi']
    )

    volume = float(
        latest['volume']
    )

    # =========================
    # RANDOM TEST SIGNAL
    # =========================

    signal = random.choice([
        "LONG",
        "SHORT"
    ])

    # =========================
    # MARKET STATE
    # =========================

    market_state = (
        "BULLISH"
        if signal == "LONG"
        else "BEARISH"
    )

    # =========================
    # RANDOM CONFIDENCE
    # =========================

    confidence = round(
        random.uniform(7.0, 9.5),
        1
    )

    # =========================
    # LONG TEST
    # =========================

    if signal == "LONG":

        stoploss = current_price - (
            atr * 1.5
        )

        tp1 = current_price + (
            atr * 1.5
        )

        tp2 = current_price + (
            atr * 3
        )

        tp3 = current_price + (
            atr * 5
        )

    # =========================
    # SHORT TEST
    # =========================

    else:

        stoploss = current_price + (
            atr * 1.5
        )

        tp1 = current_price - (
            atr * 1.5
        )

        tp2 = current_price - (
            atr * 3
        )

        tp3 = current_price - (
            atr * 5
        )

    # =========================
    # RETURN TEST SIGNAL
    # =========================

    return {

        "signal": signal,

        "price": round(
            current_price,
            2
        ),

        "rsi": round(
            rsi,
            2
        ),

        "confidence": confidence,

        "market_state": market_state,

        "volume": round(
            volume,
            2
        ),

        "stoploss": round(
            stoploss,
            2
        ),

        "tp1": round(
            tp1,
            2
        ),

        "tp2": round(
            tp2,
            2
        ),

        "tp3": round(
            tp3,
            2
        )
    }