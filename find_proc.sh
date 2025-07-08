#!/bin/bash

# Check if port number is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <port_number>"
    exit 1
fi

PORT=$1

# Check if the port is a valid number
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "Error: Port must be a number"
    exit 1
fi

# Find processes using the port
PIDS=$(fuser $PORT/tcp 2>/dev/null)

# Check if any process was found
if [ -z "$PIDS" ]; then
    echo "No process found using port $PORT/tcp"
    exit 0
fi

# Display process information
echo "Processes using port $PORT/tcp:"
for PID in $PIDS; do
    # Get process details using ps
    PROCESS_INFO=$(ps -p $PID -o pid,comm --no-headers)
    if [ -n "$PROCESS_INFO" ]; then
        echo "PID: $PID, Command: $(echo $PROCESS_INFO | awk '{print $2}')"
    else
        echo "PID: $PID, Command: (unknown)"
    fi
done

# Ask user if they want to kill the processes
read -p "Do you want to kill these processes? (y/n): " CONFIRM
if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ]; then
    for PID in $PIDS; do
        echo "Killing process $PID..."
        kill -9 $PID 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "Process $PID terminated successfully"
        else
            echo "Failed to terminate process $PID (may require sudo or process already terminated)"
        fi
    done
else
    echo "No processes were killed"
    exit 0
fi

# Verify if the port is now free
if fuser $PORT/tcp >/dev/null 2>&1; then
    echo "Warning: Port $PORT/tcp is still in use"
else
    echo "Port $PORT/tcp is now free"
fi