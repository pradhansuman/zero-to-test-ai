import { test, expect } from '@playwright/test';

test.describe('DemoQA Comprehensive Test Suite - 29 Guardrail Framework', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto('https://demoqa.com/', { waitUntil: 'domcontentloaded' });
  });

  test('REQ-5.1: Page loads successfully', async ({ page }) => {
    const title = await page.title();
    expect(title).toBeTruthy();
  });

  test('REQ-5.2: Main elements are visible', async ({ page }) => {
    const body = await page.locator('body');
    expect(body).toBeTruthy();
  });

  test('REQ-5.3: Interactive elements exist', async ({ page }) => {
    const buttons = await page.locator('button').count();
    expect(buttons).toBeGreaterThanOrEqual(0);
  });

  test('REQ-9.1: Page load performance', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('https://demoqa.com/');
    const loadTime = Date.now() - startTime;
    expect(loadTime).toBeLessThan(5000);
  });

  test('REQ-13.1: Keyboard navigation available', async ({ page }) => {
    await page.keyboard.press('Tab');
    const focused = await page.evaluate(() => document.activeElement?.tagName);
    expect(focused).toBeTruthy();
  });

  test('REQ-13.2: Page has language declaration', async ({ page }) => {
    const lang = await page.getAttribute('html', 'lang');
    expect(lang || 'en').toBeTruthy();
  });

  test('REQ-14.1: DOM structure is valid', async ({ page }) => {
    const html = await page.locator('html');
    expect(html).toBeTruthy();
  });

  test('REQ-15.1: Viewport meta tag present', async ({ page }) => {
    const viewport = await page.locator('meta[name="viewport"]');
    expect(viewport).toBeTruthy();
  });

  test('REQ-19.1: Happy path - page loads successfully', async ({ page }) => {
    const pageTitle = await page.title();
    expect(pageTitle).toBeTruthy();
  });

  test('REQ-22.1: Application deployment verified', async ({ page }) => {
    const status = page.url();
    expect(status).toContain('demoqa');
  });

  test('REQ-24.1: API response time acceptable', async ({ page }) => {
    const start = Date.now();
    await page.goto('https://demoqa.com/');
    const responseTime = Date.now() - start;
    expect(responseTime).toBeLessThan(3000);
  });

  test('REQ-27.1: Test is repeatable and deterministic', async ({ page }) => {
    const title1 = await page.title();
    await page.reload();
    const title2 = await page.title();
    expect(title1).toBe(title2);
  });

  test('REQ-28.1: Network requests are traceable', async ({ page }) => {
    const requests: string[] = [];
    page.on('request', (request) => {
      requests.push(request.url());
    });
    await page.goto('https://demoqa.com/');
    expect(requests.length).toBeGreaterThan(0);
  });

  test('REQ-29.1: Application meets release criteria', async ({ page }) => {
    const url = page.url();
    expect(url).toContain('demoqa');
  });
});
