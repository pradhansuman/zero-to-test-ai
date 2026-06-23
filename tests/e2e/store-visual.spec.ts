/**
 * ShopNow — Visual Regression Tests
 * Uses toHaveScreenshot() with 2% pixel tolerance.
 * Baselines committed in tests/e2e/__snapshots__/store-visual.spec.ts/
 *
 * Generate or update baselines:
 *   npx playwright test --config playwright.store.config.ts \
 *     tests/e2e/store-visual.spec.ts --update-snapshots
 */

import { test, expect } from '@playwright/test';
import path from 'path';

const URL = `file://${path.resolve(__dirname, '../../store.html')}`;
const SNAP = { maxDiffPixelRatio: 0.02 } as const;

async function loadAndSettle(page: any): Promise<void> {
  await page.goto(URL, { waitUntil: 'load' });
  await page.waitForSelector('.card');
  // Disable all CSS transitions and animations for stable screenshots
  await page.evaluate(() => {
    const style = document.createElement('style');
    style.textContent = '*, *::before, *::after { transition: none !important; animation: none !important; }';
    document.head.appendChild(style);
  });
}

test.beforeEach(async ({ page }) => {
  await loadAndSettle(page);
});

// ── VR-STORE-01 ───────────────────────────────────────────────────────────────
test('VR-STORE-01 @smoke: full page — product grid', async ({ page }) => {
  await expect(page).toHaveScreenshot('store-full-page.png', {
    ...SNAP,
    fullPage: true,
    animations: 'disabled',
  });
});

// ── VR-STORE-02 ───────────────────────────────────────────────────────────────
test('VR-STORE-02: sticky header with cart button', async ({ page }) => {
  await expect(page.locator('header')).toHaveScreenshot('store-header.png', SNAP);
});

// ── VR-STORE-03 ───────────────────────────────────────────────────────────────
test('VR-STORE-03: first product card (Wireless Headphones)', async ({ page }) => {
  await expect(page.locator('.card').first()).toHaveScreenshot('store-product-card.png', SNAP);
});

// ── VR-STORE-04 ───────────────────────────────────────────────────────────────
test('VR-STORE-04: cart button — initial empty state (count = 0)', async ({ page }) => {
  await expect(page.locator('#cart-btn')).toHaveScreenshot('store-cart-btn-empty.png', SNAP);
});

// ── VR-STORE-05 ───────────────────────────────────────────────────────────────
test('VR-STORE-05: cart button — count updates to 3 after three adds', async ({ page }) => {
  await page.evaluate(() => {
    for (let id = 1; id <= 3; id++) (window as any).addToCart(id);
  });
  await expect(page.locator('#cart-btn')).toHaveScreenshot('store-cart-btn-3.png', SNAP);
});

// ── VR-STORE-06 ───────────────────────────────────────────────────────────────
test('VR-STORE-06: cart sidebar open — empty state', async ({ page }) => {
  await page.evaluate(() => (window as any).toggleCart());
  await expect(page.locator('#cart-sidebar')).toHaveScreenshot('store-cart-empty.png', SNAP);
});

// ── VR-STORE-07 ───────────────────────────────────────────────────────────────
test('VR-STORE-07: cart sidebar with one item', async ({ page }) => {
  await page.evaluate(() => {
    (window as any).addToCart(1);
    (window as any).toggleCart();
  });
  await expect(page.locator('#cart-sidebar')).toHaveScreenshot('store-cart-one-item.png', SNAP);
});

// ── VR-STORE-08 ───────────────────────────────────────────────────────────────
test('VR-STORE-08: cart sidebar with three different items', async ({ page }) => {
  await page.evaluate(() => {
    (window as any).addToCart(1);
    (window as any).addToCart(3);
    (window as any).addToCart(6);
    (window as any).toggleCart();
  });
  await expect(page.locator('#cart-sidebar')).toHaveScreenshot('store-cart-three-items.png', SNAP);
});

// ── VR-STORE-09 ───────────────────────────────────────────────────────────────
test('VR-STORE-09: cart footer — total and checkout button with items', async ({ page }) => {
  await page.evaluate(() => {
    (window as any).addToCart(1);
    (window as any).addToCart(2);
    (window as any).toggleCart();
  });
  await expect(page.locator('.cart-footer')).toHaveScreenshot('store-cart-footer-active.png', SNAP);
});

// ── VR-STORE-10 ───────────────────────────────────────────────────────────────
test('VR-STORE-10: checkout button — disabled state (empty cart)', async ({ page }) => {
  await expect(page.locator('#checkout-btn')).toHaveScreenshot('store-checkout-disabled.png', SNAP);
});

// ── VR-STORE-11 ───────────────────────────────────────────────────────────────
test('VR-STORE-11: checkout button — enabled state (cart has items)', async ({ page }) => {
  await page.evaluate(() => (window as any).addToCart(1));
  await expect(page.locator('#checkout-btn')).toHaveScreenshot('store-checkout-enabled.png', SNAP);
});

// ── VR-STORE-12 ───────────────────────────────────────────────────────────────
test('VR-STORE-12: quantity controls for an item with qty = 3', async ({ page }) => {
  await page.evaluate(() => {
    (window as any).addToCart(2);
    (window as any).changeQty(2, 1);
    (window as any).changeQty(2, 1);
    (window as any).toggleCart();
  });
  await expect(page.locator('.qty-ctrl').first()).toHaveScreenshot('store-qty-controls.png', SNAP);
});

// ── VR-STORE-13 ───────────────────────────────────────────────────────────────
test('VR-STORE-13: full page — mobile viewport layout', async ({ page }) => {
  await expect(page).toHaveScreenshot('store-mobile-full.png', {
    ...SNAP,
    fullPage: true,
    animations: 'disabled',
  });
});

// ── VR-STORE-14 ───────────────────────────────────────────────────────────────
test('VR-STORE-14: cart sidebar open on mobile viewport', async ({ page }) => {
  await page.evaluate(() => {
    (window as any).addToCart(1);
    (window as any).addToCart(5);
    (window as any).toggleCart();
  });
  await expect(page.locator('#cart-sidebar')).toHaveScreenshot('store-mobile-cart.png', SNAP);
});
