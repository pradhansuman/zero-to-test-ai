# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: tricentis.spec.ts >> Tricentis Demo Web Shop - E-Commerce Suite >> 4. Shopping Cart Operations >> Add item to cart and verify
- Location: tests/e2e/tricentis.spec.ts:154:9

# Error details

```
Error: locator.click: Error: strict mode violation: locator('a:has-text("Cart")') resolved to 3 elements:
    1) <a href="/cart">shopping cart</a> aka getByRole('link', { name: 'shopping cart', exact: true })
    2) <a href="/cart" class="ico-cart">…</a> aka getByRole('link', { name: 'Shopping cart (1)' })
    ...

Call log:
  - waiting for locator('a:has-text("Cart")')

```

# Page snapshot

```yaml
- generic [ref=e1]:
  - generic [ref=e2]:
    - generic "Close" [ref=e3] [cursor=pointer]
    - paragraph [ref=e4]:
      - text: The product has been added to your
      - link "shopping cart" [ref=e5] [cursor=pointer]:
        - /url: /cart
  - generic [ref=e6]:
    - generic [ref=e7]:
      - generic [ref=e8]:
        - link "Tricentis Demo Web Shop" [ref=e10] [cursor=pointer]:
          - /url: /
          - img "Tricentis Demo Web Shop" [ref=e11]
        - list [ref=e14]:
          - listitem [ref=e15]:
            - link "Register" [ref=e16] [cursor=pointer]:
              - /url: /register
          - listitem [ref=e17]:
            - link "Log in" [ref=e18] [cursor=pointer]:
              - /url: /login
          - listitem [ref=e19]:
            - link "Shopping cart (1)" [ref=e20] [cursor=pointer]:
              - /url: /cart
              - generic [ref=e21]: Shopping cart
              - generic [ref=e22]: (1)
          - listitem [ref=e23]:
            - link "Wishlist (0)" [ref=e24] [cursor=pointer]:
              - /url: /wishlist
              - generic [ref=e25]: Wishlist
              - generic [ref=e26]: (0)
        - generic [ref=e28]:
          - status [ref=e29]
          - textbox [ref=e30]: Search store
          - button "Search" [ref=e31] [cursor=pointer]
      - list [ref=e33]:
        - listitem [ref=e34]:
          - link "Books" [ref=e35] [cursor=pointer]:
            - /url: /books
        - listitem [ref=e36]:
          - link "Computers" [ref=e37] [cursor=pointer]:
            - /url: /computers
        - listitem [ref=e38]:
          - link "Electronics" [ref=e39] [cursor=pointer]:
            - /url: /electronics
        - listitem [ref=e40]:
          - link "Apparel & Shoes" [ref=e41] [cursor=pointer]:
            - /url: /apparel-shoes
        - listitem [ref=e42]:
          - link "Digital downloads" [ref=e43] [cursor=pointer]:
            - /url: /digital-downloads
        - listitem [ref=e44]:
          - link "Jewelry" [ref=e45] [cursor=pointer]:
            - /url: /jewelry
        - listitem [ref=e46]:
          - link "Gift Cards" [ref=e47] [cursor=pointer]:
            - /url: /gift-cards
      - generic:
        - generic [ref=e48]:
          - generic [ref=e49]:
            - strong [ref=e51]: Categories
            - list [ref=e53]:
              - listitem [ref=e54]:
                - link "Books" [ref=e55] [cursor=pointer]:
                  - /url: /books
              - listitem [ref=e56]:
                - link "Computers" [ref=e57] [cursor=pointer]:
                  - /url: /computers
              - listitem [ref=e58]:
                - link "Electronics" [ref=e59] [cursor=pointer]:
                  - /url: /electronics
              - listitem [ref=e60]:
                - link "Apparel & Shoes" [ref=e61] [cursor=pointer]:
                  - /url: /apparel-shoes
              - listitem [ref=e62]:
                - link "Digital downloads" [ref=e63] [cursor=pointer]:
                  - /url: /digital-downloads
              - listitem [ref=e64]:
                - link "Jewelry" [ref=e65] [cursor=pointer]:
                  - /url: /jewelry
              - listitem [ref=e66]:
                - link "Gift Cards" [ref=e67] [cursor=pointer]:
                  - /url: /gift-cards
          - generic [ref=e68]:
            - strong [ref=e70]: Manufacturers
            - list [ref=e72]:
              - listitem [ref=e73]:
                - link "Tricentis" [ref=e74] [cursor=pointer]:
                  - /url: /tricentis
          - generic [ref=e75]:
            - strong [ref=e77]: Newsletter
            - generic [ref=e79]:
              - text: "Sign up for our newsletter:"
              - textbox [ref=e81]
              - button "Subscribe" [ref=e83] [cursor=pointer]
        - generic [ref=e84]:
          - list [ref=e86]:
            - listitem [ref=e87]:
              - link "Home" [ref=e88] [cursor=pointer]:
                - /url: /
              - text: /
            - listitem [ref=e89]:
              - strong [ref=e90]: Books
          - generic [ref=e91]:
            - heading "Books" [level=1] [ref=e93]
            - generic [ref=e94]:
              - generic [ref=e95]:
                - generic [ref=e96]:
                  - text: View as
                  - combobox [ref=e97]:
                    - option "Grid" [selected]
                    - option "List"
                - generic [ref=e98]:
                  - text: Sort by
                  - combobox [ref=e99]:
                    - option "Position" [selected]
                    - 'option "Name: A to Z"'
                    - 'option "Name: Z to A"'
                    - 'option "Price: Low to High"'
                    - 'option "Price: High to Low"'
                    - option "Created on"
                - generic [ref=e100]:
                  - text: Display
                  - combobox [ref=e101]:
                    - option "4"
                    - option "8" [selected]
                    - option "12"
                  - text: per page
              - generic [ref=e103]:
                - strong [ref=e105]: Filter by price
                - list [ref=e107]:
                  - listitem [ref=e108]:
                    - link "Under 25.00" [ref=e109] [cursor=pointer]:
                      - /url: https://demowebshop.tricentis.com/books?price=-25
                  - listitem [ref=e110]:
                    - link "25.00 - 50.00" [ref=e111] [cursor=pointer]:
                      - /url: https://demowebshop.tricentis.com/books?price=25-50
                  - listitem [ref=e112]:
                    - link "Over 50.00" [ref=e113] [cursor=pointer]:
                      - /url: https://demowebshop.tricentis.com/books?price=50-
              - generic [ref=e114]:
                - generic [ref=e116]:
                  - link "Picture of Computing and Internet" [ref=e118] [cursor=pointer]:
                    - /url: /computing-and-internet
                    - img "Picture of Computing and Internet" [ref=e119]
                  - generic [ref=e120]:
                    - heading "Computing and Internet" [level=2] [ref=e121]:
                      - link "Computing and Internet" [ref=e122] [cursor=pointer]:
                        - /url: /computing-and-internet
                    - generic "2660 review(s)" [ref=e123]
                    - generic [ref=e126]:
                      - generic [ref=e127]:
                        - generic [ref=e128]: "30.00"
                        - generic [ref=e129]: "10.00"
                      - button "Add to cart" [active] [ref=e131] [cursor=pointer]
                - generic [ref=e133]:
                  - link "Picture of Copy of Computing and Internet EX" [ref=e135] [cursor=pointer]:
                    - /url: /copy-of-computing-and-internet
                    - img "Picture of Copy of Computing and Internet EX" [ref=e136]
                  - generic [ref=e137]:
                    - heading "Copy of Computing and Internet EX" [level=2] [ref=e138]:
                      - link "Copy of Computing and Internet EX" [ref=e139] [cursor=pointer]:
                        - /url: /copy-of-computing-and-internet
                    - generic "382 review(s)" [ref=e140]
                    - generic [ref=e144]:
                      - generic [ref=e145]: "30.00"
                      - generic [ref=e146]: "10.00"
                - generic [ref=e148]:
                  - link "Picture of Fiction" [ref=e150] [cursor=pointer]:
                    - /url: /fiction
                    - img "Picture of Fiction" [ref=e151]
                  - generic [ref=e152]:
                    - heading "Fiction" [level=2] [ref=e153]:
                      - link "Fiction" [ref=e154] [cursor=pointer]:
                        - /url: /fiction
                    - generic "789 review(s)" [ref=e155]
                    - generic [ref=e158]:
                      - generic [ref=e159]:
                        - generic [ref=e160]: "35.00"
                        - generic [ref=e161]: "24.00"
                      - button "Add to cart" [ref=e163] [cursor=pointer]
                - generic [ref=e165]:
                  - link "Picture of Fiction EX" [ref=e167] [cursor=pointer]:
                    - /url: /fiction-ex
                    - img "Picture of Fiction EX" [ref=e168]
                  - generic [ref=e169]:
                    - heading "Fiction EX" [level=2] [ref=e170]:
                      - link "Fiction EX" [ref=e171] [cursor=pointer]:
                        - /url: /fiction-ex
                    - generic "420 review(s)" [ref=e172]
                    - generic [ref=e176]:
                      - generic [ref=e177]: "35.00"
                      - generic [ref=e178]: "24.00"
                - generic [ref=e180]:
                  - link "Picture of Health Book" [ref=e182] [cursor=pointer]:
                    - /url: /health
                    - img "Picture of Health Book" [ref=e183]
                  - generic [ref=e184]:
                    - heading "Health Book" [level=2] [ref=e185]:
                      - link "Health Book" [ref=e186] [cursor=pointer]:
                        - /url: /health
                    - generic "526 review(s)" [ref=e187]
                    - generic [ref=e190]:
                      - generic [ref=e191]:
                        - generic [ref=e192]: "27.00"
                        - generic [ref=e193]: "10.00"
                      - button "Add to cart" [ref=e195] [cursor=pointer]
                - generic [ref=e197]:
                  - link "Picture of Science" [ref=e199] [cursor=pointer]:
                    - /url: /science
                    - img "Picture of Science" [ref=e200]
                  - generic [ref=e201]:
                    - heading "Science" [level=2] [ref=e202]:
                      - link "Science" [ref=e203] [cursor=pointer]:
                        - /url: /science
                    - generic "451 review(s)" [ref=e204]
                    - generic [ref=e208]:
                      - generic [ref=e209]: "67.00"
                      - generic [ref=e210]: "51.00"
    - generic [ref=e211]:
      - generic [ref=e212]:
        - generic [ref=e213]:
          - heading "Information" [level=3] [ref=e214]
          - list [ref=e215]:
            - listitem [ref=e216]:
              - link "Sitemap" [ref=e217] [cursor=pointer]:
                - /url: /sitemap
            - listitem [ref=e218]:
              - link "Shipping & Returns" [ref=e219] [cursor=pointer]:
                - /url: /shipping-returns
            - listitem [ref=e220]:
              - link "Privacy Notice" [ref=e221] [cursor=pointer]:
                - /url: /privacy-policy
            - listitem [ref=e222]:
              - link "Conditions of Use" [ref=e223] [cursor=pointer]:
                - /url: /conditions-of-use
            - listitem [ref=e224]:
              - link "About us" [ref=e225] [cursor=pointer]:
                - /url: /about-us
            - listitem [ref=e226]:
              - link "Contact us" [ref=e227] [cursor=pointer]:
                - /url: /contactus
        - generic [ref=e228]:
          - heading "Customer service" [level=3] [ref=e229]
          - list [ref=e230]:
            - listitem [ref=e231]:
              - link "Search" [ref=e232] [cursor=pointer]:
                - /url: /search
            - listitem [ref=e233]:
              - link "News" [ref=e234] [cursor=pointer]:
                - /url: /news
            - listitem [ref=e235]:
              - link "Blog" [ref=e236] [cursor=pointer]:
                - /url: /blog
            - listitem [ref=e237]:
              - link "Recently viewed products" [ref=e238] [cursor=pointer]:
                - /url: /recentlyviewedproducts
            - listitem [ref=e239]:
              - link "Compare products list" [ref=e240] [cursor=pointer]:
                - /url: /compareproducts
            - listitem [ref=e241]:
              - link "New products" [ref=e242] [cursor=pointer]:
                - /url: /newproducts
        - generic [ref=e243]:
          - heading "My account" [level=3] [ref=e244]
          - list [ref=e245]:
            - listitem [ref=e246]:
              - link "My account" [ref=e247] [cursor=pointer]:
                - /url: /customer/info
            - listitem [ref=e248]:
              - link "Orders" [ref=e249] [cursor=pointer]:
                - /url: /customer/orders
            - listitem [ref=e250]:
              - link "Addresses" [ref=e251] [cursor=pointer]:
                - /url: /customer/addresses
            - listitem [ref=e252]:
              - link "Shopping cart" [ref=e253] [cursor=pointer]:
                - /url: /cart
            - listitem [ref=e254]:
              - link "Wishlist" [ref=e255] [cursor=pointer]:
                - /url: /wishlist
        - generic [ref=e256]:
          - heading "Follow us" [level=3] [ref=e257]
          - list [ref=e258]:
            - listitem [ref=e259]:
              - link "Facebook" [ref=e260] [cursor=pointer]:
                - /url: http://www.facebook.com/nopCommerce
            - listitem [ref=e261]:
              - link "Twitter" [ref=e262] [cursor=pointer]:
                - /url: https://twitter.com/nopCommerce
            - listitem [ref=e263]:
              - link "RSS" [ref=e264] [cursor=pointer]:
                - /url: /news/rss/1
            - listitem [ref=e265]:
              - link "YouTube" [ref=e266] [cursor=pointer]:
                - /url: http://www.youtube.com/user/nopCommerce
            - listitem [ref=e267]:
              - link "Google+" [ref=e268] [cursor=pointer]:
                - /url: https://plus.google.com/+nopcommerce
      - generic [ref=e269]:
        - text: Powered by
        - link "nopCommerce" [ref=e270] [cursor=pointer]:
          - /url: http://www.nopcommerce.com/
      - generic [ref=e271]: Copyright © 2026 Tricentis Demo Web Shop. All rights reserved.
```

