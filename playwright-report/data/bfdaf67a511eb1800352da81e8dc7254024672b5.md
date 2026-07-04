# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: demowebshop.spec.ts >> Tricentis Demo Web Shop - 70 Approved Tests >> Functional - Core Features >> Order history page loads
- Location: tests/e2e/demowebshop.spec.ts:222:9

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: page.waitForLoadState: Test timeout of 30000ms exceeded.
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
      - generic [ref=e81]:
        - heading "Welcome, Please Sign In!" [level=1] [ref=e83]
        - generic [ref=e84]:
          - generic [ref=e85]:
            - generic [ref=e86]:
              - strong [ref=e88]: New Customer
              - generic [ref=e89]: By creating an account on our website you will be able to shop faster, be up to date on an orders status, and keep track of the orders you have previously made.
              - button "Register" [ref=e91] [cursor=pointer]
            - generic [ref=e92]:
              - strong [ref=e94]: Returning Customer
              - generic [ref=e96]:
                - generic [ref=e97]:
                  - generic [ref=e98]: "Email:"
                  - textbox "Email:" [active] [ref=e99]
                - generic [ref=e100]:
                  - generic [ref=e101]: "Password:"
                  - textbox "Password:" [ref=e102]
                - generic [ref=e103]:
                  - checkbox "Remember me?" [ref=e104]
                  - generic [ref=e105]: Remember me?
                  - link "Forgot password?" [ref=e107] [cursor=pointer]:
                    - /url: /passwordrecovery
                - button "Log in" [ref=e109] [cursor=pointer]
          - generic [ref=e110]:
            - heading "About login / registration" [level=2] [ref=e112]
            - paragraph [ref=e114]: Put your login / registration information here. You can edit this in the admin site.
  - generic [ref=e115]:
    - generic [ref=e116]:
      - generic [ref=e117]:
        - heading "Information" [level=3] [ref=e118]
        - list [ref=e119]:
          - listitem [ref=e120]:
            - link "Sitemap" [ref=e121] [cursor=pointer]:
              - /url: /sitemap
          - listitem [ref=e122]:
            - link "Shipping & Returns" [ref=e123] [cursor=pointer]:
              - /url: /shipping-returns
          - listitem [ref=e124]:
            - link "Privacy Notice" [ref=e125] [cursor=pointer]:
              - /url: /privacy-policy
          - listitem [ref=e126]:
            - link "Conditions of Use" [ref=e127] [cursor=pointer]:
              - /url: /conditions-of-use
          - listitem [ref=e128]:
            - link "About us" [ref=e129] [cursor=pointer]:
              - /url: /about-us
          - listitem [ref=e130]:
            - link "Contact us" [ref=e131] [cursor=pointer]:
              - /url: /contactus
      - generic [ref=e132]:
        - heading "Customer service" [level=3] [ref=e133]
        - list [ref=e134]:
          - listitem [ref=e135]:
            - link "Search" [ref=e136] [cursor=pointer]:
              - /url: /search
          - listitem [ref=e137]:
            - link "News" [ref=e138] [cursor=pointer]:
              - /url: /news
          - listitem [ref=e139]:
            - link "Blog" [ref=e140] [cursor=pointer]:
              - /url: /blog
          - listitem [ref=e141]:
            - link "Recently viewed products" [ref=e142] [cursor=pointer]:
              - /url: /recentlyviewedproducts
          - listitem [ref=e143]:
            - link "Compare products list" [ref=e144] [cursor=pointer]:
              - /url: /compareproducts
          - listitem [ref=e145]:
            - link "New products" [ref=e146] [cursor=pointer]:
              - /url: /newproducts
      - generic [ref=e147]:
        - heading "My account" [level=3] [ref=e148]
        - list [ref=e149]:
          - listitem [ref=e150]:
            - link "My account" [ref=e151] [cursor=pointer]:
              - /url: /customer/info
          - listitem [ref=e152]:
            - link "Orders" [ref=e153] [cursor=pointer]:
              - /url: /customer/orders
          - listitem [ref=e154]:
            - link "Addresses" [ref=e155] [cursor=pointer]:
              - /url: /customer/addresses
          - listitem [ref=e156]:
            - link "Shopping cart" [ref=e157] [cursor=pointer]:
              - /url: /cart
          - listitem [ref=e158]:
            - link "Wishlist" [ref=e159] [cursor=pointer]:
              - /url: /wishlist
      - generic [ref=e160]:
        - heading "Follow us" [level=3] [ref=e161]
        - list [ref=e162]:
          - listitem [ref=e163]:
            - link "Facebook" [ref=e164] [cursor=pointer]:
              - /url: http://www.facebook.com/nopCommerce
          - listitem [ref=e165]:
            - link "Twitter" [ref=e166] [cursor=pointer]:
              - /url: https://twitter.com/nopCommerce
          - listitem [ref=e167]:
            - link "RSS" [ref=e168] [cursor=pointer]:
              - /url: /news/rss/1
          - listitem [ref=e169]:
            - link "YouTube" [ref=e170] [cursor=pointer]:
              - /url: http://www.youtube.com/user/nopCommerce
          - listitem [ref=e171]:
            - link "Google+" [ref=e172] [cursor=pointer]:
              - /url: https://plus.google.com/+nopcommerce
    - generic [ref=e173]:
      - text: Powered by
      - link "nopCommerce" [ref=e174] [cursor=pointer]:
        - /url: http://www.nopcommerce.com/
    - generic [ref=e175]: Copyright © 2026 Tricentis Demo Web Shop. All rights reserved.
