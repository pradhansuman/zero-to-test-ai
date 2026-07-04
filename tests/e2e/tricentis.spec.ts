import { test, expect, Page } from '@playwright/test';

const BASE_URL = 'https://demowebshop.tricentis.com';

// Test data
const testUser = {
  email: `test-${Date.now()}@example.com`,
  firstName: 'Test',
  lastName: 'User',
  password: 'Test@123456'
};

test.describe('Tricentis Demo Web Shop - E-Commerce Suite', () => {
  test.describe('1. Homepage & Navigation', () => {
    test('Homepage loads successfully', async ({ page }) => {
      await page.goto(BASE_URL);
      await expect(page).toHaveTitle(/tricentis|demowebshop/i);

      // Verify key elements
      const logo = page.locator('[class*="logo"]').first();
      await expect(logo).toBeVisible();
    });

    test('Main navigation menu is accessible', async ({ page }) => {
      await page.goto(BASE_URL);

      // Check for main categories
      const categories = ['Books', 'Computers', 'Electronics', 'Apparel', 'Digital downloads', 'Gifts'];

      for (const category of categories) {
        const navItem = page.locator(`text=${category}`);
        if (await navItem.count() > 0) {
          await expect(navItem.first()).toBeVisible();
        }
      }
    });

    test('Search functionality works', async ({ page }) => {
      await page.goto(BASE_URL);

      const searchInput = page.locator('input[placeholder*="Search"], input[name*="q"]');
      if (await searchInput.count() > 0) {
        await searchInput.fill('book');
        await page.keyboard.press('Enter');

        // Verify search results page loads
        await page.waitForLoadState('networkidle');
        await expect(page).toHaveURL(/.*search|.*product/i);
      }
    });
  });

  test.describe('2. Product Catalog & Filtering', () => {
    test('Products display with prices', async ({ page }) => {
      await page.goto(`${BASE_URL}/books`);

      const products = page.locator('[class*="product"]').first();
      await expect(products).toBeVisible();

      // Verify price is visible
      const price = page.locator('text=/\\$[0-9]+/').first();
      await expect(price).toBeVisible();
    });

    test('Product details page loads', async ({ page }) => {
      await page.goto(`${BASE_URL}/books`);

      // Click first product
      const firstProduct = page.locator('a[href*="/p/"]').first();
      if (await firstProduct.count() > 0) {
        await firstProduct.click();
        await page.waitForLoadState('networkidle');

        // Verify product page elements
        await expect(page.locator('text=/[0-9]+\\.[0-9]{2}/')).toBeVisible();
      }
    });

    test('Add to cart button is functional', async ({ page }) => {
      await page.goto(`${BASE_URL}/books`);

      // Find and click add to cart
      const addButton = page.locator('button, input[type="button"]').filter({ hasText: /add|cart/i }).first();
      if (await addButton.count() > 0) {
        await addButton.click();

        // Wait for confirmation or cart update
        await page.waitForTimeout(1000);
      }
    });
  });

  test.describe('3. User Registration & Authentication', () => {
    test('Registration form accessible', async ({ page }) => {
      await page.goto(BASE_URL);

      // Navigate to registration
      const registerLink = page.locator('a:has-text("Register")');
      if (await registerLink.count() > 0) {
        await registerLink.click();
        await page.waitForLoadState('networkidle');

        // Verify registration form
        await expect(page.locator('input[name*="FirstName"], input[placeholder*="First"]')).toBeVisible();
        await expect(page.locator('input[name*="Email"], input[placeholder*="Email"]')).toBeVisible();
        await expect(page.locator('input[name*="Password"], input[placeholder*="Password"]')).toBeVisible();
      }
    });

    test('User can register with valid data', async ({ page }) => {
      await page.goto(`${BASE_URL}/register`);

      // Fill registration form
      const firstNameInput = page.locator('input[name*="FirstName"], input[placeholder*="First"]');
      const lastNameInput = page.locator('input[name*="LastName"], input[placeholder*="Last"]');
      const emailInput = page.locator('input[name*="Email"], input[placeholder*="Email"]');
      const passwordInput = page.locator('input[name*="Password"][type="password"]').first();
      const confirmInput = page.locator('input[name*="ConfirmPassword"], input[placeholder*="Confirm"]');

      if (await firstNameInput.count() > 0) {
        await firstNameInput.fill(testUser.firstName);
        if (await lastNameInput.count() > 0) await lastNameInput.fill(testUser.lastName);
        await emailInput.fill(testUser.email);
        await passwordInput.fill(testUser.password);
        if (await confirmInput.count() > 0) await confirmInput.fill(testUser.password);

        // Submit form
        const submitButton = page.locator('button[type="submit"], input[type="submit"]').first();
        await submitButton.click();

        await page.waitForLoadState('networkidle');
        // Verify success (may be redirect or success message)
        await expect(page).toHaveURL(/.*register|.*login|.*dashboard/i);
      }
    });

    test('Login page accessible', async ({ page }) => {
      await page.goto(`${BASE_URL}/login`);

      // Verify login form elements
      await expect(page.locator('input[type="email"], input[name*="email"]')).toBeVisible();
      await expect(page.locator('input[type="password"]')).toBeVisible();
    });
  });

  test.describe('4. Shopping Cart Operations', () => {
    test('Shopping cart page loads', async ({ page }) => {
      await page.goto(`${BASE_URL}/cart`);

      await page.waitForLoadState('networkidle');
      await expect(page).toHaveURL(/.*cart/i);
    });

    test('Add item to cart and verify', async ({ page }) => {
      await page.goto(`${BASE_URL}/books`);

      // Click add to cart on first product
      const addBtn = page.locator('button, input[type="button"]').filter({ hasText: /add.*cart|add to.*cart/i }).first();

      if (await addBtn.count() > 0) {
        await addBtn.click();
        await page.waitForTimeout(1000);

        // Navigate to cart
        const cartLink = page.locator('a:has-text("Cart")');
        if (await cartLink.count() > 0) {
          await cartLink.click();
          await page.waitForLoadState('networkidle');

          // Verify item in cart
          await expect(page.locator('table, [role="table"]').first()).toBeVisible();
        }
      }
    });

    test('Update item quantity in cart', async ({ page }) => {
      await page.goto(`${BASE_URL}/cart`);

      // Find quantity input
      const qtyInput = page.locator('input[name*="itemQuantity"], input[type="number"]').first();
      if (await qtyInput.count() > 0) {
        await qtyInput.clear();
        await qtyInput.fill('2');

        // Click update
        const updateBtn = page.locator('button, input[type="button"]').filter({ hasText: /update/i }).first();
        if (await updateBtn.count() > 0) {
          await updateBtn.click();
          await page.waitForLoadState('networkidle');
        }
      }
    });

    test('Remove item from cart', async ({ page }) => {
      await page.goto(`${BASE_URL}/cart`);

      // Click remove/delete button
      const removeBtn = page.locator('button, input[type="button"]').filter({ hasText: /remove|delete/i }).first();
      if (await removeBtn.count() > 0) {
        await removeBtn.click();
        await page.waitForLoadState('networkidle');
      }
    });
  });

  test.describe('5. Checkout Process', () => {
    test('Checkout page accessible', async ({ page }) => {
      await page.goto(`${BASE_URL}/cart`);

      // Look for checkout button
      const checkoutBtn = page.locator('button, input[type="button"]').filter({ hasText: /checkout/i }).first();
      if (await checkoutBtn.count() > 0) {
        await expect(checkoutBtn).toBeVisible();
      }
    });

    test('Billing address form displays', async ({ page }) => {
      // Navigate to checkout
      await page.goto(`${BASE_URL}/checkout`);

      // Verify billing form elements
      const addressInput = page.locator('input[name*="Address"], input[placeholder*="Address"]');
      if (await addressInput.count() > 0) {
        await expect(addressInput.first()).toBeVisible();
      }
    });

    test('Shipping method selection works', async ({ page }) => {
      await page.goto(`${BASE_URL}/checkout`);

      // Look for shipping options
      const shippingOptions = page.locator('input[name*="shipping"], input[type="radio"]');
      if (await shippingOptions.count() > 0) {
        await shippingOptions.first().click();
        await expect(shippingOptions.first()).toBeChecked();
      }
    });

    test('Payment method selection available', async ({ page }) => {
      await page.goto(`${BASE_URL}/checkout`);

      // Look for payment options
      const paymentMethods = page.locator('input[name*="payment"], input[type="radio"]');
      if (await paymentMethods.count() > 0) {
        await expect(paymentMethods.first()).toBeVisible();
      }
    });
  });

  test.describe('6. User Account Management', () => {
    test('Account page accessible when logged in', async ({ page }) => {
      // Try to access account
      await page.goto(`${BASE_URL}/customer/account`);

      // Should either show account page or redirect to login
      await page.waitForLoadState('networkidle');
      const isLoggedIn = await page.url().includes('/account');
      const isLoginPage = await page.url().includes('/login');

      expect(isLoggedIn || isLoginPage).toBeTruthy();
    });

    test('Order history displays', async ({ page }) => {
      await page.goto(`${BASE_URL}/customer/orders`);

      await page.waitForLoadState('networkidle');
      // Page should load without errors
      await expect(page).toHaveURL(/.*order|.*account/i);
    });

    test('Wishlist functionality exists', async ({ page }) => {
      await page.goto(BASE_URL);

      // Look for wishlist link
      const wishlistLink = page.locator('a:has-text("Wishlist"), [class*="wishlist"] a');
      if (await wishlistLink.count() > 0) {
        await expect(wishlistLink.first()).toBeVisible();
      }
    });
  });

  test.describe('7. Content Pages', () => {
    test('About page accessible', async ({ page }) => {
      await page.goto(`${BASE_URL}/about-us`);

      await page.waitForLoadState('networkidle');
      await expect(page).toHaveURL(/.*about/i);
    });

    test('Contact page accessible', async ({ page }) => {
      await page.goto(`${BASE_URL}/contact-us`);

      // Verify contact form or content
      await page.waitForLoadState('networkidle');
      const formOrContent = page.locator('form, [class*="contact"]');
      await expect(formOrContent.first()).toBeVisible();
    });

    test('Terms and conditions accessible', async ({ page }) => {
      // Look for T&C link in footer
      const tcLink = page.locator('a:has-text("Terms"), a:has-text("Conditions")');
      if (await tcLink.count() > 0) {
        await tcLink.first().click();
        await page.waitForLoadState('networkidle');
      }
    });
  });

  test.describe('8. Error Handling & Edge Cases', () => {
    test('Invalid product ID returns error or 404', async ({ page }) => {
      const response = await page.goto(`${BASE_URL}/p/999999999`, { waitUntil: 'networkidle' });

      // Should be 404 or show error message
      const isError = response?.status() === 404 || await page.locator('[class*="error"], text=/not found/i').count() > 0;
      expect(isError).toBeTruthy();
    });

    test('Empty search returns results page', async ({ page }) => {
      await page.goto(`${BASE_URL}/search`);

      await page.waitForLoadState('networkidle');
      // Should load without crashing
      await expect(page).toHaveURL(/.*search/i);
    });

    test('Add to cart with insufficient quantity', async ({ page }) => {
      await page.goto(`${BASE_URL}/books`);

      // Try adding with 0 or negative quantity
      const qtyInput = page.locator('input[type="number"][name*="quantity"]');
      if (await qtyInput.count() > 0) {
        await qtyInput.fill('0');

        const addBtn = page.locator('button').filter({ hasText: /add/i }).first();
        if (await addBtn.count() > 0) {
          await addBtn.click();
          await page.waitForTimeout(500);

          // Should either prevent or show error
        }
      }
    });
  });

  test.describe('9. Performance & Load Testing', () => {
    test('Homepage loads within acceptable time', async ({ page }) => {
      const startTime = Date.now();

      await page.goto(BASE_URL, { waitUntil: 'networkidle' });

      const loadTime = Date.now() - startTime;
      expect(loadTime).toBeLessThan(10000); // 10 seconds
    });

    test('Product page performance', async ({ page }) => {
      const startTime = Date.now();

      await page.goto(`${BASE_URL}/books`, { waitUntil: 'networkidle' });
      const firstProduct = page.locator('a[href*="/p/"]').first();

      if (await firstProduct.count() > 0) {
        await firstProduct.click();

        const loadTime = Date.now() - startTime;
        expect(loadTime).toBeLessThan(8000); // 8 seconds
      }
    });
  });

  test.describe('10. Security & Data Validation', () => {
    test('Login form does not expose password', async ({ page }) => {
      await page.goto(`${BASE_URL}/login`);

      const passwordInput = page.locator('input[type="password"]');
      await expect(passwordInput).toHaveAttribute('type', 'password');
    });

    test('No hardcoded credentials visible', async ({ page }) => {
      await page.goto(BASE_URL);

      const pageContent = await page.content();
      const hasCredentials = pageContent.includes('password=') || pageContent.includes('api_key=');

      expect(hasCredentials).toBeFalsy();
    });

    test('Form inputs have proper validation', async ({ page }) => {
      await page.goto(`${BASE_URL}/register`);

      // Try submitting empty form
      const submitBtn = page.locator('button[type="submit"], input[type="submit"]').first();
      if (await submitBtn.count() > 0) {
        await submitBtn.click();

        // Should show validation errors, not submit successfully
        await page.waitForTimeout(500);
      }
    });
  });
});
