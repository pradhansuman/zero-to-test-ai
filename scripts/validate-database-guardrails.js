#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const DB_TESTS = [
  { id: 'DB-11.1', name: 'CRUD', pattern: /crud|create|read|update|delete/i },
  { id: 'DB-11.2', name: 'Indexes', pattern: /index|indexes|indexing|performance/i },
  { id: 'DB-11.3', name: 'Constraints', pattern: /constraint|constraints|pk|fk/i },
  { id: 'DB-11.4', name: 'Foreign keys', pattern: /foreign key|fk|referential integrity/i },
  { id: 'DB-11.5', name: 'Transactions', pattern: /transaction|acid|consistency/i },
  { id: 'DB-11.6', name: 'Rollback', pattern: /rollback|rollback|transaction abort/i },
  { id: 'DB-11.7', name: 'Deadlocks', pattern: /deadlock|deadlock detection|circular wait/i },
  { id: 'DB-11.8', name: 'Replication', pattern: /replication|replica|slave|streaming/i },
  { id: 'DB-11.9', name: 'Backup', pattern: /backup|backup strategy|backup frequency/i },
  { id: 'DB-11.10', name: 'Restore', pattern: /restore|recovery|restore procedure/i },
  { id: 'DB-11.11', name: 'Migration', pattern: /migration|data migration|schema migration/i },
  { id: 'DB-11.12', name: 'Data consistency', pattern: /consistency|consistent|data consistency/i },
  { id: 'DB-11.13', name: 'Data corruption', pattern: /corruption|corrupt|data integrity/i },
  { id: 'DB-11.14', name: 'Performance', pattern: /performance|query performance|slow query/i },
  { id: 'DB-11.15', name: 'Concurrency', pattern: /concurrency|concurrent|locking|lock/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ DATABASE VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 DATABASE GUARDRAILS VALIDATION\n');
  DB_TESTS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${DB_TESTS.length} database tests documented\n`);
  process.exit(p === DB_TESTS.length ? 0 : 1);
}
validate();
