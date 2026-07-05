#!/usr/bin/env node

/**
 * Requirement Guardrails Validator - REQ-1
 * Enforces that ALL requirement documentation is complete before testing
 * Exit: 0 = requirements met (testing approved), 1 = blocked
 */

const fs = require('fs');
const path = require('path');

const REQUIREMENTS = [
  { id: 'REQ-1.1', name: 'Functional Requirements', pattern: /functional requirement|feature|functionality/i },
  { id: 'REQ-1.2', name: 'Non-Functional Requirements', pattern: /non-functional|performance|scalability|security/i },
  { id: 'REQ-1.3', name: 'Business Objectives', pattern: /business objective|goal|purpose|mission/i },
  { id: 'REQ-1.4', name: 'User Personas', pattern: /user persona|end user|customer|admin/i },
  { id: 'REQ-1.5', name: 'Supported Devices', pattern: /device|desktop|mobile|tablet/i },
  { id: 'REQ-1.6', name: 'Supported Browsers', pattern: /browser|chrome|firefox|safari|edge/i },
  { id: 'REQ-1.7', name: 'Supported Operating Systems', pattern: /operating system|windows|macos|linux/i },
  { id: 'REQ-1.8', name: 'Supported Languages', pattern: /language|localization|i18n/i },
  { id: 'REQ-1.9', name: 'Regional Restrictions', pattern: /region|geographic|restriction/i },
  { id: 'REQ-1.10', name: 'Compliance Requirements', pattern: /compliance|gdpr|pci dss|hipaa|owasp|wcag/i },
  { id: 'REQ-1.11', name: 'Data Flow', pattern: /data flow|workflow|process flow/i },
  { id: 'REQ-1.12', name: 'External Dependencies', pattern: /dependency|external|third-party|integration/i },
  { id: 'REQ-1.13', name: 'APIs', pattern: /api|rest|graphql|endpoint/i },
  { id: 'REQ-1.14', name: 'Authentication Methods', pattern: /authentication|auth|oauth|jwt|session/i },
  { id: 'REQ-1.15', name: 'Third-Party Services', pattern: /payment|gateway|analytics|email/i },
  { id: 'REQ-1.16', name: 'Feature Flags', pattern: /feature flag|toggle|a\/b test|experiment/i },
  { id: 'REQ-1.17', name: 'Rollback Strategy', pattern: /rollback|revert|deployment|backup|recovery/i },
];

function validate() {
  const scopeFile = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  
  if (!fs.existsSync(scopeFile)) {
    console.error('\n❌ REQUIREMENT VALIDATION FAILED');
    console.error(`   Missing: DEMOWEBSHOP_SCOPE_DOCUMENT.md`);
    console.error('   Action: Create scope document before testing\n');
    process.exit(1);
  }

  const content = fs.readFileSync(scopeFile, 'utf-8');
  let passed = 0, failed = 0;

  console.log('\n📋 REQUIREMENT GUARDRAILS VALIDATION\n');

  REQUIREMENTS.forEach((req) => {
    const met = req.pattern.test(content);
    const status = met ? '✓' : '✗';
    console.log(`${status} ${req.id}: ${req.name}`);
    met ? passed++ : failed++;
  });

  console.log(`\n${passed}/17 requirements documented\n`);

  if (failed === 0) {
    console.log('✅ ALL REQUIREMENT GUARDRAILS MET - Testing Approved\n');
    process.exit(0);
  } else {
    console.log(`❌ ${failed} REQUIREMENT(S) MISSING - Testing Blocked\n`);
    process.exit(1);
  }
}

validate();
