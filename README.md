# Makerspace-Pi

RFID card reader and LED traffic light controller for the makerspace.

## Installation

1. **Create and activate a virtual environment:**

   - **Raspberry Pi / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

   - **Windows:**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

With your virtual environment active:

```bash
python production/main.py
```
