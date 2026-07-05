#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const A11Y_TESTS = [
  { id: 'A11Y-13.1', name: 'WCAG 2.2', pattern: /wcag|wcag 2.2|wcag a|wcag aa|wcag aaa/i },
  { id: 'A11Y-13.2', name: 'Keyboard only', pattern: /keyboard only|keyboard accessible|keyboard navigation/i },
  { id: 'A11Y-13.3', name: 'Tab order', pattern: /tab order|tab sequence|focus order/i },
  { id: 'A11Y-13.4', name: 'Focus', pattern: /focus indicator|focus visible|focus/i },
  { id: 'A11Y-13.5', name: 'ARIA', pattern: /aria|aria label|aria description|role/i },
  { id: 'A11Y-13.6', name: 'Contrast', pattern: /contrast|color contrast|wcag contrast/i },
  { id: 'A11Y-13.7', name: 'Screen readers', pattern: /screen reader|jaws|nvda|voiceover|accessible/i },
  { id: 'A11Y-13.8', name: 'Color blindness', pattern: /color blindness|colorblind|color contrast/i },
  { id: 'A11Y-13.9', name: 'Captions', pattern: /caption|closed caption|subtitle|audio description/i },
  { id: 'A11Y-13.10', name: 'Alternative text', pattern: /alt text|alternative text|alt attribute/i },
  { id: 'A11Y-13.11', name: 'Resize', pattern: /resize|text resize|zoom|magnification/i },
  { id: 'A11Y-13.12', name: 'Motion reduction', pattern: /motion reduction|prefers-reduced-motion|animation/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ ACCESSIBILITY VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 ACCESSIBILITY GUARDRAILS VALIDATION\n');
  A11Y_TESTS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${A11Y_TESTS.length} accessibility tests documented\n`);
  process.exit(p === A11Y_TESTS.length ? 0 : 1);
}
validate();
