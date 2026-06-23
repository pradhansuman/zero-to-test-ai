import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  testMatch: '**/math-hub.spec.golden.ts',
  fullyParallel: true,
  workers: 4,
  retries: 1,
  timeout: 30_000,
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report-math-hub', open: 'never' }],
  ],
  use: {
    baseURL: 'https://pradhansuman.github.io/qa-agent-pipeline/math_hub.html',
    headless: true,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'Desktop Chrome',  use: { ...devices['Desktop Chrome'] } },
    { name: 'Mobile Chrome',   use: { ...devices['Pixel 7'] } },
    { name: 'Mobile Safari',   use: { ...devices['iPhone 14'] } },
  ],
});
