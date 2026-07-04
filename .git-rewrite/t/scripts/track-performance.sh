#!/bin/bash
# Track test suite performance metrics over time

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
RESULTS_FILE="results/performance-benchmarks.json"

# Extract metrics from latest test run
if [ -f "test-results-store/results.json" ]; then
  PASSED=$(jq '.stats.expected' test-results-store/results.json)
  TOTAL=$(jq '.stats.total' test-results-store/results.json)
  DURATION=$(jq '.stats.duration' test-results-store/results.json | xargs printf "%.0f")
else
  echo "❌ No test results found"
  exit 1
fi

# Create or append to benchmark file
if [ ! -f "$RESULTS_FILE" ]; then
  mkdir -p results
  echo "[]" > "$RESULTS_FILE"
fi

# Append new benchmark
jq \
  --arg ts "$TIMESTAMP" \
  --arg passed "$PASSED" \
  --arg total "$TOTAL" \
  --arg duration "$DURATION" \
  '. += [{"timestamp": $ts, "passed": ($passed | tonumber), "total": ($total | tonumber), "duration_ms": ($duration | tonumber)}]' \
  "$RESULTS_FILE" > "$RESULTS_FILE.tmp" && mv "$RESULTS_FILE.tmp" "$RESULTS_FILE"

echo "✅ Benchmark recorded: $PASSED/$TOTAL passed in ${DURATION}ms"
echo "📊 View: $RESULTS_FILE"
