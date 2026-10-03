#!/usr/bin/env bash
set -euo pipefail

# Navigate to project root
PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"
SERVICE_NAME="makerspace-rfid.service"

if [[ "$(uname -s)" != Linux ]] || ! command -v systemctl >/dev/null; then
    echo "Run this installer on the Raspberry Pi with systemd."
    exit 1
fi
if [[ "$EUID" -eq 0 ]]; then
    echo "Run bash setup.sh as your normal user; it will request sudo when needed."
    exit 1
fi
if [[ "$PROJECT_DIR" == *\"* || "$PROJECT_DIR" == *\\* || "$PROJECT_DIR" == *%* || "$PROJECT_DIR" == *$'\n'* ]]; then
    echo "Use an installation path without quotes, backslashes, percent signs, or newlines."
    exit 1
fi
sudo -v
chmod +x "$PROJECT_DIR/setup.sh"

echo "=== Setting up Makerspace-Pi ==="

# 1. Install python3-venv if missing (Raspberry Pi / Debian)
if command -v apt-get >/dev/null 2>&1 && ! dpkg -s python3-venv >/dev/null 2>&1; then
    echo "Installing python3-venv..."
    sudo apt-get update
    sudo apt-get install -y python3-venv
fi

# 2. Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment (.venv)..."
    python3 -m venv .venv
else
    echo "Virtual environment (.venv) already exists."
fi

# 3. Install requirements into .venv
echo "Installing dependencies from requirements.txt..."
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

# Prompt through /dev/tty because Python reads this program from stdin.
# Secrets stay out of command-line arguments and existing values are preserved.
.venv/bin/python - <<'PY'
from pathlib import Path
from urllib.parse import urlsplit
import getpass
from dotenv import dotenv_values, set_key

path = Path(".env")
values = dotenv_values(path) if path.exists() else {}
with open("/dev/tty", "r") as terminal_input, open("/dev/tty", "w", buffering=1) as terminal_output:
    def prompt(message):
        terminal_output.write(message)
        terminal_output.flush()
        value = terminal_input.readline()
        if not value:
            raise SystemExit("Setup cancelled: no input received.")
        return value.strip()

    updates = {}
    if not values.get("MAKERSPACE_API_URL"):
        while True:
            url = prompt("Full check-in API URL (https://your-site/api/checkin): ")
            parsed = urlsplit(url)
            if parsed.scheme in ("http", "https") and parsed.hostname:
                updates["MAKERSPACE_API_URL"] = url
                break
            terminal_output.write("Enter a complete HTTP or HTTPS URL.\n")
    if not values.get("MAKERSPACE_API_KEY"):
        while True:
            key = getpass.getpass("API key (hidden): ", stream=terminal_output).strip()
            if key:
                updates["MAKERSPACE_API_KEY"] = key
                break
            terminal_output.write("An API key is required.\n")

    if not path.exists():
        path.touch(mode=0o600, exist_ok=False)
    path.chmod(0o600)
    for name, value in updates.items():
        set_key(str(path), name, value, quote_mode="always")
print("API configuration ready; existing values preserved.")
PY

echo "Stop any manually running production/main.py before continuing."
read -r -p "Press Enter once the manual process is stopped..." _confirmation

# Install and validate the definition before reloading systemd. The restart
# below stops an existing instance or starts the service on first installation.

sudo tee "/etc/systemd/system/$SERVICE_NAME" >/dev/null <<EOF
[Unit]
Description=Makerspace RFID and traffic light controller
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=$PROJECT_DIR
ExecStart="$PROJECT_DIR/.venv/bin/python" -u "$PROJECT_DIR/production/main.py"
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
sudo chmod 644 "/etc/systemd/system/$SERVICE_NAME"
if ! sudo systemd-analyze verify "/etc/systemd/system/$SERVICE_NAME"; then
    echo "Service definition failed validation; see the errors above."
    exit 1
fi
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
if ! sudo systemctl restart "$SERVICE_NAME"; then
    sudo systemctl status "$SERVICE_NAME" --no-pager --full || true
    sudo journalctl -u "$SERVICE_NAME" -n 30 --no-pager
    exit 1
fi
sleep 2
if ! sudo systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "Service is not running. Recent logs:"
    sudo journalctl -u "$SERVICE_NAME" -n 30 --no-pager
    exit 1
fi

echo "=== Service running and enabled for boot ==="
echo "Scan a known card and check the lights and check-in result."
echo "Then close the terminal and scan again; reboot and repeat before logging in."
echo "Logs: sudo journalctl -u $SERVICE_NAME -f"

