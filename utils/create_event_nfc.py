import requests
from dotenv import load_dotenv
import os

load_dotenv()


def create_event_nfc(name, time_start, time_end):
    url = f"{os.getenv(
    "NFC_BACKEND_URL",
)
}/create-event/"
    payload = {
        "name": name,
        "timeStart": time_start,
        "timeEnd": time_end,
    }
    response = requests.post(url, json=payload, timeout=10)
    if response.status_code == 201:
        return response.json()
    else:
        return {
            "error": f"Failed to create event: {response.status_code}, {response.text}"
        }
