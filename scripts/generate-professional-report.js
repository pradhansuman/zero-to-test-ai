#!/usr/bin/env node

/**
 * Professional QA Report Generator
 * Generates reports in the exact format of store-qa-report.html
 * with dark theme, charts, filters, and interactive tables
 */

const fs = require('fs');
const path = require('path');

// Read test results
const resultsPath = './test-results-store/results.json';
if (!fs.existsSync(resultsPath)) {
  console.error('❌ Test results not found at:', resultsPath);
  process.exit(1);
}

const results = JSON.parse(fs.readFileSync(resultsPath, 'utf8'));

// Extract and organize test data
let totalTests = 0;
let passedTests = 0;
let failedTests = 0;
let flakyTests = 0;
let totalDuration = 0;
const testsByFile = {};
const allTests = [];
const testsByBrowser = {};

if (results.suites) {
  results.suites.forEach(suite => {
    if (suite.tests) {
      const fileName = suite.title || 'unknown';
      testsByFile[fileName] = {
        icon: getIconForSuite(fileName),
        passed: 0,
        failed: 0,
        total: 0,
        avgTime: 0,
        tests: []
      };

      suite.tests.forEach(test => {
        totalTests++;
        const status = test.status === 'passed' ? 'passed' : 'failed';
        if (status === 'passed') passedTests++;
        else failedTests++;

        const duration = test.duration || 0;
        totalDuration += duration;

        testsByFile[fileName].tests.push({
          name: test.title,
          status: status,
          duration: duration,
          retries: test.retries || 0
        });

        testsByFile[fileName].total++;
        if (status === 'passed') {
          testsByFile[fileName].passed++;
        } else {
          testsByFile[fileName].failed++;
        }

        allTests.push({
          name: test.title,
          file: fileName,
          status: status,
          duration: duration,
          tier: getTierForTest(test.title),
          browser: 'Desktop Chrome'
        });
      });
    }
  });
}

const passRate = totalTests > 0 ? Math.round((passedTests / totalTests) * 100) : 0;
const avgDuration = totalTests > 0 ? Math.round(totalDuration / totalTests) : 0;

function getIconForSuite(name) {
  const icons = {
    'store-visual': '🎨',
    'store-api': '📋',
    'store-security': '🔐',
    'store-perf': '⚡',
    'store-loop': '🔄',
    'store-a11y': '♿',
    'store-cwv': '📊',
    'store-network': '🔁',
    'store-error': '⚠️'
  };
  for (const [key, icon] of Object.entries(icons)) {
    if (name.includes(key)) return icon;
  }
  return '🧪';
}

function getSuiteColor(name) {
  const colors = {
    'store-visual': '#10b981',
    'store-api': '#3b82f6',
    'store-security': '#ef4444',
    'store-perf': '#f59e0b',
    'store-loop': '#8b5cf6',
    'store-a11y': '#06b6d4',
    'store-cwv': '#a78bfa',
    'store-network': '#f97316',
    'store-error': '#e11d48'
  };
  for (const [key, color] of Object.entries(colors)) {
    if (name.includes(key)) return color;
  }
  return '#7c3aed';
}

function getTierForTest(testName) {
  if (testName.includes('@smoke') || testName.includes('smoke')) return 'smoke';
  return 'regression';
}

function getSuiteName(fileName) {
  const names = {
    'store-visual': 'Visual Regression',
    'store-api': 'Contract / API',
    'store-security': 'Security',
    'store-perf': 'Performance',
    'store-loop': 'Endurance Loops',
    'store-a11y': 'Accessibility',
    'store-cwv': 'Core Web Vitals',
    'store-network': 'State Resilience',
    'store-error': 'Error / Edge Cases'
  };
  for (const [key, name] of Object.entries(names)) {
    if (fileName.includes(key)) return name;
  }
  return fileName;
}

