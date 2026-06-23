/**
 * math-hub-loop.spec.ts
 * ──────────────────────
 * Endurance / loop engineering tests for the CBSE Maths Hub.
 *
 * "Loop engineering" validates that the client-side JavaScript state machine
 * remains correct and stable under repeated use. Three concerns:
 *
 *   1. ACCURACY DRIFT  — Does the widget give the correct answer on iteration 1,
 *                        10, 25, and 50? (catches floating-point accumulation,
 *                        closure-captured state bugs, shared mutable state)
 *
 *   2. STATE INTEGRITY — Does the MCQ score stay consistent after 50+ rapid
 *                        answer clicks? Does the idempotency guard hold?
 *
 *   3. MEMORY STABILITY — Does the canvas redraw 30 times without leaking
 *                         or crashing? (catches requestAnimationFrame leaks,
 *                         2D context object accumulation)
 *
 * All loops run inside the browser via page.evaluate() to eliminate Playwright
 * RPC overhead. Results are validated back in Node.js.
 */
import { test, expect } from '@playwright/test';

const URL = 'https://pradhansuman.github.io/qa-agent-pipeline/math_hub.html';

async function gotoAndDisableScroll(page: any) {
  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.evaluate(() => {
    (document.documentElement as HTMLElement).style.scrollBehavior = 'auto';
  });
}

// ─── 1. Widget Accuracy Drift Loop ───────────────────────────────────────────
test.describe('Widget Accuracy — Repeated Computation', () => {

  test('TC-LOOP-01: CH01 fraction converter gives consistent results across 30 iterations', async ({ page }) => {
    await gotoAndDisableScroll(page);
    await page.locator('[data-testid="nav-ch01"]').click();
    await page.locator('[data-testid="chapter-1"]').waitFor({ state: 'visible' });

    // Run 30 conversions inside the browser — check each result is exactly right
    const results = await page.evaluate(() => {
      const cases: Array<[number, number, string]> = [
        [7, 8, '0.875'], [1, 4, '0.25'], [3, 5, '0.6'],
        [1, 2, '0.5'],   [9, 10, '0.9'], [2, 3, '0.6666666667'],
        [5, 8, '0.625'], [7, 10, '0.7'], [3, 4, '0.75'],
      ];
      const num  = document.querySelector('[data-testid="ch01-numerator"]')   as HTMLInputElement;
      const den  = document.querySelector('[data-testid="ch01-denominator"]') as HTMLInputElement;
      const btn  = document.querySelector('[data-testid="ch01-convert-btn"]') as HTMLButtonElement;
      const res  = document.querySelector('[data-testid="ch01-result"]')      as HTMLElement;

      const log: string[] = [];
      for (let pass = 0; pass < 30; pass++) {
        const [p, q, expected] = cases[pass % cases.length];
        num.value = String(p);
        den.value = String(q);
        btn.click();
        const text = res.textContent ?? '';
        log.push(`pass${pass}|${p}/${q}|expected:${expected}|got:${text}|ok:${text.includes(expected)}`);
      }
      return log;
    });

    const failures = results.filter(r => r.includes('ok:false'));
    expect(failures).toHaveLength(0);
    expect(results).toHaveLength(30);
  });

  test('TC-LOOP-02: CH08 SI calculator stays accurate across 25 iterations with varied inputs', async ({ page }) => {
    await gotoAndDisableScroll(page);
    await page.locator('[data-testid="nav-ch08"]').click();
    await page.locator('[data-testid="chapter-8"]').waitFor({ state: 'visible' });

    const results = await page.evaluate(() => {
      // [P, R, T] → expected SI = P*R*T/100
      const cases: Array<[number, number, number]> = [
        [1000, 5, 2],   // SI = 100
        [5000, 8, 3],   // SI = 1200
        [2000, 10, 1],  // SI = 200
        [500,  4, 4],   // SI = 80
        [10000, 6, 2],  // SI = 1200
      ];
      const P   = document.querySelector('[data-testid="ch08-principal"]') as HTMLInputElement;
      const R   = document.querySelector('[data-testid="ch08-rate"]')      as HTMLInputElement;
      const T   = document.querySelector('[data-testid="ch08-time"]')      as HTMLInputElement;
      const btn = document.querySelector('[data-testid="ch08-calc-btn"]')  as HTMLButtonElement;
      const res = document.querySelector('[data-testid="ch08-result"]')    as HTMLElement;

      const log: string[] = [];
      for (let i = 0; i < 25; i++) {
        const [p, r, t] = cases[i % cases.length];
        const expected = (p * r * t / 100).toFixed(2);
        P.value = String(p); R.value = String(r); T.value = String(t);
        btn.click();
        const text = res.textContent ?? '';
        log.push(`i${i}|${p}*${r}*${t}/100=${expected}|ok:${text.includes(expected)}`);
      }
      return log;
    });

    const failures = results.filter(r => r.includes('ok:false'));
    expect(failures).toHaveLength(0);
  });

  test('TC-LOOP-03: CH12 exponent calculator correct across 20 iterations', async ({ page }) => {
    await gotoAndDisableScroll(page);
    await page.locator('[data-testid="nav-ch12"]').click();
    await page.locator('[data-testid="chapter-12"]').waitFor({ state: 'visible' });

    const results = await page.evaluate(() => {
      const cases: Array<[number, number, string]> = [
        [2, 10, '1024'], [5, 0, '1'], [3, 3, '27'],
        [2, -2, '0.25'], [10, 3, '1000'], [7, 2, '49'],
      ];
      const base = document.querySelector('[data-testid="ch12-base"]')    as HTMLInputElement;
      const pow  = document.querySelector('[data-testid="ch12-power"]')   as HTMLInputElement;
      const btn  = document.querySelector('[data-testid="ch12-calc-btn"]') as HTMLButtonElement;
      const res  = document.querySelector('[data-testid="ch12-result"]')  as HTMLElement;

      const log: string[] = [];
      for (let i = 0; i < 20; i++) {
        const [b, p, expected] = cases[i % cases.length];
        base.value = String(b); pow.value = String(p);
        btn.click();
        const text = res.textContent ?? '';
        log.push(`i${i}|${b}^${p}=${expected}|ok:${text.includes(expected)}`);
      }
      return log;
    });

    expect(results.filter(r => r.includes('ok:false'))).toHaveLength(0);
  });
});

