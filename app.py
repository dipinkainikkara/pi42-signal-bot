from market_data import (
    get_candles,
    get_usdtinr_rate
)

from strategy import analyze
from telegram_alerts import send_alert
from chart_generator import generate_chart

import signal_state
import time
import traceback


print("BOT STARTED", flush=True)


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

        print(
            "\n=========================",
            flush=True
        )

        print(
            "MAIN LOOP RUNNING",
            flush=True
        )

        print(
            "=========================\n",
            flush=True
        )

        for market_symbol, display_symbol in SYMBOLS:

            try:

                print(
                    f"\nChecking {display_symbol}...",
                    flush=True
                )

                # =========================
                # FETCH MARKET DATA
                # =========================

                print(
                    f"Fetching candles for {market_symbol}",
                    flush=True
                )

                df = get_candles(
                    symbol=market_symbol
                )

                # =========================
                # EMPTY DATA PROTECTION
                # =========================

                if df.empty:

                    print(
                        f"No candle data for {display_symbol}",
                        flush=True
                    )

                    continue

                print(
                    f"Fetched {len(df)} candles",
                    flush=True
                )

                # =========================
                # NOT ENOUGH DATA
                # =========================

                if len(df) < 50:

                    print(
                        f"Not enough candles for {display_symbol}",
                        flush=True
                    )

                    continue

                # =========================
                # ANALYZE STRATEGY
                # =========================

                print(
                    "Running strategy analysis...",
                    flush=True
                )

                result = analyze(df)

                print(
                    f"Analysis result: {result}",
                    flush=True
                )

                # =========================
                # INVALID RESULT
                # =========================

                if not result:

                    print(
                        f"No analysis result for {display_symbol}",
                        flush=True
                    )

                    continue

                # =========================
                # NO SIGNAL
                # =========================

                if not result.get("signal"):

                    print(
                        f"No signal for {display_symbol}",
                        flush=True
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
                        f"Duplicate signal skipped for {display_symbol}",
                        flush=True
                    )

                    continue

                # =========================
                # SAVE SIGNAL
                # =========================

                signal_state.last_signals[
                    display_symbol
                ] = result["signal"]

                # =========================
                # INR CONVERSION
                # =========================

                print(
                    "Fetching USDINR rate...",
                    flush=True
                )

                usdtinr = get_usdtinr_rate()

                print(
                    f"USDINR Rate: {usdtinr}",
                    flush=True
                )

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

                print(
                    "Generating chart...",
                    flush=True
                )

                chart_path = generate_chart(
                    df,
                    display_symbol
                )

                print(
                    f"Chart generated: {chart_path}",
                    flush=True
                )

                # =========================
                # SEND TELEGRAM ALERT
                # =========================

                print(
                    "Sending Telegram alert...",
                    flush=True
                )

                send_alert(
                    message,
                    image_path=chart_path
                )

                print(
                    f"Signal sent successfully for {display_symbol}",
                    flush=True
                )

            except Exception as pair_error:

                print(
                    f"\nPAIR ERROR ({display_symbol}):",
                    flush=True
                )

                print(
                    str(pair_error),
                    flush=True
                )

                traceback.print_exc()

                continue

    except Exception as main_error:

        print(
            "\nMAIN LOOP ERROR:",
            flush=True
        )

        print(
            str(main_error),
            flush=True
        )

        traceback.print_exc()

    # =========================
    # WAIT 5 MINUTES
    # =========================

    print(
        "\nSleeping for 5 minutes...\n",
        flush=True
    )

    time.sleep(300)