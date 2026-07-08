# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: orangehrm-comprehensive-sub-functions.spec.ts >> PIM: Employee List >> WF-2.9: Employment status column sort
- Location: tests/e2e/orangehrm-comprehensive-sub-functions.spec.ts:159:7

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('th:has-text("Employment Status")')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('th:has-text("Employment Status")')

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
  - heading "PIM" [level=6]
  - link "Upgrade":
    - /url: https://orangehrm.com/open-source/upgrade-to-advanced
    - button "Upgrade"
  - list:
    - listitem:
      - img "profile picture"
      - paragraph: manda user
      - text: 
  - navigation "Topbar Menu":
    - list:
      - listitem: Configuration 
      - listitem:
        - link "Employee List":
          - /url: "#"
      - listitem:
        - link "Add Employee":
          - /url: "#"
      - listitem:
        - link "Reports":
          - /url: "#"
      - button ""
- heading "Employee Information" [level=5]
- button ""
- separator
- text: Employee Name
- textbox "Type for hints..."
- text: Employee Id
- textbox
- text: Employment Status -- Select --  Include Current Employees Only  Supervisor Name
- textbox "Type for hints..."
- text: Job Title -- Select --  Sub Unit -- Select -- 
- separator
- button "Reset"
- button "Search"
- button " Add"
- separator
- text: (96) Records Found
- table:
  - rowgroup:
    - row " Id  First (& Middle) Name  Last Name  Job Title  Employment Status  Sub Unit  Supervisor  Actions":
      - columnheader "":
        - checkbox ""
        - text: 
      - columnheader "Id "
      - columnheader "First (& Middle) Name "
      - columnheader "Last Name "
      - columnheader "Job Title "
      - columnheader "Employment Status "
      - columnheader "Sub Unit "
      - columnheader "Supervisor "
      - columnheader "Actions"
  - rowgroup:
    - row " 0295 99N75 425 5TlV  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0295"
      - cell "99N75 425"
      - cell "5TlV"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0312 A8DCo 4Ys 010Z  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0312"
      - cell "A8DCo 4Ys"
      - cell "010Z"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 01715 Amelia Brown  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "01715"
      - cell "Amelia"
      - cell "Brown"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0360 aniket t t  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0360"
      - cell "aniket t"
      - cell "t"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0367 Ash J Tyson  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0367"
      - cell "Ash J"
      - cell "Tyson"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0303 bala kumar ravi  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0303"
      - cell "bala kumar"
      - cell "ravi"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0292 bmrtahvwhibmrtahvwhi hbfqkhjfqbhbfqkhjfqb  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0292"
      - cell "bmrtahvwhibmrtahvwhi"
      - cell "hbfqkhjfqbhbfqkhjfqb"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0320 Charles Carter  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0320"
      - cell "Charles"
      - cell "Carter"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 00392 Charlotte Smith  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "00392"
      - cell "Charlotte"
      - cell "Smith"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0363 Christopher Mcmillan  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0363"
      - cell "Christopher"
      - cell "Mcmillan"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0290 dhbrukkuzldhbrukkuzl ibuvlwtfsfibuvlwtfsf  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0290"
      - cell "dhbrukkuzldhbrukkuzl"
      - cell "ibuvlwtfsfibuvlwtfsf"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0294 DHINA KARAN P  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0294"
      - cell "DHINA KARAN"
      - cell "P"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 09557 Emily Jones  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "09557"
      - cell "Emily"
      - cell "Jones"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 1235 FName Mname LName  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "1235"
      - cell "FName Mname"
      - cell "LName"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue ftdkux ltsxgy  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "ftdkux"
      - cell "ltsxgy"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue fthnvn ltwrrt  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "fthnvn"
      - cell "ltwrrt"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue fthnvn ltwrrt  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "fthnvn"
      - cell "ltwrrt"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue fthyfv ltrhtm  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "fthyfv"
      - cell "ltrhtm"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue ftioiu ltpugr  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "ftioiu"
      - cell "ltpugr"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue ftioiu ltpugr  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "ftioiu"
      - cell "ltpugr"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue ftioiu ltpugr  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "ftioiu"
      - cell "ltpugr"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue ftioiu ltpugr  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "ftioiu"
      - cell "ltpugr"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue ftndlm ltdyyf  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "ftndlm"
      - cell "ltdyyf"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue ftpjte ltpzkj  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "ftpjte"
      - cell "ltpzkj"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue ftyseo ltzbbp  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "ftyseo"
      - cell "ltzbbp"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue ftyseo ltzbbp  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "ftyseo"
      - cell "ltzbbp"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue ftyseo ltzbbp  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "ftyseo"
      - cell "ltzbbp"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue ftyseo ltzbbp  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "ftyseo"
      - cell "ltzbbp"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue ftyseo ltzbbp  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "ftyseo"
      - cell "ltzbbp"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " ATPValue ftyseo ltzbbp  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "ATPValue"
      - cell "ftyseo"
      - cell "ltzbbp"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0315hh hh hh  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0315hh"
      - cell "hh"
      - cell "hh"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0365 James Butler  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0365"
      - cell "James"
      - cell "Butler"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0367010 Jobin Mathew Sam  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0367010"
      - cell "Jobin Mathew"
      - cell "Sam"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0303 joker john selvam  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0303"
      - cell "joker john"
      - cell "selvam"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 1257 Joko Cahaya Langit  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "1257"
      - cell "Joko Cahaya"
      - cell "Langit"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0361 Joseph Evans  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0361"
      - cell "Joseph"
      - cell "Evans"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0321 Joy Smith  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0321"
      - cell "Joy"
      - cell "Smith"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0359 Joy Smith  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0359"
      - cell "Joy"
      - cell "Smith"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0335 Joy Smith  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0335"
      - cell "Joy"
      - cell "Smith"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0364 Joy Smith  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0364"
      - cell "Joy"
      - cell "Smith"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0342 Joy Smith  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0342"
      - cell "Joy"
      - cell "Smith"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0323 Joy Smith  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0323"
      - cell "Joy"
      - cell "Smith"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0317 Joy Smith  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0317"
      - cell "Joy"
      - cell "Smith"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0322 Joy Smith  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0322"
      - cell "Joy"
      - cell "Smith"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0315 JoyToy SmithSmith  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0315"
      - cell "JoyToy"
      - cell "SmithSmith"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " muser manda akhil user HR Manager Full-Time Permanent Human Resources ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "muser"
      - cell "manda akhil"
      - cell "user"
      - cell "HR Manager"
      - cell "Full-Time Permanent"
      - cell "Human Resources"
      - cell
      - cell "":
        - button ""
    - row " 0308 murugan moorthi thiru  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0308"
      - cell "murugan moorthi"
      - cell "thiru"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0301 Nalim R P  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0301"
      - cell "Nalim"
      - cell "R P"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0264 njycvonotxnjycvonotx zguczzwxfazguczzwxfa  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0264"
      - cell "njycvonotxnjycvonotx"
      - cell "zguczzwxfazguczzwxfa"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
    - row " 0001 Orange Test  ":
      - cell "":
        - checkbox ""
        - text: 
      - cell "0001"
      - cell "Orange"
      - cell "Test"
      - cell
      - cell
      - cell
      - cell
      - cell " ":
        - button ""
        - button ""