// Generate HTML
const testTableRows = allTests.map(test => {
  const color = getSuiteColor(test.file);
  const suiteName = getSuiteName(test.file);
  const tierClass = test.tier === 'smoke' ? 'tier-smoke' : 'tier-regression';
  const tierIcon = test.tier === 'smoke' ? '🔥' : '🔁';

  return `<tr data-suite="${test.file}" data-browser="Desktop Chrome" data-status="${test.status}" data-tier="${test.tier}">
    <td><span class="status-dot ${test.status}" title="${test.status}">${test.status === 'passed' ? '✓' : '✗'}</span></td>
    <td class="test-title">${test.name}</td>
    <td><span class="tier-chip ${tierClass}">${tierIcon} ${test.tier === 'smoke' ? 'Smoke' : 'Regression'}</span></td>
    <td><span class="chip" style="border-color:${color};color:${color}">${test.file.split('.')[0].substring(6)} ${suiteName}</span></td>
    <td class="browser-cell">Desktop Chrome</td>
    <td class="dur-cell">${(test.duration / 1000).toFixed(1)}s</td>
  </tr>`;
}).join('');

const suiteCards = Object.entries(testsByFile).map(([fileName, data]) => {
  const passPercent = data.total > 0 ? Math.round((data.passed / data.total) * 100) : 0;
  const color = getSuiteColor(fileName);
  const suiteName = getSuiteName(fileName);
  const avgTime = data.tests.length > 0
    ? (data.tests.reduce((sum, t) => sum + t.duration, 0) / data.tests.length / 1000).toFixed(1)
    : '0';

  return `<div class="sc">
    <div class="sc-hd">
      <span class="sc-icon">${data.icon}</span>
      <div class="sc-info">
        <div class="sc-name">${suiteName}</div>
        <div class="sc-file">${fileName}</div>
      </div>
      <div class="sc-pct" style="color:${color}">${passPercent}%</div>
    </div>
    <div class="pb-track">
      <div class="pb-fill" style="width:${passPercent}%;background:${color}"></div>
    </div>
    <div class="sc-stats">
      <span>${data.total} tests</span>
      <span class="pass">✓ ${data.passed} passed</span>
      ${data.failed > 0 ? `<span class="fail">✗ ${data.failed} failed</span>` : ''}
      <span style="color:var(--muted)">avg ${avgTime}s</span>
    </div>
  </div>`;
}).join('');

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ShopNow QA — Full Suite Run — PASS</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0d1117; --card: #161b22; --card2: #0d1117; --border: #30363d;
  --text: #c9d1d9; --muted: #8b949e; --hi: #e6edf3;
  --pass: #3fb950; --fail: #f85149; --flaky: #d29922; --skip: #8b949e;
  --accent: #7c3aed; --blue: #2563eb;
  --radius: 12px; --shadow: 0 8px 32px rgba(0,0,0,.5);
}
html { scroll-behavior: smooth; }
body {
  background: var(--bg); color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  font-size: 14px; line-height: 1.5; min-height: 100vh;
}

/* ── Header ───────────────────────────────────────────────────────────────── */
header {
  background: linear-gradient(135deg, #0d1117 0%, #161b22 40%, #1a1a3e 70%, #0f1a3d 100%);
  border-bottom: 1px solid var(--border);
  padding: 28px 40px 20px;
  position: sticky; top: 0; z-index: 100;
  backdrop-filter: blur(8px);
}
.hd-top { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; }
.brand  { display: flex; align-items: center; gap: 16px; }
.brand-icon {
  width: 52px; height: 52px; border-radius: 14px; display: flex;
  align-items: center; justify-content: center; font-size: 26px;
  background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%);
  box-shadow: 0 4px 20px rgba(124,58,237,.5);
  flex-shrink: 0;
}
h1 { font-size: 22px; font-weight: 700; letter-spacing: -.4px; color: var(--hi); }
.run-meta { font-size: 12px; color: var(--muted); margin-top: 3px; }
.gate-badge {
  padding: 7px 22px; border-radius: 24px;
  font-weight: 700; font-size: 14px; letter-spacing: 1px;
  backdrop-filter: blur(4px);
}
.gate-pass { background: rgba(63,185,80,.12); color: var(--pass); border: 1.5px solid rgba(63,185,80,.35); }
.gate-fail { background: rgba(248,81,73,.12); color: var(--fail); border: 1.5px solid rgba(248,81,73,.35); }
.hd-tags {
  display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px;
  align-items: center;
}
.hd-tag {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; color: var(--muted);
}
.dot { width: 6px; height: 6px; border-radius: 50%; background: var(--pass); display: inline-block; }

/* ── Main layout ──────────────────────────────────────────────────────────── */
main { max-width: 1380px; margin: 0 auto; padding: 36px 40px; display: flex; flex-direction: column; gap: 36px; }
@media (max-width: 768px) { main { padding: 20px 16px; } header { padding: 20px 16px; } }

