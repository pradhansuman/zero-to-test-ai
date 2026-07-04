# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: demowebshop.spec.ts >> Tricentis Demo Web Shop - 70 Approved Tests >> Checkout & Payment >> Checkout page loads
- Location: tests/e2e/demowebshop.spec.ts:248:9

# Error details

```
Error: expect(page).toHaveURL(expected) failed

Expected pattern: /.*checkout/i
Received string:  "https://demowebshop.tricentis.com/cart"
Timeout: 5000ms

Call log:
  - Expect "toHaveURL" with timeout 5000ms
    14 × unexpected value "https://demowebshop.tricentis.com/cart"

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
- list:
  - listitem:
    - link "Cart":
      - /url: /cart
  - listitem: Address
  - listitem: Shipping
  - listitem: Payment
  - listitem: Confirm
  - listitem: Complete
- heading "Shopping cart" [level=1]
- text: Your Shopping Cart is empty!
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
> 251 |       await expect(page).toHaveURL(/.*checkout/i);
      |                          ^ Error: expect(page).toHaveURL(expected) failed
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
```