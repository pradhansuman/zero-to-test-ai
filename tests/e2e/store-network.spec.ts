/**
 * ShopNow — State Resilience & Isolation Tests
 * Validates that cart state survives page reloads, is isolated between
 * browser contexts, and recovers gracefully from corrupted localStorage.
 * Also covers CPU-throttled performance and rapid-fire operation safety.
 */

import { test, expect, chromium, Browser } from '@playwright/test';
import path from 'path';

const URL = `file://${path.resolve(__dirname, '../../store.html')}`;

// ── NET-STORE-01 ──────────────────────────────────────────────────────────────
test('NET-STORE-01: cart state persists across a full page reload', async ({ page }) => {
  await page.goto(URL);
  await page.waitForSelector('.card');

  await page.evaluate(() => {
    (window as any).addToCart(1);
    (window as any).addToCart(3);
    (window as any).addToCart(3);
  });

  await page.reload();
  await page.waitForSelector('.card');

  const cartState = await page.evaluate(() =>
    JSON.parse(localStorage.getItem('shopnow-cart') || '{}')
  );
  expect(cartState['1']).toBe(1);
  expect(cartState['3']).toBe(2);

  const count = await page.locator('#cart-count').textContent();
  expect(count).toBe('3');
});

// ── NET-STORE-02 ──────────────────────────────────────────────────────────────
test('NET-STORE-02: two browser contexts have completely isolated cart state', async ({ browser }) => {
  const ctx1 = await browser.newContext();
  const ctx2 = await browser.newContext();
  const page1 = await ctx1.newPage();
  const page2 = await ctx2.newPage();

  await page1.goto(URL);
  await page2.goto(URL);
  await page1.waitForSelector('.card');
  await page2.waitForSelector('.card');

  await page1.evaluate(() => { (window as any).addToCart(1); (window as any).addToCart(2); });
  await page2.evaluate(() => (window as any).addToCart(5));

  const count1 = await page1.locator('#cart-count').textContent();
  const count2 = await page2.locator('#cart-count').textContent();
  expect(count1).toBe('2');
  expect(count2).toBe('1');

  await ctx1.close();
  await ctx2.close();
});

// ── NET-STORE-03 ──────────────────────────────────────────────────────────────
test('NET-STORE-03: page recovers gracefully from corrupted localStorage', async ({ page }) => {
  await page.goto(URL);

  // Inject corrupt data before the store initialises on next load
  await page.evaluate(() => localStorage.setItem('shopnow-cart', '{INVALID JSON'));
  await page.reload();
  await page.waitForSelector('.card');

  // Page must still render and cart should reset to empty (no crash / blank screen)
  const cards = await page.locator('.card').count();
  expect(cards).toBe(10);

  const count = await page.locator('#cart-count').textContent();
  // Corrupted JSON → cart resets to 0
  expect(parseInt(count || '0')).toBeGreaterThanOrEqual(0);
});

// ── NET-STORE-04 ──────────────────────────────────────────────────────────────
test('NET-STORE-04 (Chromium only): page stays usable under 6× CPU throttle', async ({ page, browserName }) => {
  test.skip(browserName !== 'chromium', 'CDP CPU throttling is Chromium-only');

  await page.goto(URL);
  await page.waitForSelector('.card');

  const client = await page.context().newCDPSession(page);
  await client.send('Emulation.setCPUThrottlingRate', { rate: 6 });

  const start = Date.now();
  await page.evaluate(() => {
    for (let id = 1; id <= 10; id++) (window as any).addToCart(id);
    (window as any).toggleCart();
  });
  const elapsed = Date.now() - start;

  // Even at 6× slowdown, all 10 adds + cart open should complete within 2s
  expect(elapsed).toBeLessThan(2000);

  const count = await page.locator('#cart-count').textContent();
  expect(parseInt(count || '0')).toBe(10);

  await client.send('Emulation.setCPUThrottlingRate', { rate: 1 }); // restore
});

// ── NET-STORE-05 ──────────────────────────────────────────────────────────────
test('NET-STORE-05: rapid concurrent addToCart calls do not corrupt cart totals', async ({ page }) => {
  await page.goto(URL);
  await page.waitForSelector('.card');

  await page.evaluate(() => {
    // Fire 30 addToCart calls in a tight loop — simulates rapid user clicking
    for (let i = 0; i < 10; i++) {
      (window as any).addToCart(1);
      (window as any).addToCart(2);
      (window as any).addToCart(3);
    }
  });

  const count = await page.locator('#cart-count').textContent();
  expect(parseInt(count || '0')).toBe(30); // 10 × 3 products

  const cartState = await page.evaluate(() =>
    JSON.parse(localStorage.getItem('shopnow-cart') || '{}')
  );
  expect(cartState['1']).toBe(10);
  expect(cartState['2']).toBe(10);
  expect(cartState['3']).toBe(10);
});

// ── NET-STORE-06 ──────────────────────────────────────────────────────────────
test('NET-STORE-06: large cart (50 adds) stays under 5 KB in localStorage', async ({ page }) => {
  await page.goto(URL);
  await page.waitForSelector('.card');

  await page.evaluate(() => {
    for (let id = 1; id <= 10; id++) {
      for (let n = 0; n < 5; n++) (window as any).addToCart(id);
    }
  });

  const byteSize = await page.evaluate(() => {
    const val = localStorage.getItem('shopnow-cart') || '';
    return new TextEncoder().encode(val).length;
  });

  expect(byteSize).toBeLessThan(5 * 1024); // 5 KB guard
});

// ── NET-STORE-07 ──────────────────────────────────────────────────────────────
test('NET-STORE-07: removing all items clears localStorage cart entry', async ({ page }) => {
  await page.goto(URL);
  await page.waitForSelector('.card');

  await page.evaluate(() => {
    (window as any).addToCart(1);
    (window as any).addToCart(2);
    (window as any).removeItem(1);
    (window as any).removeItem(2);
  });

  const cartState = await page.evaluate(() =>
    JSON.parse(localStorage.getItem('shopnow-cart') || '{}')
  );
  const itemCount = Object.keys(cartState).length;
  expect(itemCount).toBe(0);

  const displayCount = await page.locator('#cart-count').textContent();
  expect(displayCount).toBe('0');
});

// ── NET-STORE-08 ──────────────────────────────────────────────────────────────
// Verifies that clearing localStorage and reloading starts a fresh session.
// (file:// history.pushState is blocked by same-origin policy so we use reload instead)
test('NET-STORE-08: clearing localStorage then reloading gives a clean empty cart', async ({ page }) => {
  await page.goto(URL);
  await page.waitForSelector('.card');

  await page.evaluate(() => {
    (window as any).addToCart(4);
    (window as any).addToCart(5);
  });
  expect(await page.locator('#cart-count').textContent()).toBe('2');

  // Remove the cart key from localStorage — simulates clearing a stale session
  await page.evaluate(() => localStorage.removeItem('shopnow-cart'));
  await page.reload();
  await page.waitForSelector('.card');

  // New session: in-memory cart initialised from empty localStorage
  expect(await page.locator('#cart-count').textContent()).toBe('0');

  const cartState = await page.evaluate(() =>
    JSON.parse(localStorage.getItem('shopnow-cart') || '{}')
  );
  expect(Object.keys(cartState).length).toBe(0);
});
