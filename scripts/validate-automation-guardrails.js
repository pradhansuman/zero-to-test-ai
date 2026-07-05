#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const AUTO_ITEMS = [
  { id: 'AUTO-27.1', name: 'Independent tests', pattern: /independent|test.*isolation/i },
  { id: 'AUTO-27.2', name: 'Repeatable', pattern: /repeatable|repeat|reproducib/i },
  { id: 'AUTO-27.3', name: 'Deterministic', pattern: /deterministic|deterministic/i },
  { id: 'AUTO-27.4', name: 'Fast execution', pattern: /fast|speed|performance/i },
  { id: 'AUTO-27.5', name: 'Parallel', pattern: /parallel|concurr|concurrent/i },
  { id: 'AUTO-27.6', name: 'Maintainable', pattern: /maintain|maintain/i },
  { id: 'AUTO-27.7', name: 'Reusable', pattern: /reusable|reuse/i },
  { id: 'AUTO-27.8', name: 'Reliable', pattern: /reliable|reliability|flaky/i },
  { id: 'AUTO-27.9', name: 'Environment independent', pattern: /environment.*independent|env.?indep/i },
  { id: 'AUTO-27.10', name: 'Stable', pattern: /stable|stability/i },
  { id: 'AUTO-27.11', name: 'CI/CD ready', pattern: /ci\/cd|cicd|pipeline/i },
  { id: 'AUTO-27.12', name: 'Docker', pattern: /docker|container|image/i },
  { id: 'AUTO-27.13', name: 'Cloud execution', pattern: /cloud|cloud.?native/i },
  { id: 'AUTO-27.14', name: 'Reporting', pattern: /report|reporting|artifact/i },
  { id: 'AUTO-27.15', name: 'Retry', pattern: /retry|retries|retry.*logic/i },
  { id: 'AUTO-27.16', name: 'Test isolation', pattern: /test.*isolation|isolated/i },
  { id: 'AUTO-27.17', name: 'Test cleanup', pattern: /cleanup|tear.?down|cleanup/i },
  { id: 'AUTO-27.18', name: 'Test data', pattern: /test.*data|test data/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ AUTOMATION GUARDRAILS VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 AUTOMATION GUARDRAILS VALIDATION (REQ-27)\n');
  AUTO_ITEMS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${AUTO_ITEMS.length} automation validations documented\n`);
  process.exit(p === AUTO_ITEMS.length ? 0 : 1);
}
validate();