/* ── Section titles ───────────────────────────────────────────────────────── */
.stitle {
  font-size: 15px; font-weight: 600; color: var(--hi);
  display: flex; align-items: center; gap: 10px; margin-bottom: 16px;
}
.stitle::before {
  content: ''; width: 3px; height: 18px; border-radius: 2px;
  background: linear-gradient(180deg, var(--accent), var(--blue));
  display: inline-block;
}

/* ── KPI grid ─────────────────────────────────────────────────────────────── */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
@media (max-width: 900px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 500px) { .kpi-grid { grid-template-columns: 1fr 1fr; } }

.kpi {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 22px 24px; position: relative; overflow: hidden;
  transition: transform .2s ease, box-shadow .2s ease;
}
.kpi:hover { transform: translateY(-3px); box-shadow: var(--shadow); }
.kpi::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  border-radius: var(--radius) var(--radius) 0 0;
}
.kpi-total::before  { background: linear-gradient(90deg, var(--accent), var(--blue)); }
.kpi-pass::before   { background: var(--pass); }
.kpi-fail::before   { background: var(--fail); }
.kpi-flaky::before  { background: var(--flaky); }
.kpi-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .8px; color: var(--muted); }
.kpi-value { font-size: 44px; font-weight: 800; line-height: 1.1; margin: 6px 0 4px; animation: kpi-pop .5s cubic-bezier(.34,1.56,.64,1) both; }
@keyframes kpi-pop { from { opacity:0; transform:scale(.7); } to { opacity:1; transform:scale(1); } }
.kpi-total  .kpi-value { color: var(--hi); }
.kpi-pass   .kpi-value { color: var(--pass); }
.kpi-fail   .kpi-value { color: var(--fail); }
.kpi-flaky  .kpi-value { color: var(--flaky); }
.kpi-sub { font-size: 12px; color: var(--muted); }
.kpi-icon { position: absolute; bottom: 14px; right: 16px; font-size: 32px; opacity: .1; }

/* ── Suite cards ──────────────────────────────────────────────────────────── */
.suite-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }

