# Makerspace-Pi

RFID card reader and LED traffic light controller for the makerspace.

## Setup

### Raspberry Pi (One-Step Script)
```bash
chmod +x setup.sh
./setup.sh
```

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
See [docs/wiring.txt](docs/wiring.txt) and [docs/gpio_pin_map.png](docs/gpio_pin_map.png) for traffic light pin connections.
