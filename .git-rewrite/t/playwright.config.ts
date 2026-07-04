/**
 * Default Playwright config — runs the ShopNow store pyramid.
 * Equivalent to: npx playwright test --config playwright.store.config.ts
 *
 * Named configs for targeted runs:
 *   playwright.store.config.ts    — store pyramid (9 suites, 3 browsers)
 *   playwright.math-hub.config.ts — math hub (6 suites, 2 browsers)
 */
import { defineConfig, devices } from '@playwright/test';
import path from 'path';

export default defineConfig({
  testDir: './tests/e2e',
  testMatch: ['store-*.spec.ts'],
  fullyParallel: true,
  workers: 4,
  retries: 1,
  outputDir: 'test-results-store/',
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report-store', open: 'never' }],
    ['json', { outputFile: 'test-results-store/results.json' }],
  ],
  snapshotDir: './tests/e2e/__snapshots__',
  snapshotPathTemplate: '{snapshotDir}/{testFilePath}/{projectName}/{arg}{ext}',
  use: {
    screenshot: 'only-on-failure',
    video: 'off',
    trace: 'off',
  },
  expect: {
    toHaveScreenshot: { maxDiffPixelRatio: 0.02 },
  },
  projects: [
    { name: 'Desktop Chrome', use: { ...devices['Desktop Chrome'] } },
    { name: 'Mobile Chrome',  use: { ...devices['Pixel 7'] } },
    {
      name: 'Desktop Firefox',
      use: { ...devices['Desktop Firefox'] },
      testIgnore: ['**/store-visual.spec.ts'],
    },
    ...(process.env.CI || process.env.INCLUDE_SAFARI ? [{
      name: 'Mobile Safari',
      use: { ...devices['iPhone 14'] },
      testIgnore: ['**/store-visual.spec.ts'],
    }] : []),
  ],
});
