from market_data import get_candles
from strategy import analyze
from telegram_alerts import send_alert
from chart_generator import generate_chart
from ai_assistant import generate_ai_explanation

import signal_state
import logging
import traceback
import time


# =========================
# STARTUP
# =========================

print("BOT STARTED", flush=True)


# =========================
# LOGGING
# =========================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# =========================
# SETTINGS
# =========================

TIMEFRAME = "15m"

CHECK_INTERVAL = 900

LEVERAGE = "5x"

MIN_CONFIDENCE = 6.5


# =========================
# PAIRS
# =========================

PAIRS = [

    "BTCINR",

    "ETHINR",

    "SOLINR"
]


# =========================
# SIGNAL STORAGE
# =========================

if not hasattr(
    signal_state,
    "last_signals"
):

    signal_state.last_signals = {}

if not hasattr(
    signal_state,
    "signal_cooldowns"
):

    signal_state.signal_cooldowns = {}


# =========================
# MAIN LOOP
# =========================

while True:

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

    try:

        for pair in PAIRS:

            try:

                print(
                    f"Checking {pair}",
                    flush=True
                )

                # =========================
                # FETCH MARKET DATA
                # =========================

                df = get_candles(

                    pair=pair,

                    interval=TIMEFRAME,

                    limit=200
                )

                # =========================
                # EMPTY CHECK
                # =========================

                if df.empty:

                    print(
                        f"No candle data for {pair}",
                        flush=True
                    )

                    continue

                print(
                    f"Fetched {len(df)} candles",
                    flush=True
                )

                # =========================
                # STRATEGY ANALYSIS
                # =========================

                result = analyze(df)

                print(
                    f"Analysis result: {result}",
                    flush=True
                )

                # =========================
                # NO SIGNAL
                # =========================

                if not result:

                    continue

                if not result.get("signal"):

                    print(
                        f"No signal for {pair}",
                        flush=True
                    )

                    continue

                # =========================
                # CONFIDENCE FILTER
                # =========================

                if (

                    result["confidence"]

                    < MIN_CONFIDENCE
                ):

                    print(
                        f"Low confidence skipped",
                        flush=True
                    )

                    continue

                # =========================
                # DUPLICATE FILTER
                # =========================

                previous_signal = (

                    signal_state.last_signals.get(
                        pair
                    )
                )

                if (

                    previous_signal

                    == result["signal"]
                ):

                    print(
                        f"Duplicate signal skipped for {pair}",
                        flush=True
                    )

                    continue

                # =========================
                # SAVE SIGNAL
                # =========================

                signal_state.last_signals[
                    pair
                ] = result["signal"]

                # =========================
                # AI ANALYSIS
                # =========================

                print(
                    f"Generating AI analysis for {pair}",
                    flush=True
                )

                try:

                    ai_analysis = generate_ai_explanation(

                        pair=pair,

                        signal=result["signal"],

                        rsi=result["rsi"],

                        market_state=result["market_state"],

                        price=result["price"]
                    )

                except Exception as ai_error:

                    print(
                        f"AI ERROR: {ai_error}",
                        flush=True
                    )

                    ai_analysis = (
                        "AI analysis unavailable."
                    )

                print(
                    "AI analysis completed",
                    flush=True
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
{direction_emoji} PI42 {result['signal']} SIGNAL

━━━━━━━━━━━━━━
📈 Pair: {pair}
⏰ Timeframe: {TIMEFRAME.upper()}
⚡ Suggested Leverage: {LEVERAGE}
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
{round(result['volume'], 2)}

━━━━━━━━━━━━━━
📉 EMA Fast
{result['ema20']}

📈 EMA Slow
{result['ema50']}

━━━━━━━━━━━━━━
🔥 Confidence
{result['confidence']} / 10

━━━━━━━━━━━━━━
🤖 AI Analysis

{ai_analysis}

━━━━━━━━━━━━━━
⚠️ Risk Managed Setup
"""

                # =========================
                # GENERATE CHART
                # =========================

                print(
                    f"Generating chart for {pair}",
                    flush=True
                )

                chart_path = generate_chart(

                    df,

                    pair
                )

                print(
                    f"Chart generated: {chart_path}",
                    flush=True
                )

                # =========================
                # SEND ALERT
                # =========================

                print(
                    f"Sending Telegram alert for {pair}",
                    flush=True
                )

                send_alert(

                    message,

                    image_path=chart_path
                )

                print(
                    f"Signal sent successfully for {pair}",
                    flush=True
                )

            except Exception as pair_error:

                print(
                    f"\nPAIR ERROR ({pair})",
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
            "\nMAIN LOOP ERROR",
            flush=True
        )

        print(
            str(main_error),
            flush=True
        )

        traceback.print_exc()

    print(
        f"\nSleeping for {CHECK_INTERVAL} seconds...\n",
        flush=True
    )

    time.sleep(CHECK_INTERVAL)