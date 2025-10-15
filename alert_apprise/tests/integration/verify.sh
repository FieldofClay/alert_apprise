#!/bin/bash
set -e

LOG_FILE="./nginx/webhook_logs/access.log"
TIMEOUT=${1:-90}
CHECK_INTERVAL=5

echo "============================================"
echo "Integration Test Verification"
echo "============================================"
echo "Log file: $LOG_FILE"
echo "Timeout: ${TIMEOUT}s"
echo "Checking for webhook delivery..."
echo ""

start_time=$(date +%s)

while true; do
    current_time=$(date +%s)
    elapsed=$((current_time - start_time))
    
    if [ $elapsed -ge $TIMEOUT ]; then
        echo ""
        echo "❌ TIMEOUT: No webhook received after ${TIMEOUT}s"
        echo ""
        echo "=== Nginx Access Log ==="
        if [ -f "$LOG_FILE" ]; then
            cat "$LOG_FILE"
        else
            echo "Log file not found at: $LOG_FILE"
        fi
        echo ""
        echo "=== Docker Container Status ==="
        docker compose ps
        echo ""
        echo "=== Splunk Logs (last 50 lines) ==="
        docker compose logs --tail=50 splunk
        exit 1
    fi
    
    if [ -f "$LOG_FILE" ]; then
        # Check if the log contains our test alert
        if grep -q "Test Alert Body" "$LOG_FILE"; then
            echo ""
            echo "✅ SUCCESS: Webhook received!"
            echo ""
            echo "=== Webhook Details ==="
            grep "Test Alert Body" "$LOG_FILE"
            echo ""
            echo "=== Full Access Log ==="
            cat "$LOG_FILE"
            echo ""
            echo "Integration test PASSED in ${elapsed}s"
            exit 0
        fi
    fi
    
    echo -n "."
    sleep $CHECK_INTERVAL
done
