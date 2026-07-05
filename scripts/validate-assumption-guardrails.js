#!/usr/bin/env node

/**
 * Assumption Guardrails Validator - REQ-2
 * Enforces that ALL assumptions are documented before testing
 * Exit: 0 = assumptions documented (testing approved), 1 = blocked
 */

const fs = require('fs');
const path = require('path');

const ASSUMPTIONS = [
  { id: 'ASM-2.1', name: 'Test Environment Parity', pattern: /test environment|production parity|environment equivalence/i },
  { id: 'ASM-2.2', name: 'Test Data Representative', pattern: /test data|representative|realistic|production-like/i },
  { id: 'ASM-2.3', name: 'APIs Stable', pattern: /api stability|stable api|api contract|breaking change/i },
  { id: 'ASM-2.4', name: 'Network Available', pattern: /network|connectivity|internet|bandwidth/i },
  { id: 'ASM-2.5', name: 'Payment Gateway Sandbox Parity', pattern: /payment gateway|payment sandbox|payment behavior|stripe|paypal/i },
  { id: 'ASM-2.6', name: 'Database Consistency', pattern: /database|consistency|replication|backup|data integrity/i },
  { id: 'ASM-2.7', name: 'External Service Availability', pattern: /external service|third-party|service availability|sla|uptime/i },
  { id: 'ASM-2.8', name: 'Authentication Service Operational', pattern: /authentication|auth service|sso|oauth|login service/i },
  { id: 'ASM-2.9', name: 'Cache Invalidation Strategy', pattern: /cache|cache invalidation|ttl|expiration|cache coherence/i },
  { id: 'ASM-2.10', name: 'Concurrent User Limits', pattern: /concurrent user|concurrent session|connection pool|thread pool/i },
];

function validate() {
  const assumptionFile = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  
  if (!fs.existsSync(assumptionFile)) {
    console.error('\n❌ ASSUMPTION VALIDATION FAILED');
    console.error(`   Missing: DEMOWEBSHOP_SCOPE_DOCUMENT.md`);
    console.error('   Action: Ensure scope document includes assumptions section\n');
    process.exit(1);
  }

  const content = fs.readFileSync(assumptionFile, 'utf-8');
  let passed = 0, failed = 0;

  console.log('\n📋 ASSUMPTION GUARDRAILS VALIDATION\n');

  ASSUMPTIONS.forEach((assumption) => {
    const met = assumption.pattern.test(content);
    const status = met ? '✓' : '✗';
    console.log(`${status} ${assumption.id}: ${assumption.name}`);
    met ? passed++ : failed++;
  });

  console.log(`\n${passed}/${ASSUMPTIONS.length} assumptions documented\n`);

  if (failed === 0) {
    console.log('✅ ALL ASSUMPTION GUARDRAILS MET - Testing Approved\n');
    process.exit(0);
  } else {
    console.log(`❌ ${failed} ASSUMPTION(S) MISSING - Testing Blocked\n`);
    process.exit(1);
  }
}

validate();
