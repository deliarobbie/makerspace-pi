# Makerspace-Pi

RFID card reader and LED traffic light controller for the makerspace.

## Setup

### Raspberry Pi (One-Step Script)
```bash
bash setup.sh
```

Run this on the Pi as your normal user, not with `sudo bash`. Connect the reader
and lights and ensure network access first. The installer requests sudo access,
installs dependencies, prompts for missing API URL/key values, and saves them in
`.env` with restricted permissions. Obtain these values from your administrator;
the URL must include `/api/checkin`. Existing values are preserved on reruns.

Stop any manually running `production/main.py` when prompted. Setup installs and
enables `makerspace-rfid.service`, using the actual installation path. The current
`keyboard` library requires the service to run as root. No reader device variable
is needed for this implementation. Setup does not install a dedicated device reader
or provide USB reconnect recovery.

### Verify automatic startup

1. Check `sudo systemctl status makerspace-rfid.service` and view logs with
   `sudo journalctl -u makerspace-rfid.service -f`.
2. Scan a known card and confirm the expected LEDs and check-in result.
3. Close the terminal or disconnect SSH and scan again.
4. Run `sudo reboot`; scan after boot before logging in. Inspect boot logs with
   `sudo journalctl -u makerspace-rfid.service -b --no-pager` if needed.

A running service alone does not verify the hardware. Ctrl+C exits the log viewer
without stopping the service. For manual testing, first run
`sudo systemctl stop makerspace-rfid.service` to avoid duplicate scans. Resume with
`sudo systemctl start makerspace-rfid.service`. After code or `.env` changes, use
`sudo systemctl restart makerspace-rfid.service`. To remove boot startup, use
`sudo systemctl disable --now makerspace-rfid.service`.

The current program only handles Ctrl+C cleanup; clean service shutdown and reader
reconnection remain separate improvements. To change API settings, edit `.env`
and restart the service. Never commit that file or share logs containing card IDs
and names outside the intended administration team.

---

### Manual Setup (or Windows)
1. **Create & activate virtual environment:**
   - **Linux / Pi:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows:**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   nano .env  # set MAKERSPACE_API_URL and MAKERSPACE_API_KEY
   ```

## Running the Application

- **Raspberry Pi:**
  *(Must point `sudo` directly to `.venv` so `keyboard` has root permissions to capture USB keystrokes)*
  ```bash
  sudo .venv/bin/python production/main.py
  ```

- **Windows (Mock / Dev Mode):**
  ```powershell
  python production\main.py
  ```

## Hardware Wiring

The traffic light plugs into 4 contiguous pins on the left (odd) side of the header (see [docs/gpio_pin_map.png](docs/gpio_pin_map.png)):

| Traffic Light | BCM GPIO | Physical Pin | Header Location |
| :--- | :--- | :--- | :--- |
| **Yellow LED** | GPIO 10 | Pin 19 | 4th pin from Ground |
| **Red LED** | GPIO 9 | Pin 21 | 3rd pin from Ground |
| **Green LED** | GPIO 11 | Pin 23 | 2nd pin from Ground |
| **GND (Ground)** | Ground | Pin 25 | Left side, Ground |

Detailed notes available in [docs/wiring.txt](docs/wiring.txt).
