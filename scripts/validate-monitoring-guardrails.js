#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const MON_ITEMS = [
  { id: 'MON-24.1', name: 'Uptime monitoring', pattern: /uptime|availability|sla/i },
  { id: 'MON-24.2', name: 'Response time', pattern: /response time|latency|performance/i },
  { id: 'MON-24.3', name: 'Error rate', pattern: /error rate|error.*rate|failure rate/i },
  { id: 'MON-24.4', name: 'Resource utilization', pattern: /resource|cpu|memory|disk/i },
  { id: 'MON-24.5', name: 'Throughput', pattern: /throughput|requests.*sec|rps/i },
  { id: 'MON-24.6', name: 'Alerts', pattern: /alert|alerting|notification/i },
  { id: 'MON-24.7', name: 'Thresholds', pattern: /threshold|trigger|limit/i },
  { id: 'MON-24.8', name: 'Dashboards', pattern: /dashboard|visualization|graphs/i },
  { id: 'MON-24.9', name: 'Historical data', pattern: /historical|history|retention/i },
  { id: 'MON-24.10', name: 'Trending', pattern: /trend|trending|pattern/i },
  { id: 'MON-24.11', name: 'Anomaly detection', pattern: /anomaly|detect|deviation/i },
  { id: 'MON-24.12', name: 'Custom metrics', pattern: /custom metric|business metric/i },
  { id: 'MON-24.13', name: 'Real-time monitoring', pattern: /real.?time|realtime|live/i },
  { id: 'MON-24.14', name: 'Alert routing', pattern: /alert.*routing|on.?call|escalat/i },
  { id: 'MON-24.15', name: 'Incident correlation', pattern: /correlat|incident|incident.*correlation/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ MONITORING GUARDRAILS VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 MONITORING GUARDRAILS VALIDATION (REQ-24 - FINAL)\n');
  MON_ITEMS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${MON_ITEMS.length} monitoring validations documented\n`);
  process.exit(p === MON_ITEMS.length ? 0 : 1);
}
validate();
