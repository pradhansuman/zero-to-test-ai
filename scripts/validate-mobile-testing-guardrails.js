#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const MOBILE_TESTS = [
  { id: 'MOBILE-15.1', name: 'Rotation', pattern: /rotation|portrait|landscape|orientation/i },
  { id: 'MOBILE-15.2', name: 'Background', pattern: /background|background process|app background/i },
  { id: 'MOBILE-15.3', name: 'Foreground', pattern: /foreground|app foreground|active/i },
  { id: 'MOBILE-15.4', name: 'Battery', pattern: /battery|battery drain|power/i },
  { id: 'MOBILE-15.5', name: 'GPS', pattern: /gps|location|geolocation/i },
  { id: 'MOBILE-15.6', name: 'Camera', pattern: /camera|photo|video/i },
  { id: 'MOBILE-15.7', name: 'Bluetooth', pattern: /bluetooth|bt|wireless/i },
  { id: 'MOBILE-15.8', name: 'NFC', pattern: /nfc|near field/i },
  { id: 'MOBILE-15.9', name: 'Biometrics', pattern: /biometric|fingerprint|face id|touch id/i },
  { id: 'MOBILE-15.10', name: 'Offline', pattern: /offline|offline mode|connectivity/i },
  { id: 'MOBILE-15.11', name: 'Slow network', pattern: /slow network|3g|network throttle|latency/i },
  { id: 'MOBILE-15.12', name: 'Airplane mode', pattern: /airplane mode|airplane/i },
  { id: 'MOBILE-15.13', name: 'Notifications', pattern: /notification|push|alert/i },
  { id: 'MOBILE-15.14', name: 'Permissions', pattern: /permission|app permission|privacy/i },
  { id: 'MOBILE-15.15', name: 'Storage', pattern: /storage|disk space|cache/i },
  { id: 'MOBILE-15.16', name: 'Memory pressure', pattern: /memory pressure|memory|ram/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ MOBILE TESTING VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 MOBILE TESTING GUARDRAILS VALIDATION\n');
  MOBILE_TESTS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${MOBILE_TESTS.length} mobile tests documented\n`);
  process.exit(p === MOBILE_TESTS.length ? 0 : 1);
}
validate();
