import requests
from dotenv import load_dotenv
import os

load_dotenv()


def create_event_nfc(name, time_start, time_end):
    key = login_nfc()
    if not key:
        return {"error": "Failed to authenticate with NFC backend"}
    url = f"{os.getenv('NFC_BACKEND_URL')}/events/create/"
    # url = f"http://localhost:9000/events/create/"
    payload = {
        "name": name,
        "timeStart": time_start,
        "timeEnd": time_end,
        "restricted": False,
        "type": "NHS",
    }
    headers = {"Authorization": f"Bearer {key}"}
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    if response.status_code == 201:
        return response.json()
    else:
        return {
            "error": f"Failed to create event: {response.status_code}, {response.text}"
        }


def login_nfc():
    # url = f"{os.getenv('NFC_BACKEND_URL')}/auth/login/"
    url = f"http://localhost:9000/auth/login/"
    payload = {
        "username": os.getenv("NFC_BACKEND_USERNAME"),
        "password": os.getenv("NFC_BACKEND_PASSWORD"),
    }
    response = requests.post(url, json=payload, timeout=10)
    if response.json().get("key"):
        return response.json().get("key")
    else:
        return None
