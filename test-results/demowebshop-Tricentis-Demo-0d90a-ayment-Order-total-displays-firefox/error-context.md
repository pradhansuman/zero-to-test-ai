# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: demowebshop.spec.ts >> Tricentis Demo Web Shop - 70 Approved Tests >> Checkout & Payment >> Order total displays
- Location: tests/e2e/demowebshop.spec.ts:287:9

# Error details

```
Error: locator.count: Unexpected token "=" while parsing css selector "[class*="total"], text=/total/i". Did you mean to CSS.escape it?
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
    - generic [ref=e44]:
      - list [ref=e46]:
        - listitem [ref=e47]:
          - link "Cart" [ref=e48] [cursor=pointer]:
            - /url: /cart
        - listitem [ref=e49]: Address
        - listitem [ref=e50]: Shipping
        - listitem [ref=e51]: Payment
        - listitem [ref=e52]: Confirm
        - listitem [ref=e53]: Complete
      - generic [ref=e54]:
        - heading "Shopping cart" [level=1] [ref=e56]
        - generic [ref=e58]: Your Shopping Cart is empty!
  - generic [ref=e59]:
    - generic [ref=e60]:
      - generic [ref=e61]:
        - heading "Information" [level=3] [ref=e62]
        - list [ref=e63]:
          - listitem [ref=e64]:
            - link "Sitemap" [ref=e65] [cursor=pointer]:
              - /url: /sitemap
          - listitem [ref=e66]:
            - link "Shipping & Returns" [ref=e67] [cursor=pointer]:
              - /url: /shipping-returns
          - listitem [ref=e68]:
            - link "Privacy Notice" [ref=e69] [cursor=pointer]:
              - /url: /privacy-policy
          - listitem [ref=e70]:
            - link "Conditions of Use" [ref=e71] [cursor=pointer]:
              - /url: /conditions-of-use
          - listitem [ref=e72]:
            - link "About us" [ref=e73] [cursor=pointer]:
              - /url: /about-us
          - listitem [ref=e74]:
            - link "Contact us" [ref=e75] [cursor=pointer]:
              - /url: /contactus
      - generic [ref=e76]:
        - heading "Customer service" [level=3] [ref=e77]
        - list [ref=e78]:
          - listitem [ref=e79]:
            - link "Search" [ref=e80] [cursor=pointer]:
              - /url: /search
          - listitem [ref=e81]:
            - link "News" [ref=e82] [cursor=pointer]:
              - /url: /news
          - listitem [ref=e83]:
            - link "Blog" [ref=e84] [cursor=pointer]:
              - /url: /blog
          - listitem [ref=e85]:
            - link "Recently viewed products" [ref=e86] [cursor=pointer]:
              - /url: /recentlyviewedproducts
          - listitem [ref=e87]:
            - link "Compare products list" [ref=e88] [cursor=pointer]:
              - /url: /compareproducts
          - listitem [ref=e89]:
            - link "New products" [ref=e90] [cursor=pointer]:
              - /url: /newproducts
      - generic [ref=e91]:
        - heading "My account" [level=3] [ref=e92]
        - list [ref=e93]:
          - listitem [ref=e94]:
            - link "My account" [ref=e95] [cursor=pointer]:
              - /url: /customer/info
          - listitem [ref=e96]:
            - link "Orders" [ref=e97] [cursor=pointer]:
              - /url: /customer/orders
          - listitem [ref=e98]:
            - link "Addresses" [ref=e99] [cursor=pointer]:
              - /url: /customer/addresses
          - listitem [ref=e100]:
            - link "Shopping cart" [ref=e101] [cursor=pointer]:
              - /url: /cart
          - listitem [ref=e102]:
            - link "Wishlist" [ref=e103] [cursor=pointer]:
              - /url: /wishlist
      - generic [ref=e104]:
        - heading "Follow us" [level=3] [ref=e105]
        - list [ref=e106]:
          - listitem [ref=e107]:
            - link "Facebook" [ref=e108] [cursor=pointer]:
              - /url: http://www.facebook.com/nopCommerce
          - listitem [ref=e109]:
            - link "Twitter" [ref=e110] [cursor=pointer]:
              - /url: https://twitter.com/nopCommerce
          - listitem [ref=e111]:
            - link "RSS" [ref=e112] [cursor=pointer]:
              - /url: /news/rss/1
          - listitem [ref=e113]:
            - link "YouTube" [ref=e114] [cursor=pointer]:
              - /url: http://www.youtube.com/user/nopCommerce
          - listitem [ref=e115]:
            - link "Google+" [ref=e116] [cursor=pointer]:
              - /url: https://plus.google.com/+nopcommerce
    - generic [ref=e117]:
      - text: Powered by
      - link "nopCommerce" [ref=e118] [cursor=pointer]:
        - /url: http://www.nopcommerce.com/
    - generic [ref=e119]: Copyright © 2026 Tricentis Demo Web Shop. All rights reserved.
```

# Test source

