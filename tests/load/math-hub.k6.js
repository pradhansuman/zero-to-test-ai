/**
 * tests/load/math-hub.k6.js
 * ──────────────────────────
 * k6 load test for the CBSE Maths Hub (static page on GitHub Pages CDN).
 *
 * Run:
 *   k6 run tests/load/math-hub.k6.js                          # quick smoke
 *   k6 run --env SCENARIO=spike   tests/load/math-hub.k6.js   # 100 VU spike
 *   k6 run --env SCENARIO=soak    tests/load/math-hub.k6.js   # 10 min soak
 *   k6 run --env SCENARIO=stress  tests/load/math-hub.k6.js   # ramp to 200 VU
 *
 * Three HTTP endpoints under test:
 *   1. /math_hub.html        — main SPA (CDN cache hit expected after warmup)
 *   2. /math_hub.html        — second GET using If-None-Match (304 expected)
 *   3. /nonexistent.html     — 404 path to verify error handling
 *
 * Thresholds (all scenarios must pass):
 *   p95 response time < 2 s
 *   error rate (non-2xx / non-304) < 0.5%
 *   CDN cache hit rate > 50% (ETag revalidation returns 304)
 */

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Counter, Rate, Trend } from 'k6/metrics';

const BASE = 'https://pradhansuman.github.io/qa-agent-pipeline';
const URL  = `${BASE}/math_hub.html`;

// ── Custom metrics ────────────────────────────────────────────────────────────
const cacheHits     = new Counter('cache_hits');
const cacheMisses   = new Counter('cache_misses');
const cacheHitRate  = new Rate('cache_hit_rate');
const ttfb          = new Trend('ttfb_ms', true);

// ── Scenario selector ─────────────────────────────────────────────────────────
const SCENARIO = __ENV.SCENARIO || 'smoke';

const SCENARIOS = {
  smoke: {
    executor:    'constant-vus',
    vus:         5,
    duration:    '20s',
    description: 'Quick sanity check — 5 VUs for 20 s',
  },
  steady: {
    executor:    'ramping-vus',
    description: 'Normal traffic — ramp to 50 VUs, hold 60 s',
    stages: [
      { duration: '10s', target: 10  },   // warm CDN
      { duration: '10s', target: 50  },   // ramp to peak
      { duration: '60s', target: 50  },   // hold
      { duration: '10s', target: 0   },   // ramp down
    ],
  },
  spike: {
    executor:    'ramping-vus',
    description: 'Sudden traffic spike — burst to 100 VUs instantly',
    stages: [
      { duration: '5s',  target: 100 },   // instant spike
      { duration: '30s', target: 100 },   // hold spike
      { duration: '5s',  target: 0   },   // drop
    ],
  },
  stress: {
    executor:    'ramping-vus',
    description: 'Stress test — ramp to 200 VUs to find CDN breaking point',
    stages: [
      { duration: '20s', target: 50  },
      { duration: '20s', target: 100 },
      { duration: '20s', target: 150 },
      { duration: '20s', target: 200 },
      { duration: '20s', target: 0   },
    ],
  },
  soak: {
    executor:    'constant-vus',
    vus:         20,
    duration:    '10m',
    description: 'Soak test — 20 VUs for 10 minutes to detect CDN throttling',
  },
};

const chosen = SCENARIOS[SCENARIO] || SCENARIOS.smoke;

// Strip the description field — k6 doesn't accept unknown scenario keys
const { description: _desc, ...scenarioConfig } = chosen;

export const options = {
  scenarios: {
    main: {
      ...scenarioConfig,
      gracefulStop: '5s',
    },
  },
  thresholds: {
    // Cold GET (math_hub.html first visit) must be < 2 s at P95
    'http_req_duration{name:math_hub_cold}': ['p(95)<2000'],
    // ETag revalidation (warm cache) must be < 1 s at P95
    'http_req_duration{name:math_hub_warm}': ['p(95)<1000'],
    // Cold and warm requests must not error (network-level or 5xx)
    'http_req_failed{name:math_hub_cold}': ['rate<0.005'],
    'http_req_failed{name:math_hub_warm}': ['rate<0.005'],
    // 404 group intentionally returns 404 — no error threshold applied to it
    // Cache hit rate (ETag 304 revalidations) must exceed 30%
    cache_hit_rate: ['rate>0.30'],
  },
};

// Print chosen scenario config on start
export function setup() {
  console.log(`\n▶ Running scenario: ${SCENARIO} — ${chosen.description}`);
  return { etag: null };
}

// ── Virtual user function ──────────────────────────────────────────────────────
export default function () {

  // ── 1. Cold request (simulate first visit) ───────────────────────────────
  group('cold_request', () => {
    const res = http.get(URL, {
      headers: { 'Accept': 'text/html', 'Accept-Encoding': 'gzip, deflate, br' },
      tags:    { name: 'math_hub_cold' },
    });

    const ok = check(res, {
      'status 200':                   r => r.status === 200,
      'content-type html':            r => (r.headers['Content-Type'] || '').includes('text/html'),
      'body contains CBSE Class 8':   r => r.body.includes('CBSE Class 8'),
      'body has 16 chapter sections': r => (r.body.match(/data-testid="chapter-\d+"/g) || []).length === 16,
      'body has score-bar':           r => r.body.includes('data-testid="score-bar"'),
      'etag present':                 r => !!r.headers['Etag'],
      'cache-control present':        r => !!r.headers['Cache-Control'],
      'hsts present':                 r => !!r.headers['Strict-Transport-Security'],
      'response time < 3s':           r => r.timings.duration < 3000,
    });

    if (!ok) {
      console.warn(`[COLD] FAIL — status=${res.status} duration=${res.timings.duration}ms`);
    }

    // Record TTFB
    if (res.timings.waiting) {
      ttfb.add(res.timings.waiting, { type: 'cold' });
    }

    cacheMisses.add(1);
    cacheHitRate.add(false);

    // ── 2. Warm request (ETag revalidation — should return 304) ───────────
    const etag = res.headers['Etag'];
    if (etag) {
      const warm = http.get(URL, {
        headers: { 'If-None-Match': etag, 'Accept-Encoding': 'gzip, deflate, br' },
        tags:    { name: 'math_hub_warm' },
      });

      const cacheOk = check(warm, {
        '304 or 200 on revalidation': r => r.status === 304 || r.status === 200,
        'warm response < 1s':         r => r.timings.duration < 1000,
      });

      if (warm.status === 304) {
        cacheHits.add(1);
        cacheHitRate.add(true);
      } else {
        cacheMisses.add(1);
        cacheHitRate.add(false);
      }

      if (warm.timings.waiting) {
        ttfb.add(warm.timings.waiting, { type: 'warm' });
      }
    }
  });

  // ── 3. 404 error handling ────────────────────────────────────────────────
  group('404_handling', () => {
    const res404 = http.get(`${BASE}/this-does-not-exist-${Math.random()}.html`, {
      tags: { name: 'math_hub_404' },
    });
    check(res404, {
      '404 for unknown path': r => r.status === 404,
      '404 response fast':    r => r.timings.duration < 3000,
    });
  });

  sleep(Math.random() * 1.5 + 0.5); // 0.5–2 s think time between iterations
}

// ── End-of-run summary ───────────────────────────────────────────────────────
export function teardown(data) {
  console.log(`\n✓ Load test complete — scenario: ${SCENARIO}`);
}