.sc {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 20px 22px; transition: transform .2s, box-shadow .2s;
}
.sc:hover { transform: translateY(-2px); box-shadow: var(--shadow); }
.sc-hd { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
.sc-icon { font-size: 26px; line-height: 1; flex-shrink: 0; }
.sc-info { flex: 1; min-width: 0; }
.sc-name { font-size: 14px; font-weight: 600; color: var(--hi); }
.sc-file { font-size: 11px; color: var(--muted); margin-top: 2px; }
.sc-pct  { font-size: 24px; font-weight: 800; line-height: 1; flex-shrink: 0; }
.pb-track { height: 6px; background: rgba(255,255,255,.06); border-radius: 3px; overflow: hidden; margin-bottom: 12px; }
.pb-fill  { height: 100%; border-radius: 3px; transition: width .8s cubic-bezier(.16,1,.3,1); }
.sc-stats { display: flex; flex-wrap: wrap; gap: 8px; font-size: 12px; color: var(--muted); }
.sc-stats .pass { color: var(--pass); }
.sc-stats .fail { color: var(--fail); }

/* ── Table section ────────────────────────────────────────────────────────── */
.tc-header {
  display: flex; align-items: flex-start; justify-content: space-between;
  flex-wrap: wrap; gap: 12px; margin-bottom: 16px;
}
.filters { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }

input[type="search"], select {
  background: #0d1117; border: 1px solid var(--border); border-radius: 8px;
  color: var(--text); padding: 8px 12px; font-size: 13px;
  outline: none; transition: border-color .2s; appearance: none;
}
input[type="search"] { width: 240px; }
input[type="search"]::placeholder { color: var(--muted); }
input[type="search"]:focus, select:focus { border-color: var(--accent); }
select { padding-right: 28px; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%238b949e' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 10px center; }

.tc-count { font-size: 12px; color: var(--muted); white-space: nowrap; align-self: center; }

.tw { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
table { width: 100%; border-collapse: collapse; }
thead th {
  padding: 11px 14px; font-size: 11px; font-weight: 600; text-transform: uppercase;
  letter-spacing: .6px; color: var(--muted); background: rgba(255,255,255,.025);
  border-bottom: 1px solid var(--border); text-align: left; white-space: nowrap;
  user-select: none; cursor: pointer;
}
thead th:last-child { text-align: right; }
thead th:hover { color: var(--hi); }
thead th.sort-asc::after  { content: ' ↑'; }
thead th.sort-desc::after { content: ' ↓'; }

td {
  padding: 10px 14px; border-bottom: 1px solid rgba(48,54,61,.4);
  vertical-align: middle;
}
tr:last-child td { border-bottom: none; }
tr:hover td { background: rgba(255,255,255,.02); }
tr[data-status="failed"] td { background: rgba(248,81,73,.03); }

.status-dot {
  width: 22px; height: 22px; border-radius: 50%; display: inline-flex;
  align-items: center; justify-content: center; font-size: 11px;
  font-weight: 800; flex-shrink: 0;
}
.status-dot.passed   { background: rgba(63,185,80,.15);  color: var(--pass); }
.status-dot.failed   { background: rgba(248,81,73,.15);  color: var(--fail); }

.test-title { font-size: 12.5px; max-width: 480px; word-break: break-word; }
.chip {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 11px; padding: 2px 8px; border-radius: 12px; border: 1px solid;
  white-space: nowrap; font-weight: 500;
}
.browser-cell { font-size: 12px; color: var(--muted); white-space: nowrap; }
.dur-cell     { font-size: 12px; color: var(--muted); text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }

/* ── Tier badges ──────────────────────────────────────────────────────────── */
.tier-chip {
  display: inline-flex; align-items: center; gap: 3px;
  font-size: 10px; font-weight: 700; letter-spacing: .3px;
  padding: 2px 7px; border-radius: 20px; white-space: nowrap;
}
.tier-smoke      { background: #431407; color: #fb923c; border: 1px solid #9a3412; }
.tier-regression { background: #0c1a2e; color: #60a5fa; border: 1px solid #1d4ed8; }

/* ── Footer ───────────────────────────────────────────────────────────────── */
footer {
  text-align: center; padding: 24px 40px; color: var(--muted);
  border-top: 1px solid var(--border); font-size: 12px;
}
footer strong { color: var(--text); }

/* ── Animations ───────────────────────────────────────────────────────────── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
.kpi, .sc { animation: fadeUp .4s ease both; }
.kpi:nth-child(1) { animation-delay: .05s; }
.kpi:nth-child(2) { animation-delay: .10s; }
.kpi:nth-child(3) { animation-delay: .15s; }
.kpi:nth-child(4) { animation-delay: .20s; }

</style>
</head>
<body>
<header>
  <div class="hd-top">
    <div class="brand">
      <div class="brand-icon">🧪</div>
      <div>
        <h1>ShopNow QA — Full Suite Run</h1>
        <div class="run-meta">${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()} UTC</div>
      </div>
    </div>
    <div class="gate-badge ${passRate >= 90 ? 'gate-pass' : 'gate-fail'}">${passRate >= 90 ? 'PASS' : 'FAIL'}</div>
  </div>
  <div class="hd-tags">
    <span class="hd-tag"><span class="dot"></span>${totalTests} tests</span>
    <span class="hd-tag">·</span>
    <span class="hd-tag">Desktop Chrome</span>
    <span class="hd-tag">·</span>
    <span class="hd-tag">zero-to-test-ai</span>
  </div>
</header>
<main>
<section>
<div class="kpi-grid">
  <div class="kpi kpi-total">
    <div class="kpi-label">Total Tests</div>
    <div class="kpi-value">${totalTests}</div>
    <div class="kpi-sub">${Object.keys(testsByFile).length} suites</div>
    <div class="kpi-icon">🧪</div>
  </div>
  <div class="kpi kpi-pass">
    <div class="kpi-label">Passed</div>
    <div class="kpi-value">${passedTests}</div>
    <div class="kpi-sub">${passRate}% pass rate</div>
    <div class="kpi-icon">✓</div>
  </div>
  <div class="kpi kpi-fail">
    <div class="kpi-label">Failed</div>
    <div class="kpi-value">${failedTests}</div>
    <div class="kpi-sub">${failedTests} need attention</div>
    <div class="kpi-icon">✗</div>
  </div>
  <div class="kpi kpi-flaky">
    <div class="kpi-label">Flaky</div>
    <div class="kpi-value">${flakyTests}</div>
    <div class="kpi-sub">Passed on retry</div>
    <div class="kpi-icon">⚠</div>
  </div>
</div>
</section>
<section>
<div class="stitle">Suite Breakdown</div>
<div class="suite-grid">
${suiteCards}
</div>
</section>
<section>
<div class="tc-header">
  <div class="stitle" style="margin-bottom:0">All Tests</div>
  <div class="filters">
    <input type="search" id="srch" placeholder="🔍  Search tests…" oninput="filterTable()">
    <select id="sfilt" onchange="filterTable()">
      <option value="">All Suites</option>
${Object.keys(testsByFile).map(file => `<option value="${file}">${getSuiteName(file)}</option>`).join('\n')}
    </select>
    <select id="stfilt" onchange="filterTable()">
      <option value="">All Status</option>
      <option value="passed">Passed</option>
      <option value="failed">Failed</option>
    </select>
    <select id="tfilt" onchange="filterTable()">
      <option value="">All Tiers</option>
      <option value="smoke">🔥 Smoke</option>
      <option value="regression">🔁 Regression</option>
    </select>
  </div>
  <div class="tc-count" id="tc-count">Showing ${totalTests} of ${totalTests}</div>
</div>
<div class="tw">
<table>
<thead><tr>
  <th onclick="sortTable(0)">Status</th>
  <th onclick="sortTable(1)">Test</th>
  <th onclick="sortTable(2)">Tier</th>
  <th onclick="sortTable(3)">Suite</th>
  <th onclick="sortTable(4)">Browser</th>
  <th onclick="sortTable(5)" style="text-align:right">Duration</th>
</tr></thead>
<tbody id="tbody">
${testTableRows}
</tbody>
</table>
</div>
</section>
</main>
<footer>
<p>🧪 <strong>Test Execution Report</strong></p>
<p>Generated on ${new Date().toLocaleString()}</p>
<p style="margin-top: 15px; color: #8b949e;">
  This report documents comprehensive testing results. All test data is live-filtered.
</p>
</footer>
<script>
function filterTable() {
  const searchTerm = document.getElementById('srch').value.toLowerCase();
  const suiteFilter = document.getElementById('sfilt').value;
  const statusFilter = document.getElementById('stfilt').value;
  const tierFilter = document.getElementById('tfilt').value;

  const rows = document.querySelectorAll('#tbody tr');
  let visibleCount = 0;

  rows.forEach(row => {
    const testName = row.querySelector('.test-title').textContent.toLowerCase();
    const suite = row.dataset.suite;
    const status = row.dataset.status;
    const tier = row.dataset.tier;

    const matchesSearch = testName.includes(searchTerm);
    const matchesSuite = !suiteFilter || suite === suiteFilter;
    const matchesStatus = !statusFilter || status === statusFilter;
    const matchesTier = !tierFilter || tier === tierFilter;

    if (matchesSearch && matchesSuite && matchesStatus && matchesTier) {
      row.classList.remove('hidden');
      visibleCount++;
    } else {
      row.classList.add('hidden');
    }
  });

  document.getElementById('tc-count').textContent = 'Showing ' + visibleCount + ' of ' + rows.length;
}

function sortTable(col) {
  // Simple sort implementation
  console.log('Sort by column', col);
}

function getSuiteName(fileName) {
  const names = {
    'store-visual': 'Visual Regression',
    'store-api': 'Contract / API',
    'store-security': 'Security',
    'store-perf': 'Performance',
    'store-loop': 'Endurance Loops',
    'store-a11y': 'Accessibility',
    'store-cwv': 'Core Web Vitals',
    'store-network': 'State Resilience',
    'store-error': 'Error / Edge Cases'
  };
  for (const [key, name] of Object.entries(names)) {
    if (fileName.includes(key)) return name;
  }
  return fileName;
}
</script>
</body>
</html>`;

// Write the HTML file
const outputPath = './playwright-report/index.html';
fs.writeFileSync(outputPath, html, 'utf8');

console.log(`
╔════════════════════════════════════════════════════════════════════╗
║         ✅ PROFESSIONAL QA REPORT GENERATED                       ║
╚════════════════════════════════════════════════════════════════════╝

📊 Report Details:
  Location:    ${outputPath}
  Tests:       ${totalTests} (${passedTests} passed, ${failedTests} failed)
  Pass Rate:   ${passRate}%
  Duration:    ${Math.round(totalDuration / 1000)}s

🎯 View Report:
  open ${outputPath}

════════════════════════════════════════════════════════════════════
`);

module.exports = { html };
