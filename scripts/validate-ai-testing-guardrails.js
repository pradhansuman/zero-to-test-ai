#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const AI_TESTS = [
  { id: 'AI-16.1', name: 'Hallucination', pattern: /hallucination|hallucinate|fabricate/i },
  { id: 'AI-16.2', name: 'Prompt injection', pattern: /prompt injection|injection|prompt abuse/i },
  { id: 'AI-16.3', name: 'Data leakage', pattern: /data leakage|pii leakage|leak/i },
  { id: 'AI-16.4', name: 'Toxicity', pattern: /toxicity|toxic|offensive/i },
  { id: 'AI-16.5', name: 'Bias', pattern: /bias|biased|discrimination/i },
  { id: 'AI-16.6', name: 'Fairness', pattern: /fairness|fair|equity/i },
  { id: 'AI-16.7', name: 'Prompt robustness', pattern: /prompt robustness|robust|adversarial/i },
  { id: 'AI-16.8', name: 'Temperature effects', pattern: /temperature|randomness|variation/i },
  { id: 'AI-16.9', name: 'Consistency', pattern: /consistency|consistent|reliable/i },
  { id: 'AI-16.10', name: 'Determinism', pattern: /determinism|deterministic/i },
  { id: 'AI-16.11', name: 'Latency', pattern: /latency|response time|inference time/i },
  { id: 'AI-16.12', name: 'Fallbacks', pattern: /fallback|fallback behavior|failure mode/i },
  { id: 'AI-16.13', name: 'Grounding', pattern: /grounding|ground|source/i },
  { id: 'AI-16.14', name: 'Citation accuracy', pattern: /citation|cite|reference/i },
  { id: 'AI-16.15', name: 'Model drift', pattern: /model drift|drift|degradation/i },
  { id: 'AI-16.16', name: 'Safety', pattern: /safety|safe|harm prevention/i },
  { id: 'AI-16.17', name: 'Prompt jailbreak', pattern: /jailbreak|bypass|circumvent/i },
  { id: 'AI-16.18', name: 'RAG accuracy', pattern: /rag|retrieval|augmented/i },
  { id: 'AI-16.19', name: 'Context limits', pattern: /context limit|context window|overflow/i },
  { id: 'AI-16.20', name: 'Token usage', pattern: /token|token limit|token usage/i },
  { id: 'AI-16.21', name: 'Memory behavior', pattern: /memory|state|context memory/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ AI TESTING VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 AI TESTING GUARDRAILS VALIDATION\n');
  AI_TESTS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${AI_TESTS.length} ai tests documented\n`);
  process.exit(p === AI_TESTS.length ? 0 : 1);
}
validate();
