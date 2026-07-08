# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: orangehrm-comprehensive-sub-functions.spec.ts >> ADMIN: User Management >> WF-1.8: Add new user button
- Location: tests/e2e/orangehrm-comprehensive-sub-functions.spec.ts:79:7

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('button:has-text("Add")')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('button:has-text("Add")')

```

```yaml
- img "company-branding"
- heading "Login" [level=5]
- paragraph: "Username : Admin"
- paragraph: "Password : admin123"
- text:  Username
- textbox "Username"
- text:  Password
- textbox "Password"
- button "Login"
- paragraph: Forgot your password?
- link:
  - /url: https://www.linkedin.com/company/orangehrm/mycompany/
- link:
  - /url: https://www.facebook.com/OrangeHRM/
- link:
  - /url: https://twitter.com/orangehrm?lang=en
- link:
  - /url: https://www.youtube.com/c/OrangeHRMInc
- paragraph: OrangeHRM OS 5.8
- paragraph:
  - text: © 2005 - 2026
  - link "OrangeHRM, Inc":
    - /url: http://www.orangehrm.com
  - text: . All rights reserved.
- img "orangehrm-logo"
```

# Test source

```ts
  1   | import { test, expect, Page } from '@playwright/test';
  2   | 
  3   | const BASE_URL = 'https://opensource-demo.orangehrmlive.com';
  4   | const ADMIN_USER = 'Admin';
  5   | const ADMIN_PASSWORD = 'admin123';
  6   | 
  7   | async function login(page: Page) {
  8   |   await page.goto(`${BASE_URL}/web/index.php/auth/login`);
  9   |   await page.fill('input[name="username"]', ADMIN_USER);
  10  |   await page.fill('input[name="password"]', ADMIN_PASSWORD);
  11  |   await page.click('button[type="submit"]');
  12  |   await page.waitForURL(`${BASE_URL}/**`);
  13  | }
  14  | 
  15  | async function navigateToModule(page: Page, moduleUrl: string) {
  16  |   await page.goto(`${BASE_URL}${moduleUrl}`);
  17  |   await page.waitForLoadState('networkidle');
  18  | }
  19  | 
  20  | // ═════════════════════════════════════════════════════════════════════════
  21  | // MODULE 1: ADMIN - USER MANAGEMENT (12 Sub-functions)
  22  | // ═════════════════════════════════════════════════════════════════════════
  23  | 
  24  | test.describe('ADMIN: User Management', () => {
  25  |   test.beforeEach(async ({ page }) => {
  26  |     await login(page);
  27  |     await navigateToModule(page, '/web/index.php/admin/viewAdminModule');
  28  |   });
  29  | 
  30  |   test('WF-1.1: View all system users list', async ({ page }) => {
  31  |     await expect(page.locator('text=System Users')).toBeVisible();
  32  |     const rows = page.locator('table tbody tr');
  33  |     expect(await rows.count()).toBeGreaterThan(0);
  34  |   });
  35  | 
  36  |   test('WF-1.2: Search users by username field', async ({ page }) => {
  37  |     const searchInput = page.locator('input[placeholder*="Username"], input[name="username"]').first();
  38  |     if (await searchInput.isVisible()) {
  39  |       await searchInput.fill('Admin');
  40  |       await page.click('button:has-text("Search")');
  41  |       expect(await page.locator('table tbody tr').count()).toBeGreaterThan(0);
  42  |     }
  43  |   });
  44  | 
  45  |   test('WF-1.3: Filter by role dropdown (Admin/ESS)', async ({ page }) => {
  46  |     const selects = page.locator('select');
  47  |     if (await selects.first().isVisible()) {
  48  |       await selects.first().selectOption('1');
  49  |       await page.click('button:has-text("Search")');
  50  |     }
  51  |   });
  52  | 
  53  |   test('WF-1.4: Filter by status (Enabled/Disabled)', async ({ page }) => {
  54  |     const statusSelect = page.locator('select').nth(1);
  55  |     if (await statusSelect.isVisible()) {
  56  |       await statusSelect.selectOption('Enabled');
  57  |     }
  58  |   });
  59  | 
  60  |   test('WF-1.5: Edit user button functionality', async ({ page }) => {
  61  |     const editBtn = page.locator('button[aria-label*="Edit"], [title*="Edit"]').first();
  62  |     if (await editBtn.isVisible()) {
  63  |       expect(await editBtn.isVisible()).toBeTruthy();
  64  |     }
  65  |   });
  66  | 
  67  |   test('WF-1.6: Delete user button visibility', async ({ page }) => {
  68  |     const deleteBtn = page.locator('button[aria-label*="Delete"], [title*="Delete"]').first();
  69  |     if (await deleteBtn.isVisible()) {
  70  |       expect(await deleteBtn.isVisible()).toBeTruthy();
  71  |     }
  72  |   });
  73  | 
  74  |   test('WF-1.7: Reset filters button', async ({ page }) => {
  75  |     const resetBtn = page.locator('button:has-text("Reset")');
  76  |     await expect(resetBtn).toBeVisible();
  77  |   });
  78  | 
  79  |   test('WF-1.8: Add new user button', async ({ page }) => {
  80  |     const addBtn = page.locator('button:has-text("Add")');
> 81  |     await expect(addBtn).toBeVisible();
      |                          ^ Error: expect(locator).toBeVisible() failed
  82  |   });
  83  | 
  84  |   test('WF-1.9: Username column sortable', async ({ page }) => {
  85  |     await expect(page.locator('th:has-text("Username")')).toBeVisible();
  86  |   });
  87  | 
  88  |   test('WF-1.10: User role column sortable', async ({ page }) => {
  89  |     await expect(page.locator('th:has-text("User Role")')).toBeVisible();
  90  |   });
  91  | 
  92  |   test('WF-1.11: Employee name column sortable', async ({ page }) => {
  93  |     await expect(page.locator('th:has-text("Employee Name")')).toBeVisible();
  94  |   });
  95  | 
  96  |   test('WF-1.12: Status column sortable', async ({ page }) => {
  97  |     await expect(page.locator('th:has-text("Status")')).toBeVisible();
  98  |   });
  99  | });
  100 | 
  101 | // ═════════════════════════════════════════════════════════════════════════
  102 | // MODULE 2: PIM - EMPLOYEE LIST (15 Sub-functions)
  103 | // ═════════════════════════════════════════════════════════════════════════
  104 | 
  105 | test.describe('PIM: Employee List', () => {
  106 |   test.beforeEach(async ({ page }) => {
  107 |     await login(page);
  108 |     await navigateToModule(page, '/web/index.php/pim/viewEmployeeList');
  109 |   });
  110 | 
  111 |   test('WF-2.1: View employee list with 133 records', async ({ page }) => {
  112 |     await expect(page.locator('text=Records Found')).toBeVisible({ timeout: 10000 });
  113 |   });
  114 | 
  115 |   test('WF-2.2: Search by employee name', async ({ page }) => {
  116 |     const searchInput = page.locator('input[placeholder*="Employee Name"]').first();
  117 |     if (await searchInput.isVisible()) {
  118 |       await searchInput.fill('Alisa');
  119 |       await page.click('button:has-text("Search")');
  120 |     }
  121 |   });
  122 | 
  123 |   test('WF-2.3: Search by employee ID', async ({ page }) => {
  124 |     const idInput = page.locator('input[placeholder*="Employee ID"]').first();
  125 |     if (await idInput.isVisible()) {
  126 |       await idInput.fill('7369');
  127 |     }
  128 |   });
  129 | 
  130 |   test('WF-2.4: Filter by employment status', async ({ page }) => {
  131 |     const statusSelect = page.locator('select').filter({ has: page.locator('option') }).first();
  132 |     if (await statusSelect.isVisible()) {
  133 |       const options = statusSelect.locator('option');
  134 |       if (await options.count() > 1) {
  135 |         await statusSelect.selectOption('1');
  136 |       }
  137 |     }
  138 |   });
  139 | 
  140 |   test('WF-2.5: Include past employees checkbox', async ({ page }) => {
  141 |     const checkbox = page.locator('input[type="checkbox"]').first();
  142 |     if (await checkbox.isVisible()) {
  143 |       await expect(checkbox).toBeVisible();
  144 |     }
  145 |   });
  146 | 
  147 |   test('WF-2.6: Employee ID column sort', async ({ page }) => {
  148 |     await expect(page.locator('th:has-text("Employee ID")')).toBeVisible();
  149 |   });
  150 | 
  151 |   test('WF-2.7: Employee name column sort', async ({ page }) => {
  152 |     await expect(page.locator('th:has-text("Employee Name")')).toBeVisible();
  153 |   });
  154 | 
  155 |   test('WF-2.8: Job title column sort', async ({ page }) => {
  156 |     await expect(page.locator('th:has-text("Job Title")')).toBeVisible();
  157 |   });
  158 | 
  159 |   test('WF-2.9: Employment status column sort', async ({ page }) => {
  160 |     await expect(page.locator('th:has-text("Employment Status")')).toBeVisible();
  161 |   });
  162 | 
  163 |   test('WF-2.10: Sub unit column sort', async ({ page }) => {
  164 |     await expect(page.locator('th:has-text("Sub Unit")')).toBeVisible();
  165 |   });
  166 | 
  167 |   test('WF-2.11: Edit employee icon', async ({ page }) => {
  168 |     const editBtn = page.locator('button[aria-label*="Edit"]').first();
  169 |     if (await editBtn.isVisible()) {
  170 |       expect(await editBtn.isVisible()).toBeTruthy();
  171 |     }
  172 |   });
  173 | 
  174 |   test('WF-2.12: Delete employee icon', async ({ page }) => {
  175 |     const deleteBtn = page.locator('button[aria-label*="Delete"]').first();
  176 |     if (await deleteBtn.isVisible()) {
  177 |       expect(await deleteBtn.isVisible()).toBeTruthy();
  178 |     }
  179 |   });
  180 | 
  181 |   test('WF-2.13: Add employee button', async ({ page }) => {
```