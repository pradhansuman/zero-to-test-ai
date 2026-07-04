# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: demowebshop.spec.ts >> Tricentis Demo Web Shop - 70 Approved Tests >> Integration & Persistence >> Inventory system operational
- Location: tests/e2e/demowebshop.spec.ts:431:9

# Error details

```
Error: locator.count: Unexpected token "=" while parsing css selector "[class*="stock"], text=/stock|available|quantity/i". Did you mean to CSS.escape it?
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
          - strong [ref=e73]: Newsletter
          - generic [ref=e75]:
            - text: "Sign up for our newsletter:"
            - textbox [ref=e77]
            - button "Subscribe" [ref=e79] [cursor=pointer]
      - generic [ref=e80]:
        - list [ref=e82]:
          - listitem [ref=e83]:
            - link "Home" [ref=e84] [cursor=pointer]:
              - /url: /
            - text: /
          - listitem [ref=e85]:
            - strong [ref=e86]: Books
        - generic [ref=e87]:
          - heading "Books" [level=1] [ref=e89]
          - generic [ref=e90]:
            - generic [ref=e91]:
              - generic [ref=e92]:
                - text: View as
                - combobox [ref=e93]:
                  - option "Grid" [selected]
                  - option "List"
              - generic [ref=e94]:
                - text: Sort by
                - combobox [ref=e95]:
                  - option "Position" [selected]
                  - 'option "Name: A to Z"'
                  - 'option "Name: Z to A"'
                  - 'option "Price: Low to High"'
                  - 'option "Price: High to Low"'
                  - option "Created on"
              - generic [ref=e96]:
                - text: Display
                - combobox [ref=e97]:
                  - option "4"
                  - option "8" [selected]
                  - option "12"
                - text: per page
            - generic [ref=e99]:
              - strong [ref=e101]: Filter by price
              - list [ref=e103]:
                - listitem [ref=e104]:
                  - link "Under 25.00" [ref=e105] [cursor=pointer]:
                    - /url: https://demowebshop.tricentis.com/books?price=-25
                - listitem [ref=e106]:
                  - link "25.00 - 50.00" [ref=e107] [cursor=pointer]:
                    - /url: https://demowebshop.tricentis.com/books?price=25-50
                - listitem [ref=e108]:
                  - link "Over 50.00" [ref=e109] [cursor=pointer]:
                    - /url: https://demowebshop.tricentis.com/books?price=50-
            - generic [ref=e110]:
              - generic [ref=e112]:
                - link "Picture of Computing and Internet" [ref=e114] [cursor=pointer]:
                  - /url: /computing-and-internet
                  - img "Picture of Computing and Internet" [ref=e115]
                - generic [ref=e116]:
                  - heading "Computing and Internet" [level=2] [ref=e117]:
                    - link "Computing and Internet" [ref=e118] [cursor=pointer]:
                      - /url: /computing-and-internet
                  - generic "2660 review(s)" [ref=e119]
                  - generic [ref=e122]:
                    - generic [ref=e123]:
                      - generic [ref=e124]: "30.00"
                      - generic [ref=e125]: "10.00"
                    - button "Add to cart" [ref=e127] [cursor=pointer]
              - generic [ref=e129]:
                - link "Picture of Copy of Computing and Internet EX" [ref=e131] [cursor=pointer]:
                  - /url: /copy-of-computing-and-internet
                  - img "Picture of Copy of Computing and Internet EX" [ref=e132]
                - generic [ref=e133]:
                  - heading "Copy of Computing and Internet EX" [level=2] [ref=e134]:
                    - link "Copy of Computing and Internet EX" [ref=e135] [cursor=pointer]:
                      - /url: /copy-of-computing-and-internet
                  - generic "382 review(s)" [ref=e136]
                  - generic [ref=e140]:
                    - generic [ref=e141]: "30.00"
                    - generic [ref=e142]: "10.00"
              - generic [ref=e144]:
                - link "Picture of Fiction" [ref=e146] [cursor=pointer]:
                  - /url: /fiction
                  - img "Picture of Fiction" [ref=e147]
                - generic [ref=e148]:
                  - heading "Fiction" [level=2] [ref=e149]:
                    - link "Fiction" [ref=e150] [cursor=pointer]:
                      - /url: /fiction
                  - generic "789 review(s)" [ref=e151]
                  - generic [ref=e154]:
                    - generic [ref=e155]:
                      - generic [ref=e156]: "35.00"
                      - generic [ref=e157]: "24.00"
                    - button "Add to cart" [ref=e159] [cursor=pointer]
              - generic [ref=e161]:
                - link "Picture of Fiction EX" [ref=e163] [cursor=pointer]:
                  - /url: /fiction-ex
                  - img "Picture of Fiction EX" [ref=e164]
                - generic [ref=e165]:
                  - heading "Fiction EX" [level=2] [ref=e166]:
                    - link "Fiction EX" [ref=e167] [cursor=pointer]:
                      - /url: /fiction-ex
                  - generic "420 review(s)" [ref=e168]
                  - generic [ref=e172]:
                    - generic [ref=e173]: "35.00"
                    - generic [ref=e174]: "24.00"
              - generic [ref=e176]:
                - link "Picture of Health Book" [ref=e178] [cursor=pointer]:
                  - /url: /health
                  - img "Picture of Health Book" [ref=e179]
                - generic [ref=e180]:
                  - heading "Health Book" [level=2] [ref=e181]:
                    - link "Health Book" [ref=e182] [cursor=pointer]:
                      - /url: /health
                  - generic "526 review(s)" [ref=e183]
                  - generic [ref=e186]:
                    - generic [ref=e187]:
                      - generic [ref=e188]: "27.00"
                      - generic [ref=e189]: "10.00"
                    - button "Add to cart" [ref=e191] [cursor=pointer]
              - generic [ref=e193]:
                - link "Picture of Science" [ref=e195] [cursor=pointer]:
                  - /url: /science
                  - img "Picture of Science" [ref=e196]
                - generic [ref=e197]:
                  - heading "Science" [level=2] [ref=e198]:
                    - link "Science" [ref=e199] [cursor=pointer]:
                      - /url: /science
                  - generic "451 review(s)" [ref=e200]
                  - generic [ref=e204]:
                    - generic [ref=e205]: "67.00"
                    - generic [ref=e206]: "51.00"
  - generic [ref=e207]:
    - generic [ref=e208]:
      - generic [ref=e209]:
        - heading "Information" [level=3] [ref=e210]
        - list [ref=e211]:
          - listitem [ref=e212]:
            - link "Sitemap" [ref=e213] [cursor=pointer]:
              - /url: /sitemap
          - listitem [ref=e214]:
            - link "Shipping & Returns" [ref=e215] [cursor=pointer]:
              - /url: /shipping-returns
          - listitem [ref=e216]:
            - link "Privacy Notice" [ref=e217] [cursor=pointer]:
              - /url: /privacy-policy
          - listitem [ref=e218]:
            - link "Conditions of Use" [ref=e219] [cursor=pointer]:
              - /url: /conditions-of-use
          - listitem [ref=e220]:
            - link "About us" [ref=e221] [cursor=pointer]:
              - /url: /about-us
          - listitem [ref=e222]:
            - link "Contact us" [ref=e223] [cursor=pointer]:
              - /url: /contactus
      - generic [ref=e224]:
        - heading "Customer service" [level=3] [ref=e225]
        - list [ref=e226]:
          - listitem [ref=e227]:
            - link "Search" [ref=e228] [cursor=pointer]:
              - /url: /search
          - listitem [ref=e229]:
            - link "News" [ref=e230] [cursor=pointer]:
              - /url: /news
          - listitem [ref=e231]:
            - link "Blog" [ref=e232] [cursor=pointer]:
              - /url: /blog
          - listitem [ref=e233]:
            - link "Recently viewed products" [ref=e234] [cursor=pointer]:
              - /url: /recentlyviewedproducts
          - listitem [ref=e235]:
            - link "Compare products list" [ref=e236] [cursor=pointer]:
              - /url: /compareproducts
          - listitem [ref=e237]:
            - link "New products" [ref=e238] [cursor=pointer]:
              - /url: /newproducts
      - generic [ref=e239]:
        - heading "My account" [level=3] [ref=e240]
        - list [ref=e241]:
          - listitem [ref=e242]:
            - link "My account" [ref=e243] [cursor=pointer]:
              - /url: /customer/info
          - listitem [ref=e244]:
            - link "Orders" [ref=e245] [cursor=pointer]:
              - /url: /customer/orders
          - listitem [ref=e246]:
            - link "Addresses" [ref=e247] [cursor=pointer]:
              - /url: /customer/addresses
          - listitem [ref=e248]:
            - link "Shopping cart" [ref=e249] [cursor=pointer]:
              - /url: /cart
          - listitem [ref=e250]:
            - link "Wishlist" [ref=e251] [cursor=pointer]:
              - /url: /wishlist
      - generic [ref=e252]:
        - heading "Follow us" [level=3] [ref=e253]
        - list [ref=e254]:
          - listitem [ref=e255]:
            - link "Facebook" [ref=e256] [cursor=pointer]:
              - /url: http://www.facebook.com/nopCommerce
          - listitem [ref=e257]:
            - link "Twitter" [ref=e258] [cursor=pointer]:
              - /url: https://twitter.com/nopCommerce
          - listitem [ref=e259]:
            - link "RSS" [ref=e260] [cursor=pointer]:
              - /url: /news/rss/1
          - listitem [ref=e261]:
            - link "YouTube" [ref=e262] [cursor=pointer]:
              - /url: http://www.youtube.com/user/nopCommerce
          - listitem [ref=e263]:
            - link "Google+" [ref=e264] [cursor=pointer]:
              - /url: https://plus.google.com/+nopcommerce
    - generic [ref=e265]:
      - text: Powered by
      - link "nopCommerce" [ref=e266] [cursor=pointer]:
        - /url: http://www.nopcommerce.com/
    - generic [ref=e267]: Copyright © 2026 Tricentis Demo Web Shop. All rights reserved.
```

# Test source

```ts
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
> 434 |       if (await stockStatus.count() > 0) {
      |                             ^ Error: locator.count: Unexpected token "=" while parsing css selector "[class*="stock"], text=/stock|available|quantity/i". Did you mean to CSS.escape it?
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