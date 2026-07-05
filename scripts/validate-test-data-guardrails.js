#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const DATA_ITEMS = [
  { id: 'DATA-25.1', name: 'Valid data', pattern: /valid data|valid input/i },
  { id: 'DATA-25.2', name: 'Invalid data', pattern: /invalid data|invalid input/i },
  { id: 'DATA-25.3', name: 'Boundary values', pattern: /boundary|boundary value/i },
  { id: 'DATA-25.4', name: 'Random data', pattern: /random data|randomized/i },
  { id: 'DATA-25.5', name: 'PII data', pattern: /pii|personally identif|personal data/i },
  { id: 'DATA-25.6', name: 'Masked data', pattern: /mask|redact|masked/i },
  { id: 'DATA-25.7', name: 'Synthetic data', pattern: /synthetic|fake data/i },
  { id: 'DATA-25.8', name: 'Large dataset', pattern: /large|bulk|volume/i },
  { id: 'DATA-25.9', name: 'Corrupted data', pattern: /corrupt|malformed|invalid/i },
  { id: 'DATA-25.10', name: 'Duplicate data', pattern: /duplicate|duplicate data/i },
  { id: 'DATA-25.11', name: 'Expired data', pattern: /expired|expir|stale/i },
  { id: 'DATA-25.12', name: 'Future data', pattern: /future|tomorrow/i },
  { id: 'DATA-25.13', name: 'Historical data', pattern: /historical|historical/i },
  { id: 'DATA-25.14', name: 'Isolation', pattern: /isolat|isolation/i },
  { id: 'DATA-25.15', name: 'Cleanup', pattern: /cleanup|clean|tear.?down/i },
  { id: 'DATA-25.16', name: 'Repeatability', pattern: /repeat|reproducib|idempotent/i },
  { id: 'DATA-25.17', name: 'Versioning', pattern: /version|version.*data/i },
  { id: 'DATA-25.18', name: 'Traceability', pattern: /tracab|track|lineage/i },
  { id: 'DATA-25.19', name: 'Ownership', pattern: /owner|own.*data/i },
  { id: 'DATA-25.20', name: 'Privacy', pattern: /privacy|confidential|secret/i },
  { id: 'DATA-25.21', name: 'Special characters', pattern: /special char|symbol/i },
  { id: 'DATA-25.22', name: 'Unicode', pattern: /unicode|utf.?8/i },
  { id: 'DATA-25.23', name: 'Emoji', pattern: /emoji|emoji/i },
  { id: 'DATA-25.24', name: 'SQL injection', pattern: /sql.?inject|sql injection/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ TEST DATA GUARDRAILS VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 TEST DATA GUARDRAILS VALIDATION (REQ-25)\n');
  DATA_ITEMS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${DATA_ITEMS.length} test data validations documented\n`);
  process.exit(p === DATA_ITEMS.length ? 0 : 1);
}
validate();
