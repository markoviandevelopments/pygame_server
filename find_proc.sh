#!/bin/bash

# Script to find and close ports 12333 and 12336 by killing associated processes

PORTS=(12333 12336 9000)

for PORT in "${PORTS[@]}"; do
    # Find PIDs of processes listening on the port using lsof
    PIDS=$(lsof -t -i :$PORT 2>/dev/null)
    
    if [ -n "$PIDS" ]; then
        echo "Found processes on port $PORT: $PIDS"
        echo "Killing processes..."
        # Attempt graceful kill first
        kill $PIDS 2>/dev/null
        sleep 2  # Wait a bit for processes to terminate
        # Force kill if still running
        kill -9 $PIDS 2>/dev/null
        echo "Port $PORT should now be closed."
    else
        echo "No processes found listening on port $PORT."
    fi
done

echo "Operation complete. Note: This script may require sudo privileges if the processes are owned by another user."