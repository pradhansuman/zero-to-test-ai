#!/bin/bash
# Interactive Test Execution Wizard
# Guides users through environment selection with smart recommendations
# Usage: ./scripts/interactive-test-wizard.sh

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Global variables
USE_CASE=""
ENVIRONMENT=""
REPORTER=""
BROWSER="chromium"
WORKERS="4"
RUN_TESTS=false

# Functions
clear_screen() {
  clear
}

show_header() {
  clear_screen
  echo -e "${CYAN}"
  echo "╔════════════════════════════════════════════════════════════╗"
  echo "║                                                            ║"
  echo "║     🧪 QA TEST EXECUTION WIZARD 🧪                        ║"
  echo "║     Interactive Test Environment & Format Selection       ║"
  echo "║                                                            ║"
  echo "╚════════════════════════════════════════════════════════════╝"
  echo -e "${NC}"
}

show_progress() {
  local step=$1
  local total=$2
  echo -e "\n${BLUE}Progress: Step $step of $total${NC}\n"
}

pause() {
  read -p "Press Enter to continue..."
}

# Step 1: Use Case Selection
ask_use_case() {
  show_header
  show_progress 1 5

  echo -e "${YELLOW}What are you trying to do?${NC}\n"
  echo "1) 👨‍💻 Local Development (I'm writing/debugging tests)"
  echo "2) 🔄 CI/CD Pipeline (Automated testing in GitHub/GitLab)"
  echo "3) 📊 Load Testing (I need to scale across multiple instances)"
  echo "4) 🌍 Multi-Region Testing (Test across AWS/GCP/Azure regions)"
  echo "5) 🚀 Production Deployment (I need to validate before going live)"
  echo "6) 📈 Performance Testing (Measure and compare test metrics)"
  echo "7) 🧪 Quick Smoke Test (Run a quick sanity check)"
  echo ""

  read -p "Select your use case (1-7): " use_case_choice

  case $use_case_choice in
    1) USE_CASE="development"; RECOMMENDED_ENV="local" ;;
    2) USE_CASE="cicd"; RECOMMENDED_ENV="docker" ;;
    3) USE_CASE="load_testing"; RECOMMENDED_ENV="aws" ;;
    4) USE_CASE="multi_region"; RECOMMENDED_ENV="aws" ;;
    5) USE_CASE="production"; RECOMMENDED_ENV="aws" ;;
    6) USE_CASE="performance"; RECOMMENDED_ENV="docker" ;;
    7) USE_CASE="smoke"; RECOMMENDED_ENV="local" ;;
    *)
      echo -e "${RED}Invalid choice. Please select 1-7.${NC}"
      sleep 2
      ask_use_case
      return
      ;;
  esac

  show_use_case_details
}

show_use_case_details() {
  show_header

  echo -e "${GREEN}✅ Use Case Selected: ${YELLOW}$USE_CASE${NC}\n"

  case $USE_CASE in
    development)
      echo "📋 Development Mode Selected"
      echo "   • Fast feedback loop"
      echo "   • Local browser execution"
      echo "   • Easy debugging"
      echo "   • Recommended: LOCAL"
      ;;
    cicd)
      echo "📋 CI/CD Pipeline Mode Selected"
      echo "   • Automated execution"
      echo "   • Consistent environments"
      echo "   • Integration ready"
      echo "   • Recommended: DOCKER"
      ;;
    load_testing)
      echo "📋 Load Testing Mode Selected"
      echo "   • Scale to multiple instances"
      echo "   • Distributed execution"
      echo "   • Performance measurement"
      echo "   • Recommended: AWS (auto-scaling)"
      ;;
    multi_region)
      echo "📋 Multi-Region Testing Mode Selected"
      echo "   • Test across geographic regions"
      echo "   • Regional latency testing"
      echo "   • Global coverage validation"
      echo "   • Recommended: AWS with multiple regions"
      ;;
    production)
      echo "📋 Production Deployment Mode Selected"
      echo "   • Pre-production validation"
      echo "   • Enterprise infrastructure"
      echo "   • Compliance testing"
      echo "   • Recommended: AWS (most reliable)"
      ;;
    performance)
      echo "📋 Performance Testing Mode Selected"
      echo "   • Detailed metrics"
      echo "   • Benchmark comparison"
      echo "   • Timeline analysis"
      echo "   • Recommended: DOCKER (controlled)"
      ;;
    smoke)
      echo "📋 Smoke Test Mode Selected"
      echo "   • Quick sanity check"
      echo "   • Smoke tests only (@smoke tag)"
      echo "   • Minimal overhead"
      echo "   • Recommended: LOCAL (fastest)"
      ;;
  esac

  echo ""
  pause
}

