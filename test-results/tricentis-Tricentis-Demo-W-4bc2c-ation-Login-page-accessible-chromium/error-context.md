# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: tricentis.spec.ts >> Tricentis Demo Web Shop - E-Commerce Suite >> 3. User Registration & Authentication >> Login page accessible
- Location: tests/e2e/tricentis.spec.ts:137:9

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('input[type="email"], input[name*="email"]')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('input[type="email"], input[name*="email"]')

```

```yaml
- link "Tricentis Demo Web Shop":
  - /url: /
  - img "Tricentis Demo Web Shop"
- list:
  - listitem:
    - link "Register":
      - /url: /register
  - listitem:
    - link "Log in":
      - /url: /login
  - listitem:
    - link "Shopping cart (0)":
      - /url: /cart
  - listitem:
    - link "Wishlist (0)":
      - /url: /wishlist
- status
- textbox: Search store
- button "Search"
- list:
  - listitem:
    - link "Books":
      - /url: /books
  - listitem:
    - link "Computers":
      - /url: /computers
  - listitem:
    - link "Electronics":
      - /url: /electronics
  - listitem:
    - link "Apparel & Shoes":
      - /url: /apparel-shoes
  - listitem:
    - link "Digital downloads":
      - /url: /digital-downloads
  - listitem:
    - link "Jewelry":
      - /url: /jewelry
  - listitem:
    - link "Gift Cards":
      - /url: /gift-cards
- strong: Categories
- list:
  - listitem:
    - link "Books":
      - /url: /books
  - listitem:
    - link "Computers":
      - /url: /computers
  - listitem:
    - link "Electronics":
      - /url: /electronics
  - listitem:
    - link "Apparel & Shoes":
      - /url: /apparel-shoes
  - listitem:
    - link "Digital downloads":
      - /url: /digital-downloads
  - listitem:
    - link "Jewelry":
      - /url: /jewelry
  - listitem:
    - link "Gift Cards":
      - /url: /gift-cards
- strong: Manufacturers
- list:
  - listitem:
    - link "Tricentis":
      - /url: /tricentis
- strong: Newsletter
- text: "Sign up for our newsletter:"
- textbox
- button "Subscribe"
- heading "Welcome, Please Sign In!" [level=1]
- strong: New Customer
- text: By creating an account on our website you will be able to shop faster, be up to date on an orders status, and keep track of the orders you have previously made.
- button "Register"
- strong: Returning Customer
- text: "Email:"
- textbox "Email:"
- text: "Password:"
- textbox "Password:"
- checkbox "Remember me?"
- text: Remember me?
- link "Forgot password?":
  - /url: /passwordrecovery
- button "Log in"
- heading "About login / registration" [level=2]
- paragraph: Put your login / registration information here. You can edit this in the admin site.
- heading "Information" [level=3]
- list:
  - listitem:
    - link "Sitemap":
      - /url: /sitemap
  - listitem:
    - link "Shipping & Returns":
      - /url: /shipping-returns
  - listitem:
    - link "Privacy Notice":
      - /url: /privacy-policy
  - listitem:
    - link "Conditions of Use":
      - /url: /conditions-of-use
  - listitem:
    - link "About us":
      - /url: /about-us
  - listitem:
    - link "Contact us":
      - /url: /contactus
- heading "Customer service" [level=3]
- list:
  - listitem:
    - link "Search":
      - /url: /search
  - listitem:
    - link "News":
      - /url: /news
  - listitem:
    - link "Blog":
      - /url: /blog
  - listitem:
    - link "Recently viewed products":
      - /url: /recentlyviewedproducts
  - listitem:
    - link "Compare products list":
      - /url: /compareproducts
  - listitem:
    - link "New products":
      - /url: /newproducts
- heading "My account" [level=3]
- list:
  - listitem:
    - link "My account":
      - /url: /customer/info
  - listitem:
    - link "Orders":
      - /url: /customer/orders
  - listitem:
    - link "Addresses":
      - /url: /customer/addresses
  - listitem:
    - link "Shopping cart":
      - /url: /cart
  - listitem:
    - link "Wishlist":
      - /url: /wishlist
- heading "Follow us" [level=3]
- list:
  - listitem:
    - link "Facebook":
      - /url: http://www.facebook.com/nopCommerce
  - listitem:
    - link "Twitter":
      - /url: https://twitter.com/nopCommerce
  - listitem:
    - link "RSS":
      - /url: /news/rss/1
  - listitem:
    - link "YouTube":
      - /url: http://www.youtube.com/user/nopCommerce
  - listitem:
    - link "Google+":
      - /url: https://plus.google.com/+nopcommerce
- text: Powered by
- link "nopCommerce":
  - /url: http://www.nopcommerce.com/
