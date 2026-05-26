from market_data import (
    get_candles,
    get_usdtinr_rate
)

from strategy import analyze
from telegram_alerts import send_alert
from chart_generator import generate_chart

import signal_state
import time


# =========================
# SYMBOL MAPPING
# =========================

SYMBOLS = [

    ("BTCUSDT", "BTCINR"),

    ("ETHUSDT", "ETHINR"),

    ("SOLUSDT", "SOLINR")
]


# =========================
# MAIN LOOP
# =========================

while True:

    try:

        for market_symbol, display_symbol in SYMBOLS:

            print(f"\nChecking {display_symbol}...")

            # =========================
            # FETCH MARKET DATA
            # =========================

            df = get_candles(
                symbol=market_symbol
            )

            # =========================
            # ANALYZE STRATEGY
            # =========================

            result = analyze(df)

            print(result)

            # =========================
            # NO SIGNAL
            # =========================

            if not result["signal"]:

                print(
                    f"No signal for {display_symbol}"
                )

                continue

            # =========================
            # DUPLICATE PROTECTION
            # =========================

            previous_signal = (
                signal_state.last_signals.get(
                    display_symbol
                )
            )

            if previous_signal == result["signal"]:

                print(
                    f"Duplicate signal skipped for {display_symbol}"
                )

                continue

            # Save latest signal
            signal_state.last_signals[
                display_symbol
            ] = result["signal"]

            # =========================
            # USD → INR CONVERSION
            # =========================

            usdtinr = get_usdtinr_rate()

            result["price"] = round(
                result["price"] * usdtinr,
                2
            )

            result["stoploss"] = round(
                result["stoploss"] * usdtinr,
                2
            )

            result["tp1"] = round(
                result["tp1"] * usdtinr,
                2
            )

            result["tp2"] = round(
                result["tp2"] * usdtinr,
                2
            )

            result["tp3"] = round(
                result["tp3"] * usdtinr,
                2
            )

            # =========================
            # EMOJIS
            # =========================

            direction_emoji = (
                "🟢"
                if result["signal"] == "LONG"
                else "🔴"
            )

            market_emoji = (
                "📈"
                if result["market_state"] == "BULLISH"
                else "📉"
            )

            # =========================
            # TELEGRAM MESSAGE
            # =========================

            message = f"""
{direction_emoji} HIGH CONFIDENCE {result['signal']}

━━━━━━━━━━━━━━
📈 Pair: {display_symbol}
⏰ Timeframe: 15M
⚡ Suggested Leverage: 5x
━━━━━━━━━━━━━━

💰 Entry
₹{result['price']}

🛑 Stoploss
₹{result['stoploss']}

🎯 Targets

TP1 → ₹{result['tp1']}
TP2 → ₹{result['tp2']}
TP3 → ₹{result['tp3']}

━━━━━━━━━━━━━━
📊 Market State
{market_emoji} {result['market_state']}

📌 RSI
{result['rsi']}

📦 Volume
{result['volume']}

━━━━━━━━━━━━━━
🔥 Confidence
{result['confidence']} / 10

⚠️ Risk Managed Setup
"""

            # =========================
            # GENERATE CHART
            # =========================

            chart_path = generate_chart(
                df,
                display_symbol
            )

            # =========================
            # SEND TELEGRAM ALERT
            # =========================

            send_alert(
                message,
                image_path=chart_path
            )

            print(
                f"Signal sent for {display_symbol}"
            )

    except Exception as e:

        print("ERROR:", e)

    # =========================
    # WAIT 15 MINUTES
    # =========================

    time.sleep(300)