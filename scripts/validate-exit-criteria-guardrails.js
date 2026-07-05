#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const EXIT_ITEMS = [
  { id: 'EXIT-29.1', name: 'Requirement coverage', pattern: /requirement.*coverage|coverage.*req/i },
  { id: 'EXIT-29.2', name: 'Risk coverage', pattern: /risk.*coverage|coverage.*risk/i },
  { id: 'EXIT-29.3', name: 'Functional coverage', pattern: /functional.*coverage|feature.*coverage/i },
  { id: 'EXIT-29.4', name: 'Security coverage', pattern: /security.*coverage|sec.*coverage/i },
  { id: 'EXIT-29.5', name: 'Performance coverage', pattern: /performance.*coverage|perf.*coverage/i },
  { id: 'EXIT-29.6', name: 'Accessibility coverage', pattern: /accessibility.*coverage|a11y.*coverage/i },
  { id: 'EXIT-29.7', name: 'Compliance coverage', pattern: /compliance.*coverage|comp.*coverage/i },
  { id: 'EXIT-29.8', name: 'Automation coverage', pattern: /automation.*coverage|auto.*coverage/i },
  { id: 'EXIT-29.9', name: 'Defect status', pattern: /defect status|bug status|issue status/i },
  { id: 'EXIT-29.10', name: 'Regression testing', pattern: /regression|regression test/i },
  { id: 'EXIT-29.11', name: 'Smoke testing', pattern: /smoke|smoke test/i },
  { id: 'EXIT-29.12', name: 'UAT', pattern: /uat|user.*acceptance/i },
  { id: 'EXIT-29.13', name: 'Deployment validation', pattern: /deploy.*valid|validation.*deploy/i },
  { id: 'EXIT-29.14', name: 'Rollback validation', pattern: /rollback.*valid|validation.*rollback/i },
  { id: 'EXIT-29.15', name: 'Monitoring', pattern: /monitoring|monitor|alert/i },
  { id: 'EXIT-29.16', name: 'Logging', pattern: /logging|log|audit trail/i },
  { id: 'EXIT-29.17', name: 'Backup', pattern: /backup|backup.*plan/i },
  { id: 'EXIT-29.18', name: 'Recovery', pattern: /recovery|recover|restore/i },
  { id: 'EXIT-29.19', name: 'Stakeholder approval', pattern: /stakeholder|approval|approve/i },
  { id: 'EXIT-29.20', name: 'Documentation', pattern: /documentation|document|doc/i },
  { id: 'EXIT-29.21', name: 'Release notes', pattern: /release notes|release.*note/i },
  { id: 'EXIT-29.22', name: 'Known issues', pattern: /known.*issue|known.*bug/i },
  { id: 'EXIT-29.23', name: 'Release decision', pattern: /release decision|go.?no.?go|go decision/i },
  { id: 'EXIT-29.24', name: 'Evidence', pattern: /evidence|evidence.*support/i },
  { id: 'EXIT-29.25', name: 'Risk assessment', pattern: /risk.*assessment|risk.*analysis/i },
  { id: 'EXIT-29.26', name: 'Coverage summary', pattern: /coverage.*summary|summary.*coverage/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ EXIT CRITERIA GUARDRAILS VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 EXIT CRITERIA GUARDRAILS VALIDATION (REQ-29 - FINAL)\n');
  EXIT_ITEMS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${EXIT_ITEMS.length} exit criteria validations documented\n`);
  process.exit(p === EXIT_ITEMS.length ? 0 : 1);
}
validate();
