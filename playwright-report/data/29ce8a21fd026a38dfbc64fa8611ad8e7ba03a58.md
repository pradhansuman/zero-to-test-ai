# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auto-generated.spec.ts >> 🚀 COMPREHENSIVE TEST SUITE - AUTO-GENERATED >> Category: Apparel Shoes >> apparel-shoes filtering functionality
- Location: tests/e2e/auto-generated.spec.ts:257:9

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
            - strong [ref=e86]: Apparel & Shoes
        - generic [ref=e87]:
          - heading "Apparel & Shoes" [level=1] [ref=e89]
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
            - generic [ref=e98]:
              - generic [ref=e100]:
                - link "Picture of 50's Rockabilly Polka Dot Top JR Plus Size" [ref=e102] [cursor=pointer]:
                  - /url: /50s-rockabilly-polka-dot-top-jr-plus-size
                  - img "Picture of 50's Rockabilly Polka Dot Top JR Plus Size" [ref=e103]
                - generic [ref=e104]:
                  - heading "50's Rockabilly Polka Dot Top JR Plus Size" [level=2] [ref=e105]:
                    - link "50's Rockabilly Polka Dot Top JR Plus Size" [ref=e106] [cursor=pointer]:
                      - /url: /50s-rockabilly-polka-dot-top-jr-plus-size
                  - generic "557 review(s)" [ref=e107]
                  - generic [ref=e110]:
                    - generic [ref=e112]: "11.00"
                    - button "Add to cart" [ref=e114] [cursor=pointer]
              - generic [ref=e116]:
                - link "Picture of Blue and green Sneaker" [ref=e118] [cursor=pointer]:
                  - /url: /blue-and-green-sneaker
                  - img "Picture of Blue and green Sneaker" [ref=e119]
                - generic [ref=e120]:
                  - heading "Blue and green Sneaker" [level=2] [ref=e121]:
                    - link "Blue and green Sneaker" [ref=e122] [cursor=pointer]:
                      - /url: /blue-and-green-sneaker
                  - generic "360 review(s)" [ref=e123]
                  - generic [ref=e126]:
                    - generic [ref=e128]: "11.00"
                    - button "Add to cart" [ref=e130] [cursor=pointer]
              - generic [ref=e132]:
                - link "Picture of Blue Jeans" [ref=e134] [cursor=pointer]:
                  - /url: /blue-jeans
                  - img "Picture of Blue Jeans" [ref=e135]
                - generic [ref=e136]:
                  - heading "Blue Jeans" [level=2] [ref=e137]:
                    - link "Blue Jeans" [ref=e138] [cursor=pointer]:
                      - /url: /blue-jeans
                  - generic "698 review(s)" [ref=e139]
                  - generic [ref=e142]:
                    - generic [ref=e144]: "1.00"
                    - button "Add to cart" [ref=e146] [cursor=pointer]
              - generic [ref=e148]:
                - link "Picture of Casual Golf Belt" [ref=e150] [cursor=pointer]:
                  - /url: /casual-belt
                  - img "Picture of Casual Golf Belt" [ref=e151]
                - generic [ref=e152]:
                  - heading "Casual Golf Belt" [level=2] [ref=e153]:
                    - link "Casual Golf Belt" [ref=e154] [cursor=pointer]:
                      - /url: /casual-belt
                  - generic "228 review(s)" [ref=e155]
                  - generic [ref=e158]:
                    - generic [ref=e160]: "1.00"
                    - button "Add to cart" [ref=e162] [cursor=pointer]
              - generic [ref=e164]:
                - link "Picture of Custom T-Shirt" [ref=e166] [cursor=pointer]:
                  - /url: /custom-t-shirt
                  - img "Picture of Custom T-Shirt" [ref=e167]
                - generic [ref=e168]:
                  - heading "Custom T-Shirt" [level=2] [ref=e169]:
                    - link "Custom T-Shirt" [ref=e170] [cursor=pointer]:
                      - /url: /custom-t-shirt
                  - generic "297 review(s)" [ref=e171]
                  - generic [ref=e176]: "15.00"
              - generic [ref=e178]:
                - link "Picture of Denim Short with Rhinestones" [ref=e180] [cursor=pointer]:
                  - /url: /v-blue-juniors-cuffed-denim-short-with-rhinestones
                  - img "Picture of Denim Short with Rhinestones" [ref=e181]
                - generic [ref=e182]:
                  - heading "Denim Short with Rhinestones" [level=2] [ref=e183]:
                    - link "Denim Short with Rhinestones" [ref=e184] [cursor=pointer]:
                      - /url: /v-blue-juniors-cuffed-denim-short-with-rhinestones
                  - generic "177 review(s)" [ref=e185]
                  - generic [ref=e190]: "10.00"
              - generic [ref=e192]:
                - link "Picture of Genuine Leather Handbag with Cell Phone Holder & Many Pockets" [ref=e194] [cursor=pointer]:
                  - /url: /genuine-leather-handbag-with-cell-phone-holder-many-pockets
                  - img "Picture of Genuine Leather Handbag with Cell Phone Holder & Many Pockets" [ref=e195]
                - generic [ref=e196]:
                  - heading "Genuine Leather Handbag with Cell Phone Holder & Many Pockets" [level=2] [ref=e197]:
                    - link "Genuine Leather Handbag with Cell Phone Holder & Many Pockets" [ref=e198] [cursor=pointer]:
                      - /url: /genuine-leather-handbag-with-cell-phone-holder-many-pockets
                  - generic "153 review(s)" [ref=e199]
                  - generic [ref=e202]:
                    - generic [ref=e204]: "35.00"
                    - button "Add to cart" [ref=e206] [cursor=pointer]
              - generic [ref=e208]:
                - link "Picture of Green and blue Sneaker" [ref=e210] [cursor=pointer]:
                  - /url: /green-and-blue-sneaker
                  - img "Picture of Green and blue Sneaker" [ref=e211]
                - generic [ref=e212]:
                  - heading "Green and blue Sneaker" [level=2] [ref=e213]:
                    - link "Green and blue Sneaker" [ref=e214] [cursor=pointer]:
                      - /url: /green-and-blue-sneaker
                  - generic "294 review(s)" [ref=e215]
                  - generic [ref=e220]: "17.56"
            - list [ref=e222]:
              - listitem [ref=e223]:
                - generic [ref=e224]: "1"
              - listitem [ref=e225]:
                - link "2" [ref=e226] [cursor=pointer]:
                  - /url: /apparel-shoes?pagenumber=2
              - listitem [ref=e227]:
                - link "Next" [ref=e228] [cursor=pointer]:
                  - /url: /apparel-shoes?pagenumber=2
  - generic [ref=e229]:
    - generic [ref=e230]:
      - generic [ref=e231]:
        - heading "Information" [level=3] [ref=e232]
        - list [ref=e233]:
          - listitem [ref=e234]:
            - link "Sitemap" [ref=e235] [cursor=pointer]:
              - /url: /sitemap
          - listitem [ref=e236]:
            - link "Shipping & Returns" [ref=e237] [cursor=pointer]:
              - /url: /shipping-returns
          - listitem [ref=e238]:
            - link "Privacy Notice" [ref=e239] [cursor=pointer]:
              - /url: /privacy-policy
          - listitem [ref=e240]:
            - link "Conditions of Use" [ref=e241] [cursor=pointer]:
              - /url: /conditions-of-use
          - listitem [ref=e242]:
            - link "About us" [ref=e243] [cursor=pointer]:
              - /url: /about-us
          - listitem [ref=e244]:
            - link "Contact us" [ref=e245] [cursor=pointer]:
              - /url: /contactus
      - generic [ref=e246]:
        - heading "Customer service" [level=3] [ref=e247]
        - list [ref=e248]:
          - listitem [ref=e249]:
            - link "Search" [ref=e250] [cursor=pointer]:
              - /url: /search
          - listitem [ref=e251]:
            - link "News" [ref=e252] [cursor=pointer]:
              - /url: /news
          - listitem [ref=e253]:
            - link "Blog" [ref=e254] [cursor=pointer]:
              - /url: /blog
          - listitem [ref=e255]:
            - link "Recently viewed products" [ref=e256] [cursor=pointer]:
              - /url: /recentlyviewedproducts
          - listitem [ref=e257]:
            - link "Compare products list" [ref=e258] [cursor=pointer]:
              - /url: /compareproducts
          - listitem [ref=e259]:
            - link "New products" [ref=e260] [cursor=pointer]:
              - /url: /newproducts
      - generic [ref=e261]:
        - heading "My account" [level=3] [ref=e262]
        - list [ref=e263]:
          - listitem [ref=e264]:
            - link "My account" [ref=e265] [cursor=pointer]:
              - /url: /customer/info
          - listitem [ref=e266]:
            - link "Orders" [ref=e267] [cursor=pointer]:
              - /url: /customer/orders
          - listitem [ref=e268]:
            - link "Addresses" [ref=e269] [cursor=pointer]:
              - /url: /customer/addresses
          - listitem [ref=e270]:
            - link "Shopping cart" [ref=e271] [cursor=pointer]:
              - /url: /cart
          - listitem [ref=e272]:
            - link "Wishlist" [ref=e273] [cursor=pointer]:
              - /url: /wishlist
      - generic [ref=e274]:
        - heading "Follow us" [level=3] [ref=e275]
        - list [ref=e276]:
          - listitem [ref=e277]:
            - link "Facebook" [ref=e278] [cursor=pointer]:
              - /url: http://www.facebook.com/nopCommerce
          - listitem [ref=e279]:
            - link "Twitter" [ref=e280] [cursor=pointer]:
              - /url: https://twitter.com/nopCommerce
          - listitem [ref=e281]:
            - link "RSS" [ref=e282] [cursor=pointer]:
              - /url: /news/rss/1
          - listitem [ref=e283]:
            - link "YouTube" [ref=e284] [cursor=pointer]:
              - /url: http://www.youtube.com/user/nopCommerce
          - listitem [ref=e285]:
            - link "Google+" [ref=e286] [cursor=pointer]:
              - /url: https://plus.google.com/+nopcommerce
    - generic [ref=e287]:
      - text: Powered by
      - link "nopCommerce" [ref=e288] [cursor=pointer]:
        - /url: http://www.nopcommerce.com/
    - generic [ref=e289]: Copyright © 2026 Tricentis Demo Web Shop. All rights reserved.
