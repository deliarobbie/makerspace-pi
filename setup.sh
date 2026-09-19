#!/usr/bin/env bash
set -e

# Navigate to project root
cd "$(dirname "$0")"

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

echo ""
echo "=== Setup Complete! ==="
echo "Run the application with:"
echo "  sudo .venv/bin/python production/main.py"

