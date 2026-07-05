#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const COMPAT_TESTS = [
  { id: 'COMPAT-14.1', name: 'Chrome', pattern: /chrome|chromium/i },
  { id: 'COMPAT-14.2', name: 'Firefox', pattern: /firefox/i },
  { id: 'COMPAT-14.3', name: 'Safari', pattern: /safari|webkit/i },
  { id: 'COMPAT-14.4', name: 'Edge', pattern: /edge|microsoft edge/i },
  { id: 'COMPAT-14.5', name: 'Opera', pattern: /opera/i },
  { id: 'COMPAT-14.6', name: 'Mobile browsers', pattern: /mobile browser|mobile|app/i },
  { id: 'COMPAT-14.7', name: 'Windows', pattern: /windows|win/i },
  { id: 'COMPAT-14.8', name: 'Linux', pattern: /linux/i },
  { id: 'COMPAT-14.9', name: 'macOS', pattern: /macos|mac os|osx/i },
  { id: 'COMPAT-14.10', name: 'Android', pattern: /android/i },
  { id: 'COMPAT-14.11', name: 'iOS', pattern: /ios|iphone|ipad/i },
  { id: 'COMPAT-14.12', name: 'Tablets', pattern: /tablet|ipad|android tablet/i },
  { id: 'COMPAT-14.13', name: 'Foldables', pattern: /foldable|fold|galaxy fold/i },
  { id: 'COMPAT-14.14', name: 'Different resolutions', pattern: /resolution|screen size|viewport/i },
  { id: 'COMPAT-14.15', name: 'Version compatibility', pattern: /version|version compatibility|legacy/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ COMPATIBILITY VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 COMPATIBILITY GUARDRAILS VALIDATION\n');
  COMPAT_TESTS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${COMPAT_TESTS.length} compatibility tests documented\n`);
  process.exit(p === COMPAT_TESTS.length ? 0 : 1);
}
validate();
