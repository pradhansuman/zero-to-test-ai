import { defineConfig, devices } from '@playwright/test';

/**
 * MANDATORY HTML REPORT CONFIGURATION
 * ====================================
 * This configuration ensures that HTML reports are ALWAYS generated
 * for every test execution, regardless of outcome.
 *
 * Use with: npx playwright test --config playwright.mandatory-report.config.ts
 */

export default defineConfig({
  testDir: './tests/e2e',

  /* Reporters - MANDATORY HTML + JSON + JUnit */
  reporter: [
    // HTML Report - MANDATORY for every execution
    ['html', {
      open: 'never',  // Don't auto-open (user manually opens)
      outputFolder: './playwright-report',
    }],

    // JSON Report - For programmatic access
    ['json', {
      outputFile: './test-results-store/results.json',
    }],

    // JUnit XML - For CI/CD integration (Jenkins, GitLab, etc)
    ['junit', {
      outputFile: './test-results-store/results.xml',
    }],

    // List Reporter - Terminal output
    ['list'],
  ],

  /* Shared settings for all browsers */
  use: {
    baseURL: 'file:///' + __dirname + '/public/store.html',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'Desktop Chrome',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'Desktop Firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'Desktop Safari',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  /* Global timeout - prevent hanging tests */
  timeout: 30 * 1000,

  /* Expect timeout */
  expect: {
    timeout: 5000,
  },

  /* Parallel execution */
  fullyParallel: true,
  workers: process.env.CI ? 1 : 4,

  /* Fail on console errors */
  use: {
    ...devices['Desktop Chrome'],
  },

  /* Retry failed tests once */
  retries: process.env.CI ? 2 : 0,
});
