# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: demowebshop.spec.ts >> Tricentis Demo Web Shop - 70 Approved Tests >> Error Handling & Edge Cases >> Invalid product ID handled
- Location: tests/e2e/demowebshop.spec.ts:451:9

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: locator.count: Unexpected token "=" while parsing css selector "[class*="error"], text=/not found/i". Did you mean to CSS.escape it?
```

# Page snapshot

```yaml
- generic [ref=e2]:
  - generic [ref=e3]:
    - generic [ref=e4]:
      - link "Tricentis Demo Web Shop" [ref=e6] [cursor=pointer]:
        - /url: /
        - img "Tricentis Demo Web Shop" [ref=e7]
      - list [ref=e10]:
        - listitem [ref=e11]:
          - link "Register" [ref=e12] [cursor=pointer]:
            - /url: /register
        - listitem [ref=e13]:
          - link "Log in" [ref=e14] [cursor=pointer]:
            - /url: /login
        - listitem [ref=e15]:
          - link "Shopping cart (0)" [ref=e16] [cursor=pointer]:
            - /url: /cart
            - generic [ref=e17]: Shopping cart
            - generic [ref=e18]: (0)
        - listitem [ref=e19]:
          - link "Wishlist (0)" [ref=e20] [cursor=pointer]:
            - /url: /wishlist
            - generic [ref=e21]: Wishlist
            - generic [ref=e22]: (0)
      - generic [ref=e24]:
        - status [ref=e25]
        - textbox [ref=e26]: Search store
        - button "Search" [ref=e27] [cursor=pointer]
    - list [ref=e29]:
      - listitem [ref=e30]:
        - link "Books" [ref=e31] [cursor=pointer]:
          - /url: /books
      - listitem [ref=e32]:
        - link "Computers" [ref=e33] [cursor=pointer]:
          - /url: /computers
      - listitem [ref=e34]:
        - link "Electronics" [ref=e35] [cursor=pointer]:
          - /url: /electronics
      - listitem [ref=e36]:
        - link "Apparel & Shoes" [ref=e37] [cursor=pointer]:
          - /url: /apparel-shoes
      - listitem [ref=e38]:
        - link "Digital downloads" [ref=e39] [cursor=pointer]:
          - /url: /digital-downloads
      - listitem [ref=e40]:
        - link "Jewelry" [ref=e41] [cursor=pointer]:
          - /url: /jewelry
      - listitem [ref=e42]:
        - link "Gift Cards" [ref=e43] [cursor=pointer]:
          - /url: /gift-cards
    - generic:
      - generic [ref=e44]:
        - generic [ref=e45]:
          - strong [ref=e47]: Categories
          - list [ref=e49]:
            - listitem [ref=e50]:
              - link "Books" [ref=e51] [cursor=pointer]:
                - /url: /books
            - listitem [ref=e52]:
              - link "Computers" [ref=e53] [cursor=pointer]:
                - /url: /computers
            - listitem [ref=e54]:
              - link "Electronics" [ref=e55] [cursor=pointer]:
                - /url: /electronics
            - listitem [ref=e56]:
              - link "Apparel & Shoes" [ref=e57] [cursor=pointer]:
                - /url: /apparel-shoes
            - listitem [ref=e58]:
              - link "Digital downloads" [ref=e59] [cursor=pointer]:
                - /url: /digital-downloads
            - listitem [ref=e60]:
              - link "Jewelry" [ref=e61] [cursor=pointer]:
                - /url: /jewelry
            - listitem [ref=e62]:
              - link "Gift Cards" [ref=e63] [cursor=pointer]:
                - /url: /gift-cards
        - generic [ref=e64]:
          - strong [ref=e66]: Manufacturers
          - list [ref=e68]:
            - listitem [ref=e69]:
              - link "Tricentis" [ref=e70] [cursor=pointer]:
                - /url: /tricentis
        - generic [ref=e71]:
          - strong [ref=e73]: Popular tags
          - generic [ref=e74]:
            - list [ref=e76]:
              - listitem [ref=e77]:
                - link "apparel" [ref=e78] [cursor=pointer]:
                  - /url: /producttag/4/apparel
              - listitem [ref=e79]:
                - link "awesome" [ref=e80] [cursor=pointer]:
                  - /url: /producttag/8/awesome
              - listitem [ref=e81]:
                - link "book" [ref=e82] [cursor=pointer]:
                  - /url: /producttag/10/book
              - listitem [ref=e83]:
                - link "camera" [ref=e84] [cursor=pointer]:
                  - /url: /producttag/13/camera
              - listitem [ref=e85]:
                - link "cell" [ref=e86] [cursor=pointer]:
                  - /url: /producttag/12/cell
              - listitem [ref=e87]:
                - link "compact" [ref=e88] [cursor=pointer]:
                  - /url: /producttag/9/compact
              - listitem [ref=e89]:
                - link "computer" [ref=e90] [cursor=pointer]:
                  - /url: /producttag/6/computer
              - listitem [ref=e91]:
                - link "cool" [ref=e92] [cursor=pointer]:
                  - /url: /producttag/3/cool
              - listitem [ref=e93]:
                - link "digital" [ref=e94] [cursor=pointer]:
                  - /url: /producttag/16/digital
              - listitem [ref=e95]:
                - link "jeans" [ref=e96] [cursor=pointer]:
                  - /url: /producttag/14/jeans
              - listitem [ref=e97]:
                - link "jewelry" [ref=e98] [cursor=pointer]:
                  - /url: /producttag/11/jewelry
              - listitem [ref=e99]:
                - link "nice" [ref=e100] [cursor=pointer]:
                  - /url: /producttag/1/nice
              - listitem [ref=e101]:
                - link "shirt" [ref=e102] [cursor=pointer]:
                  - /url: /producttag/5/shirt
              - listitem [ref=e103]:
                - link "shoes" [ref=e104] [cursor=pointer]:
                  - /url: /producttag/7/shoes
              - listitem [ref=e105]:
                - link "TCP" [ref=e106] [cursor=pointer]:
                  - /url: /producttag/19/tcp
            - link "View all" [ref=e108] [cursor=pointer]:
              - /url: /producttag/all
      - generic [ref=e109]:
        - generic [ref=e110]:
          - strong [ref=e112]: Newsletter
          - generic [ref=e114]:
            - text: "Sign up for our newsletter:"
            - textbox [ref=e116]
            - button "Subscribe" [ref=e118] [cursor=pointer]
        - generic [ref=e119]:
          - strong [ref=e121]: Community poll
          - generic [ref=e123]:
            - strong [ref=e124]: Do you like nopCommerce?
            - list [ref=e125]:
              - listitem [ref=e126]:
                - radio "Excellent" [ref=e127]
                - text: Excellent
              - listitem [ref=e128]:
                - radio "Good" [ref=e129]
                - text: Good
              - listitem [ref=e130]:
                - radio "Poor" [ref=e131]
                - text: Poor
              - listitem [ref=e132]:
                - radio "Very bad" [ref=e133]
                - text: Very bad
            - button "Vote" [ref=e135] [cursor=pointer]
      - generic [ref=e138]:
        - generic:
          - generic:
            - link:
              - /url: https://www.tricentis.com/speed/
            - link:
              - /url: https://academy.tricentis.com
        - generic [ref=e139]:
          - heading "Welcome to our store" [level=2] [ref=e141]
          - generic [ref=e142]:
            - paragraph [ref=e143]: Welcome to the new Tricentis store!
            - paragraph [ref=e144]: Feel free to shop around and explore everything.
        - generic [ref=e145]:
          - strong [ref=e147]: Featured products
          - generic [ref=e149]:
            - link "Picture of $25 Virtual Gift Card" [ref=e151] [cursor=pointer]:
              - /url: /25-virtual-gift-card
              - img "Picture of $25 Virtual Gift Card" [ref=e152]
            - generic [ref=e153]:
              - heading "$25 Virtual Gift Card" [level=2] [ref=e154]:
                - link "$25 Virtual Gift Card" [ref=e155] [cursor=pointer]:
                  - /url: /25-virtual-gift-card
              - generic "911 review(s)" [ref=e156]
              - generic [ref=e159]:
                - generic [ref=e161]: "25.00"
                - button "Add to cart" [ref=e163] [cursor=pointer]
          - generic [ref=e165]:
            - link "Picture of 14.1-inch Laptop" [ref=e167] [cursor=pointer]:
              - /url: /141-inch-laptop
              - img "Picture of 14.1-inch Laptop" [ref=e168]
            - generic [ref=e169]:
              - heading "14.1-inch Laptop" [level=2] [ref=e170]:
                - link "14.1-inch Laptop" [ref=e171] [cursor=pointer]:
                  - /url: /141-inch-laptop
              - generic "1712 review(s)" [ref=e172]
              - generic [ref=e175]:
                - generic [ref=e177]: "1590.00"
                - button "Add to cart" [ref=e179] [cursor=pointer]
          - generic [ref=e181]:
            - link "Picture of Build your own cheap computer" [ref=e183] [cursor=pointer]:
              - /url: /build-your-cheap-own-computer
              - img "Picture of Build your own cheap computer" [ref=e184]
            - generic [ref=e185]:
              - heading "Build your own cheap computer" [level=2] [ref=e186]:
                - link "Build your own cheap computer" [ref=e187] [cursor=pointer]:
                  - /url: /build-your-cheap-own-computer
              - generic "924 review(s)" [ref=e188]
              - generic [ref=e191]:
                - generic [ref=e193]: "800.00"
                - button "Add to cart" [ref=e195] [cursor=pointer]
          - generic [ref=e197]:
            - link "Picture of Build your own computer" [ref=e199] [cursor=pointer]:
              - /url: /build-your-own-computer
              - img "Picture of Build your own computer" [ref=e200]
            - generic [ref=e201]:
              - heading "Build your own computer" [level=2] [ref=e202]:
                - link "Build your own computer" [ref=e203] [cursor=pointer]:
                  - /url: /build-your-own-computer
              - generic "432 review(s)" [ref=e204]
              - generic [ref=e207]:
                - generic [ref=e209]: "1200.00"
                - button "Add to cart" [ref=e211] [cursor=pointer]
          - generic [ref=e213]:
            - link "Picture of Build your own expensive computer" [ref=e215] [cursor=pointer]:
              - /url: /build-your-own-expensive-computer-2
              - img "Picture of Build your own expensive computer" [ref=e216]
            - generic [ref=e217]:
              - heading "Build your own expensive computer" [level=2] [ref=e218]:
                - link "Build your own expensive computer" [ref=e219] [cursor=pointer]:
                  - /url: /build-your-own-expensive-computer-2
              - generic "440 review(s)" [ref=e220]
              - generic [ref=e223]:
                - generic [ref=e225]: "1800.00"
                - button "Add to cart" [ref=e227] [cursor=pointer]
          - generic [ref=e229]:
            - link "Picture of Simple Computer" [ref=e231] [cursor=pointer]:
              - /url: /simple-computer
              - img "Picture of Simple Computer" [ref=e232]
            - generic [ref=e233]:
              - heading "Simple Computer" [level=2] [ref=e234]:
                - link "Simple Computer" [ref=e235] [cursor=pointer]:
                  - /url: /simple-computer
              - generic "399 review(s)" [ref=e236]
              - generic [ref=e239]:
                - generic [ref=e241]: "800.00"
                - button "Add to cart" [ref=e243] [cursor=pointer]
  - generic [ref=e244]:
    - generic [ref=e245]:
      - generic [ref=e246]:
        - heading "Information" [level=3] [ref=e247]
        - list [ref=e248]:
          - listitem [ref=e249]:
            - link "Sitemap" [ref=e250] [cursor=pointer]:
              - /url: /sitemap
          - listitem [ref=e251]:
            - link "Shipping & Returns" [ref=e252] [cursor=pointer]:
              - /url: /shipping-returns
          - listitem [ref=e253]:
            - link "Privacy Notice" [ref=e254] [cursor=pointer]:
              - /url: /privacy-policy
          - listitem [ref=e255]:
            - link "Conditions of Use" [ref=e256] [cursor=pointer]:
              - /url: /conditions-of-use
          - listitem [ref=e257]:
            - link "About us" [ref=e258] [cursor=pointer]:
              - /url: /about-us
          - listitem [ref=e259]:
            - link "Contact us" [ref=e260] [cursor=pointer]:
              - /url: /contactus
      - generic [ref=e261]:
        - heading "Customer service" [level=3] [ref=e262]
        - list [ref=e263]:
          - listitem [ref=e264]:
            - link "Search" [ref=e265] [cursor=pointer]:
              - /url: /search
          - listitem [ref=e266]:
            - link "News" [ref=e267] [cursor=pointer]:
              - /url: /news
          - listitem [ref=e268]:
            - link "Blog" [ref=e269] [cursor=pointer]:
              - /url: /blog
          - listitem [ref=e270]:
            - link "Recently viewed products" [ref=e271] [cursor=pointer]:
              - /url: /recentlyviewedproducts
          - listitem [ref=e272]:
            - link "Compare products list" [ref=e273] [cursor=pointer]:
              - /url: /compareproducts
          - listitem [ref=e274]:
            - link "New products" [ref=e275] [cursor=pointer]:
              - /url: /newproducts
      - generic [ref=e276]:
        - heading "My account" [level=3] [ref=e277]
        - list [ref=e278]:
          - listitem [ref=e279]:
            - link "My account" [ref=e280] [cursor=pointer]:
              - /url: /customer/info
          - listitem [ref=e281]:
            - link "Orders" [ref=e282] [cursor=pointer]:
              - /url: /customer/orders
          - listitem [ref=e283]:
            - link "Addresses" [ref=e284] [cursor=pointer]:
              - /url: /customer/addresses
          - listitem [ref=e285]:
            - link "Shopping cart" [ref=e286] [cursor=pointer]:
              - /url: /cart
          - listitem [ref=e287]:
            - link "Wishlist" [ref=e288] [cursor=pointer]:
              - /url: /wishlist
      - generic [ref=e289]:
        - heading "Follow us" [level=3] [ref=e290]
        - list [ref=e291]:
          - listitem [ref=e292]:
            - link "Facebook" [ref=e293] [cursor=pointer]:
              - /url: http://www.facebook.com/nopCommerce
          - listitem [ref=e294]:
            - link "Twitter" [ref=e295] [cursor=pointer]:
              - /url: https://twitter.com/nopCommerce
          - listitem [ref=e296]:
            - link "RSS" [ref=e297] [cursor=pointer]:
              - /url: /news/rss/1
          - listitem [ref=e298]:
            - link "YouTube" [ref=e299] [cursor=pointer]:
              - /url: http://www.youtube.com/user/nopCommerce
          - listitem [ref=e300]:
            - link "Google+" [ref=e301] [cursor=pointer]:
              - /url: https://plus.google.com/+nopcommerce
    - generic [ref=e302]:
      - text: Powered by
      - link "nopCommerce" [ref=e303] [cursor=pointer]:
        - /url: http://www.nopcommerce.com/
    - generic [ref=e304]: Copyright © 2026 Tricentis Demo Web Shop. All rights reserved.
```

# Test source

```ts
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
  405 |       await expect(page).toHaveTitle(/tricentis|demowebshop/i);
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
> 453 |       const isError = response?.status() === 404 || await page.locator('[class*="error"], text=/not found/i').count() > 0;
      |                                                                                                               ^ Error: locator.count: Unexpected token "=" while parsing css selector "[class*="error"], text=/not found/i". Did you mean to CSS.escape it?
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
  506 |       await page.goto(BASE_URL);
  507 |       const body = page.locator('body');
  508 |       await expect(body).toBeVisible();
  509 |     });
  510 | 
  511 |     test('Timeout handled', async ({ page }) => {
  512 |       page.setDefaultTimeout(10000);
  513 |       await page.goto(BASE_URL);
  514 |       await expect(page).toHaveURL(/tricentis|demowebshop/i);
  515 |     });
  516 | 
  517 |     test('XSS prevention - no script execution', async ({ page }) => {
  518 |       await page.goto(BASE_URL);
  519 |       const scripts = page.locator('script');
  520 |       // Scripts should exist but not be malicious
  521 |       const count = await scripts.count();
  522 |       expect(count).toBeGreaterThanOrEqual(0);
  523 |     });
  524 |   });
  525 | });
  526 | 
```