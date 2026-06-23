import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  testMatch: '**/math-hub*.spec.ts',
  fullyParallel: true,
  workers: 4,
  retries: 1,
  timeout: 30_000,
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report-math-hub', open: 'never' }],
  ],
  // Visual regression baseline storage — committed alongside spec files
  snapshotDir: './tests/e2e/__snapshots__',
  snapshotPathTemplate: '{snapshotDir}/{testFilePath}/{projectName}/{arg}{ext}',
  expect: {
    // 2% pixel tolerance — absorbs sub-pixel font rendering across OS versions
    toHaveScreenshot: { maxDiffPixelRatio: 0.02 },
  },
  use: {
    baseURL: 'https://pradhansuman.github.io/qa-agent-pipeline/math_hub.html',
    headless: true,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'Desktop Chrome',  use: { ...devices['Desktop Chrome'] } },
    { name: 'Mobile Chrome',   use: { ...devices['Pixel 7'] } },
    // Mobile Safari (WebKit) runs in CI (Linux, Playwright Docker) — not locally on macOS 13
    // To run locally: PWTEST_WEBKIT=1 npx playwright test --config playwright.math-hub.config.ts
    ...(process.env.PWTEST_WEBKIT ? [
      { name: 'Mobile Safari', use: { ...devices['iPhone 14'] } },
    ] : []),
  ],
});