```ts
  190 | 
  191 |     test('Login form has email and password fields', async ({ page }) => {
  192 |       await page.goto(`${BASE_URL}/login`);
  193 |       const email = page.locator('input[type="email"], input[name*="email"]').first();
  194 |       const password = page.locator('input[type="password"]').first();
  195 |       if (await email.count() > 0) {
  196 |         await expect(email).toBeVisible();
  197 |       }
  198 |       if (await password.count() > 0) {
  199 |         await expect(password).toBeVisible();
  200 |       }
  201 |     });
  202 | 
  203 |     test('Logout link accessible when logged in', async ({ page }) => {
  204 |       await page.goto(BASE_URL);
  205 |       const logoutLink = page.locator('a, button').filter({ hasText: /logout|sign out/i }).first();
  206 |       // Will be invisible if not logged in, which is expected
  207 |     });
  208 | 
  209 |     test('Password reset page accessible', async ({ page }) => {
  210 |       await page.goto(`${BASE_URL}/password-recovery`);
  211 |       await page.waitForLoadState('networkidle');
  212 |     });
  213 | 
  214 |     test('User account page requires login', async ({ page }) => {
  215 |       await page.goto(`${BASE_URL}/customer/account`);
  216 |       await page.waitForLoadState('networkidle');
  217 |       const isLoggedIn = await page.url().includes('/account');
  218 |       const isLoginPage = await page.url().includes('/login');
  219 |       expect(isLoggedIn || isLoginPage).toBeTruthy();
  220 |     });
  221 | 
  222 |     test('Order history page loads', async ({ page }) => {
  223 |       await page.goto(`${BASE_URL}/customer/orders`);
  224 |       await page.waitForLoadState('networkidle');
  225 |     });
  226 | 
  227 |     test('Wishlist link present', async ({ page }) => {
  228 |       await page.goto(BASE_URL);
  229 |       const wishlist = page.locator('a, button').filter({ hasText: /wishlist|favorites|save/i }).first();
  230 |       // Will be present or not depending on app design
  231 |     });
  232 | 
  233 |     test('Category navigation works', async ({ page }) => {
  234 |       await page.goto(BASE_URL);
  235 |       const categories = page.locator('a').filter({ hasText: /books|computers|electronics/i }).first();
  236 |       if (await categories.count() > 0) {
  237 |         await categories.click();
  238 |         await page.waitForLoadState('networkidle');
  239 |       }
  240 |     });
  241 |   });
  242 | 
  243 |   // ═══════════════════════════════════════════════════════════════════
  244 |   // PHASE 3: CHECKOUT & PAYMENT TESTS (15 tests)
  245 |   // ═══════════════════════════════════════════════════════════════════
  246 | 
  247 |   test.describe('Checkout & Payment', () => {
  248 |     test('Checkout page loads', async ({ page }) => {
  249 |       await page.goto(`${BASE_URL}/checkout`);
  250 |       await page.waitForLoadState('networkidle');
  251 |       await expect(page).toHaveURL(/.*checkout/i);
  252 |     });
  253 | 
  254 |     test('Billing address form displays', async ({ page }) => {
  255 |       await page.goto(`${BASE_URL}/checkout`);
  256 |       const addressField = page.locator('input[name*="address"], input[placeholder*="address"]').first();
  257 |       if (await addressField.count() > 0) {
  258 |         await expect(addressField).toBeVisible();
  259 |       }
  260 |     });
  261 | 
  262 |     test('Shipping address selection available', async ({ page }) => {
  263 |       await page.goto(`${BASE_URL}/checkout`);
  264 |       const shippingField = page.locator('input[name*="shipping"], select[name*="address"]').first();
  265 |       if (await shippingField.count() > 0) {
  266 |         await expect(shippingField).toBeVisible();
  267 |       }
  268 |     });
  269 | 
  270 |     test('Shipping method selection works', async ({ page }) => {
  271 |       await page.goto(`${BASE_URL}/checkout`);
  272 |       const shippingOption = page.locator('input[type="radio"][name*="shipping"], input[type="radio"][name*="method"]').first();
  273 |       if (await shippingOption.count() > 0) {
  274 |         await shippingOption.click();
  275 |         await expect(shippingOption).toBeChecked();
  276 |       }
  277 |     });
  278 | 
  279 |     test('Payment method selection available', async ({ page }) => {
  280 |       await page.goto(`${BASE_URL}/checkout`);
  281 |       const paymentMethod = page.locator('input[type="radio"][name*="payment"]').first();
  282 |       if (await paymentMethod.count() > 0) {
  283 |         await expect(paymentMethod).toBeVisible();
  284 |       }
  285 |     });
  286 | 
  287 |     test('Order total displays', async ({ page }) => {
  288 |       await page.goto(`${BASE_URL}/checkout`);
  289 |       const total = page.locator('[class*="total"], text=/total/i').first();
> 290 |       if (await total.count() > 0) {
      |                       ^ Error: locator.count: Unexpected token "=" while parsing css selector "[class*="total"], text=/total/i". Did you mean to CSS.escape it?
  291 |         await expect(total).toBeVisible();
  292 |       }
  293 |     });
  294 | 
  295 |     test('Order summary displays', async ({ page }) => {
  296 |       await page.goto(`${BASE_URL}/checkout`);
  297 |       const summary = page.locator('[class*="summary"], [class*="order"]').first();
  298 |       if (await summary.count() > 0) {
  299 |         await expect(summary).toBeVisible();
  300 |       }
  301 |     });
  302 | 
  303 |     test('Confirm order button present', async ({ page }) => {
  304 |       await page.goto(`${BASE_URL}/checkout`);
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
```