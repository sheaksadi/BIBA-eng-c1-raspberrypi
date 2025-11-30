#!/bin/bash

# Configuration
PYTHON_SCRIPT="run.py"
CHECK_INTERVAL=5 # Seconds between checks
VENV_DIR="venv"

# Ensure venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment (with system packages)..."
    python3 -m venv --system-site-packages "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    # Check if we need to install/upgrade (quietly to avoid spam)
    # Using --upgrade only if needed might be better, or just install
    echo "Checking requirements..."
    pip install -r requirements.txt --quiet
fi

# Function to run the python script
start_script() {
    echo "Starting $PYTHON_SCRIPT..."
    python3 "$PYTHON_SCRIPT" &
    SCRIPT_PID=$!
}

# Function to stop the python script
stop_script() {
    if [ -n "$SCRIPT_PID" ]; then
        echo "Stopping $PYTHON_SCRIPT (PID: $SCRIPT_PID)..."
        kill "$SCRIPT_PID"
        wait "$SCRIPT_PID" 2>/dev/null
    fi
}

# Initial start
echo "Checking for updates..."
git fetch origin

# Check if we are behind
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "Updates found. Pulling..."
    git pull
fi

start_script

# Set Pin Factory to Native to avoid RPi.GPIO/lgpio issues
export GPIOZERO_PIN_FACTORY=native

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo) to access GPIO pins with native factory."
  echo "Usage: sudo ./monitor_and_run.sh"
  exit 1
fi

# Monitor loop
while true; do
    sleep "$CHECK_INTERVAL"
    
    git fetch origin
    
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})
    
    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "New updates detected!"
        stop_script
        
        echo "Pulling updates..."
        git pull
        
        echo "Restarting script..."
        start_script
    fi
done
