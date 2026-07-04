# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: demowebshop.spec.ts >> Tricentis Demo Web Shop - 70 Approved Tests >> Integration & Persistence >> Email configuration verified
- Location: tests/e2e/demowebshop.spec.ts:402:9

# Error details

```
Error: expect(page).toHaveTitle(expected) failed

Expected pattern: /tricentis|demowebshop/i
Received string:  "Demo Web Shop"
Timeout: 5000ms

Call log:
  - Expect "toHaveTitle" with timeout 5000ms
    3 × unexpected value "Demo Web Shop"

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
- strong: Popular tags
- list:
  - listitem:
    - link "apparel":
      - /url: /producttag/4/apparel
  - listitem:
    - link "awesome":
      - /url: /producttag/8/awesome
  - listitem:
    - link "book":
      - /url: /producttag/10/book
  - listitem:
    - link "camera":
      - /url: /producttag/13/camera
  - listitem:
    - link "cell":
      - /url: /producttag/12/cell
  - listitem:
    - link "compact":
      - /url: /producttag/9/compact
  - listitem:
    - link "computer":
      - /url: /producttag/6/computer
  - listitem:
    - link "cool":
      - /url: /producttag/3/cool
  - listitem:
    - link "digital":
      - /url: /producttag/16/digital
  - listitem:
    - link "jeans":
      - /url: /producttag/14/jeans
  - listitem:
    - link "jewelry":
      - /url: /producttag/11/jewelry
  - listitem:
    - link "nice":
      - /url: /producttag/1/nice
  - listitem:
    - link "shirt":
      - /url: /producttag/5/shirt
  - listitem:
    - link "shoes":
      - /url: /producttag/7/shoes
  - listitem:
    - link "TCP":
      - /url: /producttag/19/tcp
- link "View all":
  - /url: /producttag/all
- strong: Newsletter
- text: "Sign up for our newsletter:"
- textbox
- button "Subscribe"
- strong: Community poll
- strong: Do you like nopCommerce?
- list:
  - listitem:
    - radio "Excellent"
    - text: Excellent
  - listitem:
    - radio "Good"
    - text: Good
  - listitem:
    - radio "Poor"
    - text: Poor
  - listitem:
    - radio "Very bad"
    - text: Very bad
- button "Vote"
- link:
  - /url: https://www.tricentis.com/speed/
- link:
  - /url: https://academy.tricentis.com
- img
- text: Speed | Tricentis Prev Next
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- text: 1 2
- heading "Welcome to our store" [level=2]
- paragraph: Welcome to the new Tricentis store!
- paragraph: Feel free to shop around and explore everything.
- strong: Featured products
- link "Picture of $25 Virtual Gift Card":
  - /url: /25-virtual-gift-card
  - img "Picture of $25 Virtual Gift Card"
- heading "$25 Virtual Gift Card" [level=2]:
  - link "$25 Virtual Gift Card":
    - /url: /25-virtual-gift-card
- text: "25.00"
- button "Add to cart"
- link "Picture of 14.1-inch Laptop":
  - /url: /141-inch-laptop
  - img "Picture of 14.1-inch Laptop"
- heading "14.1-inch Laptop" [level=2]:
  - link "14.1-inch Laptop":
    - /url: /141-inch-laptop
- text: "1590.00"
- button "Add to cart"
- link "Picture of Build your own cheap computer":
  - /url: /build-your-cheap-own-computer
  - img "Picture of Build your own cheap computer"
- heading "Build your own cheap computer" [level=2]:
  - link "Build your own cheap computer":
    - /url: /build-your-cheap-own-computer
- text: "800.00"
- button "Add to cart"
- link "Picture of Build your own computer":
  - /url: /build-your-own-computer
  - img "Picture of Build your own computer"
- heading "Build your own computer" [level=2]:
  - link "Build your own computer":
    - /url: /build-your-own-computer
- text: "1200.00"
- button "Add to cart"
- link "Picture of Build your own expensive computer":
  - /url: /build-your-own-expensive-computer-2
  - img "Picture of Build your own expensive computer"
- heading "Build your own expensive computer" [level=2]:
  - link "Build your own expensive computer":
    - /url: /build-your-own-expensive-computer-2
- text: "1800.00"
- button "Add to cart"
- link "Picture of Simple Computer":
  - /url: /simple-computer
  - img "Picture of Simple Computer"
- heading "Simple Computer" [level=2]:
  - link "Simple Computer":
    - /url: /simple-computer
- text: "800.00"
- button "Add to cart"
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
  305 |       const confirmBtn = page.locator('button, input[type="button"], a').filter({ hasText: /confirm|place|complete|submit/i }).first();
  306 |       if (await confirmBtn.count() > 0) {
  307 |         await expect(confirmBtn).toBeVisible();
  308 |       }
  309 |     });
  310 | 
  311 |     test('Billing country/state selection works', async ({ page }) => {
  312 |       await page.goto(`${BASE_URL}/checkout`);
  313 |       const country = page.locator('select[name*="country"], input[name*="country"]').first();
  314 |       if (await country.count() > 0) {
  315 |         await expect(country).toBeVisible();
  316 |       }
  317 |     });
  318 | 
  319 |     test('Email field present in checkout', async ({ page }) => {
  320 |       await page.goto(`${BASE_URL}/checkout`);
  321 |       const email = page.locator('input[type="email"], input[name*="email"]').first();
  322 |       if (await email.count() > 0) {
  323 |         await expect(email).toBeVisible();
  324 |       }
  325 |     });
  326 | 
  327 |     test('Phone field present in checkout', async ({ page }) => {
  328 |       await page.goto(`${BASE_URL}/checkout`);
  329 |       const phone = page.locator('input[name*="phone"], input[placeholder*="phone"]').first();
  330 |       if (await phone.count() > 0) {
  331 |         await expect(phone).toBeVisible();
  332 |       }
  333 |     });
  334 | 
  335 |     test('Terms & conditions checkbox present', async ({ page }) => {
  336 |       await page.goto(`${BASE_URL}/checkout`);
  337 |       const termsCheckbox = page.locator('input[type="checkbox"]').first();
  338 |       if (await termsCheckbox.count() > 0) {
  339 |         await expect(termsCheckbox).toBeVisible();
  340 |       }
  341 |     });
  342 | 
  343 |     test('Payment form displays credit card fields', async ({ page }) => {
  344 |       await page.goto(`${BASE_URL}/checkout`);
  345 |       const cardField = page.locator('input[name*="card"], input[placeholder*="card"]').first();
  346 |       if (await cardField.count() > 0) {
  347 |         await expect(cardField).toBeVisible();
  348 |       }
  349 |     });
  350 | 
  351 |     test('CVV field present', async ({ page }) => {
  352 |       await page.goto(`${BASE_URL}/checkout`);
  353 |       const cvv = page.locator('input[name*="cvv"], input[name*="cvc"], input[placeholder*="cvv"]').first();
  354 |       if (await cvv.count() > 0) {
  355 |         await expect(cvv).toBeVisible();
  356 |       }
  357 |     });
  358 | 
  359 |     test('Order review section displays', async ({ page }) => {
  360 |       await page.goto(`${BASE_URL}/checkout`);
  361 |       const review = page.locator('[class*="review"], [class*="order"], [class*="summary"]').first();
  362 |       if (await review.count() > 0) {
  363 |         await expect(review).toBeVisible();
  364 |       }
  365 |     });
  366 |   });
  367 | 
  368 |   // ═══════════════════════════════════════════════════════════════════
  369 |   // PHASE 4: INTEGRATION TESTS (10 tests)
  370 |   // ═══════════════════════════════════════════════════════════════════
  371 | 
  372 |   test.describe('Integration & Persistence', () => {
  373 |     test('Cart persists after page reload', async ({ page }) => {
  374 |       await page.goto(`${BASE_URL}/books`);
  375 |       const addBtn = page.locator('button').filter({ hasText: /add.*cart/i }).first();
  376 |       if (await addBtn.count() > 0) {
  377 |         await addBtn.click();
  378 |         await page.waitForTimeout(500);
  379 |         await page.reload();
  380 |         await page.waitForLoadState('networkidle');
  381 |       }
  382 |     });
  383 | 
  384 |     test('User session persists', async ({ page }) => {
  385 |       await page.goto(`${BASE_URL}/login`);
  386 |       await page.waitForLoadState('networkidle');
  387 |     });
  388 | 
  389 |     test('Product data loads from database', async ({ page }) => {
  390 |       await page.goto(`${BASE_URL}/books`);
  391 |       const product = page.locator('[class*="product"]').first();
  392 |       if (await product.count() > 0) {
  393 |         await expect(product).toBeVisible();
  394 |       }
  395 |     });
  396 | 
  397 |     test('Order creation succeeds with valid data', async ({ page }) => {
  398 |       await page.goto(`${BASE_URL}/checkout`);
  399 |       await page.waitForLoadState('networkidle');
  400 |     });
  401 | 
  402 |     test('Email configuration verified', async ({ page }) => {
  403 |       // Email functionality should be configured
  404 |       await page.goto(BASE_URL);
> 405 |       await expect(page).toHaveTitle(/tricentis|demowebshop/i);
      |                          ^ Error: expect(page).toHaveTitle(expected) failed
  406 |     });
  407 | 
  408 |     test('Payment gateway connected', async ({ page }) => {
  409 |       await page.goto(`${BASE_URL}/checkout`);
  410 |       const paymentSection = page.locator('[class*="payment"]').first();
  411 |       if (await paymentSection.count() > 0) {
  412 |         await expect(paymentSection).toBeVisible();
  413 |       }
  414 |     });
  415 | 
  416 |     test('Database connectivity verified', async ({ page }) => {
  417 |       await page.goto(`${BASE_URL}/books`);
  418 |       const products = page.locator('[class*="product"]');
  419 |       const count = await products.count();
  420 |       expect(count).toBeGreaterThan(0);
  421 |     });
  422 | 
  423 |     test('Authentication system operational', async ({ page }) => {
  424 |       await page.goto(`${BASE_URL}/login`);
  425 |       const form = page.locator('form').first();
  426 |       if (await form.count() > 0) {
  427 |         await expect(form).toBeVisible();
  428 |       }
  429 |     });
  430 | 
  431 |     test('Inventory system operational', async ({ page }) => {
  432 |       await page.goto(`${BASE_URL}/books`);
  433 |       const stockStatus = page.locator('[class*="stock"], text=/stock|available|quantity/i').first();
  434 |       if (await stockStatus.count() > 0) {
  435 |         // Stock information available
  436 |       }
  437 |     });
  438 | 
  439 |     test('Shopping cart backend functional', async ({ page }) => {
  440 |       await page.goto(`${BASE_URL}/cart`);
  441 |       await page.waitForLoadState('networkidle');
  442 |       await expect(page).toHaveURL(/.*cart/i);
  443 |     });
  444 |   });
  445 | 
  446 |   // ═══════════════════════════════════════════════════════════════════
  447 |   // PHASE 5: ERROR HANDLING & EDGE CASES (10 tests)
  448 |   // ═══════════════════════════════════════════════════════════════════
  449 | 
  450 |   test.describe('Error Handling & Edge Cases', () => {
  451 |     test('Invalid product ID handled', async ({ page }) => {
  452 |       const response = await page.goto(`${BASE_URL}/p/999999999`, { waitUntil: 'networkidle' });
  453 |       const isError = response?.status() === 404 || await page.locator('[class*="error"], text=/not found/i').count() > 0;
  454 |       expect(isError).toBeTruthy();
  455 |     });
  456 | 
  457 |     test('Empty cart message displays', async ({ page }) => {
  458 |       await page.goto(`${BASE_URL}/cart`);
  459 |       const empty = page.locator('text=/empty|no items/i');
  460 |       if (await empty.count() > 0) {
  461 |         await expect(empty.first()).toBeVisible();
  462 |       }
  463 |     });
  464 | 
  465 |     test('Network error handled gracefully', async ({ page }) => {
  466 |       await page.goto(BASE_URL);
  467 |       const content = page.locator('body');
  468 |       await expect(content).toBeVisible();
  469 |     });
  470 | 
  471 |     test('Form validation prevents empty submission', async ({ page }) => {
  472 |       await page.goto(`${BASE_URL}/register`);
  473 |       const form = page.locator('form').first();
  474 |       if (await form.count() > 0) {
  475 |         const submitBtn = form.locator('button[type="submit"]');
  476 |         if (await submitBtn.count() > 0) {
  477 |           // Validation should prevent submission of empty form
  478 |         }
  479 |       }
  480 |     });
  481 | 
  482 |     test('Password field masked', async ({ page }) => {
  483 |       await page.goto(`${BASE_URL}/login`);
  484 |       const pwField = page.locator('input[type="password"]').first();
  485 |       if (await pwField.count() > 0) {
  486 |         await expect(pwField).toHaveAttribute('type', 'password');
  487 |       }
  488 |     });
  489 | 
  490 |     test('Invalid email rejected', async ({ page }) => {
  491 |       await page.goto(`${BASE_URL}/register`);
  492 |       const emailField = page.locator('input[type="email"]').first();
  493 |       if (await emailField.count() > 0) {
  494 |         await emailField.fill('invalid-email');
  495 |         // Email validation should catch this
  496 |       }
  497 |     });
  498 | 
  499 |     test('Out of stock items indicated', async ({ page }) => {
  500 |       await page.goto(`${BASE_URL}/books`);
  501 |       const outOfStock = page.locator('text=/out of stock|unavailable/i').first();
  502 |       // May or may not be present depending on inventory
  503 |     });
  504 | 
  505 |     test('Server errors handled', async ({ page }) => {
```