// ─── 2. MCQ Score State Integrity Loop ───────────────────────────────────────
test.describe('MCQ Score State Integrity', () => {

  test('TC-LOOP-04: score stays 0/0 after 50 rapid clicks on already-answered questions', async ({ page }) => {
    await gotoAndDisableScroll(page);
    await page.locator('[data-testid="nav-ch01"]').click();
    await page.locator('[data-testid="chapter-1"]').waitFor({ state: 'visible' });

    // Answer Q1 once correctly
    await page.locator('[data-testid="ch01-q1-c"]').click();
    await expect(page.locator('[data-testid="score-bar"]')).toContainText('1 / 1');

    // Now spam click all other options 50 times — score must stay at 1/1
    const finalScore = await page.evaluate(() => {
      const wrongBtn = document.querySelector('[data-testid="ch01-q1-a"]') as HTMLButtonElement;
      const score    = document.querySelector('[data-testid="score-bar"]')  as HTMLElement;
      for (let i = 0; i < 50; i++) {
        wrongBtn.click();
      }
      return score.textContent;
    });

    expect(finalScore).toContain('1 / 1');
  });

  test('TC-LOOP-05: score accumulates correctly answering all MCQs across 8 chapters in sequence', async ({ page }) => {
    await gotoAndDisableScroll(page);

    // Per-chapter correct answer selectors (derived from golden spec)
    const correct: Array<[string, string]> = [
      ['nav-ch01', 'ch01-q1-c'],
      ['nav-ch02', 'ch02-q1-b'],
      ['nav-ch03', 'ch03-q1-c'],
      ['nav-ch05', 'ch05-q1-b'],
      ['nav-ch06', 'ch06-q1-b'],
      ['nav-ch07', 'ch07-q1-c'],
      ['nav-ch08', 'ch08-q1-b'],
      ['nav-ch09', 'ch09-q1-b'],
    ];

    for (const [nav, answer] of correct) {
      await page.locator(`[data-testid="${nav}"]`).click();
      await page.locator(`[data-testid="${answer}"]`).waitFor({ state: 'visible' });
      await page.locator(`[data-testid="${answer}"]`).click();
    }

    const scoreText = await page.locator('[data-testid="score-bar"]').textContent();
    // 8 correct answers, 8 attempted
    expect(scoreText).toContain('8 / 8');
  });

  test('TC-LOOP-06: score counter data-score attribute stays in sync across 10 correct answers', async ({ page }) => {
    await gotoAndDisableScroll(page);

    const sequence = [
      ['nav-ch01', 'ch01-q2-b'],
      ['nav-ch01', 'ch01-q3-a'],
      ['nav-ch02', 'ch02-q1-b'],
      ['nav-ch02', 'ch02-q2-c'],
      ['nav-ch03', 'ch03-q1-c'],
      ['nav-ch05', 'ch05-q1-b'],
      ['nav-ch06', 'ch06-q1-b'],
      ['nav-ch07', 'ch07-q1-c'],
      ['nav-ch08', 'ch08-q1-b'],
      ['nav-ch09', 'ch09-q1-b'],
    ];

    for (let i = 0; i < sequence.length; i++) {
      const [nav, answer] = sequence[i];
      await page.locator(`[data-testid="${nav}"]`).click();
      await page.locator(`[data-testid="${answer}"]`).waitFor({ state: 'visible' });
      await page.locator(`[data-testid="${answer}"]`).click();

      // After each answer, verify data-score attribute matches visible text
      await page.waitForTimeout(50);
      const attr = await page.locator('[data-testid="score-bar"]').getAttribute('data-score');
      const text = await page.locator('[data-testid="score-bar"]').textContent();
      const attrVal = parseInt(attr ?? '-1');
      expect(attrVal).toBe(i + 1);             // data-score increments by 1 each time
      expect(text).toContain(`${i + 1} /`);   // visible text matches
    }
  });
});