- navigation "Pagination Navigation":
  - list:
    - listitem:
      - button "1"
    - listitem:
      - button "2"
    - listitem:
      - button ""
- paragraph: OrangeHRM OS 5.8
- paragraph:
  - text: © 2005 - 2026
  - link "OrangeHRM, Inc":
    - /url: http://www.orangehrm.com
  - text: . All rights reserved.
```

# Test source

```ts
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
> 160 |     await expect(page.locator('th:has-text("Employment Status")')).toBeVisible();
      |                                                                    ^ Error: expect(locator).toBeVisible() failed
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
  198 | 
  199 | test.describe('PIM: My Info - Personal Details', () => {
  200 |   test.beforeEach(async ({ page }) => {
  201 |     await login(page);
  202 |     await navigateToModule(page, '/web/index.php/pim/viewMyDetails');
  203 |   });
  204 | 
  205 |   test('WF-3.1: Personal details section visible', async ({ page }) => {
  206 |     await expect(page.locator('text=Personal Details')).toBeVisible();
  207 |   });
  208 | 
  209 |   test('WF-3.2: First name field', async ({ page }) => {
  210 |     const inputs = page.locator('input');
  211 |     expect(await inputs.count()).toBeGreaterThan(0);
  212 |   });
  213 | 
  214 |   test('WF-3.3: Middle name field', async ({ page }) => {
  215 |     const inputs = page.locator('input');
  216 |     if (await inputs.count() > 1) {
  217 |       await expect(inputs.nth(1)).toBeVisible();
  218 |     }
  219 |   });
  220 | 
  221 |   test('WF-3.4: Last name field', async ({ page }) => {
  222 |     const inputs = page.locator('input');
  223 |     if (await inputs.count() > 2) {
  224 |       await expect(inputs.nth(2)).toBeVisible();
  225 |     }
  226 |   });
  227 | 
  228 |   test('WF-3.5: Employee ID read-only field', async ({ page }) => {
  229 |     const empIdInput = page.locator('input').filter({ hasNot: page.locator('[readonly]') }).first();
  230 |     if (await empIdInput.isVisible()) {
  231 |       expect(await empIdInput.isVisible()).toBeTruthy();
  232 |     }
  233 |   });
  234 | 
  235 |   test('WF-3.6: Driver license number field', async ({ page }) => {
  236 |     const inputs = page.locator('input');
  237 |     expect(await inputs.count()).toBeGreaterThan(0);
  238 |   });
  239 | 
  240 |   test('WF-3.7: License expiry date field', async ({ page }) => {
  241 |     const dateInputs = page.locator('input[type="date"]');
  242 |     if (await dateInputs.count() > 0) {
  243 |       expect(await dateInputs.first().isVisible()).toBeTruthy();
  244 |     }
  245 |   });
  246 | 
  247 |   test('WF-3.8: Nationality dropdown', async ({ page }) => {
  248 |     const selects = page.locator('select');
  249 |     if (await selects.count() > 0) {
  250 |       expect(await selects.first().isVisible()).toBeTruthy();
  251 |     }
  252 |   });
  253 | 
  254 |   test('WF-3.9: Marital status dropdown', async ({ page }) => {
  255 |     const selects = page.locator('select');
  256 |     if (await selects.count() > 1) {
  257 |       expect(await selects.nth(1).isVisible()).toBeTruthy();
  258 |     }
  259 |   });
  260 | 
```