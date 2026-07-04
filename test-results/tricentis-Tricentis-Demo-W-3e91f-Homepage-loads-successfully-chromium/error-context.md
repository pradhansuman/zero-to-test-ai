# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: tricentis.spec.ts >> Tricentis Demo Web Shop - E-Commerce Suite >> 1. Homepage & Navigation >> Homepage loads successfully
- Location: tests/e2e/tricentis.spec.ts:15:9

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
  16  |       await page.goto(BASE_URL);
> 17  |       await expect(page).toHaveTitle(/tricentis|demowebshop/i);
      |                          ^ Error: expect(page).toHaveTitle(expected) failed
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
  117 |       const passwordInput = page.locator('input[name*="Password"][type="password"]').first();
```