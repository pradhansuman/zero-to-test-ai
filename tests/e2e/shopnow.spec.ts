import { test, expect } from '@playwright/test';

test.describe('ShopNow Store - Complete User Journey', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('file:///Users/skp/Downloads/QA_AGents/store.html');
    // Clear localStorage before each test
    await page.evaluate(() => localStorage.clear());
    await page.reload();
  });

  test('1. Display all 10 products on page load', async ({ page }) => {
    const productCards = await page.locator('[data-testid="product-card"]').count();
    expect(productCards).toBe(10);

    const productNames = await page.locator('[data-testid="product-name"]').allTextContents();
    expect(productNames).toContain('Wireless Headphones');
    expect(productNames).toContain('Gaming Keyboard');
    expect(productNames).toContain('Notebook Set');
  });

  test('2. Display correct product prices', async ({ page }) => {
    const prices = await page.locator('[data-testid="product-price"]').allTextContents();
    expect(prices[0]).toBe('$79.99'); // Wireless Headphones
    expect(prices[2]).toBe('$39.95'); // Portable Charger
    expect(prices[9]).toBe('$18.00'); // Notebook Set
  });

  test('3. Add single item to cart', async ({ page }) => {
    await page.click('[data-testid="add-to-cart"][data-product-id="1"]');

    const cartCount = await page.locator('[data-testid="cart-count"]').textContent();
    expect(cartCount).toBe('1');

    const buttonText = await page.locator('[data-testid="add-to-cart"][data-product-id="1"]').textContent();
    expect(buttonText).toBe('Added!');
  });

  test('4. Add multiple different items to cart', async ({ page }) => {
    await page.click('[data-testid="add-to-cart"][data-product-id="1"]');
    await page.click('[data-testid="add-to-cart"][data-product-id="3"]');
    await page.click('[data-testid="add-to-cart"][data-product-id="5"]');

    const cartCount = await page.locator('[data-testid="cart-count"]').textContent();
    expect(cartCount).toBe('3');
  });

  test('5. Add same item multiple times increases quantity', async ({ page }) => {
    await page.click('[data-testid="add-to-cart"][data-product-id="2"]');
    await page.click('[data-testid="add-to-cart"][data-product-id="2"]');

    const cartCount = await page.locator('[data-testid="cart-count"]').textContent();
    expect(cartCount).toBe('2');
  });

  test('6. Open and close cart sidebar', async ({ page }) => {
    const sidebar = page.locator('[data-testid="cart-sidebar"]');

    // Initially closed
    const initialClass = await sidebar.getAttribute('class');
    expect(initialClass).not.toContain('open');

    // Open cart
    await page.click('[data-testid="cart-button"]');
    const openClass = await sidebar.getAttribute('class');
    expect(openClass).toContain('open');

    // Close cart
    await page.click('[data-testid="cart-button"]');
    const closedClass = await sidebar.getAttribute('class');
    expect(closedClass).not.toContain('open');
  });

  test('7. Display correct cart total', async ({ page }) => {
    // Add items: Wireless Headphones ($79.99) + Gaming Keyboard ($119.00)
    await page.click('[data-testid="add-to-cart"][data-product-id="1"]');
    await page.click('[data-testid="add-to-cart"][data-product-id="2"]');

    await page.click('[data-testid="cart-button"]');

    const total = await page.locator('[data-testid="cart-total"]').textContent();
    expect(total).toBe('$198.99');
  });

  test('8. Increase item quantity in cart', async ({ page }) => {
    await page.click('[data-testid="add-to-cart"][data-product-id="1"]');
    await page.click('[data-testid="cart-button"]');

    // Increase quantity
    await page.click('[data-testid="qty-increase"][data-product-id="1"]');

    const cartCount = await page.locator('[data-testid="cart-count"]').textContent();
    expect(cartCount).toBe('2');

    const total = await page.locator('[data-testid="cart-total"]').textContent();
    expect(total).toBe('$159.98'); // 79.99 * 2
  });

  test('9. Decrease item quantity in cart', async ({ page }) => {
    await page.click('[data-testid="add-to-cart"][data-product-id="3"]');
    await page.click('[data-testid="add-to-cart"][data-product-id="3"]');
    await page.click('[data-testid="add-to-cart"][data-product-id="3"]');
    await page.click('[data-testid="cart-button"]');

    // Decrease quantity
    await page.click('[data-testid="qty-decrease"][data-product-id="3"]');

    const cartCount = await page.locator('[data-testid="cart-count"]').textContent();
    expect(cartCount).toBe('2');

    const total = await page.locator('[data-testid="cart-total"]').textContent();
    expect(total).toBe('$79.90'); // 39.95 * 2
  });

  test('10. Remove item from cart', async ({ page }) => {
    await page.click('[data-testid="add-to-cart"][data-product-id="4"]');
    await page.click('[data-testid="add-to-cart"][data-product-id="5"]');
    await page.click('[data-testid="cart-button"]');

    // Remove first item
    await page.click('[data-testid="remove-item"][data-product-id="4"]');

    const cartCount = await page.locator('[data-testid="cart-count"]').textContent();
    expect(cartCount).toBe('1');

    const total = await page.locator('[data-testid="cart-total"]').textContent();
    expect(total).toBe('$89.00'); // Only Running Shoes left
  });

  test('11. Empty cart shows "No items" message', async ({ page }) => {
    await page.click('[data-testid="cart-button"]');

    const emptyMessage = await page.locator('text=No items in cart yet.').isVisible();
    expect(emptyMessage).toBe(true);
  });

  test('12. Checkout button disabled when cart is empty', async ({ page }) => {
    await page.click('[data-testid="cart-button"]');

    const checkoutBtn = page.locator('[data-testid="checkout-btn"]');
    const isDisabled = await checkoutBtn.isDisabled();
    expect(isDisabled).toBe(true);
  });

  test('13. Checkout button enabled when cart has items', async ({ page }) => {
    await page.click('[data-testid="add-to-cart"][data-product-id="1"]');
    await page.click('[data-testid="cart-button"]');

    const checkoutBtn = page.locator('[data-testid="checkout-btn"]');
    const isDisabled = await checkoutBtn.isDisabled();
    expect(isDisabled).toBe(false);
  });

  test('14. Complete checkout clears cart', async ({ page }) => {
    await page.click('[data-testid="add-to-cart"][data-product-id="1"]');
    await page.click('[data-testid="add-to-cart"][data-product-id="2"]');

    await page.click('[data-testid="cart-button"]');

    // Handle alert
    page.once('dialog', dialog => {
      expect(dialog.message()).toContain('Order placed!');
      expect(dialog.message()).toContain('Wireless Headphones × 1');
      expect(dialog.message()).toContain('Gaming Keyboard × 1');
      expect(dialog.message()).toContain('Total: $198.99');
      dialog.accept();
    });

    await page.click('[data-testid="checkout-btn"]');

    // Verify cart is cleared
    const cartCount = await page.locator('[data-testid="cart-count"]').textContent();
    expect(cartCount).toBe('0');

    const emptyMessage = await page.locator('text=No items in cart yet.').isVisible();
    expect(emptyMessage).toBe(true);
  });

  test('15. LocalStorage persists cart across page reload', async ({ page }) => {
    await page.click('[data-testid="add-to-cart"][data-product-id="1"]');
    await page.click('[data-testid="add-to-cart"][data-product-id="3"]');

    const countBeforeReload = await page.locator('[data-testid="cart-count"]').textContent();
    expect(countBeforeReload).toBe('2');

    // Reload page
    await page.reload();

    // Cart should still have items
    const countAfterReload = await page.locator('[data-testid="cart-count"]').textContent();
    expect(countAfterReload).toBe('2');

    const total = await page.locator('[data-testid="cart-total"]').textContent();
    expect(total).toBe('$119.94'); // 79.99 + 39.95
  });

  test('16. Toast notification shows when item added', async ({ page }) => {
    await page.click('[data-testid="add-to-cart"][data-product-id="1"]');

    const toast = page.locator('#toast');
    const isVisible = await toast.isVisible();
    expect(isVisible).toBe(true);

    const toastText = await toast.textContent();
    expect(toastText).toContain('Wireless Headphones added to cart');
  });

  test('17. Product grid is responsive (desktop layout)', async ({ page }) => {
    const grid = page.locator('[data-testid="product-grid"]');
    const gridStyle = await grid.getAttribute('class');
    expect(gridStyle).toContain('grid');
  });

  test('18. Complete shopping journey', async ({ page }) => {
    // Browse and add multiple items
    await page.click('[data-testid="add-to-cart"][data-product-id="1"]'); // Headphones $79.99
    await page.click('[data-testid="add-to-cart"][data-product-id="3"]'); // Charger $39.95
    await page.click('[data-testid="add-to-cart"][data-product-id="6"]'); // Water Bottle $24.99

    // Open cart and verify
    await page.click('[data-testid="cart-button"]');
    let total = await page.locator('[data-testid="cart-total"]').textContent();
    expect(total).toBe('$144.93');

    // Increase charger quantity
    await page.click('[data-testid="qty-increase"][data-product-id="3"]');
    total = await page.locator('[data-testid="cart-total"]').textContent();
    expect(total).toBe('$184.88');

    // Remove water bottle
    await page.click('[data-testid="remove-item"][data-product-id="6"]');
    total = await page.locator('[data-testid="cart-total"]').textContent();
    expect(total).toBe('$159.88');

    // Checkout
    page.once('dialog', dialog => {
      expect(dialog.message()).toContain('$159.88');
      dialog.accept();
    });
    await page.click('[data-testid="checkout-btn"]');

    // Verify empty cart after checkout
    const cartCount = await page.locator('[data-testid="cart-count"]').textContent();
    expect(cartCount).toBe('0');
  });

  test('19. Accessibility - ARIA labels present', async ({ page }) => {
    const cartBtn = page.locator('[data-testid="cart-button"]');
    const ariaLabel = await cartBtn.getAttribute('aria-label');
    expect(ariaLabel).toBeTruthy();
    expect(ariaLabel).toContain('Shopping cart');
  });

  test('20. Edge case - Remove all items then add again', async ({ page }) => {
    await page.click('[data-testid="add-to-cart"][data-product-id="2"]');
    await page.click('[data-testid="cart-button"]');
    await page.click('[data-testid="remove-item"][data-product-id="2"]');

    let cartCount = await page.locator('[data-testid="cart-count"]').textContent();
    expect(cartCount).toBe('0');

    // Close and re-open cart
    await page.click('[data-testid="cart-button"]');
    await page.click('[data-testid="cart-button"]');

    // Add item again
    await page.click('[data-testid="add-to-cart"][data-product-id="2"]');
    cartCount = await page.locator('[data-testid="cart-count"]').textContent();
    expect(cartCount).toBe('1');
  });
});
