#!/bin/bash
# Automatic Test Report Generator
# Runs after test execution and generates comprehensive report

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                   🧪 TEST EXECUTION REPORT - FINAL RESULTS                   ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if test results exist
if [ ! -f ./playwright-report/index.html ]; then
  echo -e "${RED}❌ No test results found. Run tests first with:${NC}"
  echo -e "   ${YELLOW}./scripts/test-runner-simple.sh${NC}"
  exit 1
fi

# Extract test summary from report
echo -e "${BLUE}📊 EXECUTION SUMMARY${NC}"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "  Test Report:         ./playwright-report/index.html"
echo "  Generated:           $(date)"
echo ""

# Check for test results file
if [ -f test-results-store/results.json ]; then
  echo "  Test Results File:   test-results-store/results.json"

  # Try to extract test count
  TOTAL=$(grep -o '"tests"' test-results-store/results.json | wc -l)
  if [ "$TOTAL" -gt 0 ]; then
    echo "  Total Tests Found:   ~$TOTAL"
  fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Show view instructions
echo -e "${GREEN}✅ TEST EXECUTION COMPLETE${NC}"
echo ""
echo "📋 HOW TO VIEW RESULTS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Interactive HTML Report:"
echo -e "    ${YELLOW}open ./playwright-report/index.html${NC}"
echo ""
echo "  Includes:"
echo "    • Test timeline and results"
echo "    • Screenshots of each test"
echo "    • Video recordings"
echo "    • Performance metrics"
echo "    • Network traces"
echo ""
echo "  Machine-Readable Results:"
echo -e "    ${YELLOW}cat test-results-store/results.json${NC}"
echo ""
echo "  JUnit XML (for CI/CD):"
echo -e "    ${YELLOW}cat test-results-store/results.xml${NC}"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Show directory structure
echo -e "${BLUE}📁 ARTIFACT LOCATIONS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
if [ -d playwright-report ]; then
  SIZE=$(du -sh ./playwright-report | cut -f1)
  FILES=$(find ./playwright-report -type f | wc -l)
  echo "  playwright-report/         ($SIZE, $FILES files)"
  echo "    ├─ index.html             ← Main interactive report"
  echo "    └─ data/                  ← Embedded test data"
fi

if [ -d test-results-store ]; then
  SIZE=$(du -sh ./test-results-store | cut -f1)
  echo "  test-results-store/        ($SIZE)"
  echo "    ├─ results.json           ← Machine-readable results"
  echo "    ├─ results.xml            ← JUnit format"
  echo "    ├─ screenshots/           ← Test screenshots"
  echo "    ├─ videos/                ← Test recordings"
  echo "    └─ traces/                ← Performance traces"
fi
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Summary statistics
echo -e "${GREEN}✨ QUICK STATS${NC}"
echo ""
echo "  ✅ Test Suite Status:  READY TO REVIEW"
echo "  📊 Report Location:    ./playwright-report/index.html"
echo "  ⏱️  Report Generation: Complete"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
