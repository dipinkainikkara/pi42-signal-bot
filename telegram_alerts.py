import os
import logging
import requests

from dotenv import load_dotenv


# =========================
# LOAD ENV
# =========================

load_dotenv()


# =========================
# LOGGING
# =========================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# =========================
# ENV VARIABLES
# =========================

BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)


# =========================
# VALIDATION
# =========================

if not BOT_TOKEN:

    raise ValueError(
        "Missing TELEGRAM_BOT_TOKEN"
    )

if not CHAT_ID:

    raise ValueError(
        "Missing TELEGRAM_CHAT_ID"
    )


# =========================
# SEND ALERT
# =========================

def send_alert(

    message,

    image_path=None
):

    try:

        # =========================
        # IMAGE ALERT
        # =========================

        if image_path:

            logger.info(
                "Sending image alert..."
            )

            url = (

                f"https://api.telegram.org/bot"

                f"{BOT_TOKEN}/sendPhoto"
            )

            with open(
                image_path,
                "rb"
            ) as photo:

                payload = {

                    "chat_id":
                    CHAT_ID,

                    "caption":
                    message,

                    "parse_mode":
                    "HTML"
                }

                files = {

                    "photo":
                    photo
                }

                response = requests.post(

                    url,

                    data=payload,

                    files=files,

                    timeout=20
                )

        # =========================
        # TEXT ALERT
        # =========================

        else:

            logger.info(
                "Sending text alert..."
            )

            url = (

                f"https://api.telegram.org/bot"

                f"{BOT_TOKEN}/sendMessage"
            )

            payload = {

                "chat_id":
                CHAT_ID,

                "text":
                message,

                "parse_mode":
                "HTML"
            }

            response = requests.post(

                url,

                json=payload,

                timeout=20
            )

        # =========================
        # RESPONSE
        # =========================

        result = response.json()

        logger.info(
            f"Telegram Response: {result}"
        )

        # =========================
        # SUCCESS CHECK
        # =========================

        if not result.get("ok"):

            logger.error(
                f"Telegram API Error: {result}"
            )

        return result

    except Exception as e:

        logger.error(
            f"TELEGRAM ERROR: {e}"
        )

        return None


# =========================
# TEST
# =========================

if __name__ == "__main__":

    send_alert(
        "✅ Pi42 Telegram Alert System Working"
    )