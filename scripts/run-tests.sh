#!/bin/bash
# Universal Test Runner with Mandatory HTML Report Generation
# Ensures HTML report is ALWAYS generated for every test execution

set -euo pipefail

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
BROWSER="${1:-Desktop Chrome}"
WORKERS="${2:-4}"
REPORTER="html,json,junit"  # MANDATORY: Always include HTML

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              🧪 TEST EXECUTION WITH MANDATORY HTML REPORT                      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Configuration:${NC}"
echo "  Browser:     $BROWSER"
echo "  Workers:     $WORKERS"
echo "  Reporters:   HTML, JSON, JUnit (MANDATORY)"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════════════"
echo ""

# Create required directories
mkdir -p ./playwright-report
mkdir -p ./test-results-store

# Record start time
START_TIME=$(date +%s)
echo -e "${YELLOW}⏱️  Starting test execution at $(date)${NC}"
echo ""

# Execute tests with mandatory reporters
echo -e "${YELLOW}🚀 Running Playwright tests...${NC}"
echo ""

if npx playwright test \
  --project="$BROWSER" \
  --workers="$WORKERS" \
  --reporter="$REPORTER" 2>&1; then
  TEST_RESULT="PASSED"
  TEST_EXIT=0
else
  TEST_RESULT="FAILED"
  TEST_EXIT=1
fi

# Record end time
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════════════"
echo ""

# Verify HTML report was generated
if [ ! -f ./playwright-report/index.html ]; then
  echo -e "${RED}❌ CRITICAL: HTML report was NOT generated!${NC}"
  echo "   Expected: ./playwright-report/index.html"
  exit 1
fi

# Display HTML report information
echo -e "${GREEN}✅ HTML REPORT GENERATED SUCCESSFULLY${NC}"
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                      📊 TEST REPORT SUMMARY                                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Report metadata
REPORT_SIZE=$(du -h ./playwright-report/index.html | cut -f1)
REPORT_DATE=$(date)

echo "📋 Report Details:"
echo "  Status:        $TEST_RESULT"
echo "  Location:      ./playwright-report/index.html"
echo "  Size:          $REPORT_SIZE"
echo "  Generated:     $REPORT_DATE"
echo "  Execution Time: ${DURATION}s"
echo ""

# List all artifacts
echo "📁 Artifacts Generated:"
echo "  ✅ HTML Report:   ./playwright-report/index.html"
if [ -f ./test-results-store/results.json ]; then
  JSON_SIZE=$(du -h ./test-results-store/results.json | cut -f1)
  echo "  ✅ JSON Results:  ./test-results-store/results.json ($JSON_SIZE)"
fi
if [ -f ./test-results-store/results.xml ]; then
  XML_SIZE=$(du -h ./test-results-store/results.xml | cut -f1)
  echo "  ✅ JUnit XML:     ./test-results-store/results.xml ($XML_SIZE)"
fi

# Count test results
TEST_COUNT=$(grep -o '"test"' ./playwright-report/index.html | wc -l)
echo "  📊 Tests Found:   ~$TEST_COUNT"
echo ""

# Display viewing instructions
echo "═══════════════════════════════════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}🎯 HOW TO VIEW THE HTML REPORT:${NC}"
echo ""
echo "  1. Open in Browser:"
echo -e "     ${YELLOW}open ./playwright-report/index.html${NC}"
echo ""
echo "  2. View in VS Code:"
echo -e "     ${YELLOW}code ./playwright-report/index.html${NC}"
echo ""
echo "  3. Python HTTP Server:"
echo -e "     ${YELLOW}python3 -m http.server 8000 --directory ./playwright-report${NC}"
echo -e "     Then visit: http://localhost:8000"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════════════"
echo ""

# Report contents
echo -e "${BLUE}📊 HTML REPORT INCLUDES:${NC}"
echo ""
echo "  ✓ Test Timeline        - Sequential test execution visualization"
echo "  ✓ Pass/Fail Status     - Color-coded results for all tests"
echo "  ✓ Screenshots          - Captured at each test step"
echo "  ✓ Video Recordings     - Full test execution videos"
echo "  ✓ Performance Metrics  - Execution time per test"
echo "  ✓ Network Logs         - HTTP requests and responses"
echo "  ✓ Console Messages     - Browser console output"
echo "  ✓ Error Details        - Full stack traces for failures"
echo "  ✓ Trace Files          - Chrome DevTools traces"
echo ""

# Additional artifact information
echo "═══════════════════════════════════════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}📦 MACHINE-READABLE FORMATS:${NC}"
echo ""
echo "  JSON Format (for programmatic access):"
echo -e "    ${YELLOW}cat ./test-results-store/results.json${NC}"
echo ""
echo "  JUnit XML (for CI/CD integration):"
echo -e "    ${YELLOW}cat ./test-results-store/results.xml${NC}"
echo ""

# Recommendations
echo "═══════════════════════════════════════════════════════════════════════════════════════"
echo ""
echo -e "${YELLOW}⚠️  NEXT STEPS:${NC}"
echo ""
if [ "$TEST_RESULT" = "PASSED" ]; then
  echo "  ✅ Tests PASSED - Review report for coverage and insights"
  echo "  → Open: open ./playwright-report/index.html"
else
  echo "  ❌ Tests FAILED - Review screenshots and error details in HTML report"
  echo "  → Open: open ./playwright-report/index.html"
  echo "  → Look at failed test videos and screenshots for debugging"
fi
echo ""

# Ensure report is displayed/accessible
echo "═══════════════════════════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ TEST EXECUTION COMPLETE${NC}"
echo ""
echo -e "${GREEN}📊 HTML report is READY for review at:${NC}"
echo -e "   ${BLUE}./playwright-report/index.html${NC}"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════════════"
echo ""

exit $TEST_EXIT
