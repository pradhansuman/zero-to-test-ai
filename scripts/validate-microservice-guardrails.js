#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const MS_ITEMS = [
  { id: 'MS-20.1', name: 'Service discovery', pattern: /service discovery|identify.*service/i },
  { id: 'MS-20.2', name: 'Dependencies mapping', pattern: /depend|dependency graph/i },
  { id: 'MS-20.3', name: 'Communication patterns', pattern: /communication|protocol/i },
  { id: 'MS-20.4', name: 'Sync vs async', pattern: /sync|async|asynchronous/i },
  { id: 'MS-20.5', name: 'Message queues', pattern: /queue|messaging/i },
  { id: 'MS-20.6', name: 'Kafka integration', pattern: /kafka/i },
  { id: 'MS-20.7', name: 'RabbitMQ integration', pattern: /rabbitmq|amqp/i },
  { id: 'MS-20.8', name: 'REST endpoints', pattern: /rest|http|endpoint/i },
  { id: 'MS-20.9', name: 'GraphQL integration', pattern: /graphql/i },
  { id: 'MS-20.10', name: 'gRPC integration', pattern: /grpc|protobuf/i },
  { id: 'MS-20.11', name: 'Service mesh', pattern: /service mesh|istio/i },
  { id: 'MS-20.12', name: 'API gateway', pattern: /api gateway|gateway/i },
  { id: 'MS-20.13', name: 'Circuit breaker', pattern: /circuit breaker/i },
  { id: 'MS-20.14', name: 'Retry logic', pattern: /retry|retries/i },
  { id: 'MS-20.15', name: 'Timeout handling', pattern: /timeout/i },
  { id: 'MS-20.16', name: 'Fallback strategy', pattern: /fallback|fallback/i },
  { id: 'MS-20.17', name: 'Bulkhead pattern', pattern: /bulkhead|isolation/i },
  { id: 'MS-20.18', name: 'Load balancing', pattern: /load balanc|load-balanc/i },
  { id: 'MS-20.19', name: 'Version compatibility', pattern: /version|compatibility/i },
  { id: 'MS-20.20', name: 'Health checks', pattern: /health check|liveness|readiness/i },
  { id: 'MS-20.21', name: 'Distributed transactions', pattern: /distributed transaction|saga/i },
  { id: 'MS-20.22', name: 'Eventual consistency', pattern: /eventual consistency/i },
  { id: 'MS-20.23', name: 'Dead letter queue', pattern: /dead letter|dlq/i },
  { id: 'MS-20.24', name: 'Idempotency', pattern: /idempotent|idempotency/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ MICROSERVICE GUARDRAILS VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 MICROSERVICE GUARDRAILS VALIDATION (REQ-20)\n');
  MS_ITEMS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${MS_ITEMS.length} microservice validations documented\n`);
  process.exit(p === MS_ITEMS.length ? 0 : 1);
}
validate();
