#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const UI_TESTS = [
  { id: 'UI-12.1', name: 'Alignment', pattern: /alignment|aligned|layout|position/i },
  { id: 'UI-12.2', name: 'Spacing', pattern: /spacing|margin|padding|gap|distance/i },
  { id: 'UI-12.3', name: 'Typography', pattern: /typography|font|text size|line height/i },
  { id: 'UI-12.4', name: 'Responsive behavior', pattern: /responsive|mobile|tablet|breakpoint/i },
  { id: 'UI-12.5', name: 'Dark mode', pattern: /dark mode|dark theme|dark|theme/i },
  { id: 'UI-12.6', name: 'Light mode', pattern: /light mode|light theme|light/i },
  { id: 'UI-12.7', name: 'Orientation', pattern: /orientation|portrait|landscape|rotate/i },
  { id: 'UI-12.8', name: 'Animations', pattern: /animation|transition|motion|smooth/i },
  { id: 'UI-12.9', name: 'Icons', pattern: /icon|icons|visual|image/i },
  { id: 'UI-12.10', name: 'Loading indicators', pattern: /loading|loader|spinner|progress/i },
  { id: 'UI-12.11', name: 'Accessibility', pattern: /accessibility|a11y|wcag|aria/i },
  { id: 'UI-12.12', name: 'Contrast', pattern: /contrast|color contrast|wcag aa|wcag aaa/i },
  { id: 'UI-12.13', name: 'Focus order', pattern: /focus order|tab order|focus/i },
  { id: 'UI-12.14', name: 'Keyboard navigation', pattern: /keyboard|tab key|enter key|arrow key/i },
  { id: 'UI-12.15', name: 'Screen reader', pattern: /screen reader|jaws|nvda|aria label/i },
  { id: 'UI-12.16', name: 'Zoom', pattern: /zoom|magnification|scale/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ UI TESTING VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 UI TESTING GUARDRAILS VALIDATION\n');
  UI_TESTS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${UI_TESTS.length} ui tests documented\n`);
  process.exit(p === UI_TESTS.length ? 0 : 1);
}
validate();
