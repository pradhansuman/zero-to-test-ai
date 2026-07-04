# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: demowebshop.spec.ts >> Tricentis Demo Web Shop - 70 Approved Tests >> UI & Navigation >> Homepage loads successfully
- Location: tests/e2e/demowebshop.spec.ts:11:9

# Error details

```
Error: expect(page).toHaveTitle(expected) failed

Expected pattern: /tricentis|demowebshop/i
Received string:  "Demo Web Shop"
Timeout: 5000ms

Call log:
  - Expect "toHaveTitle" with timeout 5000ms
    11 × unexpected value "Demo Web Shop"

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
- strong: Categories
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
- strong: Manufacturers
- list:
  - listitem:
    - link "Tricentis":
      - /url: /tricentis
- strong: Popular tags
- list:
  - listitem:
    - link "apparel":
      - /url: /producttag/4/apparel
  - listitem:
    - link "awesome":
      - /url: /producttag/8/awesome
  - listitem:
    - link "book":
      - /url: /producttag/10/book
  - listitem:
    - link "camera":
      - /url: /producttag/13/camera
  - listitem:
    - link "cell":
      - /url: /producttag/12/cell
  - listitem:
    - link "compact":
      - /url: /producttag/9/compact
  - listitem:
    - link "computer":
      - /url: /producttag/6/computer
  - listitem:
    - link "cool":
      - /url: /producttag/3/cool
  - listitem:
    - link "digital":
      - /url: /producttag/16/digital
  - listitem:
    - link "jeans":
      - /url: /producttag/14/jeans
  - listitem:
    - link "jewelry":
      - /url: /producttag/11/jewelry
  - listitem:
    - link "nice":
      - /url: /producttag/1/nice
  - listitem:
    - link "shirt":
      - /url: /producttag/5/shirt
  - listitem:
    - link "shoes":
      - /url: /producttag/7/shoes
  - listitem:
    - link "TCP":
      - /url: /producttag/19/tcp
- link "View all":
  - /url: /producttag/all
- strong: Newsletter
- text: "Sign up for our newsletter:"
- textbox
- button "Subscribe"
- strong: Community poll
- strong: Do you like nopCommerce?
- list:
  - listitem:
    - radio "Excellent"
    - text: Excellent
  - listitem:
    - radio "Good"
    - text: Good
  - listitem:
    - radio "Poor"
    - text: Poor
  - listitem:
    - radio "Very bad"
    - text: Very bad
- button "Vote"
- link:
  - /url: https://academy.tricentis.com
- img
- text: Tricentis Academy Prev Next
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- img
- text: 1 2
- heading "Welcome to our store" [level=2]
- paragraph: Welcome to the new Tricentis store!
- paragraph: Feel free to shop around and explore everything.
- strong: Featured products
- link "Picture of $25 Virtual Gift Card":
  - /url: /25-virtual-gift-card
  - img "Picture of $25 Virtual Gift Card"
- heading "$25 Virtual Gift Card" [level=2]:
  - link "$25 Virtual Gift Card":
    - /url: /25-virtual-gift-card
- text: "25.00"
- button "Add to cart"
- link "Picture of 14.1-inch Laptop":
  - /url: /141-inch-laptop
  - img "Picture of 14.1-inch Laptop"
- heading "14.1-inch Laptop" [level=2]:
  - link "14.1-inch Laptop":
    - /url: /141-inch-laptop
- text: "1590.00"
- button "Add to cart"
- link "Picture of Build your own cheap computer":
  - /url: /build-your-cheap-own-computer
  - img "Picture of Build your own cheap computer"
- heading "Build your own cheap computer" [level=2]:
  - link "Build your own cheap computer":
    - /url: /build-your-cheap-own-computer
- text: "800.00"
- button "Add to cart"
- link "Picture of Build your own computer":
  - /url: /build-your-own-computer
  - img "Picture of Build your own computer"
- heading "Build your own computer" [level=2]:
  - link "Build your own computer":
    - /url: /build-your-own-computer
- text: "1200.00"
- button "Add to cart"
- link "Picture of Build your own expensive computer":
  - /url: /build-your-own-expensive-computer-2
  - img "Picture of Build your own expensive computer"
- heading "Build your own expensive computer" [level=2]:
  - link "Build your own expensive computer":
    - /url: /build-your-own-expensive-computer-2
- text: "1800.00"
- button "Add to cart"
- link "Picture of Simple Computer":
  - /url: /simple-computer
  - img "Picture of Simple Computer"
- heading "Simple Computer" [level=2]:
  - link "Simple Computer":
    - /url: /simple-computer
- text: "800.00"
- button "Add to cart"
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
  1   | import { test, expect, Page } from '@playwright/test';
  2   | 
  3   | const BASE_URL = 'https://demowebshop.tricentis.com';
  4   | 
  5   | test.describe('Tricentis Demo Web Shop - 70 Approved Tests', () => {
  6   |   // ═══════════════════════════════════════════════════════════════════
  7   |   // PHASE 1: UI & NAVIGATION TESTS (15 tests)
  8   |   // ═══════════════════════════════════════════════════════════════════
  9   | 
  10  |   test.describe('UI & Navigation', () => {
  11  |     test('Homepage loads successfully', async ({ page }) => {
  12  |       await page.goto(BASE_URL);
> 13  |       await expect(page).toHaveTitle(/tricentis|demowebshop/i);
      |                          ^ Error: expect(page).toHaveTitle(expected) failed
  14  |     });
  15  | 
  16  |     test('Homepage displays main content', async ({ page }) => {
  17  |       await page.goto(BASE_URL);
  18  |       const mainContent = page.locator('main, [role="main"], body').first();
  19  |       await expect(mainContent).toBeVisible();
  20  |     });
  21  | 
  22  |     test('Navigation menu is visible', async ({ page }) => {
  23  |       await page.goto(BASE_URL);
  24  |       const nav = page.locator('nav, [class*="menu"], [class*="navigation"]').first();
  25  |       await expect(nav).toBeVisible();
  26  |     });
  27  | 
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
```