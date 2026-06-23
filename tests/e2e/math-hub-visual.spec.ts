/**
 * math-hub-visual.spec.ts
 * ────────────────────────
 * Visual regression tests for the CBSE Maths Hub using Playwright's built-in
 * screenshot comparison (toHaveScreenshot). Each test captures a snapshot of
 * a critical UI region and diffs it against a stored baseline PNG.
 *
 * Baseline generation (run once, commit the PNGs):
 *   npx playwright test --config playwright.math-hub.config.ts \
 *     tests/e2e/math-hub-visual.spec.ts --update-snapshots
 *
 * Subsequent CI runs:
 *   npx playwright test --config playwright.math-hub.config.ts \
 *     tests/e2e/math-hub-visual.spec.ts
 *
 * Tolerance: maxDiffPixelRatio 0.02 (2%) — absorbs sub-pixel font rendering
 * differences across OS versions without hiding real layout regressions.
 *
 * What these tests catch (that functional tests miss):
 *   - CSS regressions (color changes, spacing shifts, font changes)
 *   - Canvas chart visual changes (bar chart shape, color palette)
 *   - Score bar layout drift after state change
 *   - Mobile viewport layout regressions on Pixel 7
 */
import { test, expect } from '@playwright/test';

const URL = 'https://pradhansuman.github.io/qa-agent-pipeline/math_hub.html';
const SNAP_OPTS = { maxDiffPixelRatio: 0.02 } as const;

async function gotoAndSettle(page: any) {
  await page.goto(URL, { waitUntil: 'networkidle' });
  // Disable smooth scroll so animations don't bleed into screenshots
  await page.evaluate(() => {
    (document.documentElement as HTMLElement).style.scrollBehavior = 'auto';
    // Also disable any CSS transitions for visual stability
    const style = document.createElement('style');
    style.id = '__vr_disable_transitions';
    style.textContent = '*, *::before, *::after { transition: none !important; animation: none !important; }';
    document.head.appendChild(style);
  });
}

// ─── Page-level snapshots ──────────────────────────────────────────────────
test.describe('Page Layout', () => {

  test('VR-01: full page layout on load', async ({ page }) => {
    await gotoAndSettle(page);
    await expect(page).toHaveScreenshot('full-page-load.png', {
      ...SNAP_OPTS,
      fullPage: true,
      animations: 'disabled', // prevent font-loading animation from causing timeout
    });
  });

  test('VR-02: navigation bar renders correctly', async ({ page }) => {
    await gotoAndSettle(page);
    await expect(page.locator('[data-testid="nav-bar"]')).toHaveScreenshot(
      'nav-bar.png', SNAP_OPTS
    );
  });

  test('VR-03: score bar initial state (0/0)', async ({ page }) => {
    await gotoAndSettle(page);
    await expect(page.locator('[data-testid="score-bar"]')).toHaveScreenshot(
      'score-bar-initial.png', SNAP_OPTS
    );
  });

  test('VR-04: score bar after correct MCQ answer', async ({ page }) => {
    await gotoAndSettle(page);
    await page.locator('[data-testid="nav-ch01"]').click();
    await page.locator('[data-testid="chapter-1"]').waitFor({ state: 'visible' });
    await page.locator('[data-testid="ch01-q1-c"]').click();
    // Wait for score animation to settle
    await page.waitForTimeout(200);
    await expect(page.locator('[data-testid="score-bar"]')).toHaveScreenshot(
      'score-bar-after-correct.png', SNAP_OPTS
    );
  });
});

