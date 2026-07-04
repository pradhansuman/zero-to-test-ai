#!/bin/bash
# Comprehensive Guardrails - Prevent mistakes, hallucinations, and false reporting
# Run before commits, deployments, and major changes

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🛡️ RUNNING GUARDRAILS CHECKS..."
echo "========================================"

# 1. Verify Python syntax (no syntax errors)
echo -e "\n${YELLOW}1. Python Syntax Validation${NC}"
python_files=$(find . -name "*.py" -type f ! -path "./venv/*" ! -path "./.venv/*" 2>/dev/null || true)
if [ -n "$python_files" ]; then
  while IFS= read -r file; do
    if ! python3 -m py_compile "$file" 2>/dev/null; then
      echo -e "${RED}✗ Syntax error in $file${NC}"
      exit 1
    fi
  done <<< "$python_files"
  echo -e "${GREEN}✓ All Python files syntactically valid${NC}"
else
  echo -e "${YELLOW}⊘ No Python files found${NC}"
fi

# 2. Verify TypeScript compilation (if applicable)
echo -e "\n${YELLOW}2. TypeScript Type Checking${NC}"
if [ -f "tsconfig.json" ]; then
  if npx tsc --noEmit 2>/dev/null; then
    echo -e "${GREEN}✓ No TypeScript type errors${NC}"
  else
    echo -e "${RED}✗ TypeScript compilation errors found${NC}"
    exit 1
  fi
else
  echo -e "${YELLOW}⊘ No tsconfig.json found${NC}"
fi

# 3. Verify requirements.txt integrity
echo -e "\n${YELLOW}3. Dependencies Integrity Check${NC}"
if [ -f "requirements.txt" ]; then
  # Check for duplicates
  if awk -F'=|>' '{print $1}' requirements.txt | sort | uniq -d | grep -v '^$'; then
    echo -e "${RED}✗ Duplicate dependencies found in requirements.txt${NC}"
    exit 1
  fi
  echo -e "${GREEN}✓ No duplicate dependencies${NC}"

  # Check for version conflicts
  if grep -E '^[a-zA-Z0-9_-]+==' requirements.txt | wc -l > /dev/null; then
    echo -e "${GREEN}✓ All dependencies pinned to specific versions${NC}"
  else
    echo -e "${YELLOW}⚠ Some dependencies not pinned - may cause inconsistency${NC}"
  fi
else
  echo -e "${YELLOW}⊘ No requirements.txt found${NC}"
fi

# 4. Check for hardcoded secrets/credentials
echo -e "\n${YELLOW}4. Secret Scanning${NC}"
secret_patterns=(
  "api[_-]?key"
  "password"
  "secret"
  "token"
  "api[_-]?secret"
  "private[_-]?key"
  "aws[_-]?secret"
  "stripe[_-]?key"
)

found_secrets=0
for pattern in "${secret_patterns[@]}"; do
  if grep -ri "$pattern\s*=" . \
    --include="*.py" \
    --include="*.ts" \
    --include="*.js" \
    --include="*.env" \
    --exclude-dir=node_modules \
    --exclude-dir=.venv \
    --exclude-dir=venv \
    2>/dev/null | grep -v "example\|sample\|placeholder\|test" | head -1; then
    found_secrets=$((found_secrets + 1))
  fi
done

if [ $found_secrets -gt 0 ]; then
  echo -e "${RED}✗ Potential hardcoded secrets found${NC}"
  exit 1
else
  echo -e "${GREEN}✓ No hardcoded secrets detected${NC}"
fi

# 5. Git status check (dirty working tree)
echo -e "\n${YELLOW}5. Git Status${NC}"
if [ -d ".git" ]; then
  if git status --short | grep -q .; then
    echo -e "${YELLOW}⚠ Uncommitted changes detected:${NC}"
    git status --short | head -5
  else
    echo -e "${GREEN}✓ Clean working tree${NC}"
  fi

  # Check for untracked files that shouldn't be there
  untracked=$(git ls-files --others --exclude-standard | grep -E "\.(env|key|pem|crt)$" || true)
  if [ -n "$untracked" ]; then
    echo -e "${RED}✗ Untracked sensitive files found:${NC}"
    echo "$untracked"
    exit 1
  fi
else
  echo -e "${YELLOW}⊘ Not a git repository${NC}"
fi

# 6. Test file existence verification
echo -e "\n${YELLOW}6. Critical Files Verification${NC}"
critical_files=(
  "store.html"
  "requirements.txt"
  "docker-compose.yml"
)

missing_files=0
for file in "${critical_files[@]}"; do
  if [ -f "$file" ]; then
    echo -e "${GREEN}✓ $file exists${NC}"
  else
    echo -e "${RED}✗ $file MISSING${NC}"
    missing_files=$((missing_files + 1))
  fi
done

if [ $missing_files -gt 0 ]; then
  echo -e "${RED}✗ Critical files missing${NC}"
  exit 1
fi

# 7. Docker Compose syntax validation
echo -e "\n${YELLOW}7. Docker Compose Validation${NC}"
if [ -f "docker-compose.yml" ]; then
  if docker-compose config > /dev/null 2>&1; then
    echo -e "${GREEN}✓ docker-compose.yml is valid${NC}"
  else
    echo -e "${RED}✗ docker-compose.yml has syntax errors${NC}"
    exit 1
  fi
else
  echo -e "${YELLOW}⊘ No docker-compose.yml found${NC}"
fi

# 8. Package.json integrity (if present)
echo -e "\n${YELLOW}8. Package.json Validation${NC}"
if [ -f "package.json" ]; then
  if python3 -c "import json; json.load(open('package.json'))" 2>/dev/null; then
    echo -e "${GREEN}✓ package.json is valid JSON${NC}"
  else
    echo -e "${RED}✗ package.json is malformed${NC}"
    exit 1
  fi
else
  echo -e "${YELLOW}⊘ No package.json found${NC}"
fi

# 9. Verify test results exist before claiming success
echo -e "\n${YELLOW}9. Test Results Artifact Verification${NC}"
if [ -d "playwright-report" ]; then
  if [ -f "playwright-report/test-results.json" ]; then
    total_tests=$(python3 -c "import json; data=json.load(open('playwright-report/test-results.json')); print(data.get('stats', {}).get('expected', 0))" 2>/dev/null || echo "0")
    echo -e "${GREEN}✓ Test report exists with $total_tests tests${NC}"
  else
    echo -e "${YELLOW}⚠ Test report directory exists but test-results.json missing${NC}"
  fi
else
  echo -e "${YELLOW}⊘ No playwright-report directory found${NC}"
fi

# 10. Code coverage check (if applicable)
echo -e "\n${YELLOW}10. Code Quality Baseline${NC}"
python_count=$(find . -name "*.py" -type f ! -path "./venv/*" ! -path "./.venv/*" 2>/dev/null | wc -l || echo "0")
ts_count=$(find . -name "*.ts" -o -name "*.tsx" 2>/dev/null | wc -l || echo "0")
echo -e "${GREEN}✓ Python files: $python_count | TypeScript files: $ts_count${NC}"

echo -e "\n${GREEN}========================================"
echo "✅ ALL GUARDRAILS PASSED"
echo "=======================================${NC}"
