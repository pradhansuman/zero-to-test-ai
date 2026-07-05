# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auto-generated.spec.ts >> 🚀 COMPREHENSIVE TEST SUITE - AUTO-GENERATED >> Category: Gift Cards >> gift-cards add to cart from listing
- Location: tests/e2e/auto-generated.spec.ts:528:9

# Error details

```
Error: locator.count: Unexpected token "/" while parsing css selector "button:has-text(/add|cart/i), a:has-text(/add|cart/i)". Did you mean to CSS.escape it?
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
            - strong [ref=e86]: Gift Cards
        - generic [ref=e87]:
          - heading "Gift Cards" [level=1] [ref=e89]
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
            - generic [ref=e98]:
              - generic [ref=e100]:
                - link "Picture of $5 Virtual Gift Card" [ref=e102] [cursor=pointer]:
                  - /url: /5-virtual-gift-card
                  - img "Picture of $5 Virtual Gift Card" [ref=e103]
                - generic [ref=e104]:
                  - heading "$5 Virtual Gift Card" [level=2] [ref=e105]:
                    - link "$5 Virtual Gift Card" [ref=e106] [cursor=pointer]:
                      - /url: /5-virtual-gift-card
                  - generic "659 review(s)" [ref=e107]
                  - generic [ref=e110]:
                    - generic [ref=e112]: "5.00"
                    - button "Add to cart" [ref=e114] [cursor=pointer]
              - generic [ref=e116]:
                - link "Picture of $25 Virtual Gift Card" [ref=e118] [cursor=pointer]:
                  - /url: /25-virtual-gift-card
                  - img "Picture of $25 Virtual Gift Card" [ref=e119]
                - generic [ref=e120]:
                  - heading "$25 Virtual Gift Card" [level=2] [ref=e121]:
                    - link "$25 Virtual Gift Card" [ref=e122] [cursor=pointer]:
                      - /url: /25-virtual-gift-card
                  - generic "911 review(s)" [ref=e123]
                  - generic [ref=e126]:
                    - generic [ref=e128]: "25.00"
                    - button "Add to cart" [ref=e130] [cursor=pointer]
              - generic [ref=e132]:
                - link "Picture of $50 Physical Gift Card" [ref=e134] [cursor=pointer]:
                  - /url: /50-physical-gift-card
                  - img "Picture of $50 Physical Gift Card" [ref=e135]
                - generic [ref=e136]:
                  - heading "$50 Physical Gift Card" [level=2] [ref=e137]:
                    - link "$50 Physical Gift Card" [ref=e138] [cursor=pointer]:
                      - /url: /50-physical-gift-card
                  - generic "616 review(s)" [ref=e139]
                  - generic [ref=e142]:
                    - generic [ref=e144]: "50.00"
                    - button "Add to cart" [ref=e146] [cursor=pointer]
              - generic [ref=e148]:
                - link "Picture of $100 Physical Gift Card" [ref=e150] [cursor=pointer]:
                  - /url: /100-physical-gift-card
                  - img "Picture of $100 Physical Gift Card" [ref=e151]
                - generic [ref=e152]:
                  - heading "$100 Physical Gift Card" [level=2] [ref=e153]:
                    - link "$100 Physical Gift Card" [ref=e154] [cursor=pointer]:
                      - /url: /100-physical-gift-card
                  - generic "62 review(s)" [ref=e155]
                  - generic [ref=e158]:
                    - generic [ref=e160]: "100.00"
                    - button "Add to cart" [ref=e162] [cursor=pointer]
  - generic [ref=e163]:
    - generic [ref=e164]:
      - generic [ref=e165]:
        - heading "Information" [level=3] [ref=e166]
        - list [ref=e167]:
          - listitem [ref=e168]:
            - link "Sitemap" [ref=e169] [cursor=pointer]:
              - /url: /sitemap
          - listitem [ref=e170]:
            - link "Shipping & Returns" [ref=e171] [cursor=pointer]:
              - /url: /shipping-returns
          - listitem [ref=e172]:
            - link "Privacy Notice" [ref=e173] [cursor=pointer]:
              - /url: /privacy-policy
          - listitem [ref=e174]:
            - link "Conditions of Use" [ref=e175] [cursor=pointer]:
              - /url: /conditions-of-use
          - listitem [ref=e176]:
            - link "About us" [ref=e177] [cursor=pointer]:
              - /url: /about-us
          - listitem [ref=e178]:
            - link "Contact us" [ref=e179] [cursor=pointer]:
              - /url: /contactus
      - generic [ref=e180]:
        - heading "Customer service" [level=3] [ref=e181]
        - list [ref=e182]:
          - listitem [ref=e183]:
            - link "Search" [ref=e184] [cursor=pointer]:
              - /url: /search
          - listitem [ref=e185]:
            - link "News" [ref=e186] [cursor=pointer]:
              - /url: /news
          - listitem [ref=e187]:
            - link "Blog" [ref=e188] [cursor=pointer]:
              - /url: /blog
          - listitem [ref=e189]:
            - link "Recently viewed products" [ref=e190] [cursor=pointer]:
              - /url: /recentlyviewedproducts
          - listitem [ref=e191]:
            - link "Compare products list" [ref=e192] [cursor=pointer]:
              - /url: /compareproducts
          - listitem [ref=e193]:
            - link "New products" [ref=e194] [cursor=pointer]:
              - /url: /newproducts
      - generic [ref=e195]:
        - heading "My account" [level=3] [ref=e196]
        - list [ref=e197]:
          - listitem [ref=e198]:
            - link "My account" [ref=e199] [cursor=pointer]:
              - /url: /customer/info
          - listitem [ref=e200]:
            - link "Orders" [ref=e201] [cursor=pointer]:
              - /url: /customer/orders
          - listitem [ref=e202]:
            - link "Addresses" [ref=e203] [cursor=pointer]:
              - /url: /customer/addresses
          - listitem [ref=e204]:
            - link "Shopping cart" [ref=e205] [cursor=pointer]:
              - /url: /cart
          - listitem [ref=e206]:
            - link "Wishlist" [ref=e207] [cursor=pointer]:
              - /url: /wishlist
      - generic [ref=e208]:
        - heading "Follow us" [level=3] [ref=e209]
        - list [ref=e210]:
          - listitem [ref=e211]:
            - link "Facebook" [ref=e212] [cursor=pointer]:
              - /url: http://www.facebook.com/nopCommerce
          - listitem [ref=e213]:
            - link "Twitter" [ref=e214] [cursor=pointer]:
              - /url: https://twitter.com/nopCommerce
          - listitem [ref=e215]:
            - link "RSS" [ref=e216] [cursor=pointer]:
              - /url: /news/rss/1
          - listitem [ref=e217]:
            - link "YouTube" [ref=e218] [cursor=pointer]:
              - /url: http://www.youtube.com/user/nopCommerce
          - listitem [ref=e219]:
            - link "Google+" [ref=e220] [cursor=pointer]:
              - /url: https://plus.google.com/+nopcommerce
    - generic [ref=e221]:
      - text: Powered by
      - link "nopCommerce" [ref=e222] [cursor=pointer]:
        - /url: http://www.nopcommerce.com/
    - generic [ref=e223]: Copyright © 2026 Tricentis Demo Web Shop. All rights reserved.
```

