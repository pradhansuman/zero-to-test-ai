# Professional QA Report Template

A **production-grade HTML dashboard** for any QA/testing project. Based on the `store-qa-report.html` template used for the Tricentis Demo Web Shop testing.

## Features

✅ **KPI Cards** – Total Tests, Passed, Failed, Flaky with animated pop-in effects  
✅ **Analytics Charts** – Pass rate (doughnut), suite breakdown (stacked bar), browser distribution (doughnut)  
✅ **Suite Breakdown** – Individual cards per test suite with progress bars and pass/fail counts  
✅ **Dark Theme** – Professional GitHub-style dark theme (#0d1117) with green/red accents  
✅ **Interactive** – Responsive design, smooth animations, Chart.js integration  
✅ **Customizable** – Works with ANY project, ANY test framework, ANY number of suites/browsers  

---

## Template Structure

```
Header Section
  ├─ Project name + status badge (PASS/FAIL)
  ├─ Date/time + test count + browsers
  └─ Gradient background with branding

KPI Cards
  ├─ Total Tests
  ├─ Passed (green)
  ├─ Failed (red)
  └─ Flaky (orange)

Charts Section
  ├─ Overall Pass Rate (doughnut with center text)
  ├─ Tests by Suite (horizontal stacked bar chart)
  └─ By Browser (doughnut distribution)

Suite Breakdown
  ├─ Individual cards per suite
  ├─ Pass rate %, progress bar, counts
  └─ Emoji icons + color-coded

Footer
  └─ Generation timestamp
```

---

## Usage

### Option 1: Use the Store Report as Template

The `store-qa-report.html` serves as a complete reference. To adapt it:

1. **Copy the entire HTML**
2. **Replace these sections:**
   - Project name in `<h1>` and `<title>`
   - Date/time in `.run-meta`
   - KPI values (Total, Passed, Failed, Flaky)
   - Suite data in `DATA` object
   - Browser data in `DATA.browsers`
   - Chart.js datasets

### Option 2: Programmatic Generation (Node.js)

```bash
node scripts/generate-professional-report.js \
  --project "MyApp QA Report" \
  --passed 285 \
  --failed 39 \
  --flaky 4
```

This generates: `myapp-qa-report.html`

### Option 3: Manual HTML Creation

```html
<!DOCTYPE html>
<html>
<head>
  <title>My Project QA Report</title>
  <!-- Copy CSS from store-qa-report.html -->
</head>
<body>
  <header>
    <div class="brand">
      <div class="brand-icon">🧪</div>
      <h1>My Project Name</h1>
    </div>
    <div class="gate-badge gate-pass">PASS</div>
  </header>
  
  <main>
    <!-- Copy KPI cards, charts, suite cards from template -->
  </main>
  
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <!-- Copy Chart.js code from store-qa-report.html -->
</body>
</html>
```

---

## Data Format

### KPI Data
```javascript
{
  total: 325,           // sum of all statuses
  passed: 281,          // tests with status = passed
  failed: 39,           // tests with status = failed
  flaky: 4              // tests with status = flaky
}
```

### Suite Data
```javascript
{
  suites: [
    {
      name: "Visual Regression",
      file: "visual.spec.ts",
      icon: "🎨",
      color: "#10b981",    // Tailwind green
      passed: 28,
      failed: 0
    },
    // ... more suites
  ]
}
```

### Browser Data
```javascript
{
  browsers: [
    { name: "Desktop Chrome", passed: 111 },
    { name: "Mobile Chrome", passed: 112 },
    { name: "Desktop Firefox", passed: 62 }
  ]
}
```

---

## Color Palette

Professional colors matching GitHub's dark theme:

| Element | Color | Usage |
|---------|-------|-------|
| Background | `#0d1117` | Main background |
| Cards | `#161b22` | Card backgrounds |
| Border | `#30363d` | Borders/dividers |
| Text | `#c9d1d9` | Main text |
| Muted | `#8b949e` | Secondary text |
| Pass | `#3fb950` | Green checkmarks |
| Fail | `#f85149` | Red X marks |
| Flaky | `#d29922` | Orange warning |
| Accent | `#7c3aed` | Gradient accent |

---

## Customization Examples

### Change Colors
```css
:root {
  --pass: #10b981;    /* Green to Emerald */
  --fail: #ef4444;    /* Red to Crimson */
  --accent: #6366f1;  /* Purple accent */
}
```

### Add More Suites
```javascript
suites: [
  { name: "New Suite", file: "new.spec.ts", icon: "📋", color: "#f59e0b", passed: 15, failed: 2 },
  // ... more
]
```

### Change Gate Logic
```javascript
const gate = config.failed === 0 && passRate >= 95 ? 'PASS' : 'FAIL';
```

---

## Integration with Test Runners

### Playwright
```javascript
// After test run completes, collect data:
const results = {
  passed: report.stats.expected,
  failed: report.stats.unexpected,
  flaky: report.stats.flaky,
};

// Generate report
generateReport({ project: "MyApp", ...results });
```

### Jest
```javascript
const testResult = runner.getTestResult();
const data = {
  passed: testResult.numPassedTests,
  failed: testResult.numFailedTests,
  flaky: testResult.numPendingTests,
};
```

### Cypress
```javascript
cy.task('afterRunHook', (results) => {
  const data = {
    passed: results.stats.passes,
    failed: results.stats.failures,
    flaky: results.stats.pending,
  };
});
```

---

## Real-World Examples

### Example 1: Tricentis Demo Web Shop
**File**: `store-qa-report.html` (complete production report)  
**Data**: 325 tests, 281 passed, 39 failed, 4 flaky  
**Suites**: 9 (Visual, API, Security, Performance, Endurance, A11y, CWV, Network, Error)  
**Browsers**: Desktop Chrome, Mobile Chrome, Desktop Firefox  

### Example 2: Your Project
```bash
node scripts/generate-professional-report.js \
  --project "YourApp" \
  --passed 150 \
  --failed 8 \
  --flaky 1
```

---

## Mobile Responsiveness

The template is fully responsive:
- **Desktop**: 4-column KPI grid → 2-column grid at 900px
- **Tablet**: Charts grid changes from 3 cols → 2 cols at 1100px
- **Mobile**: Single column layouts, 20px padding

All animations work on mobile with optimized performance.

---

## Accessibility

- ✅ Semantic HTML
- ✅ Color contrast meets WCAG AA
- ✅ No animation that disrespects `prefers-reduced-motion`
- ✅ Screen reader friendly with proper labels

---

## Performance

- **CSS**: Inline, no external stylesheets
- **Charts**: Chart.js v4.4.0 (30KB gzipped)
- **Total**: Single 200-400KB HTML file
- **Load time**: <1s on 4G
- **Rendering**: 60fps animations via CSS

---

## License

This template is based on the professional QA report design from the Zero-to-Test AI project. Use freely in any testing context.

---

## Next Steps

1. **For Tricentis**: Use `store-qa-report.html` directly
2. **For your project**: Copy the template and customize the data
3. **For automation**: Use `generate-professional-report.js` to auto-generate reports
4. **For CI/CD**: Integrate report generation into your pipeline

See `scripts/generate-professional-report.js` for programmatic usage.