# Test source

```ts
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
  141 |       await expect(page.locator('input[type="email"], input[name*="email"]')).toBeVisible();
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
> 167 |           await cartLink.click();
      |                          ^ Error: locator.click: Error: strict mode violation: locator('a:has-text("Cart")') resolved to 3 elements:
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
  242 |       // Look for payment options
  243 |       const paymentMethods = page.locator('input[name*="payment"], input[type="radio"]');
  244 |       if (await paymentMethods.count() > 0) {
  245 |         await expect(paymentMethods.first()).toBeVisible();
  246 |       }
  247 |     });
  248 |   });
  249 | 
  250 |   test.describe('6. User Account Management', () => {
  251 |     test('Account page accessible when logged in', async ({ page }) => {
  252 |       // Try to access account
  253 |       await page.goto(`${BASE_URL}/customer/account`);
  254 | 
  255 |       // Should either show account page or redirect to login
  256 |       await page.waitForLoadState('networkidle');
  257 |       const isLoggedIn = await page.url().includes('/account');
  258 |       const isLoginPage = await page.url().includes('/login');
  259 | 
  260 |       expect(isLoggedIn || isLoginPage).toBeTruthy();
  261 |     });
  262 | 
  263 |     test('Order history displays', async ({ page }) => {
  264 |       await page.goto(`${BASE_URL}/customer/orders`);
  265 | 
  266 |       await page.waitForLoadState('networkidle');
  267 |       // Page should load without errors
```