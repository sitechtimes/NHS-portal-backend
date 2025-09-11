import requests


def create_event_nfc(name, time_start, time_end, description):
    url = "http://localhost:8000/api/backend/events/"
    payload = {
        "name": name,
        "timeStart": time_start,
        "timeEnd": time_end,
        "description": description,
    }
    response = requests.post(url, json=payload, timeout=10)
    if response.status_code == 201:
        return response.json()
    else:
        return {
            "error": f"Failed to create event: {response.status_code}, {response.text}"
        }
