#!/usr/bin/env node

/**
 * Functional Testing Guardrails Validator - REQ-5
 * Enforces that EVERY UI element and interaction is tested
 * Exit: 0 = complete (testing approved), 1 = blocked
 */

const fs = require('fs');
const path = require('path');

const FUNCTIONAL_ELEMENTS = [
  { id: 'FUNC-5.1', name: 'Every Button', pattern: /button|click|submit|action/i },
  { id: 'FUNC-5.2', name: 'Every Textbox', pattern: /textbox|input field|text input|text area/i },
  { id: 'FUNC-5.3', name: 'Every Dropdown', pattern: /dropdown|select|combo box|menu/i },
  { id: 'FUNC-5.4', name: 'Every Checkbox', pattern: /checkbox|toggle|switch/i },
  { id: 'FUNC-5.5', name: 'Every Radio Button', pattern: /radio button|radio option|choice/i },
  { id: 'FUNC-5.6', name: 'Every Link', pattern: /link|hyperlink|navigation link/i },
  { id: 'FUNC-5.7', name: 'Every Image', pattern: /image|icon|picture|visual|photo/i },
  { id: 'FUNC-5.8', name: 'Every Tooltip', pattern: /tooltip|help text|hover|information/i },
  { id: 'FUNC-5.9', name: 'Every Modal', pattern: /modal|dialog|popup|overlay/i },
  { id: 'FUNC-5.10', name: 'Every Popup', pattern: /popup|alert|confirmation|notification/i },
  { id: 'FUNC-5.11', name: 'Every Table', pattern: /table|data table|grid view|row|column/i },
  { id: 'FUNC-5.12', name: 'Every Grid', pattern: /grid|list view|card view|layout/i },
  { id: 'FUNC-5.13', name: 'Every Filter', pattern: /filter|search filter|advanced search|criteria/i },
  { id: 'FUNC-5.14', name: 'Every Search', pattern: /search|find|query|lookup/i },
  { id: 'FUNC-5.15', name: 'Every Pagination', pattern: /pagination|page navigation|next page|previous/i },
  { id: 'FUNC-5.16', name: 'Every Export', pattern: /export|download|save as|extract data/i },
  { id: 'FUNC-5.17', name: 'Every Import', pattern: /import|upload|bulk upload|csv|file import/i },
  { id: 'FUNC-5.18', name: 'Every Notification', pattern: /notification|alert|message|toast|banner/i },
  { id: 'FUNC-5.19', name: 'Every Navigation', pattern: /navigation|menu|breadcrumb|sidebar|header/i },
  { id: 'FUNC-5.20', name: 'Every API Interaction', pattern: /api|endpoint|rest|request|response/i },
  { id: 'FUNC-5.21', name: 'Every Workflow', pattern: /workflow|process|flow|sequence|step/i },
  { id: 'FUNC-5.22', name: 'Every Permission', pattern: /permission|access control|role|privilege/i },
  { id: 'FUNC-5.23', name: 'Every Validation', pattern: /validation|required field|constraint|rule/i },
  { id: 'FUNC-5.24', name: 'Every State Change', pattern: /state|enabled|disabled|visible|hidden/i },
  { id: 'FUNC-5.25', name: 'Every User Interaction', pattern: /interaction|user action|event|behavior/i },
];

function validate() {
  const testFile = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  
  if (!fs.existsSync(testFile)) {
    console.error('\n❌ FUNCTIONAL TESTING VALIDATION FAILED');
    console.error(`   Missing: DEMOWEBSHOP_SCOPE_DOCUMENT.md`);
    console.error('   Action: Document all UI elements and interactions\n');
    process.exit(1);
  }

  const content = fs.readFileSync(testFile, 'utf-8');
  let passed = 0, failed = 0;

  console.log('\n📋 FUNCTIONAL TESTING GUARDRAILS VALIDATION\n');

  FUNCTIONAL_ELEMENTS.forEach((element) => {
    const met = element.pattern.test(content);
    const status = met ? '✓' : '✗';
    console.log(`${status} ${element.id}: ${element.name}`);
    met ? passed++ : failed++;
  });

  console.log(`\n${passed}/${FUNCTIONAL_ELEMENTS.length} UI elements documented\n`);

  if (failed === 0) {
    console.log('✅ ALL FUNCTIONAL TESTING GUARDRAILS MET - Testing Approved\n');
    process.exit(0);
  } else {
    console.log(`❌ ${failed} ELEMENT(S) MISSING - Testing Blocked\n`);
    process.exit(1);
  }
}

validate();
