#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const LLM_TESTS = [
  { id: 'LLM-17.1', name: 'Prompt validation', pattern: /prompt validation|validate prompt/i },
  { id: 'LLM-17.2', name: 'Prompt escaping', pattern: /prompt escaping|escape|sanitize/i },
  { id: 'LLM-17.3', name: 'Tool permissions', pattern: /tool permission|permission|access control/i },
  { id: 'LLM-17.4', name: 'Tool failures', pattern: /tool failure|tool failure handling|error/i },
  { id: 'LLM-17.5', name: 'Agent loops', pattern: /agent loop|infinite loop|loop detection/i },
  { id: 'LLM-17.6', name: 'Recursion', pattern: /recursion|recursive|depth limit/i },
  { id: 'LLM-17.7', name: 'Memory poisoning', pattern: /memory poison|memory attack|context poison/i },
  { id: 'LLM-17.8', name: 'Prompt leakage', pattern: /prompt leakage|system prompt leak|leak/i },
  { id: 'LLM-17.9', name: 'Output validation', pattern: /output validation|validate output|output check/i },
  { id: 'LLM-17.10', name: 'Schema validation', pattern: /schema validation|validate schema/i },
  { id: 'LLM-17.11', name: 'PII detection', pattern: /pii detection|detect pii|personally identifiable/i },
  { id: 'LLM-17.12', name: 'Sensitive information', pattern: /sensitive information|sensitive data|confidential/i },
  { id: 'LLM-17.13', name: 'Policy violations', pattern: /policy violation|policy compliance|usage policy/i },
  { id: 'LLM-17.14', name: 'Fact verification', pattern: /fact verification|verify fact|factual/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ LLM VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 LLM GUARDRAILS VALIDATION\n');
  LLM_TESTS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${LLM_TESTS.length} llm tests documented\n`);
  process.exit(p === LLM_TESTS.length ? 0 : 1);
}
validate();
