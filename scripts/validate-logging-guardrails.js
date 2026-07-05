#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const LOG_ITEMS = [
  { id: 'LOG-23.1', name: 'Application logs', pattern: /application log|app log/i },
  { id: 'LOG-23.2', name: 'Audit logs', pattern: /audit log|audit trail/i },
  { id: 'LOG-23.3', name: 'Security logs', pattern: /security log|security event/i },
  { id: 'LOG-23.4', name: 'Access logs', pattern: /access log|http log/i },
  { id: 'LOG-23.5', name: 'API logs', pattern: /api log|api call/i },
  { id: 'LOG-23.6', name: 'Database logs', pattern: /database log|db log|query log/i },
  { id: 'LOG-23.7', name: 'Infrastructure logs', pattern: /infrastructure log|system log/i },
  { id: 'LOG-23.8', name: 'Log level', pattern: /log level|debug|info|warning|error/i },
  { id: 'LOG-23.9', name: 'Correlation ID', pattern: /correlation id|corr.?id/i },
  { id: 'LOG-23.10', name: 'Request ID', pattern: /request id|req.?id/i },
  { id: 'LOG-23.11', name: 'Trace ID', pattern: /trace id|trace.?id/i },
  { id: 'LOG-23.12', name: 'Timestamp', pattern: /timestamp|timestamp/i },
  { id: 'LOG-23.13', name: 'Timezone', pattern: /timezone|utc|gmt/i },
  { id: 'LOG-23.14', name: 'Sensitive data masking', pattern: /mask|redact|pii|sensitive/i },
  { id: 'LOG-23.15', name: 'Stack trace', pattern: /stack trace|traceback/i },
  { id: 'LOG-23.16', name: 'Structured logs', pattern: /structured log|json log|structured/i },
  { id: 'LOG-23.17', name: 'Retention', pattern: /retention|keep|archive/i },
  { id: 'LOG-23.18', name: 'Rotation', pattern: /rotation|rotate|roll/i },
  { id: 'LOG-23.19', name: 'Log integrity', pattern: /integrity|tamper|sign/i },
  { id: 'LOG-23.20', name: 'Missing logs', pattern: /missing log|log missing/i },
  { id: 'LOG-23.21', name: 'Duplicate logs', pattern: /duplicate log|log duplicate/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ LOGGING GUARDRAILS VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 LOGGING GUARDRAILS VALIDATION (REQ-23)\n');
  LOG_ITEMS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${LOG_ITEMS.length} logging validations documented\n`);
  process.exit(p === LOG_ITEMS.length ? 0 : 1);
}
validate();
