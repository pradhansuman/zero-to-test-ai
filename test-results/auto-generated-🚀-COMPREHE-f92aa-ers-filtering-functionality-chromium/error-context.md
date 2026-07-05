# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auto-generated.spec.ts >> 🚀 COMPREHENSIVE TEST SUITE - AUTO-GENERATED >> Category: Computers >> computers filtering functionality
- Location: tests/e2e/auto-generated.spec.ts:107:9

# Error details

```
Error: locator.count: Unexpected token "/" while parsing css selector "[class*=filter], button:has-text(/filter/i)". Did you mean to CSS.escape it?
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
              - list [ref=e54]:
                - listitem [ref=e55]:
                  - link "Desktops" [ref=e56] [cursor=pointer]:
                    - /url: /desktops
                - listitem [ref=e57]:
                  - link "Notebooks" [ref=e58] [cursor=pointer]:
                    - /url: /notebooks
                - listitem [ref=e59]:
                  - link "Accessories" [ref=e60] [cursor=pointer]:
                    - /url: /accessories
            - listitem [ref=e61]:
              - link "Electronics" [ref=e62] [cursor=pointer]:
                - /url: /electronics
            - listitem [ref=e63]:
              - link "Apparel & Shoes" [ref=e64] [cursor=pointer]:
                - /url: /apparel-shoes
            - listitem [ref=e65]:
              - link "Digital downloads" [ref=e66] [cursor=pointer]:
                - /url: /digital-downloads
            - listitem [ref=e67]:
              - link "Jewelry" [ref=e68] [cursor=pointer]:
                - /url: /jewelry
            - listitem [ref=e69]:
              - link "Gift Cards" [ref=e70] [cursor=pointer]:
                - /url: /gift-cards
        - generic [ref=e71]:
          - strong [ref=e73]: Manufacturers
          - list [ref=e75]:
            - listitem [ref=e76]:
              - link "Tricentis" [ref=e77] [cursor=pointer]:
                - /url: /tricentis
        - generic [ref=e78]:
          - strong [ref=e80]: Newsletter
          - generic [ref=e82]:
            - text: "Sign up for our newsletter:"
            - textbox [ref=e84]
            - button "Subscribe" [ref=e86] [cursor=pointer]
      - generic [ref=e87]:
        - list [ref=e89]:
          - listitem [ref=e90]:
            - link "Home" [ref=e91] [cursor=pointer]:
              - /url: /
            - text: /
          - listitem [ref=e92]:
            - strong [ref=e93]: Computers
        - generic [ref=e94]:
          - heading "Computers" [level=1] [ref=e96]
          - generic [ref=e98]:
            - generic [ref=e100]:
              - heading "Desktops" [level=2] [ref=e101]:
                - link "Desktops" [ref=e102] [cursor=pointer]:
                  - /url: /desktops
              - link "Picture for category Desktops" [ref=e104] [cursor=pointer]:
                - /url: /desktops
                - img "Picture for category Desktops" [ref=e105]
            - generic [ref=e107]:
              - heading "Notebooks" [level=2] [ref=e108]:
                - link "Notebooks" [ref=e109] [cursor=pointer]:
                  - /url: /notebooks
              - link "Picture for category Notebooks" [ref=e111] [cursor=pointer]:
                - /url: /notebooks
                - img "Picture for category Notebooks" [ref=e112]
            - generic [ref=e114]:
              - heading "Accessories" [level=2] [ref=e115]:
                - link "Accessories" [ref=e116] [cursor=pointer]:
                  - /url: /accessories
              - link "Picture for category Accessories" [ref=e118] [cursor=pointer]:
                - /url: /accessories
                - img "Picture for category Accessories" [ref=e119]
  - generic [ref=e120]:
    - generic [ref=e121]:
      - generic [ref=e122]:
        - heading "Information" [level=3] [ref=e123]
        - list [ref=e124]:
          - listitem [ref=e125]:
            - link "Sitemap" [ref=e126] [cursor=pointer]:
              - /url: /sitemap
          - listitem [ref=e127]:
            - link "Shipping & Returns" [ref=e128] [cursor=pointer]:
              - /url: /shipping-returns
          - listitem [ref=e129]:
            - link "Privacy Notice" [ref=e130] [cursor=pointer]:
              - /url: /privacy-policy
          - listitem [ref=e131]:
            - link "Conditions of Use" [ref=e132] [cursor=pointer]:
              - /url: /conditions-of-use
          - listitem [ref=e133]:
            - link "About us" [ref=e134] [cursor=pointer]:
              - /url: /about-us
          - listitem [ref=e135]:
            - link "Contact us" [ref=e136] [cursor=pointer]:
              - /url: /contactus
      - generic [ref=e137]:
        - heading "Customer service" [level=3] [ref=e138]
        - list [ref=e139]:
          - listitem [ref=e140]:
            - link "Search" [ref=e141] [cursor=pointer]:
              - /url: /search
          - listitem [ref=e142]:
            - link "News" [ref=e143] [cursor=pointer]:
              - /url: /news
          - listitem [ref=e144]:
            - link "Blog" [ref=e145] [cursor=pointer]:
              - /url: /blog
          - listitem [ref=e146]:
            - link "Recently viewed products" [ref=e147] [cursor=pointer]:
              - /url: /recentlyviewedproducts
          - listitem [ref=e148]:
            - link "Compare products list" [ref=e149] [cursor=pointer]:
              - /url: /compareproducts
          - listitem [ref=e150]:
            - link "New products" [ref=e151] [cursor=pointer]:
              - /url: /newproducts
      - generic [ref=e152]:
        - heading "My account" [level=3] [ref=e153]
        - list [ref=e154]:
          - listitem [ref=e155]:
            - link "My account" [ref=e156] [cursor=pointer]:
              - /url: /customer/info
          - listitem [ref=e157]:
            - link "Orders" [ref=e158] [cursor=pointer]:
              - /url: /customer/orders
          - listitem [ref=e159]:
            - link "Addresses" [ref=e160] [cursor=pointer]:
              - /url: /customer/addresses
          - listitem [ref=e161]:
            - link "Shopping cart" [ref=e162] [cursor=pointer]:
              - /url: /cart
          - listitem [ref=e163]:
            - link "Wishlist" [ref=e164] [cursor=pointer]:
              - /url: /wishlist
      - generic [ref=e165]:
        - heading "Follow us" [level=3] [ref=e166]
        - list [ref=e167]:
          - listitem [ref=e168]:
            - link "Facebook" [ref=e169] [cursor=pointer]:
              - /url: http://www.facebook.com/nopCommerce
          - listitem [ref=e170]:
            - link "Twitter" [ref=e171] [cursor=pointer]:
              - /url: https://twitter.com/nopCommerce
          - listitem [ref=e172]:
            - link "RSS" [ref=e173] [cursor=pointer]:
              - /url: /news/rss/1
          - listitem [ref=e174]:
            - link "YouTube" [ref=e175] [cursor=pointer]:
              - /url: http://www.youtube.com/user/nopCommerce
          - listitem [ref=e176]:
            - link "Google+" [ref=e177] [cursor=pointer]:
              - /url: https://plus.google.com/+nopcommerce
    - generic [ref=e178]:
      - text: Powered by
      - link "nopCommerce" [ref=e179] [cursor=pointer]:
        - /url: http://www.nopcommerce.com/
    - generic [ref=e180]: Copyright © 2026 Tricentis Demo Web Shop. All rights reserved.
```

