#!/bin/bash
set -e

TIMEOUT=${1:-90}
CHECK_INTERVAL=5

echo "Integration Test Verification"
echo "Timeout: ${TIMEOUT}s"
echo "Checking for webhook delivery via httpbin logs..."

start_time=$(date +%s)

while true; do
    current_time=$(date +%s)
    elapsed=$((current_time - start_time))
    
    if [ $elapsed -ge $TIMEOUT ]; then
        echo ""
        echo "TIMEOUT: No webhook received after ${TIMEOUT}s"
        echo ""
        echo "=== Docker Container Status ==="
        docker compose ps
        echo ""
        echo "=== Webhook Receiver Logs ==="
        docker compose logs webhook-receiver
        echo "=== Splunk Logs (last 50 lines) ==="
        "
        echo "docker compose logs --tail=50 splunk
        exit 1
    fi
    
    # Check httpbin logs for POST requests with Apprise user agent
    LOGS=$(docker compose logs webhook-receiver 2>/dev/null || echo "")
    
    # Look for Apprise user agent in POST requests to /post endpoint
    if echo "$LOGS" | grep -E "(POST /post|python-apprise|Apprise/)" > /dev/null; then
        echo ""
        echo "SUCCESS: Webhook received from Apprise!"
        echo ""
        echo "=== Webhook Details ==="
        echo "$LOGS" | grep -E "(POST|apprise)" -i || echo "$LOGS" | tail -20
        echo ""
        echo "Integration test PASSED in ${elapsed}s"
        exit 0
    fi
    
    echo -n "."
    sleep $CHECK_INTERVAL
done
