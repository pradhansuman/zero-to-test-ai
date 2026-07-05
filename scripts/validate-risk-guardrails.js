#!/usr/bin/env node

/**
 * Risk Guardrails Validator - REQ-3
 * Enforces that ALL risk categories are identified and documented
 * Exit: 0 = risks identified (testing approved), 1 = blocked
 */

const fs = require('fs');
const path = require('path');

const RISKS = [
  { id: 'RISK-3.1', name: 'Business Risks', pattern: /business risk|revenue|market|competitive|customer impact/i },
  { id: 'RISK-3.2', name: 'Technical Risks', pattern: /technical risk|architecture|scalability|technical debt|integration|compatibility/i },
  { id: 'RISK-3.3', name: 'Security Risks', pattern: /security risk|vulnerability|breach|attack|injection|xss|csrf|authentication|authorization/i },
  { id: 'RISK-3.4', name: 'Performance Risks', pattern: /performance risk|latency|throughput|bottleneck|slow|timeout/i },
  { id: 'RISK-3.5', name: 'Compliance Risks', pattern: /compliance risk|regulatory|gdpr|pci dss|hipaa|legal|audit/i },
  { id: 'RISK-3.6', name: 'Privacy Risks', pattern: /privacy risk|pii|data protection|user data|sensitive information|gdpr violation/i },
  { id: 'RISK-3.7', name: 'Financial Risks', pattern: /financial risk|cost|budget|expense|payment|fraud|loss/i },
  { id: 'RISK-3.8', name: 'Operational Risks', pattern: /operational risk|availability|downtime|incident|outage|sla/i },
  { id: 'RISK-3.9', name: 'Deployment Risks', pattern: /deployment risk|rollout|release|migration|downtime|cutover/i },
  { id: 'RISK-3.10', name: 'Recovery Risks', pattern: /recovery risk|backup|disaster recovery|rto|rpo|failover|restore/i },
];

function validate() {
  const riskFile = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  
  if (!fs.existsSync(riskFile)) {
    console.error('\n❌ RISK VALIDATION FAILED');
    console.error(`   Missing: DEMOWEBSHOP_SCOPE_DOCUMENT.md`);
    console.error('   Action: Ensure scope document includes risk assessment\n');
    process.exit(1);
  }

  const content = fs.readFileSync(riskFile, 'utf-8');
  let passed = 0, failed = 0;

  console.log('\n📋 RISK GUARDRAILS VALIDATION\n');

  RISKS.forEach((risk) => {
    const met = risk.pattern.test(content);
    const status = met ? '✓' : '✗';
    console.log(`${status} ${risk.id}: ${risk.name}`);
    met ? passed++ : failed++;
  });

  console.log(`\n${passed}/${RISKS.length} risk categories identified\n`);

  if (failed === 0) {
    console.log('✅ ALL RISK GUARDRAILS MET - Testing Approved\n');
    process.exit(0);
  } else {
    console.log(`❌ ${failed} RISK CATEGORY(IES) MISSING - Testing Blocked\n`);
    process.exit(1);
  }
}

validate();
