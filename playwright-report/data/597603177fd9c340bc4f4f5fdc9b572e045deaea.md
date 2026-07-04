# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: tricentis.spec.ts >> Tricentis Demo Web Shop - E-Commerce Suite >> 2. Product Catalog & Filtering >> Products display with prices
- Location: tests/e2e/tricentis.spec.ts:54:9

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('text=/\\$[0-9]+/').first()
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('text=/\\$[0-9]+/').first()

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
- strong: Newsletter
- text: "Sign up for our newsletter:"
- textbox
- button "Subscribe"
- list:
  - listitem:
    - link "Home":
      - /url: /
    - text: /
  - listitem:
    - strong: Books
- heading "Books" [level=1]
- text: View as
- combobox:
  - option "Grid" [selected]
  - option "List"
- text: Sort by
- combobox:
  - option "Position" [selected]
  - 'option "Name: A to Z"'
  - 'option "Name: Z to A"'
  - 'option "Price: Low to High"'
  - 'option "Price: High to Low"'
  - option "Created on"
- text: Display
- combobox:
  - option "4"
  - option "8" [selected]
  - option "12"
- text: per page
- strong: Filter by price
- list:
  - listitem:
    - link "Under 25.00":
      - /url: https://demowebshop.tricentis.com/books?price=-25
  - listitem:
    - link "25.00 - 50.00":
      - /url: https://demowebshop.tricentis.com/books?price=25-50
  - listitem:
    - link "Over 50.00":
      - /url: https://demowebshop.tricentis.com/books?price=50-
- link "Picture of Computing and Internet":
  - /url: /computing-and-internet
  - img "Picture of Computing and Internet"
- heading "Computing and Internet" [level=2]:
  - link "Computing and Internet":
    - /url: /computing-and-internet
- text: 30.00 10.00
- button "Add to cart"
- link "Picture of Copy of Computing and Internet EX":
  - /url: /copy-of-computing-and-internet
  - img "Picture of Copy of Computing and Internet EX"
- heading "Copy of Computing and Internet EX" [level=2]:
  - link "Copy of Computing and Internet EX":
    - /url: /copy-of-computing-and-internet
- text: 30.00 10.00
- link "Picture of Fiction":
  - /url: /fiction
  - img "Picture of Fiction"
- heading "Fiction" [level=2]:
  - link "Fiction":
    - /url: /fiction
- text: 35.00 24.00
- button "Add to cart"
- link "Picture of Fiction EX":
  - /url: /fiction-ex
  - img "Picture of Fiction EX"
- heading "Fiction EX" [level=2]:
  - link "Fiction EX":
    - /url: /fiction-ex
- text: 35.00 24.00
- link "Picture of Health Book":
  - /url: /health
  - img "Picture of Health Book"
- heading "Health Book" [level=2]:
  - link "Health Book":
    - /url: /health
- text: 27.00 10.00
- button "Add to cart"
- link "Picture of Science":
  - /url: /science
  - img "Picture of Science"
- heading "Science" [level=2]:
  - link "Science":
    - /url: /science
- text: 67.00 51.00
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
> 62  |       await expect(price).toBeVisible();
      |                           ^ Error: expect(locator).toBeVisible() failed
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
```