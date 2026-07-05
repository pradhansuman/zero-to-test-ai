#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const DATA_TESTS = [
  { id: 'DV-7.1', name: 'Stored correctly', pattern: /stored|database storage|persistence/i },
  { id: 'DV-7.2', name: 'Displayed correctly', pattern: /displayed|rendering|ui display|output/i },
  { id: 'DV-7.3', name: 'Retrieved correctly', pattern: /retrieved|fetch|query|read/i },
  { id: 'DV-7.4', name: 'Updated correctly', pattern: /updated|modified|updated|changed/i },
  { id: 'DV-7.5', name: 'Deleted correctly', pattern: /deleted|removed|purged/i },
  { id: 'DV-7.6', name: 'Encrypted', pattern: /encrypted|encryption|cipher|secure/i },
  { id: 'DV-7.7', name: 'Masked', pattern: /masked|obfuscated|hidden/i },
  { id: 'DV-7.8', name: 'Hashed', pattern: /hashed|hash|bcrypt|argon/i },
  { id: 'DV-7.9', name: 'Audited', pattern: /audit|audit trail|audit log/i },
  { id: 'DV-7.10', name: 'Versioned', pattern: /versioned|version control|revision/i },
  { id: 'DV-7.11', name: 'Backed up', pattern: /backup|backed up|snapshot/i },
  { id: 'DV-7.12', name: 'Recovered', pattern: /recovered|recovery|restore/i },
  { id: 'DV-7.13', name: 'Integrity verified', pattern: /integrity|checksum|validate/i },
];

function validate() {
  const testFile = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(testFile)) { console.error('\n❌ DATA VALIDATION FAILED\n'); process.exit(1); }

  const content = fs.readFileSync(testFile, 'utf-8');
  let passed = 0;

  console.log('\n📋 DATA VALIDATION GUARDRAILS VALIDATION\n');
  DATA_TESTS.forEach((test) => {
    const met = test.pattern.test(content);
    console.log(`${met ? '✓' : '✗'} ${test.id}: ${test.name}`);
    if (met) passed++;
  });

  console.log(`\n${passed}/${DATA_TESTS.length} data validation tests documented\n`);
  process.exit(passed === DATA_TESTS.length ? 0 : 1);
}
validate();