```

# Test source

```ts
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
  211 |       const pageLinks = page.locator('[class*=pager], a:has-text(/\d+/)');
  212 |       expect(await pageLinks.count()).toBeGreaterThanOrEqual(0);
  213 |     });
  214 | 
  215 |     test('electronics product detail link navigates', async ({ page }) => {
  216 |       await page.goto(`${BASE_URL}/electronics`);
  217 |       const productLink = page.locator('a[href*=product]').first();
  218 |       if (await productLink.count() > 0) {
  219 |         const isVisible = await productLink.isVisible().catch(() => false);
  220 |         if (isVisible) {
  221 |           await productLink.click();
  222 |           await page.waitForLoadState('networkidle');
  223 |           expect(page.url()).toContain('product');
  224 |         }
  225 |       }
  226 |     });
  227 | 
  228 |     test('electronics add to cart from listing', async ({ page }) => {
  229 |       await page.goto(`${BASE_URL}/electronics`);
  230 |       const addBtn = page.locator('button:has-text(/add|cart/i), a:has-text(/add|cart/i)').first();
  231 |       if (await addBtn.count() > 0) {
  232 |         const isVisible = await addBtn.isVisible().catch(() => false);
  233 |         if (isVisible) {
  234 |           await addBtn.click();
  235 |           await page.waitForLoadState('networkidle');
  236 |         }
  237 |       }
  238 |     });
  239 |   });
  240 | 
  241 |   test.describe('Category: Apparel Shoes', () => {
  242 |     test('apparel-shoes page loads correctly', async ({ page }) => {
  243 |       await page.goto(`${BASE_URL}/apparel-shoes`);
  244 |       await page.waitForLoadState('networkidle');
  245 |       const title = page.locator('h1, [class*=title]').first();
  246 |       if (await title.count() > 0) {
  247 |         await expect(title).toBeVisible();
  248 |       }
  249 |     });
  250 | 
  251 |     test('apparel-shoes displays product list', async ({ page }) => {
  252 |       await page.goto(`${BASE_URL}/apparel-shoes`);
  253 |       const products = page.locator('[class*=product], a[href*=product]');
  254 |       expect(await products.count()).toBeGreaterThan(0);
  255 |     });
  256 | 
  257 |     test('apparel-shoes filtering functionality', async ({ page }) => {
  258 |       await page.goto(`${BASE_URL}/apparel-shoes`);
  259 |       const filter = page.locator('[class*=filter], button:has-text(/filter/i)').first();
> 260 |       if (await filter.count() > 0) {
      |                        ^ Error: locator.count: Unexpected token "/" while parsing css selector "[class*=filter], button:has-text(/filter/i)". Did you mean to CSS.escape it?
  261 |         const isVisible = await filter.isVisible().catch(() => false);
  262 |         if (isVisible) {
  263 |           await filter.click();
  264 |           await page.waitForLoadState('networkidle');
  265 |         }
  266 |       }
  267 |     });
  268 | 
  269 |     test('apparel-shoes sorting by price', async ({ page }) => {
  270 |       await page.goto(`${BASE_URL}/apparel-shoes`);
  271 |       const sort = page.locator('select[name*=sort], [class*=sort]').first();
  272 |       if (await sort.count() > 0) {
  273 |         const isVisible = await sort.isVisible().catch(() => false);
  274 |         if (isVisible) {
  275 |           try {
  276 |             await sort.selectOption('1');
  277 |           } catch (e) {
  278 |             // Fallback for non-select elements
  279 |           }
  280 |         }
  281 |       }
  282 |     });
  283 | 
  284 |     test('apparel-shoes pagination works', async ({ page }) => {
  285 |       await page.goto(`${BASE_URL}/apparel-shoes`);
  286 |       const pageLinks = page.locator('[class*=pager], a:has-text(/\d+/)');
  287 |       expect(await pageLinks.count()).toBeGreaterThanOrEqual(0);
  288 |     });
  289 | 
  290 |     test('apparel-shoes product detail link navigates', async ({ page }) => {
  291 |       await page.goto(`${BASE_URL}/apparel-shoes`);
  292 |       const productLink = page.locator('a[href*=product]').first();
  293 |       if (await productLink.count() > 0) {
  294 |         const isVisible = await productLink.isVisible().catch(() => false);
  295 |         if (isVisible) {
  296 |           await productLink.click();
  297 |           await page.waitForLoadState('networkidle');
  298 |           expect(page.url()).toContain('product');
  299 |         }
  300 |       }
  301 |     });
  302 | 
  303 |     test('apparel-shoes add to cart from listing', async ({ page }) => {
  304 |       await page.goto(`${BASE_URL}/apparel-shoes`);
  305 |       const addBtn = page.locator('button:has-text(/add|cart/i), a:has-text(/add|cart/i)').first();
  306 |       if (await addBtn.count() > 0) {
  307 |         const isVisible = await addBtn.isVisible().catch(() => false);
  308 |         if (isVisible) {
  309 |           await addBtn.click();
  310 |           await page.waitForLoadState('networkidle');
  311 |         }
  312 |       }
  313 |     });
  314 |   });
  315 | 
  316 |   test.describe('Category: Digital Downloads', () => {
  317 |     test('digital-downloads page loads correctly', async ({ page }) => {
  318 |       await page.goto(`${BASE_URL}/digital-downloads`);
  319 |       await page.waitForLoadState('networkidle');
  320 |       const title = page.locator('h1, [class*=title]').first();
  321 |       if (await title.count() > 0) {
  322 |         await expect(title).toBeVisible();
  323 |       }
  324 |     });
  325 | 
  326 |     test('digital-downloads displays product list', async ({ page }) => {
  327 |       await page.goto(`${BASE_URL}/digital-downloads`);
  328 |       const products = page.locator('[class*=product], a[href*=product]');
  329 |       expect(await products.count()).toBeGreaterThan(0);
  330 |     });
  331 | 
  332 |     test('digital-downloads filtering functionality', async ({ page }) => {
  333 |       await page.goto(`${BASE_URL}/digital-downloads`);
  334 |       const filter = page.locator('[class*=filter], button:has-text(/filter/i)').first();
  335 |       if (await filter.count() > 0) {
  336 |         const isVisible = await filter.isVisible().catch(() => false);
  337 |         if (isVisible) {
  338 |           await filter.click();
  339 |           await page.waitForLoadState('networkidle');
  340 |         }
  341 |       }
  342 |     });
  343 | 
  344 |     test('digital-downloads sorting by price', async ({ page }) => {
  345 |       await page.goto(`${BASE_URL}/digital-downloads`);
  346 |       const sort = page.locator('select[name*=sort], [class*=sort]').first();
  347 |       if (await sort.count() > 0) {
  348 |         const isVisible = await sort.isVisible().catch(() => false);
  349 |         if (isVisible) {
  350 |           try {
  351 |             await sort.selectOption('1');
  352 |           } catch (e) {
  353 |             // Fallback for non-select elements
  354 |           }
  355 |         }
  356 |       }
  357 |     });
  358 | 
  359 |     test('digital-downloads pagination works', async ({ page }) => {
  360 |       await page.goto(`${BASE_URL}/digital-downloads`);
```