"""Check the Pi's resource API connection without displaying its API key."""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import requests
from dotenv import dotenv_values


def main():
    path = Path(__file__).resolve().parents[1] / ".env"
    values = dotenv_values(path)
    key = values.get("MAKERSPACE_API_KEY") or ""
    base = urlsplit(values.get("MAKERSPACE_API_URL") or "")

    print("Config file:", path)
    print("Key present:", bool(key))
    print("Key has surrounding whitespace:", key != key.strip())
    if base.scheme not in ("http", "https") or not base.hostname or base.username or base.password:
        print("Configure MAKERSPACE_API_URL as an HTTP(S) URL without embedded credentials.")
        return 1
    if not key:
        print("Configure MAKERSPACE_API_KEY in the Pi's .env.")
        return 1

    url = urlunsplit((base.scheme, base.netloc, "/api/rfid/resources", "", ""))
    print("Target:", url)
    try:
        response = requests.get(
            url,
            params={"mode": "equipment"},
            headers={"Authorization": f"Bearer {key}"},
            allow_redirects=False,
            timeout=10,
        )
    except requests.RequestException as error:
        # Avoid printing exception text, which can contain request details.
        print("Request failed:", type(error).__name__)
        return 1

    print("Status:", response.status_code)
    print("Redirect present:", "Location" in response.headers)
    if response.is_redirect:
        print("The server redirects this URL. Configure the final server address directly.")
    elif response.status_code == 200:
        print("Authentication and resource listing succeeded.")
    elif response.status_code == 401:
        print("This server rejected the key read from the config file above.")
    elif response.status_code == 503:
        print("The server has no configured RFID API key.")
    else:
        print("Check the web server logs for this request.")
    return 0 if response.status_code == 200 else 1


if __name__ == "__main__":
    raise SystemExit(main())
