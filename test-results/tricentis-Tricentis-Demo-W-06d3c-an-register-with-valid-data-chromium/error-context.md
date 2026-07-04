# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: tricentis.spec.ts >> Tricentis Demo Web Shop - E-Commerce Suite >> 3. User Registration & Authentication >> User can register with valid data
- Location: tests/e2e/tricentis.spec.ts:110:9

# Error details

```
Error: locator.fill: Error: strict mode violation: locator('input[name*="Email"], input[placeholder*="Email"]') resolved to 2 elements:
    1) <input value="" type="text" id="newsletter-email" name="NewsletterEmail"/> aka locator('#newsletter-email')
    2) <input value="" id="Email" type="text" name="Email" data-val="true" class="text-box single-line" data-val-email="Wrong email" data-val-required="Email is required."/> aka getByRole('textbox', { name: 'Email:' })

Call log:
  - waiting for locator('input[name*="Email"], input[placeholder*="Email"]')

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
      - generic [ref=e82]:
        - heading "Register" [level=1] [ref=e84]
        - generic [ref=e85]:
          - generic [ref=e86]:
            - strong [ref=e88]: Your Personal Details
            - generic [ref=e89]:
              - generic [ref=e90]:
                - generic [ref=e91]: "Gender:"
                - generic [ref=e92]:
                  - radio "Male" [ref=e93]
                  - text: Male
                - generic [ref=e94]:
                  - radio "Female" [ref=e95]
                  - text: Female
              - generic [ref=e96]:
                - generic [ref=e97]: "First name:"
                - textbox "First name:" [ref=e98]: Test
                - text: "*"
              - generic [ref=e99]:
                - generic [ref=e100]: "Last name:"
                - textbox "Last name:" [active] [ref=e101]: User
                - text: "*"
              - generic [ref=e102]:
                - generic [ref=e103]: "Email:"
                - textbox "Email:" [ref=e104]
                - text: "*"
          - generic [ref=e105]:
            - strong [ref=e107]: Your Password
            - generic [ref=e108]:
              - generic [ref=e109]:
                - generic [ref=e110]: "Password:"
                - textbox "Password:" [ref=e111]
                - text: "*"
              - generic [ref=e112]:
                - generic [ref=e113]: "Confirm password:"
                - textbox "Confirm password:" [ref=e114]
                - text: "*"
          - button "Register" [ref=e116] [cursor=pointer]
  - generic [ref=e117]:
    - generic [ref=e118]:
      - generic [ref=e119]:
        - heading "Information" [level=3] [ref=e120]
        - list [ref=e121]:
          - listitem [ref=e122]:
            - link "Sitemap" [ref=e123] [cursor=pointer]:
              - /url: /sitemap
          - listitem [ref=e124]:
            - link "Shipping & Returns" [ref=e125] [cursor=pointer]:
              - /url: /shipping-returns
          - listitem [ref=e126]:
            - link "Privacy Notice" [ref=e127] [cursor=pointer]:
              - /url: /privacy-policy
          - listitem [ref=e128]:
            - link "Conditions of Use" [ref=e129] [cursor=pointer]:
              - /url: /conditions-of-use
          - listitem [ref=e130]:
            - link "About us" [ref=e131] [cursor=pointer]:
              - /url: /about-us
          - listitem [ref=e132]:
            - link "Contact us" [ref=e133] [cursor=pointer]:
              - /url: /contactus
      - generic [ref=e134]:
        - heading "Customer service" [level=3] [ref=e135]
        - list [ref=e136]:
          - listitem [ref=e137]:
            - link "Search" [ref=e138] [cursor=pointer]:
              - /url: /search
          - listitem [ref=e139]:
            - link "News" [ref=e140] [cursor=pointer]:
              - /url: /news
          - listitem [ref=e141]:
            - link "Blog" [ref=e142] [cursor=pointer]:
              - /url: /blog
          - listitem [ref=e143]:
            - link "Recently viewed products" [ref=e144] [cursor=pointer]:
              - /url: /recentlyviewedproducts
          - listitem [ref=e145]:
            - link "Compare products list" [ref=e146] [cursor=pointer]:
              - /url: /compareproducts
          - listitem [ref=e147]:
            - link "New products" [ref=e148] [cursor=pointer]:
              - /url: /newproducts
      - generic [ref=e149]:
        - heading "My account" [level=3] [ref=e150]
        - list [ref=e151]:
          - listitem [ref=e152]:
            - link "My account" [ref=e153] [cursor=pointer]:
              - /url: /customer/info
          - listitem [ref=e154]:
            - link "Orders" [ref=e155] [cursor=pointer]:
              - /url: /customer/orders
          - listitem [ref=e156]:
            - link "Addresses" [ref=e157] [cursor=pointer]:
              - /url: /customer/addresses
          - listitem [ref=e158]:
            - link "Shopping cart" [ref=e159] [cursor=pointer]:
              - /url: /cart
          - listitem [ref=e160]:
            - link "Wishlist" [ref=e161] [cursor=pointer]:
              - /url: /wishlist
      - generic [ref=e162]:
        - heading "Follow us" [level=3] [ref=e163]
        - list [ref=e164]:
          - listitem [ref=e165]:
            - link "Facebook" [ref=e166] [cursor=pointer]:
              - /url: http://www.facebook.com/nopCommerce
          - listitem [ref=e167]:
            - link "Twitter" [ref=e168] [cursor=pointer]:
              - /url: https://twitter.com/nopCommerce
          - listitem [ref=e169]:
            - link "RSS" [ref=e170] [cursor=pointer]:
              - /url: /news/rss/1
          - listitem [ref=e171]:
            - link "YouTube" [ref=e172] [cursor=pointer]:
              - /url: http://www.youtube.com/user/nopCommerce
          - listitem [ref=e173]:
            - link "Google+" [ref=e174] [cursor=pointer]:
              - /url: https://plus.google.com/+nopcommerce
    - generic [ref=e175]:
      - text: Powered by
      - link "nopCommerce" [ref=e176] [cursor=pointer]:
        - /url: http://www.nopcommerce.com/
    - generic [ref=e177]: Copyright © 2026 Tricentis Demo Web Shop. All rights reserved.
```

# Test source

```ts
  23  | 
  24  |     test('Main navigation menu is accessible', async ({ page }) => {
  25  |       await page.goto(BASE_URL);
  26  | 
  27  |       // Check for main categories
  28  |       const categories = ['Books', 'Computers', 'Electronics', 'Apparel', 'Digital downloads', 'Gifts'];
  29  | 
  30  |       for (const category of categories) {
  31  |         const navItem = page.locator(`text=${category}`);
  32  |         if (await navItem.count() > 0) {
  33  |           await expect(navItem.first()).toBeVisible();
  34  |         }
  35  |       }
  36  |     });
  37  | 
  38  |     test('Search functionality works', async ({ page }) => {
  39  |       await page.goto(BASE_URL);
  40  | 
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
> 123 |         await emailInput.fill(testUser.email);
      |                          ^ Error: locator.fill: Error: strict mode violation: locator('input[name*="Email"], input[placeholder*="Email"]') resolved to 2 elements:
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
```