# Step 2: Environment Selection
ask_environment() {
  show_header
  show_progress 2 5

  echo -e "${YELLOW}Where do you want to run tests?${NC}\n"
  echo "Based on your use case (${CYAN}$USE_CASE${NC}), we recommend: ${GREEN}$RECOMMENDED_ENV${NC}\n"
  echo "OPTIONS:"
  echo ""
  echo "1) 💻 LOCAL (Your machine)"
  echo "   • Setup: 5 minutes | Cost: \$0 | Speed: ⭐⭐⭐⭐⭐"
  echo "   • Best for: Development, quick testing"
  echo ""
  echo "2) 🐳 DOCKER (Containerized)"
  echo "   • Setup: 2 minutes | Cost: \$0 | Speed: ⭐⭐⭐⭐"
  echo "   • Best for: CI/CD, consistency"
  echo ""
  echo "3) ☁️  AWS (Amazon EC2)"
  echo "   • Setup: 20 minutes | Cost: \$0.10/run | Speed: ⭐⭐⭐"
  echo "   • Best for: Enterprise, scaling"
  echo ""
  echo "4) ☁️  GOOGLE CLOUD (Google Compute)"
  echo "   • Setup: 15 minutes | Cost: \$0.08/run | Speed: ⭐⭐⭐"
  echo "   • Best for: Google ecosystem"
  echo ""
  echo "5) ☁️  AZURE (Microsoft)"
  echo "   • Setup: 15 minutes | Cost: \$0.13/run | Speed: ⭐⭐"
  echo "   • Best for: Microsoft ecosystem"
  echo ""

  read -p "Select environment (1-5) or press Enter for recommended ($RECOMMENDED_ENV): " env_choice

  if [ -z "$env_choice" ]; then
    env_choice=$(case $RECOMMENDED_ENV in
      local) echo "1" ;;
      docker) echo "2" ;;
      aws) echo "3" ;;
      gcp) echo "4" ;;
      azure) echo "5" ;;
    esac)
  fi

  case $env_choice in
    1) ENVIRONMENT="local" ;;
    2) ENVIRONMENT="docker" ;;
    3) ENVIRONMENT="aws" ;;
    4) ENVIRONMENT="gcp" ;;
    5) ENVIRONMENT="azure" ;;
    *)
      echo -e "${RED}Invalid choice. Please select 1-5.${NC}"
      sleep 2
      ask_environment
      return
      ;;
  esac

  show_environment_details
}

show_environment_details() {
  show_header

  echo -e "${GREEN}✅ Environment Selected: ${YELLOW}$ENVIRONMENT${NC}\n"

  case $ENVIRONMENT in
    local)
      echo "💻 LOCAL EXECUTION"
      echo "   • Runs on your machine"
      echo "   • Requires: Node.js 20+, Playwright"
      echo "   • Results stored in: ./playwright-report/"
      echo "   • Best for immediate feedback"
      ;;
    docker)
      echo "🐳 DOCKER EXECUTION"
      echo "   • Containerized execution"
      echo "   • Consistent across all platforms"
      echo "   • Requires: Docker Desktop"
      echo "   • Perfect for CI/CD pipelines"
      ;;
    aws)
      echo "☁️  AWS EC2 EXECUTION"
      echo "   • Auto-provisioning EC2 instance"
      echo "   • Requires: AWS credentials configured"
      echo "   • Instance auto-terminates after tests"
      echo "   • Cost: ~\$0.10 per run"
      ;;
    gcp)
      echo "☁️  GOOGLE CLOUD EXECUTION"
      echo "   • Auto-provisioning Google Cloud VM"
      echo "   • Requires: gcloud CLI configured"
      echo "   • VM auto-deleted after tests"
      echo "   • Cost: ~\$0.08 per run"
      ;;
    azure)
      echo "☁️  AZURE EXECUTION"
      echo "   • Auto-provisioning Azure VM"
      echo "   • Requires: Azure CLI configured"
      echo "   • VM auto-deleted after tests"
      echo "   • Cost: ~\$0.13 per run"
      ;;
  esac

  echo ""
  pause
}