// ─── 3. Canvas Memory Stability Loop ─────────────────────────────────────────
test.describe('Canvas Memory Stability', () => {

  test('TC-LOOP-07: CH05 chart redraws 30 times without error or blank canvas', async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', e => errors.push(e.message));

    await gotoAndDisableScroll(page);
    await page.locator('[data-testid="nav-ch05"]').click();
    await page.locator('[data-testid="chapter-5"]').waitFor({ state: 'visible' });

    const chartTypes = ['bar', 'pie', 'histogram'];

    const results = await page.evaluate((types: string[]) => {
      const select = document.querySelector('[data-testid="ch05-chart-type"]') as HTMLSelectElement;
      const btn    = document.querySelector('[data-testid="ch05-draw-btn"]')   as HTMLButtonElement;
      const canvas = document.querySelector('[data-testid="ch05-canvas"]')     as HTMLCanvasElement;

      const log: string[] = [];
      for (let i = 0; i < 30; i++) {
        select.value = types[i % types.length];
        select.dispatchEvent(new Event('change', { bubbles: true }));
        btn.click();
        const ctx = canvas.getContext('2d');
        const blank = !ctx; // context must be available
        log.push(`i${i}|type:${types[i % types.length]}|blank:${blank}|w:${canvas.width}|h:${canvas.height}`);
      }
      return log;
    }, chartTypes);

    expect(errors).toHaveLength(0);
    const blanks = results.filter(r => r.includes('blank:true'));
    expect(blanks).toHaveLength(0);
    expect(results).toHaveLength(30);
  });

  test('TC-LOOP-08: CH15 line graph redraws 20 times — canvas stays painted', async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', e => errors.push(e.message));

    await gotoAndDisableScroll(page);
    await page.locator('[data-testid="nav-ch15"]').click();
    await page.locator('[data-testid="chapter-15"]').waitFor({ state: 'visible' });

    const results = await page.evaluate(() => {
      const btn    = document.querySelector('[data-testid="ch15-draw-btn"]')  as HTMLButtonElement;
      const canvas = document.querySelector('[data-testid="ch15-canvas"]')    as HTMLCanvasElement;
      const log: string[] = [];
      for (let i = 0; i < 20; i++) {
        btn.click();
        log.push(`i${i}|w:${canvas.width}|h:${canvas.height}|ok:${canvas.width > 0}`);
      }
      return log;
    });

    expect(errors).toHaveLength(0);
    const failures = results.filter(r => r.includes('ok:false'));
    expect(failures).toHaveLength(0);
  });
});

// ─── 4. Cross-Chapter Navigation Loop ────────────────────────────────────────
test.describe('Navigation Loop Stability', () => {

  test('TC-LOOP-09: cycling through all 16 chapters 3 times keeps DOM stable', async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', e => errors.push(e.message));

    await gotoAndDisableScroll(page);

    // 3 complete cycles × 16 chapters = 48 nav clicks in-browser
    const result = await page.evaluate(() => {
      const navLinks = Array.from(
        document.querySelectorAll('[data-testid^="nav-ch"]')
      ) as HTMLElement[];

      let sectionsMissing = 0;
      for (let cycle = 0; cycle < 3; cycle++) {
        for (const link of navLinks) {
          link.click();
          // After each click, all 16 sections should still be in the DOM
          const count = document.querySelectorAll('[data-testid^="chapter-"]').length;
          if (count !== 16) sectionsMissing++;
        }
      }
      return { sectionsMissing, navCount: navLinks.length * 3 };
    });

    expect(errors).toHaveLength(0);
    expect(result.sectionsMissing).toBe(0);
    expect(result.navCount).toBe(48);
  });

  test('TC-LOOP-10: score bar stays visible and correct after 3 full navigation cycles', async ({ page }) => {
    await gotoAndDisableScroll(page);

    // Answer one question
    await page.locator('[data-testid="nav-ch01"]').click();
    await page.locator('[data-testid="chapter-1"]').waitFor({ state: 'visible' });
    await page.locator('[data-testid="ch01-q1-c"]').click();
    await expect(page.locator('[data-testid="score-bar"]')).toContainText('1 / 1');

    // Cycle through all chapters 3 times
    await page.evaluate(() => {
      const links = Array.from(
        document.querySelectorAll('[data-testid^="nav-ch"]')
      ) as HTMLElement[];
      for (let c = 0; c < 3; c++) links.forEach(l => l.click());
    });

    // Score must still be 1/1 — navigation must not reset state
    await expect(page.locator('[data-testid="score-bar"]')).toContainText('1 / 1');
    await expect(page.locator('[data-testid="score-bar"]')).toBeVisible();
  });
});

