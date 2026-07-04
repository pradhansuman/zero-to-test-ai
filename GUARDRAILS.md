# Quality Guardrails & Anti-Hallucination Checks

This document defines all safety checks to prevent mistakes, false reporting, and hallucinations in development and testing workflows.

## Why Guardrails?

The mistake of reporting 325 tests when there were actually 286 happened because:
1. Output was parsed from truncated log tails
2. Numbers were not verified against authoritative sources
3. No validation occurred before claiming metrics

**Guardrails ensure:**
- ✅ No reporting without verification
- ✅ Automatic validation of critical metrics
- ✅ Early detection of configuration errors
- ✅ Consistent, auditable results

---

## Guardrail Scripts

### 1. **Test Results Validator** (`scripts/validate-test-results.py`)

**Purpose:** Parse actual Playwright results from JSON, validate metrics, prevent false counts.

**Usage:**
```bash
python3 scripts/validate-test-results.py
```

**Validates:**
- ✓ Test count matches across sources
- ✓ Math integrity: passed + failed + flaky = total
- ✓ All counts are non-negative
- ✓ Flaky/failed tests are reported

**Output:**
```
✅ TEST RESULTS SUMMARY (VALIDATED)
Total Tests:     286
Passed:          284 (99.3%)
Failed:          0
Flaky:           1
Status:          🟢 PRODUCTION READY
```

### 2. **Comprehensive Guardrails** (`scripts/guardrails.sh`)

**Purpose:** Pre-commit/pre-deploy checklist validating entire project health.

**Usage:**
```bash
chmod +x scripts/guardrails.sh
./scripts/guardrails.sh
```

**Checks:**

| # | Check | Prevents |
|---|-------|----------|
| 1 | Python syntax | Syntax errors in commits |
| 2 | TypeScript types | Type-checking failures post-deploy |
| 3 | Dependency integrity | Version conflicts, duplicates |
| 4 | Secret scanning | Hardcoded API keys/credentials |
| 5 | Git status | Dirty working tree issues |
| 6 | Critical files | Missing essential project files |
| 7 | Docker Compose | Invalid container configurations |
| 8 | package.json | Malformed JSON configs |
| 9 | Test artifacts | Claiming test results without evidence |
| 10 | Code baseline | Track codebase size/changes |

---

## Pre-Commit Hook Setup

Automatically run guardrails before commits:

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "🛡️ Running pre-commit guardrails..."
if ! bash scripts/guardrails.sh; then
  echo "❌ Guardrails failed. Commit blocked."
  exit 1
fi
EOF

chmod +x .git/hooks/pre-commit
```

---

## Reporting Checklist

**Before claiming any metric or status, VERIFY:**

- [ ] **Test counts:** Run `python3 scripts/validate-test-results.py` ✓
- [ ] **All guardrails pass:** Run `./scripts/guardrails.sh` ✓
- [ ] **Read actual report:** Open `playwright-report/index.html` in browser ✓
- [ ] **Check git status:** `git status` shows clean or expected changes ✓
- [ ] **No hardcoded secrets:** Verified by guardrails ✓
- [ ] **Dependencies installed:** `pip list` / `npm list` confirms versions ✓

**Never report metrics without evidence.** Always cite the source:
- ✓ "284 tests passed (verified via playwright-report/test-results.json)"
- ✗ "325 tests passed" ← Unverified, will catch mistakes

---

## Common Mistakes & Prevention

| Mistake | Prevention |
|---------|-----------|
| Wrong test count | Always validate with `validate-test-results.py` |
| Hardcoded secrets in commit | Guardrails catch before commit |
| Type errors in TypeScript | Guardrails run `tsc --noEmit` |
| Invalid Docker config | Guardrails validate docker-compose.yml |
| Missing critical files | Guardrails check file existence |
| Reporting without evidence | Include artifact paths in reports |
| Flaky tests claimed as stable | Guardrails flag flaky tests |

---

## Integration with CI/CD

Add to GitHub Actions / CI pipeline:

```yaml
- name: Run Guardrails
  run: |
    bash scripts/guardrails.sh
    python3 scripts/validate-test-results.py

- name: Verify Test Results
  run: |
    if [ ! -f "playwright-report/test-results.json" ]; then
      echo "❌ Test report missing"
      exit 1
    fi
```

---

## Evidence-Based Reporting Template

Use this template when reporting test results:

```markdown
## Test Results ✅

**Command Run:**
```bash
npm test -- tests/e2e/shopnow.spec.ts
```

**Evidence:**
- Playwright Report: `/Users/skp/Downloads/QA_AGents/playwright-report/index.html`
- Validation: `python3 scripts/validate-test-results.py`

**Metrics (VALIDATED):**
- Total: 286 tests
- Passed: 284 (99.3%)
- Failed: 0
- Flaky: 1 (State Resilience suite - timing-sensitive)

**Status:** 🟢 PRODUCTION READY
```

---

## Future-Proofing

### What Each Agent Should Do

**When reporting metrics:**
1. Run authoritative extraction (e.g., `validate-test-results.py`)
2. Parse JSON/structured data, not human-readable output
3. Validate against mathematical constraints
4. Cite the source file/report
5. Flag any anomalies (flaky, failures, unexpected counts)

### Adding New Guardrails

If you add a new feature/component:
1. Add a validation check to `guardrails.sh`
2. Document the check in this file
3. Include evidence-collection in scripts

---

## Running Guardrails Now

```bash
# Validate test results
python3 scripts/validate-test-results.py

# Run comprehensive checks
bash scripts/guardrails.sh

# View test report
open playwright-report/index.html
```

**Result:** No more hallucinated metrics. All claims are evidence-backed. ✅