- text: Copyright © 2026 Tricentis Demo Web Shop. All rights reserved.
```

# Test source

```ts
  41  |       const searchInput = page.locator('input[placeholder*="Search"], input[name*="q"]');
  42  |       if (await searchInput.count() > 0) {
  43  |         await searchInput.fill('book');
  44  |         await page.keyboard.press('Enter');
  45  | 
  46  |         // Verify search results page loads
  47  |         await page.waitForLoadState('networkidle');
  48  |         await expect(page).toHaveURL(/.*search|.*product/i);
  49  |       }
  50  |     });
  51  |   });
  52  | 
  53  |   test.describe('2. Product Catalog & Filtering', () => {
  54  |     test('Products display with prices', async ({ page }) => {
  55  |       await page.goto(`${BASE_URL}/books`);
  56  | 
  57  |       const products = page.locator('[class*="product"]').first();
  58  |       await expect(products).toBeVisible();
  59  | 
  60  |       // Verify price is visible
  61  |       const price = page.locator('text=/\\$[0-9]+/').first();
  62  |       await expect(price).toBeVisible();
  63  |     });
  64  | 
  65  |     test('Product details page loads', async ({ page }) => {
  66  |       await page.goto(`${BASE_URL}/books`);
  67  | 
  68  |       // Click first product
  69  |       const firstProduct = page.locator('a[href*="/p/"]').first();
  70  |       if (await firstProduct.count() > 0) {
  71  |         await firstProduct.click();
  72  |         await page.waitForLoadState('networkidle');
  73  | 
  74  |         // Verify product page elements
  75  |         await expect(page.locator('text=/[0-9]+\\.[0-9]{2}/')).toBeVisible();
  76  |       }
  77  |     });
  78  | 
  79  |     test('Add to cart button is functional', async ({ page }) => {
  80  |       await page.goto(`${BASE_URL}/books`);
  81  | 
  82  |       // Find and click add to cart
  83  |       const addButton = page.locator('button, input[type="button"]').filter({ hasText: /add|cart/i }).first();
  84  |       if (await addButton.count() > 0) {
  85  |         await addButton.click();
  86  | 
  87  |         // Wait for confirmation or cart update
  88  |         await page.waitForTimeout(1000);
  89  |       }
  90  |     });
  91  |   });
  92  | 
  93  |   test.describe('3. User Registration & Authentication', () => {
  94  |     test('Registration form accessible', async ({ page }) => {
  95  |       await page.goto(BASE_URL);
  96  | 
  97  |       // Navigate to registration
  98  |       const registerLink = page.locator('a:has-text("Register")');
  99  |       if (await registerLink.count() > 0) {
  100 |         await registerLink.click();
  101 |         await page.waitForLoadState('networkidle');
  102 | 
  103 |         // Verify registration form
  104 |         await expect(page.locator('input[name*="FirstName"], input[placeholder*="First"]')).toBeVisible();
  105 |         await expect(page.locator('input[name*="Email"], input[placeholder*="Email"]')).toBeVisible();
  106 |         await expect(page.locator('input[name*="Password"], input[placeholder*="Password"]')).toBeVisible();
  107 |       }
  108 |     });
  109 | 
  110 |     test('User can register with valid data', async ({ page }) => {
  111 |       await page.goto(`${BASE_URL}/register`);
  112 | 
  113 |       // Fill registration form
  114 |       const firstNameInput = page.locator('input[name*="FirstName"], input[placeholder*="First"]');
  115 |       const lastNameInput = page.locator('input[name*="LastName"], input[placeholder*="Last"]');
  116 |       const emailInput = page.locator('input[name*="Email"], input[placeholder*="Email"]');
  117 |       const passwordInput = page.locator('input[name*="Password"][type="password"]').first();
  118 |       const confirmInput = page.locator('input[name*="ConfirmPassword"], input[placeholder*="Confirm"]');
  119 | 
  120 |       if (await firstNameInput.count() > 0) {
  121 |         await firstNameInput.fill(testUser.firstName);
  122 |         if (await lastNameInput.count() > 0) await lastNameInput.fill(testUser.lastName);
  123 |         await emailInput.fill(testUser.email);
  124 |         await passwordInput.fill(testUser.password);
  125 |         if (await confirmInput.count() > 0) await confirmInput.fill(testUser.password);
  126 | 
  127 |         // Submit form
  128 |         const submitButton = page.locator('button[type="submit"], input[type="submit"]').first();
  129 |         await submitButton.click();
  130 | 
  131 |         await page.waitForLoadState('networkidle');
  132 |         // Verify success (may be redirect or success message)
  133 |         await expect(page).toHaveURL(/.*register|.*login|.*dashboard/i);
  134 |       }
  135 |     });
  136 | 
  137 |     test('Login page accessible', async ({ page }) => {
  138 |       await page.goto(`${BASE_URL}/login`);
  139 | 
  140 |       // Verify login form elements
> 141 |       await expect(page.locator('input[type="email"], input[name*="email"]')).toBeVisible();
      |                                                                               ^ Error: expect(locator).toBeVisible() failed
  142 |       await expect(page.locator('input[type="password"]')).toBeVisible();
  143 |     });
  144 |   });
  145 | 
  146 |   test.describe('4. Shopping Cart Operations', () => {
  147 |     test('Shopping cart page loads', async ({ page }) => {
  148 |       await page.goto(`${BASE_URL}/cart`);
  149 | 
  150 |       await page.waitForLoadState('networkidle');
  151 |       await expect(page).toHaveURL(/.*cart/i);
  152 |     });
  153 | 
  154 |     test('Add item to cart and verify', async ({ page }) => {
  155 |       await page.goto(`${BASE_URL}/books`);
  156 | 
  157 |       // Click add to cart on first product
  158 |       const addBtn = page.locator('button, input[type="button"]').filter({ hasText: /add.*cart|add to.*cart/i }).first();
  159 | 
  160 |       if (await addBtn.count() > 0) {
  161 |         await addBtn.click();
  162 |         await page.waitForTimeout(1000);
  163 | 
  164 |         // Navigate to cart
  165 |         const cartLink = page.locator('a:has-text("Cart")');
  166 |         if (await cartLink.count() > 0) {
  167 |           await cartLink.click();
  168 |           await page.waitForLoadState('networkidle');
  169 | 
  170 |           // Verify item in cart
  171 |           await expect(page.locator('table, [role="table"]').first()).toBeVisible();
  172 |         }
  173 |       }
  174 |     });
  175 | 
  176 |     test('Update item quantity in cart', async ({ page }) => {
  177 |       await page.goto(`${BASE_URL}/cart`);
  178 | 
  179 |       // Find quantity input
  180 |       const qtyInput = page.locator('input[name*="itemQuantity"], input[type="number"]').first();
  181 |       if (await qtyInput.count() > 0) {
  182 |         await qtyInput.clear();
  183 |         await qtyInput.fill('2');
  184 | 
  185 |         // Click update
  186 |         const updateBtn = page.locator('button, input[type="button"]').filter({ hasText: /update/i }).first();
  187 |         if (await updateBtn.count() > 0) {
  188 |           await updateBtn.click();
  189 |           await page.waitForLoadState('networkidle');
  190 |         }
  191 |       }
  192 |     });
  193 | 
  194 |     test('Remove item from cart', async ({ page }) => {
  195 |       await page.goto(`${BASE_URL}/cart`);
  196 | 
  197 |       // Click remove/delete button
  198 |       const removeBtn = page.locator('button, input[type="button"]').filter({ hasText: /remove|delete/i }).first();
  199 |       if (await removeBtn.count() > 0) {
  200 |         await removeBtn.click();
  201 |         await page.waitForLoadState('networkidle');
  202 |       }
  203 |     });
  204 |   });
  205 | 
  206 |   test.describe('5. Checkout Process', () => {
  207 |     test('Checkout page accessible', async ({ page }) => {
  208 |       await page.goto(`${BASE_URL}/cart`);
  209 | 
  210 |       // Look for checkout button
  211 |       const checkoutBtn = page.locator('button, input[type="button"]').filter({ hasText: /checkout/i }).first();
  212 |       if (await checkoutBtn.count() > 0) {
  213 |         await expect(checkoutBtn).toBeVisible();
  214 |       }
  215 |     });
  216 | 
  217 |     test('Billing address form displays', async ({ page }) => {
  218 |       // Navigate to checkout
  219 |       await page.goto(`${BASE_URL}/checkout`);
  220 | 
  221 |       // Verify billing form elements
  222 |       const addressInput = page.locator('input[name*="Address"], input[placeholder*="Address"]');
  223 |       if (await addressInput.count() > 0) {
  224 |         await expect(addressInput.first()).toBeVisible();
  225 |       }
  226 |     });
  227 | 
  228 |     test('Shipping method selection works', async ({ page }) => {
  229 |       await page.goto(`${BASE_URL}/checkout`);
  230 | 
  231 |       // Look for shipping options
  232 |       const shippingOptions = page.locator('input[name*="shipping"], input[type="radio"]');
  233 |       if (await shippingOptions.count() > 0) {
  234 |         await shippingOptions.first().click();
  235 |         await expect(shippingOptions.first()).toBeChecked();
  236 |       }
  237 |     });
  238 | 
  239 |     test('Payment method selection available', async ({ page }) => {
  240 |       await page.goto(`${BASE_URL}/checkout`);
  241 | 
```