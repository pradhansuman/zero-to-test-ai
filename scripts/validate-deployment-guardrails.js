#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const DEPLOY_ITEMS = [
  { id: 'DEPLOY-22.1', name: 'CI/CD pipeline', pattern: /ci\/cd|cicd|pipeline/i },
  { id: 'DEPLOY-22.2', name: 'Feature flags', pattern: /feature flag|flag|toggle/i },
  { id: 'DEPLOY-22.3', name: 'Rollback', pattern: /rollback|revert|roll back/i },
  { id: 'DEPLOY-22.4', name: 'Canary deployment', pattern: /canary|canary deploy/i },
  { id: 'DEPLOY-22.5', name: 'Blue-Green', pattern: /blue.?green|blue-green/i },
  { id: 'DEPLOY-22.6', name: 'Database migration', pattern: /database migration|migration|db migrate/i },
  { id: 'DEPLOY-22.7', name: 'Configuration', pattern: /config|configuration/i },
  { id: 'DEPLOY-22.8', name: 'Secrets management', pattern: /secret|credential/i },
  { id: 'DEPLOY-22.9', name: 'Certificates', pattern: /certificate|cert|ssl/i },
  { id: 'DEPLOY-22.10', name: 'Dependency validation', pattern: /depend|dependency/i },
  { id: 'DEPLOY-22.11', name: 'Fresh install', pattern: /fresh install|new install/i },
  { id: 'DEPLOY-22.12', name: 'Upgrade', pattern: /upgrade|upgrade/i },
  { id: 'DEPLOY-22.13', name: 'Downgrade', pattern: /downgrade|downgrade/i },
  { id: 'DEPLOY-22.14', name: 'Partial deployment', pattern: /partial deploy|canary/i },
  { id: 'DEPLOY-22.15', name: 'Configuration error', pattern: /config error|config.*fail/i },
  { id: 'DEPLOY-22.16', name: 'Migration failure', pattern: /migration fail|migrate.*fail/i },
  { id: 'DEPLOY-22.17', name: 'Certificate expiry', pattern: /cert.*expir|certificate.*expir/i },
  { id: 'DEPLOY-22.18', name: 'Rollback capability', pattern: /rollback|can.*rollback/i },
  { id: 'DEPLOY-22.19', name: 'Migration rollback', pattern: /migration.*rollback|rollback.*migration/i },
  { id: 'DEPLOY-22.20', name: 'Deployment pause', pattern: /pause deploy|deployment.*pause/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ DEPLOYMENT GUARDRAILS VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 DEPLOYMENT GUARDRAILS VALIDATION (REQ-22)\n');
  DEPLOY_ITEMS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${DEPLOY_ITEMS.length} deployment validations documented\n`);
  process.exit(p === DEPLOY_ITEMS.length ? 0 : 1);
}
validate();
