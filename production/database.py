import os
import requests
from dotenv import load_dotenv

# Ensure .env is loaded from the makerspace-pi project root
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(_project_root, ".env"))

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
        if "localhost" in API_URL or "127.0.0.1" in API_URL:
            print("Hint: MAKERSPACE_API_URL is pointing to localhost. If running on a Raspberry Pi, set MAKERSPACE_API_URL in .env to your deployed Vercel URL or host machine IP.")

        return None