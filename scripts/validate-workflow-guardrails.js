#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const WF_ITEMS = [
  { id: 'WF-19.1', name: 'Discover workflows', pattern: /discover.*workflow|workflow discovery/i },
  { id: 'WF-19.2', name: 'Entry points', pattern: /entry point|start.*workflow/i },
  { id: 'WF-19.3', name: 'Exit points', pattern: /exit point|end.*workflow/i },
  { id: 'WF-19.4', name: 'Alternate paths', pattern: /alternate path|alternative flow/i },
  { id: 'WF-19.5', name: 'Exception paths', pattern: /exception.*path|error flow/i },
  { id: 'WF-19.6', name: 'Hidden transitions', pattern: /hidden transition|state transition/i },
  { id: 'WF-19.7', name: 'Business rules', pattern: /business rule|validation/i },
  { id: 'WF-19.8', name: 'Missing validations', pattern: /missing validation|gap/i },
  { id: 'WF-19.9', name: 'Invalid state transitions', pattern: /invalid state|state machine/i },
  { id: 'WF-19.10', name: 'Race conditions', pattern: /race condition|concurrent|parallel/i },
  { id: 'WF-19.11', name: 'Duplicate execution', pattern: /duplicate|idempotent/i },
  { id: 'WF-19.12', name: 'Rollback validation', pattern: /rollback|revert/i },
  { id: 'WF-19.13', name: 'Compensation logic', pattern: /compensation|compensate/i },
  { id: 'WF-19.14', name: 'Approvals', pattern: /approval|approve/i },
  { id: 'WF-19.15', name: 'Escalation paths', pattern: /escalation|escalate/i },
  { id: 'WF-19.16', name: 'SLA timers', pattern: /sla|timer|timeout/i },
  { id: 'WF-19.17', name: 'Workflow diagram', pattern: /workflow diagram|state diagram/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ WORKFLOW GUARDRAILS VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 WORKFLOW GUARDRAILS VALIDATION (REQ-19)\n');
  WF_ITEMS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${WF_ITEMS.length} workflow validations documented\n`);
  process.exit(p === WF_ITEMS.length ? 0 : 1);
}
validate();
