from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange


def analyze(df):

    # =========================
    # INDICATORS
    # =========================

    df['ema20'] = EMAIndicator(
        close=df['close'],
        window=20
    ).ema_indicator()

    df['ema50'] = EMAIndicator(
        close=df['close'],
        window=50
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

    df['volume_ma'] = df['volume'].rolling(
        20
    ).mean()

    # =========================
    # CLEAN DATA
    # =========================

    df.dropna(inplace=True)

    if len(df) < 50:

        return {
            "signal": None
        }

    latest = df.iloc[-1]

    current_price = float(
        latest['close']
    )

    current_rsi = float(
        latest['rsi']
    )

    current_volume = float(
        latest['volume']
    )

    current_atr = float(
        latest['atr']
    )

    signal = None
    confidence = 0

    # =========================
    # MARKET STATE
    # =========================

    market_state = "SIDEWAYS"

    if latest['ema20'] > latest['ema50']:

        market_state = "BULLISH"

    elif latest['ema20'] < latest['ema50']:

        market_state = "BEARISH"

    # =========================
    # VOLUME CONFIRMATION
    # =========================

    strong_volume = (

        current_volume >

        (latest['volume_ma'] * 0.8)
    )

    # =========================
    # LONG CONDITIONS
    # =========================

    if (

        market_state == "BULLISH"

        and current_rsi > 52

        and strong_volume
    ):

        signal = "LONG"

        confidence = 7.0

        # RSI bonus
        if current_rsi > 60:

            confidence += 0.5

        # Strong volume bonus
        if current_volume > (

            latest['volume_ma'] * 1.3
        ):

            confidence += 0.5

        # Stoploss
        stoploss = current_price - (
            current_atr * 1.5
        )

        # Targets
        tp1 = current_price + (
            current_atr * 1.5
        )

        tp2 = current_price + (
            current_atr * 3
        )

        tp3 = current_price + (
            current_atr * 5
        )

    # =========================
    # SHORT CONDITIONS
    # =========================

    elif (

        market_state == "BEARISH"

        and current_rsi < 48

        and strong_volume
    ):

        signal = "SHORT"

        confidence = 7.0

        # RSI bonus
        if current_rsi < 40:

            confidence += 0.5

        # Strong volume bonus
        if current_volume > (

            latest['volume_ma'] * 1.3
        ):

            confidence += 0.5

        # Stoploss
        stoploss = current_price + (
            current_atr * 1.5
        )

        # Targets
        tp1 = current_price - (
            current_atr * 1.5
        )

        tp2 = current_price - (
            current_atr * 3
        )

        tp3 = current_price - (
            current_atr * 5
        )

    else:

        return {
            "signal": None
        }

    # =========================
    # RETURN SIGNAL
    # =========================

    return {

        "signal": signal,

        "price": round(
            current_price,
            2
        ),

        "rsi": round(
            current_rsi,
            2
        ),

        "confidence": round(
            confidence,
            1
        ),

        "market_state": market_state,

        "volume": round(
            current_volume,
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