#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const API_TESTS = [
  { id: 'API-10.1', name: 'Status code', pattern: /status code|http code|200|404|500/i },
  { id: 'API-10.2', name: 'Headers', pattern: /header|response header|content-type/i },
  { id: 'API-10.3', name: 'Body', pattern: /response body|body|payload/i },
  { id: 'API-10.4', name: 'Schema', pattern: /schema|json schema|contract/i },
  { id: 'API-10.5', name: 'Contract', pattern: /contract testing|contract|api contract/i },
  { id: 'API-10.6', name: 'Pagination', pattern: /pagination|page|limit|offset/i },
  { id: 'API-10.7', name: 'Sorting', pattern: /sorting|sort|order by/i },
  { id: 'API-10.8', name: 'Filtering', pattern: /filtering|filter|where|query param/i },
  { id: 'API-10.9', name: 'Authentication', pattern: /authentication|bearer|api key|token/i },
  { id: 'API-10.10', name: 'Authorization', pattern: /authorization|permission|access|role/i },
  { id: 'API-10.11', name: 'Rate limits', pattern: /rate limit|rate limiting|throttle/i },
  { id: 'API-10.12', name: 'Retries', pattern: /retry|retries|exponential backoff/i },
  { id: 'API-10.13', name: 'Timeouts', pattern: /timeout|timeout handling/i },
  { id: 'API-10.14', name: 'Error codes', pattern: /error code|error response|error/i },
  { id: 'API-10.15', name: 'Malformed payloads', pattern: /malformed|invalid json|bad request/i },
  { id: 'API-10.16', name: 'Large payloads', pattern: /large payload|big request|payload size/i },
  { id: 'API-10.17', name: 'Duplicate requests', pattern: /duplicate|idempotent|idempotency/i },
  { id: 'API-10.18', name: 'Idempotency', pattern: /idempotent|idempotency|safe/i },
  { id: 'API-10.19', name: 'Versioning', pattern: /version|api version|v1|v2/i },
  { id: 'API-10.20', name: 'Backward compatibility', pattern: /backward compatible|compatibility|breaking change/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ API TESTING VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 API TESTING GUARDRAILS VALIDATION\n');
  API_TESTS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${API_TESTS.length} api tests documented\n`);
  process.exit(p === API_TESTS.length ? 0 : 1);
}
validate();
