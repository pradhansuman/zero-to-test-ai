#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const SECURITY_TESTS = [
  { id: 'SEC-8.1', name: 'Authentication', pattern: /authentication|auth|login/i },
  { id: 'SEC-8.2', name: 'Authorization', pattern: /authorization|access control|permission/i },
  { id: 'SEC-8.3', name: 'Broken access', pattern: /broken access|iac/i },
  { id: 'SEC-8.4', name: 'Privilege escalation', pattern: /privilege escalation|privilege/i },
  { id: 'SEC-8.5', name: 'JWT validation', pattern: /jwt|token validation|bearer/i },
  { id: 'SEC-8.6', name: 'Session timeout', pattern: /session timeout|session|idle/i },
  { id: 'SEC-8.7', name: 'CSRF', pattern: /csrf|cross-site request|token/i },
  { id: 'SEC-8.8', name: 'XSS', pattern: /xss|cross-site scripting|script injection/i },
  { id: 'SEC-8.9', name: 'SQL Injection', pattern: /sql injection|sql/i },
  { id: 'SEC-8.10', name: 'Command Injection', pattern: /command injection|os command/i },
  { id: 'SEC-8.11', name: 'SSRF', pattern: /ssrf|server-side request/i },
  { id: 'SEC-8.12', name: 'XXE', pattern: /xxe|xml external entity/i },
  { id: 'SEC-8.13', name: 'Open Redirect', pattern: /open redirect|redirect/i },
  { id: 'SEC-8.14', name: 'Path Traversal', pattern: /path traversal|directory traversal/i },
  { id: 'SEC-8.15', name: 'IDOR', pattern: /idor|insecure direct object/i },
  { id: 'SEC-8.16', name: 'Rate limiting', pattern: /rate limiting|rate limit/i },
  { id: 'SEC-8.17', name: 'Password policy', pattern: /password policy|password strength/i },
  { id: 'SEC-8.18', name: 'Account lockout', pattern: /account lockout|brute force protection/i },
  { id: 'SEC-8.19', name: 'Brute force', pattern: /brute force|brute-force attack/i },
  { id: 'SEC-8.20', name: 'Sensitive logs', pattern: /sensitive log|log leak|pii in logs/i },
  { id: 'SEC-8.21', name: 'Secrets exposure', pattern: /secrets exposure|api key|secret key/i },
  { id: 'SEC-8.22', name: 'Token leakage', pattern: /token leakage|token exposure/i },
  { id: 'SEC-8.23', name: 'Cookie security', pattern: /cookie security|secure flag|httponly/i },
  { id: 'SEC-8.24', name: 'CORS', pattern: /cors|cross-origin|origin/i },
  { id: 'SEC-8.25', name: 'Headers', pattern: /security header|csp|x-frame/i },
  { id: 'SEC-8.26', name: 'Encryption', pattern: /encryption|encrypted|tls/i },
  { id: 'SEC-8.27', name: 'TLS', pattern: /tls|ssl|https/i },
  { id: 'SEC-8.28', name: 'Certificate validation', pattern: /certificate|cert validation|pinning/i },
  { id: 'SEC-8.29', name: 'File upload security', pattern: /file upload|upload security|virus scan/i },
  { id: 'SEC-8.30', name: 'API abuse', pattern: /api abuse|api attack|request/i },
];

function validate() {
  const testFile = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(testFile)) { console.error('\n❌ SECURITY VALIDATION FAILED\n'); process.exit(1); }

  const content = fs.readFileSync(testFile, 'utf-8');
  let passed = 0;

  console.log('\n📋 SECURITY GUARDRAILS VALIDATION\n');
  SECURITY_TESTS.forEach((test) => {
    const met = test.pattern.test(content);
    console.log(`${met ? '✓' : '✗'} ${test.id}: ${test.name}`);
    if (met) passed++;
  });

  console.log(`\n${passed}/${SECURITY_TESTS.length} security tests documented\n`);
  process.exit(passed === SECURITY_TESTS.length ? 0 : 1);
}
validate();