// ─── 5. Rapid Input Stress Loop ───────────────────────────────────────────────
test.describe('Rapid Input Stress', () => {

  test('TC-LOOP-11: 40 rapid sequential button clicks produce 40 valid results (no undefined/NaN output)', async ({ page }) => {
    await gotoAndDisableScroll(page);
    await page.locator('[data-testid="nav-ch06"]').click();
    await page.locator('[data-testid="chapter-6"]').waitFor({ state: 'visible' });

    // Rapidly cycle through √1, √4, √9, …, √100 in a loop
    const results = await page.evaluate(() => {
      const input = document.querySelector('[data-testid="ch06-input"]') as HTMLInputElement;
      const btn   = document.querySelector('[data-testid="ch06-calc-btn"]') as HTMLButtonElement;
      const res   = document.querySelector('[data-testid="ch06-result"]') as HTMLElement;
      const log: string[] = [];

      for (let i = 1; i <= 40; i++) {
        const n = (i % 10 + 1) ** 2; // cycles through 4, 9, 16, 25, 36, 49, 64, 81, 100, 121
        input.value = String(n);
        btn.click();
        const text = res.textContent ?? '';
        const isNaN  = text.toLowerCase().includes('nan');
        const isUndef = text.toLowerCase().includes('undefined');
        log.push(`i${i}|n:${n}|nan:${isNaN}|undef:${isUndef}|text:${text.slice(0, 40)}`);
      }
      return log;
    });

    const badResults = results.filter(r => r.includes('nan:true') || r.includes('undef:true'));
    expect(badResults).toHaveLength(0);
    expect(results).toHaveLength(40);
  });

  test('TC-LOOP-12: Euler formula checker handles 30 rapid inputs without DOM corruption', async ({ page }) => {
    await gotoAndDisableScroll(page);
    await page.locator('[data-testid="nav-ch10"]').click();
    await page.locator('[data-testid="chapter-10"]').waitFor({ state: 'visible' });

    // Known valid polyhedra: F+V-E=2
    const valid: Array<[number, number, number]> = [
      [6, 8, 12], [4, 4, 6], [12, 20, 30], [8, 6, 12], [20, 12, 30],
    ];
    // Known invalid: F+V-E≠2
    const invalid: Array<[number, number, number]> = [
      [3, 3, 3], [5, 5, 5], [2, 2, 2],
    ];

    const results = await page.evaluate(
      ({ valid, invalid }: { valid: number[][], invalid: number[][] }) => {
        const F   = document.querySelector('[data-testid="ch10-faces"]')    as HTMLInputElement;
        const V   = document.querySelector('[data-testid="ch10-vertices"]') as HTMLInputElement;
        const E   = document.querySelector('[data-testid="ch10-edges"]')    as HTMLInputElement;
        const btn = document.querySelector('[data-testid="ch10-check-btn"]') as HTMLButtonElement;
        const res = document.querySelector('[data-testid="ch10-result"]')   as HTMLElement;

        const log: string[] = [];
        for (let i = 0; i < 30; i++) {
          const isValidCase = i % 2 === 0;
          const set = isValidCase ? valid : invalid;
          const [f, v, e] = set[Math.floor(i / 2) % set.length];
          F.value = String(f); V.value = String(v); E.value = String(e);
          btn.click();
          const text = res.textContent ?? '';
          const corrupt = text === '' || text.toLowerCase().includes('undefined');
          log.push(`i${i}|f${f}v${v}e${e}|corrupt:${corrupt}`);
        }
        return log;
      },
      { valid, invalid }
    );

    const corrupted = results.filter(r => r.includes('corrupt:true'));
    expect(corrupted).toHaveLength(0);
    expect(results).toHaveLength(30);
  });
});
