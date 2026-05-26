import os
import google.generativeai as genai

from dotenv import load_dotenv


# =========================
# LOAD ENV
# =========================

load_dotenv()


# =========================
# GEMINI CONFIG
# =========================

genai.configure(

    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)


# =========================
# MODEL
# =========================

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# =========================
# AI EXPLANATION
# =========================

def generate_ai_explanation(

    pair,
    signal,
    rsi,
    market_state,
    price
):

    try:

        prompt = f"""

You are a professional crypto futures analyst.

Analyze this trading signal briefly.

PAIR: {pair}

SIGNAL: {signal}

RSI: {rsi}

MARKET STATE: {market_state}

PRICE: {price}

Explain:
- why signal triggered
- current momentum
- risk level
- what trader should watch

Keep response concise and beginner friendly.

"""

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        print(
            f"AI ERROR: {e}",
            flush=True
        )

        return "AI analysis unavailable."