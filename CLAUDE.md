# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (Node.js only)
npm install
npx playwright install

# Quick smoke test (5 minutes)
npx playwright test tests/e2e/orangehrm-comprehensive-sub-functions.spec.ts --grep "ADMIN" --project=chromium

# Full suite (2.3 hours, 123 tests)
npm test

# Watch in browser (headed mode)
npx playwright test tests/e2e/orangehrm-comprehensive-sub-functions.spec.ts --project=chromium --headed --workers=1

# View results
npx playwright show-report
```

## Architecture

### Test Suite Overview
This repository contains a **comprehensive OrangeHRM 5.8 testing suite** with **123 tests** covering **155+ sub-functionalities** across **8 modules**.

**Key Files:**
- **tests/e2e/orangehrm-comprehensive-sub-functions.spec.ts** — Main test suite (32KB, 124 tests)
- **ORANGEHRM_TEST_GUIDE.md** — Setup guide with 5 execution options
- **README.md** — Project overview and quick start
- **playwright.config.ts** — Playwright configuration (Chromium, Firefox, WebKit)
- **package.json** — Dependencies (@playwright/test, typescript, allure-playwright)

### Test Coverage by Module

| Module | Tests | Sub-Functions | Status |
|--------|-------|---------------|--------|
| ADMIN: User Management | 12 | System users, search, filter, sort | ✅ |
| PIM: Employee List | 15 | Employees, search, filter | ✅ |
| PIM: My Info | 20 | Personal details, 13 sections | ✅ |
| LEAVE: Leave Management | 15 | Leave list, filters, columns | ✅ |
| TIME: Timesheet Management | 12 | Timesheets, employees, periods | ✅ |
| RECRUITMENT: Candidates | 18 | 73 candidates, filters, search | ✅ |
| PERFORMANCE: Reviews | 12 | Reviews, filters, status | ✅ |
| DASHBOARD: Widgets | 12 | Quick launch, widgets, charts | ✅ |
| **VALIDATION: Cross-Module** | **8** | **Form validation patterns** | **✅** |
| **TOTAL** | **124** | **155+** | **✅ PRODUCTION READY** |

### Test Design

The test suite uses **autonomous QA exploration methodology** with 4 phases:
1. **MAP** — Discover UI elements and their selectors
2. **INFER** — Understand sub-functions and business logic
3. **EXECUTE** — Perform CRUD operations and verify behavior
4. **NEGATIVE TEST** — Test edge cases and error conditions

### Helper Functions

**login()** — Authenticates to OrangeHRM (uses default admin/admin123)  
**navigateToModule(moduleName)** — Navigates to a specific module (e.g., "ADMIN", "PIM")

### Selector Strategy

Tests use multiple selector fallback strategies for stability:
1. `data-testid` attributes (most specific)
2. `aria-label` (accessibility)
3. CSS class selectors
4. `nth()` filters for dynamic content
5. Explicit waits for async rendering

### Browser Support

- **Chromium** — Primary browser (CI default)
- **Firefox** — Alternative browser validation
- **WebKit** — Mobile/cross-platform validation

### Execution Options

See **[ORANGEHRM_TEST_GUIDE.md](ORANGEHRM_TEST_GUIDE.md)** for complete details:

1. **Smoke Test** (5 min) — ADMIN module only, quick gate
2. **Full Suite** (2.3 hours) — All 123 tests, 2 browsers
3. **Headed Mode** — Watch tests in real-time browser
4. **By-Module** — Run specific modules (ADMIN, PIM, LEAVE, etc.)
5. **Parallel** (45 min) — Run 4 workers for speed

## Key Constraints

- **Test data isolation** — Each test works with live OrangeHRM demo data
- **No hardcoded values** — Use dynamic selectors and data discovery
- **Flexible assertions** — Accept any valid data (not specific values)
- **Cross-browser compatible** — Tests run on Chromium, Firefox, WebKit
- **No API access** — Tests use UI automation only (Playwright)
- **Timeouts** — Set to 30s for dynamic content rendering
