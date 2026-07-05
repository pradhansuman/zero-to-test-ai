#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const CLOUD_ITEMS = [
  { id: 'CLOUD-21.1', name: 'Cloud provider', pattern: /cloud provider|aws|azure|gcp/i },
  { id: 'CLOUD-21.2', name: 'Containers', pattern: /container|docker/i },
  { id: 'CLOUD-21.3', name: 'Kubernetes', pattern: /kubernetes|k8s/i },
  { id: 'CLOUD-21.4', name: 'Serverless', pattern: /serverless|lambda|function/i },
  { id: 'CLOUD-21.5', name: 'Autoscaling', pattern: /autoscal|scaling|scale/i },
  { id: 'CLOUD-21.6', name: 'IAM', pattern: /iam|identity|access|permission/i },
  { id: 'CLOUD-21.7', name: 'Secrets management', pattern: /secret|credential|api key/i },
  { id: 'CLOUD-21.8', name: 'Regions', pattern: /region|geographic/i },
  { id: 'CLOUD-21.9', name: 'Availability zones', pattern: /availability zone|az|zone/i },
  { id: 'CLOUD-21.10', name: 'Storage', pattern: /storage|database|persistent/i },
  { id: 'CLOUD-21.11', name: 'Networking', pattern: /network|vpc|subnet/i },
  { id: 'CLOUD-21.12', name: 'DNS', pattern: /dns|domain/i },
  { id: 'CLOUD-21.13', name: 'CDN', pattern: /cdn|content delivery/i },
  { id: 'CLOUD-21.14', name: 'Caching', pattern: /cache|caching/i },
  { id: 'CLOUD-21.15', name: 'Object storage', pattern: /object storage|s3|blob/i },
  { id: 'CLOUD-21.16', name: 'High availability', pattern: /high availability|ha|redundancy/i },
  { id: 'CLOUD-21.17', name: 'Disaster recovery', pattern: /disaster recovery|dr|backup/i },
  { id: 'CLOUD-21.18', name: 'Cost optimization', pattern: /cost|optimization|efficiency/i },
  { id: 'CLOUD-21.19', name: 'Cloud limits', pattern: /limit|quota|throttle/i },
  { id: 'CLOUD-21.20', name: 'IAM policies', pattern: /iam policy|rbac/i },
  { id: 'CLOUD-21.21', name: 'Encryption', pattern: /encrypt|tls|ssl/i },
  { id: 'CLOUD-21.22', name: 'Resource cleanup', pattern: /cleanup|cleanup|gc|garbage/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ CLOUD GUARDRAILS VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 CLOUD GUARDRAILS VALIDATION (REQ-21)\n');
  CLOUD_ITEMS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${CLOUD_ITEMS.length} cloud validations documented\n`);
  process.exit(p === CLOUD_ITEMS.length ? 0 : 1);
}
validate();