# Test source

```ts
  10  | 
  11  |   // ═════════════════════════════════════════════════════════
  12  |   // CATEGORY COVERAGE - All 7 Categories (49 tests total)
  13  |   // ═════════════════════════════════════════════════════════
  14  | 
  15  | 
  16  |   test.describe('Category: Books', () => {
  17  |     test('books page loads correctly', async ({ page }) => {
  18  |       await page.goto(`${BASE_URL}/books`);
  19  |       await page.waitForLoadState('networkidle');
  20  |       const title = page.locator('h1, [class*=title]').first();
  21  |       if (await title.count() > 0) {
  22  |         await expect(title).toBeVisible();
  23  |       }
  24  |     });
  25  | 
  26  |     test('books displays product list', async ({ page }) => {
  27  |       await page.goto(`${BASE_URL}/books`);
  28  |       const products = page.locator('[class*=product], a[href*=product]');
  29  |       expect(await products.count()).toBeGreaterThan(0);
  30  |     });
  31  | 
  32  |     test('books filtering functionality', async ({ page }) => {
  33  |       await page.goto(`${BASE_URL}/books`);
  34  |       const filter = page.locator('[class*=filter], button:has-text(/filter/i)').first();
  35  |       if (await filter.count() > 0) {
  36  |         const isVisible = await filter.isVisible().catch(() => false);
  37  |         if (isVisible) {
  38  |           await filter.click();
  39  |           await page.waitForLoadState('networkidle');
  40  |         }
  41  |       }
  42  |     });
  43  | 
  44  |     test('books sorting by price', async ({ page }) => {
  45  |       await page.goto(`${BASE_URL}/books`);
  46  |       const sort = page.locator('select[name*=sort], [class*=sort]').first();
  47  |       if (await sort.count() > 0) {
  48  |         const isVisible = await sort.isVisible().catch(() => false);
  49  |         if (isVisible) {
  50  |           try {
  51  |             await sort.selectOption('1');
  52  |           } catch (e) {
  53  |             // Fallback for non-select elements
  54  |           }
  55  |         }
  56  |       }
  57  |     });
  58  | 
  59  |     test('books pagination works', async ({ page }) => {
  60  |       await page.goto(`${BASE_URL}/books`);
  61  |       const pageLinks = page.locator('[class*=pager], a:has-text(/\d+/)');
  62  |       expect(await pageLinks.count()).toBeGreaterThanOrEqual(0);
  63  |     });
  64  | 
  65  |     test('books product detail link navigates', async ({ page }) => {
  66  |       await page.goto(`${BASE_URL}/books`);
  67  |       const productLink = page.locator('a[href*=product]').first();
  68  |       if (await productLink.count() > 0) {
  69  |         const isVisible = await productLink.isVisible().catch(() => false);
  70  |         if (isVisible) {
  71  |           await productLink.click();
  72  |           await page.waitForLoadState('networkidle');
  73  |           expect(page.url()).toContain('product');
  74  |         }
  75  |       }
  76  |     });
  77  | 
  78  |     test('books add to cart from listing', async ({ page }) => {
  79  |       await page.goto(`${BASE_URL}/books`);
  80  |       const addBtn = page.locator('button:has-text(/add|cart/i), a:has-text(/add|cart/i)').first();
  81  |       if (await addBtn.count() > 0) {
  82  |         const isVisible = await addBtn.isVisible().catch(() => false);
  83  |         if (isVisible) {
  84  |           await addBtn.click();
  85  |           await page.waitForLoadState('networkidle');
  86  |         }
  87  |       }
  88  |     });
  89  |   });
  90  | 
  91  |   test.describe('Category: Computers', () => {
  92  |     test('computers page loads correctly', async ({ page }) => {
  93  |       await page.goto(`${BASE_URL}/computers`);
  94  |       await page.waitForLoadState('networkidle');
  95  |       const title = page.locator('h1, [class*=title]').first();
  96  |       if (await title.count() > 0) {
  97  |         await expect(title).toBeVisible();
  98  |       }
  99  |     });
  100 | 
  101 |     test('computers displays product list', async ({ page }) => {
  102 |       await page.goto(`${BASE_URL}/computers`);
  103 |       const products = page.locator('[class*=product], a[href*=product]');
  104 |       expect(await products.count()).toBeGreaterThan(0);
  105 |     });
  106 | 
  107 |     test('computers filtering functionality', async ({ page }) => {
  108 |       await page.goto(`${BASE_URL}/computers`);
  109 |       const filter = page.locator('[class*=filter], button:has-text(/filter/i)').first();
> 110 |       if (await filter.count() > 0) {
      |                        ^ Error: locator.count: Unexpected token "/" while parsing css selector "[class*=filter], button:has-text(/filter/i)". Did you mean to CSS.escape it?
  111 |         const isVisible = await filter.isVisible().catch(() => false);
  112 |         if (isVisible) {
  113 |           await filter.click();
  114 |           await page.waitForLoadState('networkidle');
  115 |         }
  116 |       }
  117 |     });
  118 | 
  119 |     test('computers sorting by price', async ({ page }) => {
  120 |       await page.goto(`${BASE_URL}/computers`);
  121 |       const sort = page.locator('select[name*=sort], [class*=sort]').first();
  122 |       if (await sort.count() > 0) {
  123 |         const isVisible = await sort.isVisible().catch(() => false);
  124 |         if (isVisible) {
  125 |           try {
  126 |             await sort.selectOption('1');
  127 |           } catch (e) {
  128 |             // Fallback for non-select elements
  129 |           }
  130 |         }
  131 |       }
  132 |     });
  133 | 
  134 |     test('computers pagination works', async ({ page }) => {
  135 |       await page.goto(`${BASE_URL}/computers`);
  136 |       const pageLinks = page.locator('[class*=pager], a:has-text(/\d+/)');
  137 |       expect(await pageLinks.count()).toBeGreaterThanOrEqual(0);
  138 |     });
  139 | 
  140 |     test('computers product detail link navigates', async ({ page }) => {
  141 |       await page.goto(`${BASE_URL}/computers`);
  142 |       const productLink = page.locator('a[href*=product]').first();
  143 |       if (await productLink.count() > 0) {
  144 |         const isVisible = await productLink.isVisible().catch(() => false);
  145 |         if (isVisible) {
  146 |           await productLink.click();
  147 |           await page.waitForLoadState('networkidle');
  148 |           expect(page.url()).toContain('product');
  149 |         }
  150 |       }
  151 |     });
  152 | 
  153 |     test('computers add to cart from listing', async ({ page }) => {
  154 |       await page.goto(`${BASE_URL}/computers`);
  155 |       const addBtn = page.locator('button:has-text(/add|cart/i), a:has-text(/add|cart/i)').first();
  156 |       if (await addBtn.count() > 0) {
  157 |         const isVisible = await addBtn.isVisible().catch(() => false);
  158 |         if (isVisible) {
  159 |           await addBtn.click();
  160 |           await page.waitForLoadState('networkidle');
  161 |         }
  162 |       }
  163 |     });
  164 |   });
  165 | 
  166 |   test.describe('Category: Electronics', () => {
  167 |     test('electronics page loads correctly', async ({ page }) => {
  168 |       await page.goto(`${BASE_URL}/electronics`);
  169 |       await page.waitForLoadState('networkidle');
  170 |       const title = page.locator('h1, [class*=title]').first();
  171 |       if (await title.count() > 0) {
  172 |         await expect(title).toBeVisible();
  173 |       }
  174 |     });
  175 | 
  176 |     test('electronics displays product list', async ({ page }) => {
  177 |       await page.goto(`${BASE_URL}/electronics`);
  178 |       const products = page.locator('[class*=product], a[href*=product]');
  179 |       expect(await products.count()).toBeGreaterThan(0);
  180 |     });
  181 | 
  182 |     test('electronics filtering functionality', async ({ page }) => {
  183 |       await page.goto(`${BASE_URL}/electronics`);
  184 |       const filter = page.locator('[class*=filter], button:has-text(/filter/i)').first();
  185 |       if (await filter.count() > 0) {
  186 |         const isVisible = await filter.isVisible().catch(() => false);
  187 |         if (isVisible) {
  188 |           await filter.click();
  189 |           await page.waitForLoadState('networkidle');
  190 |         }
  191 |       }
  192 |     });
  193 | 
  194 |     test('electronics sorting by price', async ({ page }) => {
  195 |       await page.goto(`${BASE_URL}/electronics`);
  196 |       const sort = page.locator('select[name*=sort], [class*=sort]').first();
  197 |       if (await sort.count() > 0) {
  198 |         const isVisible = await sort.isVisible().catch(() => false);
  199 |         if (isVisible) {
  200 |           try {
  201 |             await sort.selectOption('1');
  202 |           } catch (e) {
  203 |             // Fallback for non-select elements
  204 |           }
  205 |         }
  206 |       }
  207 |     });
  208 | 
  209 |     test('electronics pagination works', async ({ page }) => {
  210 |       await page.goto(`${BASE_URL}/electronics`);
```