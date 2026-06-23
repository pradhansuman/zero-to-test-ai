/**
 * ShopNow — k6 Load Test
 *
 * Requires store.html to be served via HTTP (not file://):
 *   npx serve . -l 3000   # or: python3 -m http.server 3000
 *
 * Run scenarios:
 *   k6 run tests/load/store.k6.js                             # smoke:  2 VUs / 20s
 *   k6 run --env SCENARIO=steady tests/load/store.k6.js       # steady: 20 VUs / 60s
 *   k6 run --env SCENARIO=spike  tests/load/store.k6.js       # spike:  burst to 50 VUs
 *   k6 run --env SCENARIO=stress tests/load/store.k6.js       # stress: ramp to 100 VUs
 *   k6 run --env BASE_URL=http://my-server tests/load/store.k6.js
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Rate, Trend } from 'k6/metrics';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';
const SCENARIO = __ENV.SCENARIO || 'smoke';

// Custom metrics
const pageLoads   = new Counter('store_page_loads');
const pageErrors  = new Rate('store_page_errors');
const ttfb        = new Trend('store_ttfb_ms', true);
const bodySize    = new Trend('store_body_bytes', true);

const SCENARIOS = {
  smoke: {
    executor: 'constant-vus',
    vus: 2,
    duration: '20s',
    description: '2 VUs — baseline health check',
  },
  steady: {
    executor: 'ramping-vus',
    startVUs: 0,
    stages: [
      { duration: '20s', target: 20 },
      { duration: '60s', target: 20 },
      { duration: '10s', target: 0 },
    ],
    description: '20 VUs — steady throughput',
  },
  spike: {
    executor: 'ramping-vus',
    startVUs: 0,
    stages: [
      { duration: '10s', target: 50 },
      { duration: '30s', target: 50 },
      { duration: '10s', target: 0 },
    ],
    description: 'Burst to 50 VUs',
  },
  stress: {
    executor: 'ramping-vus',
    startVUs: 0,
    stages: [
      { duration: '30s', target: 100 },
      { duration: '60s', target: 100 },
      { duration: '15s', target: 0 },
    ],
    description: 'Ramp to 100 VUs',
  },
};

const chosen = SCENARIOS[SCENARIO] || SCENARIOS.smoke;
// Strip non-k6 fields before spreading into options.scenarios
const { description: _desc, ...scenarioConfig } = chosen;

export const options = {
  scenarios: {
    store_load: {
      ...scenarioConfig,
      gracefulStop: '10s',
    },
  },
  thresholds: {
    // Tag-scoped: only count the main page load requests
    'http_req_duration{name:store_page}': ['p(95)<500', 'p(99)<1000'],
    'http_req_failed{name:store_page}':   ['rate<0.01'],
    store_page_errors:                     ['rate<0.01'],
    store_ttfb_ms:                         ['p(95)<200'],
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/store.html`, {
    tags: { name: 'store_page' },
  });

  const ok = check(res, {
    'status is 200':            r => r.status === 200,
    'body contains ShopNow':    r => r.body.includes('ShopNow'),
    'body contains PRODUCTS':   r => r.body.includes('PRODUCTS'),
    'body contains cart-btn':   r => r.body.includes('data-testid="cart-button"'),
    'self-contained (no CDN)':  r => !r.body.includes('cdn.') && !r.body.includes('unpkg.'),
    'response time < 500ms':    r => r.timings.duration < 500,
    'TTFB < 200ms':             r => r.timings.waiting < 200,
  });

  pageLoads.add(1);
  pageErrors.add(!ok);
  ttfb.add(res.timings.waiting);
  bodySize.add(res.body ? res.body.length : 0);

  sleep(1);
}

export function handleSummary(data) {
  const p95 = data.metrics['http_req_duration{name:store_page}']
    ? data.metrics['http_req_duration{name:store_page}'].values['p(95)']
    : 'N/A';

  console.log(`
=== ShopNow Load Test Summary (${SCENARIO}) ===
  Requests:         ${data.metrics.http_reqs?.values.count ?? 0}
  Errors:           ${(data.metrics.store_page_errors?.values.rate * 100 || 0).toFixed(2)}%
  p95 response:     ${typeof p95 === 'number' ? p95.toFixed(0) + 'ms' : p95}
  p95 TTFB:         ${(data.metrics.store_ttfb_ms?.values['p(95)'] || 0).toFixed(0)}ms
  Avg body size:    ${(data.metrics.store_body_bytes?.values.avg || 0).toFixed(0)} bytes
`);

  return {
    'stdout': '',
  };
}
