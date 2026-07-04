#!/bin/bash
# Post-Deployment Validation Script - Phases 1-5 QA Platform
# Usage: ./validate-deployment.sh [staging|production]

set -e

ENVIRONMENT=${1:-staging}
BASE_URL=${BASE_URL:-http://localhost:8000}

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASS=0
FAIL=0

check() {
    local name=$1
    local endpoint=$2
    local expected_code=${3:-200}

    echo -ne "${BLUE}[TEST]${NC} $name... "

    response=$(curl -s -w "\n%{http_code}" "${BASE_URL}${endpoint}" 2>/dev/null || echo "000")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)

    if [ "$http_code" = "$expected_code" ]; then
        echo -e "${GREEN}PASS${NC} (HTTP $http_code)"
        ((PASS++))
    else
        echo -e "${RED}FAIL${NC} (Expected $expected_code, got $http_code)"
        ((FAIL++))
    fi
}

check_json() {
    local name=$1
    local endpoint=$2
    local field=$3

    echo -ne "${BLUE}[TEST]${NC} $name... "

    response=$(curl -s "${BASE_URL}${endpoint}" 2>/dev/null || echo "{}")

    if echo "$response" | jq -e ".$field" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((PASS++))
    else
        echo -e "${RED}FAIL${NC} (Field '$field' not found)"
        ((FAIL++))
    fi
}

echo "========================================="
echo "QA Platform Deployment Validation"
echo "Environment: ${ENVIRONMENT}"
echo "Base URL: ${BASE_URL}"
echo "========================================="
echo ""

# Health Checks
echo -e "${YELLOW}[SECTION] Health Checks${NC}"
check "Health endpoint" "/api/health" 200
check "Database connectivity" "/api/health/db" 200
echo ""

# Authentication
echo -e "${YELLOW}[SECTION] Authentication${NC}"
check "Register endpoint" "/api/auth/register" 400  # 400 because we're not sending valid data
check "Login endpoint" "/api/auth/login" 400
echo ""

# Core Features (Phase 1-2)
echo -e "${YELLOW}[SECTION] Core Features (Phases 1-2)${NC}"
check "Get projects" "/api/projects" 401  # 401 because no auth token
check "Get health" "/api/health" 200
echo ""

# Analytics (Phase 3-4)
echo -e "${YELLOW}[SECTION] Analytics & Reporting (Phases 3-4)${NC}"
check "Analytics dashboard" "/api/analytics/dashboard" 401
check "Get metrics" "/api/monitoring/metrics" 401
echo ""

# Enterprise Features (Phase 4)
echo -e "${YELLOW}[SECTION] Enterprise Features (Phase 4)${NC}"
check "Get plugins" "/api/plugins" 401
check "Get rate limit" "/api/rate-limit/test" 401
echo ""

# Phase 5 Features
echo -e "${YELLOW}[SECTION] Phase 5 Features (Scale & Security)${NC}"
check "Security compliance" "/api/phase5/security/compliance-status" 401
check "Regional endpoint" "/api/phase5/scale/regional-endpoint" 400
check "Marketplace apps" "/api/phase5/marketplace/apps" 401
echo ""

# Summary
echo "========================================="
echo -e "${BLUE}Results:${NC}"
echo -e "  ${GREEN}Passed: $PASS${NC}"
echo -e "  ${RED}Failed: $FAIL${NC}"
echo "========================================="

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ All validation checks passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some validation checks failed${NC}"
    exit 1
fi
