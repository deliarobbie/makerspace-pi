import os
import requests
from urllib.parse import urlsplit, urlunsplit
from dotenv import load_dotenv

# Ensure .env is loaded from the makerspace-pi project root
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(_project_root, ".env"))

# This file bridges the Pi to the webapp (hosted on Vercel), which owns the
# actual database lookup. The Pi never talks to Postgres/Railway directly.
API_URL = os.environ.get("MAKERSPACE_API_URL", "https://makerspacewebapplication.vercel.app/api/checkin")
API_KEY = os.environ.get("MAKERSPACE_API_KEY", "")

TIMEOUT_SECONDS = 5


def lookup_card(card_id, mode="space", resource_id=None):
    """
    POST a scanned card ID to the webapp and return its decision as a dict,
    e.g. {"status": "green"}. Returns None if the webapp can't be reached
    (e.g. Pi is offline) so callers can fail safe.
    """
    if mode not in ("space", "equipment", "studio"):
        raise ValueError("Unknown check-in mode")
    url = API_URL
    payload = {"card_id": card_id}
    if mode != "space":
        parsed = urlsplit(API_URL)
        url = urlunsplit((parsed.scheme, parsed.netloc, f"/api/checkin/{mode}", "", ""))
        payload["resource_id"] = resource_id
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        if not response.ok:
            print(f"Check-in API returned {response.status_code}: {response.text}")
        response.raise_for_status()
        result = response.json()
        if not isinstance(result, dict) or result.get("status") not in ("green", "yellow", "red"):
            raise ValueError("Invalid check-in response")
        if result["status"] == "green" and result.get("ok") is not True:
            raise ValueError("Inconsistent check-in response")
        return result
    except (requests.RequestException, ValueError) as e:
        print(f"Warning: could not reach webapp at {API_URL} ({e})")
        if "localhost" in API_URL or "127.0.0.1" in API_URL:
            print("Hint: MAKERSPACE_API_URL is pointing to localhost. If running on a Raspberry Pi, set MAKERSPACE_API_URL in .env to your deployed Vercel URL or host machine IP.")

        return None