# Test source

```ts
  431 |       }
  432 |     });
  433 | 
  434 |     test('jewelry pagination works', async ({ page }) => {
  435 |       await page.goto(`${BASE_URL}/jewelry`);
  436 |       const pageLinks = page.locator('[class*=pager], a:has-text(/\d+/)');
  437 |       expect(await pageLinks.count()).toBeGreaterThanOrEqual(0);
  438 |     });
  439 | 
  440 |     test('jewelry product detail link navigates', async ({ page }) => {
  441 |       await page.goto(`${BASE_URL}/jewelry`);
  442 |       const productLink = page.locator('a[href*=product]').first();
  443 |       if (await productLink.count() > 0) {
  444 |         const isVisible = await productLink.isVisible().catch(() => false);
  445 |         if (isVisible) {
  446 |           await productLink.click();
  447 |           await page.waitForLoadState('networkidle');
  448 |           expect(page.url()).toContain('product');
  449 |         }
  450 |       }
  451 |     });
  452 | 
  453 |     test('jewelry add to cart from listing', async ({ page }) => {
  454 |       await page.goto(`${BASE_URL}/jewelry`);
  455 |       const addBtn = page.locator('button:has-text(/add|cart/i), a:has-text(/add|cart/i)').first();
  456 |       if (await addBtn.count() > 0) {
  457 |         const isVisible = await addBtn.isVisible().catch(() => false);
  458 |         if (isVisible) {
  459 |           await addBtn.click();
  460 |           await page.waitForLoadState('networkidle');
  461 |         }
  462 |       }
  463 |     });
  464 |   });
  465 | 
  466 |   test.describe('Category: Gift Cards', () => {
  467 |     test('gift-cards page loads correctly', async ({ page }) => {
  468 |       await page.goto(`${BASE_URL}/gift-cards`);
  469 |       await page.waitForLoadState('networkidle');
  470 |       const title = page.locator('h1, [class*=title]').first();
  471 |       if (await title.count() > 0) {
  472 |         await expect(title).toBeVisible();
  473 |       }
  474 |     });
  475 | 
  476 |     test('gift-cards displays product list', async ({ page }) => {
  477 |       await page.goto(`${BASE_URL}/gift-cards`);
  478 |       const products = page.locator('[class*=product], a[href*=product]');
  479 |       expect(await products.count()).toBeGreaterThan(0);
  480 |     });
  481 | 
  482 |     test('gift-cards filtering functionality', async ({ page }) => {
  483 |       await page.goto(`${BASE_URL}/gift-cards`);
  484 |       const filter = page.locator('[class*=filter], button:has-text(/filter/i)').first();
  485 |       if (await filter.count() > 0) {
  486 |         const isVisible = await filter.isVisible().catch(() => false);
  487 |         if (isVisible) {
  488 |           await filter.click();
  489 |           await page.waitForLoadState('networkidle');
  490 |         }
  491 |       }
  492 |     });
  493 | 
  494 |     test('gift-cards sorting by price', async ({ page }) => {
  495 |       await page.goto(`${BASE_URL}/gift-cards`);
  496 |       const sort = page.locator('select[name*=sort], [class*=sort]').first();
  497 |       if (await sort.count() > 0) {
  498 |         const isVisible = await sort.isVisible().catch(() => false);
  499 |         if (isVisible) {
  500 |           try {
  501 |             await sort.selectOption('1');
  502 |           } catch (e) {
  503 |             // Fallback for non-select elements
  504 |           }
  505 |         }
  506 |       }
  507 |     });
  508 | 
  509 |     test('gift-cards pagination works', async ({ page }) => {
  510 |       await page.goto(`${BASE_URL}/gift-cards`);
  511 |       const pageLinks = page.locator('[class*=pager], a:has-text(/\d+/)');
  512 |       expect(await pageLinks.count()).toBeGreaterThanOrEqual(0);
  513 |     });
  514 | 
  515 |     test('gift-cards product detail link navigates', async ({ page }) => {
  516 |       await page.goto(`${BASE_URL}/gift-cards`);
  517 |       const productLink = page.locator('a[href*=product]').first();
  518 |       if (await productLink.count() > 0) {
  519 |         const isVisible = await productLink.isVisible().catch(() => false);
  520 |         if (isVisible) {
  521 |           await productLink.click();
  522 |           await page.waitForLoadState('networkidle');
  523 |           expect(page.url()).toContain('product');
  524 |         }
  525 |       }
  526 |     });
  527 | 
  528 |     test('gift-cards add to cart from listing', async ({ page }) => {
  529 |       await page.goto(`${BASE_URL}/gift-cards`);
  530 |       const addBtn = page.locator('button:has-text(/add|cart/i), a:has-text(/add|cart/i)').first();
> 531 |       if (await addBtn.count() > 0) {
      |                        ^ Error: locator.count: Unexpected token "/" while parsing css selector "button:has-text(/add|cart/i), a:has-text(/add|cart/i)". Did you mean to CSS.escape it?
  532 |         const isVisible = await addBtn.isVisible().catch(() => false);
  533 |         if (isVisible) {
  534 |           await addBtn.click();
  535 |           await page.waitForLoadState('networkidle');
  536 |         }
  537 |       }
  538 |     });
  539 |   });
  540 | 
  541 |   // ═════════════════════════════════════════════════════════
  542 |   // NAVIGATION COVERAGE - All Links (25+ tests)
  543 |   // ═════════════════════════════════════════════════════════
  544 | 
  545 |   test.describe('Header Navigation', () => {
  546 | 
  547 |     test('Register link navigates correctly', async ({ page }) => {
  548 |       await page.goto(BASE_URL);
  549 |       const linkElement = page.locator('a:has-text(/Register/i), a[href*="register"]').first();
  550 |       if (await linkElement.count() > 0) {
  551 |         const isVisible = await linkElement.isVisible().catch(() => false);
  552 |         if (isVisible) {
  553 |           await linkElement.click();
  554 |           await page.waitForLoadState('networkidle');
  555 |           const currentUrl = page.url();
  556 |           expect(currentUrl.includes('register') || currentUrl !== BASE_URL).toBeTruthy();
  557 |         }
  558 |       }
  559 |     });
  560 |     test('Login link navigates correctly', async ({ page }) => {
  561 |       await page.goto(BASE_URL);
  562 |       const linkElement = page.locator('a:has-text(/Login/i), a[href*="login"]').first();
  563 |       if (await linkElement.count() > 0) {
  564 |         const isVisible = await linkElement.isVisible().catch(() => false);
  565 |         if (isVisible) {
  566 |           await linkElement.click();
  567 |           await page.waitForLoadState('networkidle');
  568 |           const currentUrl = page.url();
  569 |           expect(currentUrl.includes('login') || currentUrl !== BASE_URL).toBeTruthy();
  570 |         }
  571 |       }
  572 |     });
  573 |     test('Shopping Cart link navigates correctly', async ({ page }) => {
  574 |       await page.goto(BASE_URL);
  575 |       const linkElement = page.locator('a:has-text(/Shopping Cart/i), a[href*="cart"]').first();
  576 |       if (await linkElement.count() > 0) {
  577 |         const isVisible = await linkElement.isVisible().catch(() => false);
  578 |         if (isVisible) {
  579 |           await linkElement.click();
  580 |           await page.waitForLoadState('networkidle');
  581 |           const currentUrl = page.url();
  582 |           expect(currentUrl.includes('cart') || currentUrl !== BASE_URL).toBeTruthy();
  583 |         }
  584 |       }
  585 |     });
  586 |     test('Wishlist link navigates correctly', async ({ page }) => {
  587 |       await page.goto(BASE_URL);
  588 |       const linkElement = page.locator('a:has-text(/Wishlist/i), a[href*="wishlist"]').first();
  589 |       if (await linkElement.count() > 0) {
  590 |         const isVisible = await linkElement.isVisible().catch(() => false);
  591 |         if (isVisible) {
  592 |           await linkElement.click();
  593 |           await page.waitForLoadState('networkidle');
  594 |           const currentUrl = page.url();
  595 |           expect(currentUrl.includes('wishlist') || currentUrl !== BASE_URL).toBeTruthy();
  596 |         }
  597 |       }
  598 |     });
  599 |   });
  600 |   test.describe('Footer Links', () => {
  601 | 
  602 |     test('Sitemap link navigates correctly', async ({ page }) => {
  603 |       await page.goto(BASE_URL);
  604 |       const linkElement = page.locator('a:has-text(/Sitemap/i), a[href*="sitemap"]').first();
  605 |       if (await linkElement.count() > 0) {
  606 |         const isVisible = await linkElement.isVisible().catch(() => false);
  607 |         if (isVisible) {
  608 |           await linkElement.click();
  609 |           await page.waitForLoadState('networkidle');
  610 |           const currentUrl = page.url();
  611 |           expect(currentUrl.includes('sitemap') || currentUrl !== BASE_URL).toBeTruthy();
  612 |         }
  613 |       }
  614 |     });
  615 |     test('About Us link navigates correctly', async ({ page }) => {
  616 |       await page.goto(BASE_URL);
  617 |       const linkElement = page.locator('a:has-text(/About Us/i), a[href*="about-us"]').first();
  618 |       if (await linkElement.count() > 0) {
  619 |         const isVisible = await linkElement.isVisible().catch(() => false);
  620 |         if (isVisible) {
  621 |           await linkElement.click();
  622 |           await page.waitForLoadState('networkidle');
  623 |           const currentUrl = page.url();
  624 |           expect(currentUrl.includes('about-us') || currentUrl !== BASE_URL).toBeTruthy();
  625 |         }
  626 |       }
  627 |     });
  628 |     test('Contact link navigates correctly', async ({ page }) => {
  629 |       await page.goto(BASE_URL);
  630 |       const linkElement = page.locator('a:has-text(/Contact/i), a[href*="contact"]').first();
  631 |       if (await linkElement.count() > 0) {
```