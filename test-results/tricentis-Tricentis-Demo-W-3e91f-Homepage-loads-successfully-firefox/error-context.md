# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: tricentis.spec.ts >> Tricentis Demo Web Shop - E-Commerce Suite >> 1. Homepage & Navigation >> Homepage loads successfully
- Location: tests/e2e/tricentis.spec.ts:15:9

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: page.goto: Test timeout of 30000ms exceeded.
Call log:
  - navigating to "https://demowebshop.tricentis.com/", waiting until "load"

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
  1   | import { test, expect, Page } from '@playwright/test';
  2   | 
  3   | const BASE_URL = 'https://demowebshop.tricentis.com';
  4   | 
  5   | // Test data
  6   | const testUser = {
  7   |   email: `test-${Date.now()}@example.com`,
  8   |   firstName: 'Test',
  9   |   lastName: 'User',
  10  |   password: 'Test@123456'
  11  | };
  12  | 
  13  | test.describe('Tricentis Demo Web Shop - E-Commerce Suite', () => {
  14  |   test.describe('1. Homepage & Navigation', () => {
  15  |     test('Homepage loads successfully', async ({ page }) => {
> 16  |       await page.goto(BASE_URL);
      |                  ^ Error: page.goto: Test timeout of 30000ms exceeded.
  17  |       await expect(page).toHaveTitle(/tricentis|demowebshop/i);
  18  | 
  19  |       // Verify key elements
  20  |       const logo = page.locator('[class*="logo"]').first();
  21  |       await expect(logo).toBeVisible();
  22  |     });
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
```