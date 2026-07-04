# 🔴 MANDATORY PROFESSIONAL QA REPORT FORMAT

## ⚠️ CRITICAL: THIS IS NON-NEGOTIABLE

**Every test execution MUST generate the professional QA dashboard in this exact format:**

```
📊 Professional QA Dashboard Format
├── KPI Cards (4 cards)
│   ├── Total Tests
│   ├── Passed (✅ Green)
│   ├── Failed (❌ Red)
│   └── Skipped (⚠️ Yellow)
├── Analytics Section
│   ├── Pie Chart (Pass Rate %)
│   └── Browser Coverage (bars)
├── Suite Breakdown (Grid)
│   └── Individual suite cards with pass rate %
└── Test Results Table
    └── Detailed test execution log
```

**NO EXCEPTIONS. NO ALTERNATIVES. NO OTHER FORMATS.**

---

## What the Report Contains

### 1. KPI Cards (Header Section)
- **Total Tests:** Total number of test cases executed
- **Passed:** Number of passing tests (GREEN #3fb950)
- **Failed:** Number of failing tests (RED #f85149)
- **Skipped:** Number of skipped tests (YELLOW #d29922)

### 2. Analytics Section
- **Pass Rate Pie Chart:** Visual representation of pass/fail ratio
- **Browser Coverage:** Breakdown by browser (Chromium, Firefox, WebKit)

### 3. Suite Breakdown
Grid of test suites showing:
- Suite name
- Pass rate percentage
- Test count (passed/total)
- Progress bar visualization

### 4. Test Results Table
- Test name
- Test suite
- Browser used
- Pass/Fail status with color coding

---

## Color Scheme (MANDATORY)

| Element | Color | Hex Code | Use Case |
|---------|-------|----------|----------|
| **Passed** | Green | #3fb950 | Test passed successfully |
| **Failed** | Red | #f85149 | Test failed |
| **Skipped** | Yellow | #d29922 | Test skipped |
| **Background** | Dark Grey | #0d1117 | Main background |
| **Card Background** | Darker Grey | #161b22 | Card backgrounds |
| **Border** | Light Grey | #30363d | Card borders |
| **Text** | Light Grey | #e6edf3 | Main text |
| **Accent** | Purple-Blue | #7c3aed, #2563eb | Gradients, accents |

---

## Design Requirements

### Typography
- **Font Family:** System fonts (Segoe UI, Roboto, Helvetica Neue)
- **Headings:** Font-weight 600-700, size 14-28px
- **Body Text:** Font-weight 400, size 11-14px
- **Labels:** Font-weight 600, uppercase, letter-spacing 0.5px

### Layout
- **Container:** Max-width 1400px, centered
- **Spacing:** 40px vertical sections, 20px card gaps
- **Grid:** auto-fit columns, minimum 200-280px width
- **Border Radius:** 6px (cards), 4px (buttons/tags), 50% (pie chart)

### Visual Elements
- **Borders:** 1px solid #30363d
- **Shadows:** None (flat design)
- **Gradients:** Linear/conic for accents and pie charts
- **Icons:** Emoji/Unicode icons (✓, ✅, ❌, ⚠️, 📊, 📈, 📋, 📝, 🌐)

### Interactivity
- **Hover States:** background #0d1117 on table rows
- **Progress Bars:** Green fill on light background
- **Tables:** Striped rows, border separators

---

## File Location & Naming

**Mandatory Output File:**
```
./tricentis-qa-dashboard.html
```

**Script Location:**
```
./scripts/generate-mandatory-dashboard.js
```

**This MUST be generated automatically after EVERY test execution.**

---

## How It's Generated

### Automatic Execution
The `run-tests.sh` script automatically:
1. Executes tests
2. Verifies Playwright report generated
3. **Runs the mandatory dashboard generator** (generate-mandatory-dashboard.js)
4. Verifies dashboard created
5. Displays viewing instructions

### Manual Generation
```bash
# Generate dashboard manually
node scripts/generate-mandatory-dashboard.js

# View the result
open tricentis-qa-dashboard.html
```

---

## Data Sources

The dashboard is populated from:
1. **Test Results Directory:** `./test-results/`
   - Each subdirectory = one test execution
   - Presence of `error-context.md` = test failed
   - Absence = test passed

2. **Browser Detection:** Extracted from directory names
   - `chromium` = Chromium browser
   - `firefox` = Firefox browser
   - `webkit` = WebKit (Safari) browser

3. **Suite Categorization:** Derived from test names
   - Homepage → Homepage & Navigation
   - Product → Product Catalog
   - Registration → Authentication
   - Cart → Shopping Cart
   - Checkout → Checkout
   - Account → Account Management
   - Pages → Content Pages
   - Error/Invalid → Error Handling
   - Performance/loads → Performance
   - Security/password → Security

---

## Enforcement Rules

### ✅ MUST HAVE
- [ ] KPI cards showing Total, Passed, Failed, Skipped
- [ ] Pie chart with pass rate percentage
- [ ] Browser coverage breakdown
- [ ] Suite breakdown grid with individual metrics
- [ ] Test results table with status indicators
- [ ] Color coding (green for pass, red for fail)
- [ ] Responsive design (mobile-friendly)
- [ ] Dark theme (#0d1117 background)
- [ ] Professional typography and spacing
- [ ] Generated automatically after every test run

### ❌ MUST NOT HAVE
- ❌ Alternative report formats
- ❌ Different color schemes
- ❌ Changed layout or structure
- ❌ Manual report creation
- ❌ Light theme backgrounds
- ❌ Missing KPI cards
- ❌ Incomplete data (charts without values)
- ❌ Different naming convention
- ❌ Reports in other file formats (PDF, Word, etc.)

---

## Compliance Checklist

Before considering test execution complete:

- [ ] Tests executed successfully (pass or fail)
- [ ] Playwright HTML report generated: `./playwright-report/index.html`
- [ ] **Mandatory dashboard generated: `./tricentis-qa-dashboard.html`** ← REQUIRED
- [ ] Dashboard displays KPI cards with correct numbers
- [ ] Dashboard shows pass rate pie chart
- [ ] Dashboard shows browser coverage breakdown
- [ ] Dashboard shows suite breakdown grid
- [ ] Dashboard shows test results table
- [ ] All colors match specification
- [ ] Dashboard is viewable in browser
- [ ] File size > 20KB (indicates content)
- [ ] Auto-generation script ran without errors

---

## Example Report View

```
╔═══════════════════════════════════════════════════════════════╗
║     📊 Tricentis QA - Full Suite Run                         ║
║     July 5, 2026 | 120 total tests                           ║
╚═══════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────┐
│  KPI Cards:                                                  │
│  ┌──────────────┬──────────────┬──────────────┬────────────┐ │
│  │ Total Tests  │ Passed ✅    │ Failed ❌    │ Skipped ⚠️ │ │
│  │     120      │    281       │     39       │      4     │ │
│  └──────────────┴──────────────┴──────────────┴────────────┘ │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Analytics:                                                  │
│  ┌──────────────────────────┬──────────────────────────────┐ │
│  │  Pass Rate: 88% (Pie)    │  Browser Coverage (Bars)     │ │
│  │  ✓ Passed: 281           │  Chromium: ████████░ 85%     │ │
│  │  ✗ Failed: 39            │  Firefox:  ███████░░ 75%     │ │
│  └──────────────────────────┴──────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Suite Breakdown:                                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Homepage        │  │ Product Catalog │  │ Auth        │ │
│  │ 100% (8/8)      │  │ 92% (9/10)      │  │ 83% (5/6)   │ │
│  │ ████████░░      │  │ █████████░      │  │ ██████░░░░  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│  ... more suites ...                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Test Results Table:                                        │
│  ┌────────────────────┬──────────┬──────────┬──────────┐    │
│  │ Test Name          │ Suite    │ Browser  │ Status   │    │
│  ├────────────────────┼──────────┼──────────┼──────────┤    │
│  │ Homepage loads     │ Homepage │ Chrome   │ ✓ PASSED │    │
│  │ Products display   │ Catalog  │ Chrome   │ ✓ PASSED │    │
│  │ Add to cart        │ Cart     │ Firefox  │ ✓ PASSED │    │
│  │ Checkout submit    │ Checkout │ Chrome   │ ✗ FAILED │    │
│  └────────────────────┴──────────┴──────────┴──────────┘    │
│  Showing 10 of 120 tests                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## CI/CD Integration

The dashboard is automatically generated in:
- Local development (`./scripts/run-tests.sh`)
- GitHub Actions (add to workflow)
- GitLab CI (add to pipeline)
- Jenkins (add to stage)
- Azure DevOps (add to task)

**The report MUST be committed to git with every test execution.**

---

## Summary

| Requirement | Status | Enforcement |
|------------|--------|------------|
| Professional Format | MANDATORY | No alternatives allowed |
| Auto-Generation | MANDATORY | Every test execution |
| KPI Cards | MANDATORY | 4 cards required |
| Analytics Charts | MANDATORY | Pie + Bars required |
| Suite Breakdown | MANDATORY | Grid required |
| Test Table | MANDATORY | Required |
| Dark Theme | MANDATORY | #0d1117 background |
| Color Scheme | MANDATORY | Exact colors specified |
| Responsive Design | MANDATORY | Mobile-friendly |
| Browser Coverage | MANDATORY | Chromium, Firefox, WebKit |
| Pass Rate Display | MANDATORY | Percentage shown |
| Automatic Execution | MANDATORY | No manual steps |

---

**🔴 THIS IS NON-NEGOTIABLE. NO EXCEPTIONS. NO ALTERNATIVE FORMATS.**

**Every test execution MUST produce a professional QA dashboard in the exact format specified above.**

**Failure to generate this report = Test execution is INCOMPLETE.**

---

**Report Generator Location:** `./scripts/generate-mandatory-dashboard.js`  
**Mandatory Output File:** `./tricentis-qa-dashboard.html`  
**Auto-Execution:** `./scripts/run-tests.sh` → generates automatically
