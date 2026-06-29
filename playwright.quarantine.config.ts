import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30 * 1000,
  retries: 2,
  reporter: [
    ['json', { outputFile: 'quarantine-results.json' }],
    ['html'],
  ],
});

export const FLAKY_TESTS = [
  'AX-STORE-02', // Firefox a11y audit occasionally hangs
];

export function isFlaky(testName: string): boolean {
  return FLAKY_TESTS.some(p => testName.includes(p));
}
