import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_alert(message, image_path=None):

    # Send IMAGE + caption
    if image_path:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

        with open(image_path, "rb") as photo:

            payload = {
                "chat_id": CHAT_ID,
                "caption": message
            }

            files = {
                "photo": photo
            }

            response = requests.post(
                url,
                data=payload,
                files=files
            )

    # Send TEXT only
    else:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        response = requests.post(
            url,
            json=payload
        )

    print(response.json())