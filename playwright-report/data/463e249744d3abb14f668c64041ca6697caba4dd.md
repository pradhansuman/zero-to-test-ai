# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: orangehrm-comprehensive-sub-functions.spec.ts >> ADMIN: User Management >> WF-1.12: Status column sortable
- Location: tests/e2e/orangehrm-comprehensive-sub-functions.spec.ts:96:7

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('th:has-text("Status")')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('th:has-text("Status")')

```

```yaml
- complementary:
  - navigation "Sidepanel":
    - link "client brand banner":
      - /url: https://www.orangehrm.com/
      - img "client brand banner"
    - textbox "Search"
    - button ""
    - separator
    - list:
      - listitem:
        - link "Admin":
          - /url: /web/index.php/admin/viewAdminModule
      - listitem:
        - link "PIM":
          - /url: /web/index.php/pim/viewPimModule
      - listitem:
        - link "Leave":
          - /url: /web/index.php/leave/viewLeaveModule
      - listitem:
        - link "Time":
          - /url: /web/index.php/time/viewTimeModule
      - listitem:
        - link "Recruitment":
          - /url: /web/index.php/recruitment/viewRecruitmentModule
      - listitem:
        - link "My Info":
          - /url: /web/index.php/pim/viewMyDetails
      - listitem:
        - link "Performance":
          - /url: /web/index.php/performance/viewPerformanceModule
      - listitem:
        - link "Dashboard":
          - /url: /web/index.php/dashboard/index
      - listitem:
        - link "Directory":
          - /url: /web/index.php/directory/viewDirectory
      - listitem:
        - link "Maintenance":
          - /url: /web/index.php/maintenance/viewMaintenanceModule
      - listitem:
        - link "Claim":
          - /url: /web/index.php/claim/viewClaimModule
          - img
          - text: Claim
      - listitem:
        - link "Buzz":
          - /url: /web/index.php/buzz/viewBuzz
- banner:
  - heading "Admin" [level=6]
  - heading "/ User Management" [level=6]
  - link "Upgrade":
    - /url: https://orangehrm.com/open-source/upgrade-to-advanced
    - button "Upgrade"
  - list:
    - listitem:
      - img "profile picture"
      - paragraph: Test NewLastName
      - text: 
  - navigation "Topbar Menu":
    - list:
      - listitem: User Management 
      - listitem: Job 
      - listitem: Organization 
      - listitem: Qualifications 
      - listitem:
        - link "Nationalities":
          - /url: "#"
      - listitem:
        - link "Corporate Branding":
          - /url: "#"
      - listitem: Configuration 
      - button ""
