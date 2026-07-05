#!/usr/bin/env node

/**
 * Coverage Guardrails Validator - REQ-4
 * Enforces that ALL test types are included for every feature
 * Exit: 0 = coverage complete (testing approved), 1 = blocked
 */

const fs = require('fs');
const path = require('path');

const COVERAGE_TYPES = [
  { id: 'COV-4.1', name: 'Positive Tests', pattern: /positive test|happy path|success case|valid input/i },
  { id: 'COV-4.2', name: 'Negative Tests', pattern: /negative test|invalid input|error case|bad request/i },
  { id: 'COV-4.3', name: 'Boundary Tests', pattern: /boundary test|boundary value|min|max|limit/i },
  { id: 'COV-4.4', name: 'Edge Cases', pattern: /edge case|corner case|unusual|extreme|rare condition/i },
  { id: 'COV-4.5', name: 'Error Handling', pattern: /error handling|exception|error scenario|graceful failure/i },
  { id: 'COV-4.6', name: 'Recovery', pattern: /recovery|retry|fallback|resilience|restart/i },
  { id: 'COV-4.7', name: 'Concurrency', pattern: /concurrency|concurrent|parallel|race condition|deadlock|thread/i },
  { id: 'COV-4.8', name: 'Data Validation', pattern: /data validation|input validation|schema|constraint|integrity/i },
  { id: 'COV-4.9', name: 'Accessibility', pattern: /accessibility|wcag|keyboard|screen reader|aria|a11y/i },
  { id: 'COV-4.10', name: 'Security', pattern: /security test|injection|xss|csrf|authentication|authorization/i },
  { id: 'COV-4.11', name: 'Performance', pattern: /performance test|load test|stress test|latency|throughput/i },
  { id: 'COV-4.12', name: 'Localization', pattern: /localization|i18n|language|locale|rtl|translation/i },
  { id: 'COV-4.13', name: 'Compatibility', pattern: /compatibility|browser|device|os|platform|version/i },
  { id: 'COV-4.14', name: 'Regression', pattern: /regression test|regression suite|existing feature/i },
  { id: 'COV-4.15', name: 'Chaos', pattern: /chaos test|chaos engineering|failure injection|resilience/i },
];

function validate() {
  const testFile = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  
  if (!fs.existsSync(testFile)) {
    console.error('\n❌ COVERAGE VALIDATION FAILED');
    console.error(`   Missing: DEMOWEBSHOP_SCOPE_DOCUMENT.md`);
    console.error('   Action: Ensure scope document includes coverage strategy\n');
    process.exit(1);
  }

  const content = fs.readFileSync(testFile, 'utf-8');
  let passed = 0, failed = 0;

  console.log('\n📋 COVERAGE GUARDRAILS VALIDATION\n');

  COVERAGE_TYPES.forEach((coverage) => {
    const met = coverage.pattern.test(content);
    const status = met ? '✓' : '✗';
    console.log(`${status} ${coverage.id}: ${coverage.name}`);
    met ? passed++ : failed++;
  });

  console.log(`\n${passed}/${COVERAGE_TYPES.length} test types covered\n`);

  if (failed === 0) {
    console.log('✅ ALL COVERAGE GUARDRAILS MET - Testing Approved\n');
    process.exit(0);
  } else {
    console.log(`❌ ${failed} COVERAGE TYPE(S) MISSING - Testing Blocked\n`);
    process.exit(1);
  }
}

validate();