# Step 3: Report Format Selection
ask_reporter() {
  show_header
  show_progress 3 5

  echo -e "${YELLOW}What report format do you prefer?${NC}\n"
  echo "1) 📊 HTML (Interactive web report - DEFAULT)"
  echo "   • Visual dashboards"
  echo "   • Screenshots & videos"
  echo "   • Timeline analysis"
  echo "   • Best for: Presentations, sharing"
  echo ""
  echo "2) 📋 JSON (Structured data)"
  echo "   • Machine-readable format"
  echo "   • API-friendly"
  echo "   • Detailed metrics"
  echo "   • Best for: Integration, automation"
  echo ""
  echo "3) 🔧 JUNIT (XML format)"
  echo "   • CI/CD standard"
  echo "   • Jenkins compatible"
  echo "   • Maven/Gradle integration"
  echo "   • Best for: Enterprise CI/CD"
  echo ""
  echo "4) 📦 ALL (HTML + JSON + JUNIT)"
  echo "   • Comprehensive output"
  echo "   • Multiple use cases"
  echo "   • All formats generated"
  echo "   • Best for: Complete documentation"
  echo ""

  read -p "Select report format (1-4) or press Enter for HTML: " reporter_choice

  if [ -z "$reporter_choice" ]; then
    reporter_choice="1"
  fi

  case $reporter_choice in
    1) REPORTER="html" ;;
    2) REPORTER="json" ;;
    3) REPORTER="junit" ;;
    4) REPORTER="all" ;;
    *)
      echo -e "${RED}Invalid choice. Please select 1-4.${NC}"
      sleep 2
      ask_reporter
      return
      ;;
  esac
}

# Step 4: Browser & Workers Selection
ask_browser_workers() {
  show_header
  show_progress 4 5

  echo -e "${YELLOW}Fine-tune execution settings?${NC}\n"
  echo "Current settings:"
  echo "  • Browser: $BROWSER"
  echo "  • Parallel workers: $WORKERS"
  echo ""

  read -p "Change browser? (chromium/firefox/webkit) [Enter to skip]: " browser_choice
  if [ -n "$browser_choice" ]; then
    BROWSER="$browser_choice"
  fi

  echo ""
  read -p "Change worker count? (1-16) [Enter to skip]: " workers_choice
  if [ -n "$workers_choice" ]; then
    if [ "$workers_choice" -ge 1 ] && [ "$workers_choice" -le 16 ]; then
      WORKERS="$workers_choice"
    else
      echo -e "${RED}Invalid worker count. Using default: $WORKERS${NC}"
      sleep 1
    fi
  fi

  # Add smoke test option
  echo ""
  read -p "Run SMOKE TESTS ONLY? (y/n) [Default: n]: " smoke_choice
  if [[ "$smoke_choice" =~ ^[Yy]$ ]]; then
    SMOKE_TAG="--smoke"
  else
    SMOKE_TAG=""
  fi
}

# Step 5: Review & Confirm
review_and_confirm() {
  show_header
  show_progress 5 5

  echo -e "${CYAN}═════════════════════════════════════════════════════════${NC}"
  echo -e "${CYAN}               EXECUTION CONFIGURATION SUMMARY${NC}"
  echo -e "${CYAN}═════════════════════════════════════════════════════════${NC}\n"

  echo -e "Use Case:          ${YELLOW}$USE_CASE${NC}"
  echo -e "Environment:       ${YELLOW}$ENVIRONMENT${NC}"
  echo -e "Report Format:     ${YELLOW}$REPORTER${NC}"
  echo -e "Browser:           ${YELLOW}$BROWSER${NC}"
  echo -e "Workers:           ${YELLOW}$WORKERS${NC}"
  if [ -n "$SMOKE_TAG" ]; then
    echo -e "Mode:              ${YELLOW}SMOKE TESTS ONLY${NC}"
  fi

  echo ""
  echo -e "${CYAN}═════════════════════════════════════════════════════════${NC}\n"

  # Show estimated cost/time
  show_cost_time_estimate

  echo ""
  read -p "Do you want to run tests with these settings? (y/n): " confirm_choice

  if [[ "$confirm_choice" =~ ^[Yy]$ ]]; then
    RUN_TESTS=true
    show_final_command
  else
    echo -e "${RED}Execution cancelled.${NC}"
    exit 0
  fi
}

