#!/bin/bash
# Load test runner — integrates k6 with test suite
set -e
PROJECT=${1:-store}
VUS=${2:-10}
DURATION=${3:-30s}
echo "🚀 Load test: $PROJECT (VUs=$VUS, duration=$DURATION)"
k6 run -e BASE_URL="file://$(pwd)/store.html" -e VUS="$VUS" -e DURATION="$DURATION" --out csv=results/load-test-${PROJECT}-$(date +%Y%m%d-%H%M%S).csv "k6/${PROJECT}-load.js"
echo "✅ Complete"