- heading "System Users" [level=5]
- button ""
- separator
- text: Username
- textbox
- text: User Role -- Select --  Employee Name
- textbox "Type for hints..."
- text: Status -- Select -- 
- separator
- button "Reset"
- button "Search"
- button " Add"
- separator
- text: (25) Records Found
- table:
  - rowgroup:
    - row " Username  User Role  Employee Name  Status  Actions":
      - columnheader "":
        - checkbox ""
        - text: 
      - columnheader "Username "
      - columnheader "User Role "
      - columnheader "Employee Name "
      - columnheader "Status "
      - columnheader "Actions"
  - rowgroup:
    - row " Admin Admin Test NewLastName Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "Admin"
      - cell "Admin"
      - cell "Test NewLastName"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " Jacey.Cole-Rodriguez@mail.com ESS Jacey Cole-Rodriguez Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "Jacey.Cole-Rodriguez@mail.com"
      - cell "ESS"
      - cell "Jacey Cole-Rodriguez"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " Jobinsam@6742 ESS Jobin Sam Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "Jobinsam@6742"
      - cell "ESS"
      - cell "Jobin Sam"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " johndoe.qa228916 ESS John Doe Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "johndoe.qa228916"
      - cell "ESS"
      - cell "John Doe"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " johndoe.qa497303 ESS John Doe Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "johndoe.qa497303"
      - cell "ESS"
      - cell "John Doe"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " johndoe.qa502205 ESS John Doe Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "johndoe.qa502205"
      - cell "ESS"
      - cell "John Doe"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " johndoe.qa513873 ESS John Doe Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "johndoe.qa513873"
      - cell "ESS"
      - cell "John Doe"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " johndoe.qa602794 ESS John Doe Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "johndoe.qa602794"
      - cell "ESS"
      - cell "John Doe"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " johndoe.qa679529 ESS John Doe Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "johndoe.qa679529"
      - cell "ESS"
      - cell "John Doe"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " johndoe.qa741897 ESS John Doe Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "johndoe.qa741897"
      - cell "ESS"
      - cell "John Doe"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " johndoe.qa778500 ESS John Doe Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "johndoe.qa778500"
      - cell "ESS"
      - cell "John Doe"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " johndoe.qa800947 ESS John Doe Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "johndoe.qa800947"
      - cell "ESS"
      - cell "John Doe"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " Lewis.Harvey@mail.com ESS Lewis Harvey Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "Lewis.Harvey@mail.com"
      - cell "ESS"
      - cell "Lewis Harvey"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " mamidi_prasad Admin Mamidi Varma Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "mamidi_prasad"
      - cell "Admin"
      - cell "Mamidi Varma"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " MansiUser1783407426020 ESS Mansi Thakare Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "MansiUser1783407426020"
      - cell "ESS"
      - cell "Mansi Thakare"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " MansiUser1783407765982 ESS Mansi Thakare Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "MansiUser1783407765982"
      - cell "ESS"
      - cell "Mansi Thakare"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " pimuser07883456 ESS Raj ravi Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "pimuser07883456"
      - cell "ESS"
      - cell "Raj ravi"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " pimuser08089675 ESS Raj ravi Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "pimuser08089675"
      - cell "ESS"
      - cell "Raj ravi"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " pimuser08421578 ESS Raj ravi Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "pimuser08421578"
      - cell "ESS"
      - cell "Raj ravi"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " playwright_user36370 ESS Mark Smith Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "playwright_user36370"
      - cell "ESS"
      - cell "Mark Smith"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " playwright_user80674 ESS Mark Smith Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "playwright_user80674"
      - cell "ESS"
      - cell "Mark Smith"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " playwright_user89310 ESS Mark Smith Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "playwright_user89310"
      - cell "ESS"
      - cell "Mark Smith"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " rachel.green2 ESS Rachel Green Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "rachel.green2"
      - cell "ESS"
      - cell "Rachel Green"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " raju@office.com ESS Raju M Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "raju@office.com"
      - cell "ESS"
      - cell "Raju M"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
    - row " testuser ESS test test Enabled  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "testuser"
      - cell "ESS"
      - cell "test test"
      - cell "Enabled"
      - cell " ":
        - button ""
        - button ""
- paragraph: OrangeHRM OS 5.8
- paragraph:
  - text: © 2005 - 2026
  - link "OrangeHRM, Inc":
    - /url: http://www.orangehrm.com
  - text: . All rights reserved.
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
  81  |     await expect(addBtn).toBeVisible();
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
> 97  |     await expect(page.locator('th:has-text("Status")')).toBeVisible();
      |                                                         ^ Error: expect(locator).toBeVisible() failed
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
  182 |     await expect(page.locator('button:has-text("Add")')).toBeVisible();
  183 |   });
  184 | 
  185 |   test('WF-2.14: Reset filters', async ({ page }) => {
  186 |     await expect(page.locator('button:has-text("Reset")')).toBeVisible();
  187 |   });
  188 | 
  189 |   test('WF-2.15: Table pagination', async ({ page }) => {
  190 |     const rows = page.locator('table tbody tr');
  191 |     expect(await rows.count()).toBeGreaterThan(0);
  192 |   });
  193 | });
  194 | 
  195 | // ═════════════════════════════════════════════════════════════════════════
  196 | // MODULE 3: PIM - MY INFO (20 Sub-functions with Personal Details)
  197 | // ═════════════════════════════════════════════════════════════════════════
```