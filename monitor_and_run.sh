#!/bin/bash

# Configuration
PYTHON_SCRIPT="run.py"
CHECK_INTERVAL=5 # Seconds between checks

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
