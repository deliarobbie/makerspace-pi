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

The traffic light plugs into 4 contiguous pins on the left (odd) side of the header (see [docs/gpio_pin_map.png](docs/gpio_pin_map.png)):

| Traffic Light | BCM GPIO | Physical Pin | Header Location |
| :--- | :--- | :--- | :--- |
| **Yellow LED** | GPIO 10 | Pin 19 | 4th pin from Ground |
| **Red LED** | GPIO 9 | Pin 21 | 3rd pin from Ground |
| **Green LED** | GPIO 11 | Pin 23 | 2nd pin from Ground |
| **GND (Ground)** | Ground | Pin 25 | Left side, Ground |

Detailed notes available in [docs/wiring.txt](docs/wiring.txt).