show_cost_time_estimate() {
  echo -e "${BLUE}📊 Estimated Cost & Duration:${NC}\n"

  case $ENVIRONMENT in
    local)
      echo "   • Duration: ~10-15 minutes"
      echo "   • Cost: \$0"
      echo "   • Setup: Already done"
      ;;
    docker)
      echo "   • Duration: ~12-18 minutes"
      echo "   • Cost: \$0"
      echo "   • Setup: 2 minutes (if not built)"
      ;;
    aws)
      echo "   • Duration: ~20-30 minutes (including provisioning)"
      echo "   • Cost: ~\$0.10-\$0.20 per run"
      echo "   • Setup: Instance provisioning + initialization"
      ;;
    gcp)
      echo "   • Duration: ~15-25 minutes (including provisioning)"
      echo "   • Cost: ~\$0.08-\$0.15 per run"
      echo "   • Setup: VM creation + initialization"
      ;;
    azure)
      echo "   • Duration: ~15-25 minutes (including provisioning)"
      echo "   • Cost: ~\$0.13-\$0.20 per run"
      echo "   • Setup: VM creation + initialization"
      ;;
  esac
}

show_final_command() {
  echo -e "\n${GREEN}✅ EXECUTING TESTS...${NC}\n"

  # Build command
  local cmd="./scripts/test-runner.sh"
  cmd="$cmd --env $ENVIRONMENT"
  cmd="$cmd --browser $BROWSER"
  cmd="$cmd --workers $WORKERS"
  cmd="$cmd --reporter $REPORTER"
  if [ -n "$SMOKE_TAG" ]; then
    cmd="$cmd --smoke"
  fi

  echo -e "${YELLOW}Command:${NC}"
  echo -e "${BLUE}$cmd${NC}\n"

  # Create summary log
  log_execution_start

  # Execute command
  if eval "$cmd"; then
    log_execution_success
    show_results_location
  else
    log_execution_failure
    echo -e "${RED}❌ Test execution failed!${NC}"
    exit 1
  fi
}

show_results_location() {
  echo -e "\n${GREEN}═════════════════════════════════════════════════════════${NC}"
  echo -e "${GREEN}✅ TESTS COMPLETED SUCCESSFULLY!${NC}"
  echo -e "${GREEN}═════════════════════════════════════════════════════════${NC}\n"

  echo -e "${CYAN}📊 View Your Results:${NC}\n"

  case $REPORTER in
    html|all)
      echo "📈 HTML Report:"
      echo -e "   ${BLUE}open ./playwright-report/index.html${NC}"
      echo ""
      ;;
  esac

  case $REPORTER in
    json|all)
      echo "📋 JSON Results:"
      echo -e "   ${BLUE}cat ./test-results-store/results.json${NC}"
      echo ""
      ;;
  esac

  case $REPORTER in
    junit|all)
      echo "🔧 JUnit XML:"
      echo -e "   ${BLUE}ls ./test-results-store/*.xml${NC}"
      echo ""
      ;;
  esac

  echo "📁 All Artifacts:"
  echo -e "   ${BLUE}ls -la ./test-results-store/${NC}"
  echo ""
}

log_execution_start() {
  cat >> execution-log.txt << EOF

═══════════════════════════════════════════════════════════
Test Execution: $(date)
═══════════════════════════════════════════════════════════
Use Case: $USE_CASE
Environment: $ENVIRONMENT
Reporter: $REPORTER
Browser: $BROWSER
Workers: $WORKERS
Smoke: ${SMOKE_TAG:-"No"}
═══════════════════════════════════════════════════════════

EOF
}

log_execution_success() {
  echo "Status: SUCCESS - Completed at $(date)" >> execution-log.txt
}

log_execution_failure() {
  echo "Status: FAILED - Error at $(date)" >> execution-log.txt
}

# Main flow
main() {
  ask_use_case
  ask_environment
  ask_reporter
  ask_browser_workers
  review_and_confirm
}

# Run
main
