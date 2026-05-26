from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange


def analyze(df):

    try:

        if df.empty:

            return {
                "signal": None
            }

        df = df.copy()

        # =========================
        # BALANCED INDICATORS
        # =========================

        df["ema_fast"] = EMAIndicator(
            close=df["close"],
            window=9
        ).ema_indicator()

        df["ema_slow"] = EMAIndicator(
            close=df["close"],
            window=21
        ).ema_indicator()

        df["rsi"] = RSIIndicator(
            close=df["close"],
            window=10
        ).rsi()

        df["atr"] = AverageTrueRange(
            high=df["high"],
            low=df["low"],
            close=df["close"],
            window=10
        ).average_true_range()

        # =========================
        # VOLUME MA
        # =========================

        df["volume_ma"] = (
            df["volume"]
            .rolling(20)
            .mean()
        )

        df.dropna(inplace=True)

        if len(df) < 30:

            return {
                "signal": None
            }

        latest = df.iloc[-1]

        current_price = float(
            latest["close"]
        )

        current_rsi = float(
            latest["rsi"]
        )

        current_atr = float(
            latest["atr"]
        )

        current_volume = float(
            latest["volume"]
        )

        volume_ma = float(
            latest["volume_ma"]
        )

        ema_fast = float(
            latest["ema_fast"]
        )

        ema_slow = float(
            latest["ema_slow"]
        )

        signal = None

        confidence = 7.0

        market_state = "SIDEWAYS"

        # =========================
        # VOLUME FILTER
        # =========================

        strong_volume = (
            current_volume >
            (volume_ma * 0.8)
        )

        # =========================
        # LONG
        # =========================

        if (

            ema_fast > ema_slow

            and current_rsi >= 52

            and strong_volume
        ):

            signal = "LONG"

            market_state = "BULLISH"

            if current_rsi > 60:
                confidence += 0.5

        # =========================
        # SHORT
        # =========================

        elif (

            ema_fast < ema_slow

            and current_rsi <= 48

            and strong_volume
        ):

            signal = "SHORT"

            market_state = "BEARISH"

            if current_rsi < 40:
                confidence += 0.5

        else:

            return {
                "signal": None
            }

        # =========================
        # LONG TARGETS
        # =========================

        if signal == "LONG":

            stoploss = (
                current_price -
                (current_atr * 1.3)
            )

            tp1 = (
                current_price +
                (current_atr * 1.3)
            )

            tp2 = (
                current_price +
                (current_atr * 2.5)
            )

            tp3 = (
                current_price +
                (current_atr * 4)
            )

        # =========================
        # SHORT TARGETS
        # =========================

        else:

            stoploss = (
                current_price +
                (current_atr * 1.3)
            )

            tp1 = (
                current_price -
                (current_atr * 1.3)
            )

            tp2 = (
                current_price -
                (current_atr * 2.5)
            )

            tp3 = (
                current_price -
                (current_atr * 4)
            )

        return {

            "signal":
            signal,

            "price":
            round(current_price, 2),

            "rsi":
            round(current_rsi, 2),

            "confidence":
            round(confidence, 1),

            "market_state":
            market_state,

            "volume":
            round(current_volume, 2),

            "ema20":
            round(ema_fast, 2),

            "ema50":
            round(ema_slow, 2),

            "atr":
            round(current_atr, 2),

            "stoploss":
            round(stoploss, 2),

            "tp1":
            round(tp1, 2),

            "tp2":
            round(tp2, 2),

            "tp3":
            round(tp3, 2)
        }

    except Exception as e:

        print(f"STRATEGY ERROR: {e}")

        return {
            "signal": None
        }