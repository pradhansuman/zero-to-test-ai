#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const CHAOS_ITEMS = [
  { id: 'CHAOS-26.1', name: 'Service failure', pattern: /kill service|service fail|service down/i },
  { id: 'CHAOS-26.2', name: 'Pod termination', pattern: /kill pod|pod.*fail|pod.*crash/i },
  { id: 'CHAOS-26.3', name: 'Database restart', pattern: /restart.*db|database.*fail/i },
  { id: 'CHAOS-26.4', name: 'Network slowdown', pattern: /slow network|latency|network delay/i },
  { id: 'CHAOS-26.5', name: 'Packet loss', pattern: /packet loss|packet.*drop/i },
  { id: 'CHAOS-26.6', name: 'DNS failure', pattern: /dns fail|dns.*error/i },
  { id: 'CHAOS-26.7', name: 'Disk full', pattern: /disk full|storage full|disk space/i },
  { id: 'CHAOS-26.8', name: 'Memory leak', pattern: /memory leak|memory.*issue/i },
  { id: 'CHAOS-26.9', name: 'CPU spike', pattern: /cpu spike|cpu load|cpu.*high/i },
  { id: 'CHAOS-26.10', name: 'Clock drift', pattern: /clock drift|time.*skew/i },
  { id: 'CHAOS-26.11', name: 'Region failure', pattern: /region fail|region.*down/i },
  { id: 'CHAOS-26.12', name: 'Cache failure', pattern: /cache fail|cache.*down/i },
  { id: 'CHAOS-26.13', name: 'Queue failure', pattern: /queue fail|queue.*down|broker fail/i },
  { id: 'CHAOS-26.14', name: 'Recovery', pattern: /recovery|recover|automatic recovery/i },
  { id: 'CHAOS-26.15', name: 'Retries', pattern: /retry|automatic.*retry/i },
  { id: 'CHAOS-26.16', name: 'Fallback', pattern: /fallback|graceful.*degrad/i },
  { id: 'CHAOS-26.17', name: 'Data integrity', pattern: /data integrity|data corrupt|data loss/i },
  { id: 'CHAOS-26.18', name: 'Availability', pattern: /availability|uptime|sla/i },
  { id: 'CHAOS-26.19', name: 'Monitoring', pattern: /monitor|alert|observ/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ CHAOS ENGINEERING GUARDRAILS VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 CHAOS ENGINEERING GUARDRAILS VALIDATION (REQ-26)\n');
  CHAOS_ITEMS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${CHAOS_ITEMS.length} chaos validations documented\n`);
  process.exit(p === CHAOS_ITEMS.length ? 0 : 1);
}
validate();
