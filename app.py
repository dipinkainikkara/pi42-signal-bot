from market_data import get_candles
from strategy import analyze
from telegram_alerts import send_alert
from chart_generator import generate_chart
from ai_assistant import generate_ai_explanation

import signal_state
import logging
import traceback
import time
import threading
import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# =========================
# LOAD ENV
# =========================

load_dotenv()

BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

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
# REAL PI42 PAIRS
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
    "latest_signal_data"
):

    signal_state.latest_signal_data = {}

# =========================
# SIGNAL LOOP
# =========================

def signal_loop():

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

                    df = get_candles(

                        pair=pair,

                        interval=TIMEFRAME,

                        limit=200
                    )

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

                    result = analyze(df)

                    print(
                        f"Analysis result: {result}",
                        flush=True
                    )

                    if not result:

                        continue

                    if not result.get("signal"):

                        print(
                            f"No signal for {pair}",
                            flush=True
                        )

                        continue

                    if (

                        result["confidence"]

                        < MIN_CONFIDENCE
                    ):

                        print(
                            "Low confidence skipped",
                            flush=True
                        )

                        continue

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

                    signal_state.latest_signal_data = {

                        "pair": pair,

                        "data": result
                    }

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
{direction_emoji} [PI42 FUTURES SIGNAL]

━━━━━━━━━━━━━━

📈 Pair:
{pair}

📊 Signal Type:
{result['signal']}

⏰ Timeframe:
{TIMEFRAME.upper()}

⚡ Suggested Leverage:
{LEVERAGE}

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

🔥 Confidence
{result['confidence']} / 10

━━━━━━━━━━━━━━

🤖 AI Analysis

{ai_analysis}
"""

                    print(
                        f"Generating chart for {pair}",
                        flush=True
                    )

                    chart_path = generate_chart(

                        df,

                        pair
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

# =========================
# /ASK COMMAND
# =========================

async def ask_command(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE
):

    try:

        user_question = " ".join(
            context.args
        )

        if not user_question:

            await update.message.reply_text(

                "Usage:\n/ask your question"
            )

            return

        await update.message.reply_text(

            "Thinking..."
        )

        response = generate_ai_explanation(

            pair="GENERAL",

            signal=user_question,

            rsi=50,

            market_state="GENERAL",

            price=1
        )

        await update.message.reply_text(
            response
        )

    except Exception as e:

        await update.message.reply_text(
            f"AI Error: {e}"
        )

# =========================
# /MARKET COMMAND
# =========================

async def market_command(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE
):

    latest = signal_state.latest_signal_data

    if not latest:

        await update.message.reply_text(
            "No market data yet."
        )

        return

    pair = latest["pair"]

    data = latest["data"]

    message = f"""
📈 Latest Market Signal

Pair: {pair}

Signal: {data['signal']}

Price: ₹{data['price']}

RSI: {data['rsi']}

Market State:
{data['market_state']}
"""

    await update.message.reply_text(
        message
    )

# =========================
# /LATEST COMMAND
# =========================

async def latest_command(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE
):

    latest = signal_state.latest_signal_data

    if not latest:

        await update.message.reply_text(
            "No signals yet."
        )

        return

    pair = latest["pair"]

    data = latest["data"]

    message = f"""
🔥 Latest Signal

Pair: {pair}

Signal: {data['signal']}

Entry: ₹{data['price']}

SL: ₹{data['stoploss']}

TP1: ₹{data['tp1']}
TP2: ₹{data['tp2']}
TP3: ₹{data['tp3']}
"""

    await update.message.reply_text(
        message
    )

# =========================
# START SIGNAL THREAD
# =========================

signal_thread = threading.Thread(

    target=signal_loop,

    daemon=True
)

signal_thread.start()

# =========================
# START TELEGRAM BOT
# =========================

app = ApplicationBuilder().token(
    BOT_TOKEN
).build()

app.add_handler(
    CommandHandler(
        "ask",
        ask_command
    )
)

app.add_handler(
    CommandHandler(
        "market",
        market_command
    )
)

app.add_handler(
    CommandHandler(
        "latest",
        latest_command
    )
)

print(
    "Telegram AI chatbot running...",
    flush=True
)

app.run_polling()