import requests
from dotenv import load_dotenv
import os

load_dotenv()


def create_event_nfc(name, time_start, time_end):
    base_url = os.getenv("NFC_BACKEND_URL")
    api_key = os.getenv("NFC_BACKEND_APIKEY")

    url = f"{base_url}/events/create/"
    payload = {
        "name": name,
        "timeStart": time_start,
        "timeEnd": time_end,
        "restricted": False,
        "type": "NHS",
        "api_key": api_key,
    }
    response = requests.post(url, json=payload, timeout=10)
    if response.status_code == 201:
        return response.json()
    else:
        return {
            "error": f"Failed to create event: {response.status_code}, {response.text}"
        }