```

# Test source

```ts
  124 | 
  125 |     test('Product filtering works', async ({ page }) => {
  126 |       await page.goto(`${BASE_URL}/books`);
  127 |       const filterBtn = page.locator('[class*="filter"], button:has-text(/sort|filter/i)').first();
  128 |       if (await filterBtn.count() > 0) {
  129 |         await filterBtn.click();
  130 |         await page.waitForLoadState('networkidle');
  131 |       }
  132 |     });
  133 | 
  134 |     test('Add product to cart increases counter', async ({ page }) => {
  135 |       await page.goto(`${BASE_URL}/books`);
  136 |       const cartCounter = page.locator('[data-testid*="cart"], [class*="cart-count"], span:has-text(/[0-9]+/)').first();
  137 |       const initialCount = await cartCounter.innerText().catch(() => '0');
  138 | 
  139 |       const addBtn = page.locator('button, input[type="button"]').filter({ hasText: /add|cart/i }).first();
  140 |       if (await addBtn.count() > 0) {
  141 |         await addBtn.click();
  142 |         await page.waitForTimeout(1000);
  143 |       }
  144 |     });
  145 | 
  146 |     test('Cart page accessible', async ({ page }) => {
  147 |       await page.goto(`${BASE_URL}/cart`);
  148 |       await expect(page).toHaveURL(/.*cart/i);
  149 |     });
  150 | 
  151 |     test('Remove item from cart', async ({ page }) => {
  152 |       await page.goto(`${BASE_URL}/cart`);
  153 |       const removeBtn = page.locator('button, a').filter({ hasText: /remove|delete|trash/i }).first();
  154 |       if (await removeBtn.count() > 0) {
  155 |         await expect(removeBtn).toBeVisible();
  156 |       }
  157 |     });
  158 | 
  159 |     test('Update quantity in cart', async ({ page }) => {
  160 |       await page.goto(`${BASE_URL}/cart`);
  161 |       const qtyInput = page.locator('input[type="number"], input[name*="quantity"]').first();
  162 |       if (await qtyInput.count() > 0) {
  163 |         await qtyInput.clear();
  164 |         await qtyInput.fill('2');
  165 |         await expect(qtyInput).toHaveValue('2');
  166 |       }
  167 |     });
  168 | 
  169 |     test('User registration page loads', async ({ page }) => {
  170 |       await page.goto(`${BASE_URL}/register`);
  171 |       await expect(page).toHaveURL(/.*register/i);
  172 |     });
  173 | 
  174 |     test('Registration form has required fields', async ({ page }) => {
  175 |       await page.goto(`${BASE_URL}/register`);
  176 |       const emailField = page.locator('input[type="email"], input[name*="email"]').first();
  177 |       const pwField = page.locator('input[type="password"]').first();
  178 |       if (await emailField.count() > 0) {
  179 |         await expect(emailField).toBeVisible();
  180 |       }
  181 |       if (await pwField.count() > 0) {
  182 |         await expect(pwField).toBeVisible();
  183 |       }
  184 |     });
  185 | 
  186 |     test('User login page loads', async ({ page }) => {
  187 |       await page.goto(`${BASE_URL}/login`);
  188 |       await expect(page).toHaveURL(/.*login/i);
  189 |     });
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
> 224 |       await page.waitForLoadState('networkidle');
      |                  ^ Error: page.waitForLoadState: Test timeout of 30000ms exceeded.
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
  290 |       if (await total.count() > 0) {
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
```