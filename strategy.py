from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange


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

    df['volume_ma'] = df['volume'].rolling(20).mean()

    latest = df.iloc[-1]

    current_price = latest['close']

    signal = None
    confidence = 0

    # =========================
    # MARKET STATE
    # =========================

    market_state = "SIDEWAYS"

    if latest['ema50'] > latest['ema200']:
        market_state = "BULLISH"

    elif latest['ema50'] < latest['ema200']:
        market_state = "BEARISH"

    # =========================
    # VOLUME CONFIRMATION
    # =========================

    strong_volume = (
        latest['volume'] >
        (latest['volume_ma'] * 0.8)
    )

    # =========================
    # LONG CONDITIONS
    # =========================

    if (

        market_state == "BULLISH"
        and latest['rsi'] > 52
        and strong_volume

    ):

        signal = "LONG"

        confidence = 7.0

        # RSI strength bonus
        if latest['rsi'] > 60:
            confidence += 0.5

        # Strong volume bonus
        if latest['volume'] > (
            latest['volume_ma'] * 1.3
        ):
            confidence += 0.5

        # ATR stoploss
        stoploss = current_price - (
            latest['atr'] * 1.5
        )

        # Targets
        tp1 = current_price + (
            latest['atr'] * 1.5
        )

        tp2 = current_price + (
            latest['atr'] * 3
        )

        tp3 = current_price + (
            latest['atr'] * 5
        )

    # =========================
    # SHORT CONDITIONS
    # =========================

    elif (

        market_state == "BEARISH"
        and latest['rsi'] < 48
        and strong_volume

    ):

        signal = "SHORT"

        confidence = 7.0

        if latest['rsi'] < 40:
            confidence += 0.5

        if latest['volume'] > (
            latest['volume_ma'] * 1.3
        ):
            confidence += 0.5

        stoploss = current_price + (
            latest['atr'] * 1.5
        )

        tp1 = current_price - (
            latest['atr'] * 1.5
        )

        tp2 = current_price - (
            latest['atr'] * 3
        )

        tp3 = current_price - (
            latest['atr'] * 5
        )

    else:

        return {
            "signal": None
        }

    # =========================
    # CLEAN RETURN
    # =========================

    return {

        "signal": signal,

        "price": float(round(current_price, 2)),

        "rsi": float(round(latest['rsi'], 2)),

        "confidence": float(round(confidence, 1)),

        "market_state": market_state,

        "volume": float(round(latest['volume'], 2)),

        "stoploss": float(round(stoploss, 2)),

        "tp1": float(round(tp1, 2)),
        "tp2": float(round(tp2, 2)),
        "tp3": float(round(tp3, 2))
    }