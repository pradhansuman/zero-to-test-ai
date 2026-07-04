# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: demowebshop.spec.ts >> Tricentis Demo Web Shop - 70 Approved Tests >> Functional - Core Features >> Product filtering works
- Location: tests/e2e/demowebshop.spec.ts:125:9

# Error details

```
Error: locator.count: Unexpected token "/" while parsing css selector "[class*="filter"], button:has-text(/sort|filter/i)". Did you mean to CSS.escape it?
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
  28  |     test('Product category links present', async ({ page }) => {
  29  |       await page.goto(BASE_URL);
  30  |       const categories = page.locator('a').filter({ hasText: /books|computers|electronics|apparel|gifts/i });
  31  |       await expect(categories.first()).toBeVisible();
  32  |     });
  33  | 
  34  |     test('Search bar accessible', async ({ page }) => {
  35  |       await page.goto(BASE_URL);
  36  |       const search = page.locator('input[type="search"], input[placeholder*="search"], input[name*="q"]').first();
  37  |       if (await search.count() > 0) {
  38  |         await expect(search).toBeVisible();
  39  |       }
  40  |     });
  41  | 
  42  |     test('Shopping cart button visible', async ({ page }) => {
  43  |       await page.goto(BASE_URL);
  44  |       const cart = page.locator('[class*="cart"], a:has-text("Cart"), button:has-text("Cart")').first();
  45  |       if (await cart.count() > 0) {
  46  |         await expect(cart).toBeVisible();
  47  |       }
  48  |     });
  49  | 
  50  |     test('Footer content displays', async ({ page }) => {
  51  |       await page.goto(BASE_URL);
  52  |       await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  53  |       const footer = page.locator('footer, [class*="footer"]').first();
  54  |       if (await footer.count() > 0) {
  55  |         await expect(footer).toBeVisible();
  56  |       }
  57  |     });
  58  | 
  59  |     test('Product listing page loads', async ({ page }) => {
  60  |       await page.goto(`${BASE_URL}/books`);
  61  |       await expect(page).toHaveURL(/.*books/i);
  62  |     });
  63  | 
  64  |     test('Product cards display', async ({ page }) => {
  65  |       await page.goto(`${BASE_URL}/books`);
  66  |       const product = page.locator('[class*="product"], .product-item, article').first();
  67  |       if (await product.count() > 0) {
  68  |         await expect(product).toBeVisible();
  69  |       }
  70  |     });
  71  | 
  72  |     test('Product detail page accessible', async ({ page }) => {
  73  |       await page.goto(`${BASE_URL}/books`);
  74  |       const productLink = page.locator('a[href*="/p/"], a[href*="/product"]').first();
  75  |       if (await productLink.count() > 0) {
  76  |         await productLink.click();
  77  |         await page.waitForLoadState('networkidle');
  78  |         const detail = page.locator('h1, [class*="title"], [class*="name"]').first();
  79  |         await expect(detail).toBeVisible();
  80  |       }
  81  |     });
  82  | 
  83  |     test('Price displays on product card', async ({ page }) => {
  84  |       await page.goto(`${BASE_URL}/books`);
  85  |       const price = page.locator('text=/\\$[0-9]/, [class*="price"]').first();
  86  |       if (await price.count() > 0) {
  87  |         await expect(price).toBeVisible();
  88  |       }
  89  |     });
  90  | 
  91  |     test('Add to cart button present', async ({ page }) => {
  92  |       await page.goto(`${BASE_URL}/books`);
  93  |       const addBtn = page.locator('button, input[type="button"], a').filter({ hasText: /add|cart/i }).first();
  94  |       if (await addBtn.count() > 0) {
  95  |         await expect(addBtn).toBeVisible();
  96  |       }
  97  |     });
  98  | 
  99  |     test('Page loads without JavaScript errors', async ({ page }) => {
  100 |       let errorCount = 0;
  101 |       page.on('console', msg => {
  102 |         if (msg.type() === 'error') errorCount++;
  103 |       });
  104 |       await page.goto(BASE_URL);
  105 |       expect(errorCount).toBeLessThan(3);
  106 |     });
  107 |   });
  108 | 
  109 |   // ═══════════════════════════════════════════════════════════════════
  110 |   // PHASE 2: FUNCTIONAL TESTS (20 tests)
  111 |   // ═══════════════════════════════════════════════════════════════════
  112 | 
  113 |   test.describe('Functional - Core Features', () => {
  114 |     test('Search returns results', async ({ page }) => {
  115 |       await page.goto(BASE_URL);
  116 |       const search = page.locator('input[type="search"], input[name*="q"], input[placeholder*="search"]').first();
  117 |       if (await search.count() > 0) {
  118 |         await search.fill('book');
  119 |         await page.keyboard.press('Enter');
  120 |         await page.waitForLoadState('networkidle');
  121 |         await expect(page).toHaveURL(/.*search|.*product/i);
  122 |       }
  123 |     });
  124 | 
  125 |     test('Product filtering works', async ({ page }) => {
  126 |       await page.goto(`${BASE_URL}/books`);
  127 |       const filterBtn = page.locator('[class*="filter"], button:has-text(/sort|filter/i)').first();
> 128 |       if (await filterBtn.count() > 0) {
      |                           ^ Error: locator.count: Unexpected token "/" while parsing css selector "[class*="filter"], button:has-text(/sort|filter/i)". Did you mean to CSS.escape it?
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
  224 |       await page.waitForLoadState('networkidle');
  225 |     });
  226 | 
  227 |     test('Wishlist link present', async ({ page }) => {
  228 |       await page.goto(BASE_URL);
```