#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const OBS_ITEMS = [
  { id: 'OBS-28.1', name: 'Logs', pattern: /log|logging/i },
  { id: 'OBS-28.2', name: 'Metrics', pattern: /metric|metric.*collection/i },
  { id: 'OBS-28.3', name: 'Distributed traces', pattern: /distributed trace|trace|tracing/i },
  { id: 'OBS-28.4', name: 'Events', pattern: /event|event.*stream/i },
  { id: 'OBS-28.5', name: 'Business metrics', pattern: /business metric|kpi/i },
  { id: 'OBS-28.6', name: 'Infrastructure metrics', pattern: /infrastructure|system.*metric/i },
  { id: 'OBS-28.7', name: 'User journey', pattern: /user journey|user path|flow/i },
  { id: 'OBS-28.8', name: 'Dependency graph', pattern: /depend.*graph|service map|topology/i },
  { id: 'OBS-28.9', name: 'Correlation', pattern: /correlat|correlation.*id/i },
  { id: 'OBS-28.10', name: 'End-to-end tracing', pattern: /end.?to.?end|e2e.*trace/i },
  { id: 'OBS-28.11', name: 'Failure diagnosis', pattern: /diagnos|diagnose|root cause/i },
  { id: 'OBS-28.12', name: 'Bottleneck detection', pattern: /bottleneck|performance.*issue/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ OBSERVABILITY GUARDRAILS VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 OBSERVABILITY GUARDRAILS VALIDATION (REQ-28)\n');
  OBS_ITEMS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${OBS_ITEMS.length} observability validations documented\n`);
  process.exit(p === OBS_ITEMS.length ? 0 : 1);
}
validate();
