#!/usr/bin/env node
const fs = require('fs'), path = require('path');
const PERF_TESTS = [
  { id: 'PERF-9.1', name: 'Response time', pattern: /response time|latency target|p50|p95|p99/i },
  { id: 'PERF-9.2', name: 'Latency', pattern: /latency|ms|millisecond|response/i },
  { id: 'PERF-9.3', name: 'Throughput', pattern: /throughput|requests per second|tps|rps/i },
  { id: 'PERF-9.4', name: 'CPU', pattern: /cpu usage|cpu|processor|cpu percent/i },
  { id: 'PERF-9.5', name: 'Memory', pattern: /memory usage|memory|ram|heap|oom/i },
  { id: 'PERF-9.6', name: 'Disk', pattern: /disk usage|disk|storage|io/i },
  { id: 'PERF-9.7', name: 'Network', pattern: /network|bandwidth|throughput|latency/i },
  { id: 'PERF-9.8', name: 'Database', pattern: /database performance|query time|db/i },
  { id: 'PERF-9.9', name: 'Thread usage', pattern: /thread|thread pool|worker/i },
  { id: 'PERF-9.10', name: 'Connection pool', pattern: /connection pool|pool size|connection/i },
  { id: 'PERF-9.11', name: 'Caching', pattern: /cache|caching|cache hit|ttl/i },
  { id: 'PERF-9.12', name: 'Queue depth', pattern: /queue|queue depth|backlog/i },
  { id: 'PERF-9.13', name: 'GC pauses', pattern: /garbage collection|gc|gc pause|jvm/i },
  { id: 'PERF-9.14', name: 'Scaling', pattern: /scaling|scalability|horizontal|vertical/i },
  { id: 'PERF-9.15', name: 'Load test', pattern: /load test|load testing|load/i },
  { id: 'PERF-9.16', name: 'Stress test', pattern: /stress test|stress testing|breaking point/i },
  { id: 'PERF-9.17', name: 'Spike test', pattern: /spike test|sudden spike|traffic spike/i },
  { id: 'PERF-9.18', name: 'Endurance test', pattern: /endurance test|soak test|sustained/i },
  { id: 'PERF-9.19', name: 'Volume test', pattern: /volume test|data volume|large dataset/i },
  { id: 'PERF-9.20', name: 'Failover', pattern: /failover|failover time|rto/i },
  { id: 'PERF-9.21', name: 'Recovery', pattern: /recovery|recovery time|rpo|restore/i },
  { id: 'PERF-9.22', name: 'Performance baseline', pattern: /baseline|performance baseline|benchmark/i },
];
function validate() {
  const f = path.join(__dirname, '..', 'DEMOWEBSHOP_SCOPE_DOCUMENT.md');
  if (!fs.existsSync(f)) { console.error('\n❌ PERFORMANCE VALIDATION FAILED\n'); process.exit(1); }
  const c = fs.readFileSync(f, 'utf-8');
  let p = 0;
  console.log('\n📋 PERFORMANCE GUARDRAILS VALIDATION\n');
  PERF_TESTS.forEach((t) => {
    const m = t.pattern.test(c);
    console.log(`${m ? '✓' : '✗'} ${t.id}: ${t.name}`);
    if (m) p++;
  });
  console.log(`\n${p}/${PERF_TESTS.length} performance tests documented\n`);
  process.exit(p === PERF_TESTS.length ? 0 : 1);
}
validate();