// ─── Chapter section snapshots ─────────────────────────────────────────────
test.describe('Chapter Sections', () => {

  test('VR-05: CH01 rational numbers section layout', async ({ page }) => {
    await gotoAndSettle(page);
    await page.locator('[data-testid="nav-ch01"]').click();
    await page.locator('[data-testid="chapter-1"]').waitFor({ state: 'visible' });
    await expect(page.locator('[data-testid="chapter-1"]')).toHaveScreenshot(
      'ch01-section.png', SNAP_OPTS
    );
  });

  test('VR-06: CH01 fraction converter result after computation', async ({ page }) => {
    await gotoAndSettle(page);
    await page.locator('[data-testid="nav-ch01"]').click();
    await page.locator('[data-testid="chapter-1"]').waitFor({ state: 'visible' });
    await page.locator('[data-testid="ch01-numerator"]').fill('3');
    await page.locator('[data-testid="ch01-denominator"]').fill('4');
    await page.locator('[data-testid="ch01-convert-btn"]').click();
    await expect(page.locator('[data-testid="ch01-result"]')).toHaveScreenshot(
      'ch01-result-0.75.png', SNAP_OPTS
    );
  });

  test('VR-07: CH03 quadrilaterals section with square selected', async ({ page }) => {
    await gotoAndSettle(page);
    await page.locator('[data-testid="nav-ch03"]').click();
    await page.locator('[data-testid="chapter-3"]').waitFor({ state: 'visible' });
    await page.locator('[data-testid="ch03-card-square"]').click();
    await page.waitForTimeout(150);
    await expect(page.locator('[data-testid="chapter-3"]')).toHaveScreenshot(
      'ch03-square-selected.png', SNAP_OPTS
    );
  });

  test('VR-08: CH05 bar chart canvas after render', async ({ page }) => {
    await gotoAndSettle(page);
    await page.locator('[data-testid="nav-ch05"]').click();
    await page.locator('[data-testid="chapter-5"]').waitFor({ state: 'visible' });
    await page.locator('[data-testid="ch05-chart-type"]').selectOption('bar');
    await page.locator('[data-testid="ch05-draw-btn"]').click();
    await page.waitForTimeout(200);
    await expect(page.locator('[data-testid="ch05-canvas"]')).toHaveScreenshot(
      'ch05-bar-chart.png', SNAP_OPTS
    );
  });

  test('VR-09: CH05 pie chart canvas after render', async ({ page }) => {
    await gotoAndSettle(page);
    await page.locator('[data-testid="nav-ch05"]').click();
    await page.locator('[data-testid="chapter-5"]').waitFor({ state: 'visible' });
    await page.locator('[data-testid="ch05-chart-type"]').selectOption('pie');
    await page.locator('[data-testid="ch05-draw-btn"]').click();
    await page.waitForTimeout(200);
    await expect(page.locator('[data-testid="ch05-canvas"]')).toHaveScreenshot(
      'ch05-pie-chart.png', SNAP_OPTS
    );
  });

  test('VR-10: CH15 line graph canvas after render', async ({ page }) => {
    await gotoAndSettle(page);
    await page.locator('[data-testid="nav-ch15"]').click();
    await page.locator('[data-testid="chapter-15"]').waitFor({ state: 'visible' });
    await page.locator('[data-testid="ch15-draw-btn"]').click();
    await page.waitForTimeout(200);
    await expect(page.locator('[data-testid="ch15-canvas"]')).toHaveScreenshot(
      'ch15-line-graph.png', SNAP_OPTS
    );
  });
});

// ─── MCQ interaction state snapshots ──────────────────────────────────────
test.describe('MCQ Interaction States', () => {

  test('VR-11: MCQ option shows correct styling after right answer', async ({ page }) => {
    await gotoAndSettle(page);
    await page.locator('[data-testid="nav-ch01"]').click();
    await page.locator('[data-testid="chapter-1"]').waitFor({ state: 'visible' });
    const btn = page.locator('[data-testid="ch01-q1-c"]');
    await btn.click();
    await page.waitForTimeout(150);
    await expect(btn).toHaveScreenshot('mcq-correct-state.png', SNAP_OPTS);
  });

  test('VR-12: MCQ option shows incorrect styling after wrong answer', async ({ page }) => {
    await gotoAndSettle(page);
    await page.locator('[data-testid="nav-ch01"]').click();
    await page.locator('[data-testid="chapter-1"]').waitFor({ state: 'visible' });
    const btn = page.locator('[data-testid="ch01-q1-a"]');
    await btn.click();
    await page.waitForTimeout(150);
    await expect(btn).toHaveScreenshot('mcq-incorrect-state.png', SNAP_OPTS);
  });
});

// ─── Mobile viewport snapshots (Mobile Chrome only) ───────────────────────
test.describe('Mobile Viewport Layout', () => {

  test('VR-13: mobile nav bar renders correctly', async ({ page }) => {
    await gotoAndSettle(page);
    await expect(page.locator('[data-testid="nav-bar"]')).toHaveScreenshot(
      'nav-bar-mobile.png', SNAP_OPTS
    );
  });

  test('VR-14: CH01 section layout on mobile viewport', async ({ page }) => {
    await gotoAndSettle(page);
    await page.locator('[data-testid="nav-ch01"]').click();
    await page.locator('[data-testid="chapter-1"]').waitFor({ state: 'visible' });
    await expect(page.locator('[data-testid="chapter-1"]')).toHaveScreenshot(
      'ch01-section-mobile.png', SNAP_OPTS
    );
  });
});
