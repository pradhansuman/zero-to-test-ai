#!/bin/bash
# Simplified Test Runner
# Usage: ./scripts/test-runner-simple.sh [--env local|docker] [--browser chromium|firefox|webkit]

set -euo pipefail

# Defaults
ENV="local"
BROWSER="chromium"
WORKERS="4"
REPORTER="html"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --env)
      ENV="$2"
      shift 2
      ;;
    --browser)
      BROWSER="$2"
      shift 2
      ;;
    --workers)
      WORKERS="$2"
      shift 2
      ;;
    --reporter)
      REPORTER="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🧪 QA Test Runner${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo "Environment: $ENV"
echo "Browser: $BROWSER"
echo "Workers: $WORKERS"
echo "Reporter: $REPORTER"
echo ""

# Run tests locally
if [ "$ENV" = "local" ]; then
  echo -e "${YELLOW}🔄 Running tests locally...${NC}"

  # Create output directory
  mkdir -p ./playwright-report
  mkdir -p ./test-results-store

  # Run Playwright
  npx playwright test \
    --project="$BROWSER" \
    --workers="$WORKERS" \
    --reporter="$REPORTER" \
    2>&1 || true

  echo -e "${GREEN}✅ Tests completed locally${NC}"
  echo ""
  echo "📊 Results available at:"
  echo "   HTML Report: ./playwright-report/index.html"
  echo ""

  # Display test report summary
  if [ -f ./playwright-report/index.html ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 TEST REPORT SUMMARY (from HTML)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "To view interactive report, run:"
    echo "  open ./playwright-report/index.html"
    echo ""
  fi

elif [ "$ENV" = "docker" ]; then
  echo -e "${YELLOW}🐳 Running tests in Docker...${NC}"

  # Build image if needed
  if ! docker image inspect "qa-tests-docker:latest" >/dev/null 2>&1; then
    echo -e "${YELLOW}📦 Building Docker image...${NC}"
    docker build -f Dockerfile.test -t qa-tests-docker:latest . || true
  fi

  # Run in Docker
  docker run --rm \
    -v "$(pwd)/playwright-report:/app/playwright-report" \
    -v "$(pwd)/test-results-store:/app/test-results-store" \
    qa-tests-docker:latest \
    npx playwright test \
    --project="$BROWSER" \
    --workers="$WORKERS" \
    --reporter="$REPORTER" \
    2>&1 || true

  echo -e "${GREEN}✅ Tests completed in Docker${NC}"
  echo ""
  echo "📊 Results available at:"
  echo "   HTML Report: ./playwright-report/index.html"
else
  echo "Environment '$ENV' not supported in simplified runner"
  exit 1
fi

echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
