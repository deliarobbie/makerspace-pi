import os
import requests

# This file bridges the Pi to the webapp (hosted on Vercel), which owns the
# actual database lookup. The Pi never talks to Postgres/Railway directly.
API_URL = os.environ.get("MAKERSPACE_API_URL", "http://localhost:3000/api/checkin")
API_KEY = os.environ.get("MAKERSPACE_API_KEY", "")

TIMEOUT_SECONDS = 5


def lookup_card(card_id):
    """
    POST a scanned card ID to the webapp and return its decision as a dict,
    e.g. {"status": "green"}. Returns None if the webapp can't be reached
    (e.g. Pi is offline) so callers can fail safe.
    """
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"

    try:
        response = requests.post(
            API_URL,
            json={"card_id": card_id},
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Warning: could not reach webapp at {API_URL} ({e})")
        return None