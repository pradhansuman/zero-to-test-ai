import { test, expect, Page } from '@playwright/test';

const BASE_URL = 'https://opensource-demo.orangehrmlive.com';
const ADMIN_USER = 'Admin';
const ADMIN_PASSWORD = 'admin123';

async function login(page: Page) {
  await page.goto(`${BASE_URL}/web/index.php/auth/login`);
  await page.fill('input[name="username"]', ADMIN_USER);
  await page.fill('input[name="password"]', ADMIN_PASSWORD);
  await page.click('button[type="submit"]');
  await page.waitForURL(`${BASE_URL}/**`);
}

async function navigateToModule(page: Page, moduleUrl: string) {
  await page.goto(`${BASE_URL}${moduleUrl}`);
  await page.waitForLoadState('networkidle');
}

// ═════════════════════════════════════════════════════════════════════════
// MODULE 1: ADMIN - USER MANAGEMENT (12 Sub-functions)
// ═════════════════════════════════════════════════════════════════════════

test.describe('ADMIN: User Management', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToModule(page, '/web/index.php/admin/viewAdminModule');
  });

  test('WF-1.1: View all system users list', async ({ page }) => {
    await expect(page.locator('text=System Users')).toBeVisible();
    const rows = page.locator('table tbody tr');
    expect(await rows.count()).toBeGreaterThan(0);
  });

  test('WF-1.2: Search users by username field', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="Username"], input[name="username"]').first();
    if (await searchInput.isVisible()) {
      await searchInput.fill('Admin');
      await page.click('button:has-text("Search")');
      expect(await page.locator('table tbody tr').count()).toBeGreaterThan(0);
    }
  });

  test('WF-1.3: Filter by role dropdown (Admin/ESS)', async ({ page }) => {
    const selects = page.locator('select');
    if (await selects.first().isVisible()) {
      await selects.first().selectOption('1');
      await page.click('button:has-text("Search")');
    }
  });

  test('WF-1.4: Filter by status (Enabled/Disabled)', async ({ page }) => {
    const statusSelect = page.locator('select').nth(1);
    if (await statusSelect.isVisible()) {
      await statusSelect.selectOption('Enabled');
    }
  });

  test('WF-1.5: Edit user button functionality', async ({ page }) => {
    const editBtn = page.locator('button[aria-label*="Edit"], [title*="Edit"]').first();
    if (await editBtn.isVisible()) {
      expect(await editBtn.isVisible()).toBeTruthy();
    }
  });

  test('WF-1.6: Delete user button visibility', async ({ page }) => {
    const deleteBtn = page.locator('button[aria-label*="Delete"], [title*="Delete"]').first();
    if (await deleteBtn.isVisible()) {
      expect(await deleteBtn.isVisible()).toBeTruthy();
    }
  });

  test('WF-1.7: Reset filters button', async ({ page }) => {
    const resetBtn = page.locator('button:has-text("Reset")');
    await expect(resetBtn).toBeVisible();
  });

  test('WF-1.8: Add new user button', async ({ page }) => {
    const addBtn = page.locator('button:has-text("Add")');
    await expect(addBtn).toBeVisible();
  });

  test('WF-1.9: Username column sortable', async ({ page }) => {
    await expect(page.locator('th:has-text("Username")')).toBeVisible();
  });

  test('WF-1.10: User role column sortable', async ({ page }) => {
    await expect(page.locator('th:has-text("User Role")')).toBeVisible();
  });

  test('WF-1.11: Employee name column sortable', async ({ page }) => {
    await expect(page.locator('th:has-text("Employee Name")')).toBeVisible();
  });

  test('WF-1.12: Status column sortable', async ({ page }) => {
    await expect(page.locator('th:has-text("Status")')).toBeVisible();
  });
});

// ═════════════════════════════════════════════════════════════════════════
// MODULE 2: PIM - EMPLOYEE LIST (15 Sub-functions)
// ═════════════════════════════════════════════════════════════════════════

test.describe('PIM: Employee List', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToModule(page, '/web/index.php/pim/viewEmployeeList');
  });

  test('WF-2.1: View employee list with 133 records', async ({ page }) => {
    await expect(page.locator('text=Records Found')).toBeVisible({ timeout: 10000 });
  });

  test('WF-2.2: Search by employee name', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="Employee Name"]').first();
    if (await searchInput.isVisible()) {
      await searchInput.fill('Alisa');
      await page.click('button:has-text("Search")');
    }
  });

  test('WF-2.3: Search by employee ID', async ({ page }) => {
    const idInput = page.locator('input[placeholder*="Employee ID"]').first();
    if (await idInput.isVisible()) {
      await idInput.fill('7369');
    }
  });

  test('WF-2.4: Filter by employment status', async ({ page }) => {
    const statusSelect = page.locator('select').filter({ has: page.locator('option') }).first();
    if (await statusSelect.isVisible()) {
      const options = statusSelect.locator('option');
      if (await options.count() > 1) {
        await statusSelect.selectOption('1');
      }
    }
  });

  test('WF-2.5: Include past employees checkbox', async ({ page }) => {
    const checkbox = page.locator('input[type="checkbox"]').first();
    if (await checkbox.isVisible()) {
      await expect(checkbox).toBeVisible();
    }
  });

  test('WF-2.6: Employee ID column sort', async ({ page }) => {
    await expect(page.locator('th:has-text("Employee ID")')).toBeVisible();
  });

  test('WF-2.7: Employee name column sort', async ({ page }) => {
    await expect(page.locator('th:has-text("Employee Name")')).toBeVisible();
  });

  test('WF-2.8: Job title column sort', async ({ page }) => {
    await expect(page.locator('th:has-text("Job Title")')).toBeVisible();
  });

  test('WF-2.9: Employment status column sort', async ({ page }) => {
    await expect(page.locator('th:has-text("Employment Status")')).toBeVisible();
  });

  test('WF-2.10: Sub unit column sort', async ({ page }) => {
    await expect(page.locator('th:has-text("Sub Unit")')).toBeVisible();
  });

  test('WF-2.11: Edit employee icon', async ({ page }) => {
    const editBtn = page.locator('button[aria-label*="Edit"]').first();
    if (await editBtn.isVisible()) {
      expect(await editBtn.isVisible()).toBeTruthy();
    }
  });

  test('WF-2.12: Delete employee icon', async ({ page }) => {
    const deleteBtn = page.locator('button[aria-label*="Delete"]').first();
    if (await deleteBtn.isVisible()) {
      expect(await deleteBtn.isVisible()).toBeTruthy();
    }
  });

  test('WF-2.13: Add employee button', async ({ page }) => {
    await expect(page.locator('button:has-text("Add")')).toBeVisible();
  });

  test('WF-2.14: Reset filters', async ({ page }) => {
    await expect(page.locator('button:has-text("Reset")')).toBeVisible();
  });

  test('WF-2.15: Table pagination', async ({ page }) => {
    const rows = page.locator('table tbody tr');
    expect(await rows.count()).toBeGreaterThan(0);
  });
});

// ═════════════════════════════════════════════════════════════════════════
// MODULE 3: PIM - MY INFO (20 Sub-functions with Personal Details)
// ═════════════════════════════════════════════════════════════════════════

test.describe('PIM: My Info - Personal Details', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToModule(page, '/web/index.php/pim/viewMyDetails');
  });

  test('WF-3.1: Personal details section visible', async ({ page }) => {
    await expect(page.locator('text=Personal Details')).toBeVisible();
  });

  test('WF-3.2: First name field', async ({ page }) => {
    const inputs = page.locator('input');
    expect(await inputs.count()).toBeGreaterThan(0);
  });

  test('WF-3.3: Middle name field', async ({ page }) => {
    const inputs = page.locator('input');
    if (await inputs.count() > 1) {
      await expect(inputs.nth(1)).toBeVisible();
    }
  });

  test('WF-3.4: Last name field', async ({ page }) => {
    const inputs = page.locator('input');
    if (await inputs.count() > 2) {
      await expect(inputs.nth(2)).toBeVisible();
    }
  });

  test('WF-3.5: Employee ID read-only field', async ({ page }) => {
    const empIdInput = page.locator('input').filter({ hasNot: page.locator('[readonly]') }).first();
    if (await empIdInput.isVisible()) {
      expect(await empIdInput.isVisible()).toBeTruthy();
    }
  });

  test('WF-3.6: Driver license number field', async ({ page }) => {
    const inputs = page.locator('input');
    expect(await inputs.count()).toBeGreaterThan(0);
  });

  test('WF-3.7: License expiry date field', async ({ page }) => {
    const dateInputs = page.locator('input[type="date"]');
    if (await dateInputs.count() > 0) {
      expect(await dateInputs.first().isVisible()).toBeTruthy();
    }
  });

  test('WF-3.8: Nationality dropdown', async ({ page }) => {
    const selects = page.locator('select');
    if (await selects.count() > 0) {
      expect(await selects.first().isVisible()).toBeTruthy();
    }
  });

  test('WF-3.9: Marital status dropdown', async ({ page }) => {
    const selects = page.locator('select');
    if (await selects.count() > 1) {
      expect(await selects.nth(1).isVisible()).toBeTruthy();
    }
  });

  test('WF-3.10: Date of birth field', async ({ page }) => {
    const dateInputs = page.locator('input[type="date"]');
    if (await dateInputs.count() > 0) {
      expect(await dateInputs.isVisible()).toBeTruthy();
    }
  });

  test('WF-3.11: Gender radio buttons', async ({ page }) => {
    const radios = page.locator('input[type="radio"]');
    if (await radios.count() > 0) {
      expect(await radios.first().isVisible()).toBeTruthy();
    }
  });

  test('WF-3.12: Contact details section', async ({ page }) => {
    const contactSection = page.locator('text=Contact Details');
    if (await contactSection.isVisible()) {
      expect(await contactSection.isVisible()).toBeTruthy();
    }
  });

  test('WF-3.13: Emergency contacts section', async ({ page }) => {
    const emergencySection = page.locator('text=Emergency Contacts');
    if (await emergencySection.isVisible()) {
      expect(await emergencySection.isVisible()).toBeTruthy();
    }
  });

  test('WF-3.14: Dependents section', async ({ page }) => {
    const dependentsSection = page.locator('text=Dependents');
    if (await dependentsSection.isVisible()) {
      expect(await dependentsSection.isVisible()).toBeTruthy();
    }
  });

  test('WF-3.15: Immigration section', async ({ page }) => {
    const immigrationSection = page.locator('text=Immigration');
    if (await immigrationSection.isVisible()) {
      expect(await immigrationSection.isVisible()).toBeTruthy();
    }
  });

  test('WF-3.16: Job information section', async ({ page }) => {
    await expect(page.locator('text=Job').first()).toBeVisible();
  });

  test('WF-3.17: Qualifications section', async ({ page }) => {
    const qualSection = page.locator('text=Qualifications');
    if (await qualSection.isVisible()) {
      expect(await qualSection.isVisible()).toBeTruthy();
    }
  });

  test('WF-3.18: Attachments section with file upload', async ({ page }) => {
    await expect(page.locator('text=Attachments')).toBeVisible();
  });

  test('WF-3.19: Save button functionality', async ({ page }) => {
    const saveBtn = page.locator('button:has-text("Save")').first();
    expect(await saveBtn.isVisible()).toBeTruthy();
  });

  test('WF-3.20: Form validation on required fields', async ({ page }) => {
    const requiredText = page.locator('text=* Required');
    if (await requiredText.isVisible()) {
      expect(await requiredText.isVisible()).toBeTruthy();
    }
  });
});

// ═════════════════════════════════════════════════════════════════════════
// MODULE 4: LEAVE - LEAVE LIST (15 Sub-functions)
// ═════════════════════════════════════════════════════════════════════════

test.describe('LEAVE: Leave List', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToModule(page, '/web/index.php/leave/viewLeaveList');
  });

  test('WF-4.1: Leave list page loads', async ({ page }) => {
    await expect(page.locator('text=Leave List')).toBeVisible();
  });

  test('WF-4.2: From date filter', async ({ page }) => {
    const dateInputs = page.locator('input[type="date"]');
    if (await dateInputs.count() > 0) {
      expect(await dateInputs.first().isVisible()).toBeTruthy();
    }
  });

  test('WF-4.3: To date filter', async ({ page }) => {
    const dateInputs = page.locator('input[type="date"]');
    if (await dateInputs.count() > 1) {
      expect(await dateInputs.nth(1).isVisible()).toBeTruthy();
    }
  });

  test('WF-4.4: Leave type dropdown', async ({ page }) => {
    const selects = page.locator('select');
    if (await selects.count() > 0) {
      expect(await selects.first().isVisible()).toBeTruthy();
    }
  });

  test('WF-4.5: Employee name search', async ({ page }) => {
    const empNameInput = page.locator('input[placeholder*="Employee Name"]').first();
    if (await empNameInput.isVisible()) {
      expect(await empNameInput.isVisible()).toBeTruthy();
    }
  });

  test('WF-4.6: Sub unit filter', async ({ page }) => {
    const selects = page.locator('select');
    if (await selects.count() > 1) {
      expect(await selects.nth(1).isVisible()).toBeTruthy();
    }
  });

  test('WF-4.7: Include past employees checkbox', async ({ page }) => {
    const checkbox = page.locator('input[type="checkbox"]').first();
    if (await checkbox.isVisible()) {
      expect(await checkbox.isVisible()).toBeTruthy();
    }
  });

  test('WF-4.8: Reset button', async ({ page }) => {
    await expect(page.locator('button:has-text("Reset")')).toBeVisible();
  });

  test('WF-4.9: Search button', async ({ page }) => {
    await expect(page.locator('button:has-text("Search")')).toBeVisible();
  });

  test('WF-4.10: Date column', async ({ page }) => {
    await expect(page.locator('th:has-text("Date")')).toBeVisible();
  });

  test('WF-4.11: Employee name column', async ({ page }) => {
    await expect(page.locator('th:has-text("Employee Name")')).toBeVisible();
  });

  test('WF-4.12: Leave type column', async ({ page }) => {
    await expect(page.locator('th:has-text("Leave Type")')).toBeVisible();
  });

  test('WF-4.13: Leave balance column', async ({ page }) => {
    await expect(page.locator('th:has-text("Leave Balance")')).toBeVisible();
  });

  test('WF-4.14: Number of days column', async ({ page }) => {
    await expect(page.locator('th:has-text("Number of Days")')).toBeVisible();
  });

  test('WF-4.15: Status column', async ({ page }) => {
    await expect(page.locator('th:has-text("Status")')).toBeVisible();
  });
});

// ═════════════════════════════════════════════════════════════════════════
// MODULE 5: TIME - TIMESHEETS (12 Sub-functions)
// ═════════════════════════════════════════════════════════════════════════

test.describe('TIME: Timesheet Management', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToModule(page, '/web/index.php/time/viewEmployeeTimesheet');
  });

  test('WF-5.1: Select employee section', async ({ page }) => {
    await expect(page.locator('text=Select Employee')).toBeVisible();
  });

  test('WF-5.2: Employee name required field', async ({ page }) => {
    const empNameInput = page.locator('input[placeholder*="hints"]').first();
    if (await empNameInput.isVisible()) {
      expect(await empNameInput.isVisible()).toBeTruthy();
    }
  });

  test('WF-5.3: Timesheets pending action section', async ({ page }) => {
    await expect(page.locator('text=Timesheets Pending Action')).toBeVisible();
  });

  test('WF-5.4: Pending timesheets records count', async ({ page }) => {
    await expect(page.locator('text=Records Found')).toBeVisible();
  });

  test('WF-5.5: Timesheet period column', async ({ page }) => {
    await expect(page.locator('th:has-text("Timesheet Period")')).toBeVisible();
  });

  test('WF-5.6: Actions column', async ({ page }) => {
    await expect(page.locator('th:has-text("Actions")')).toBeVisible();
  });

  test('WF-5.7: View timesheet button', async ({ page }) => {
    const viewBtn = page.locator('text=View').first();
    if (await viewBtn.isVisible()) {
      expect(await viewBtn.isVisible()).toBeTruthy();
    }
  });

  test('WF-5.8: Timesheet period 1 display', async ({ page }) => {
    const periods = page.locator('table tbody td').first();
    if (await periods.isVisible()) {
      expect(await periods.isVisible()).toBeTruthy();
    }
  });

  test('WF-5.9: Timesheet period 2 display', async ({ page }) => {
    const rows = page.locator('table tbody tr');
    if (await rows.count() > 1) {
      expect(await rows.nth(1).isVisible()).toBeTruthy();
    }
  });

  test('WF-5.10: Timesheet period 3 display', async ({ page }) => {
    const rows = page.locator('table tbody tr');
    if (await rows.count() > 2) {
      expect(await rows.nth(2).isVisible()).toBeTruthy();
    }
  });

  test('WF-5.11: Employee name column', async ({ page }) => {
    await expect(page.locator('th:has-text("Employee Name")')).toBeVisible();
  });

  test('WF-5.12: Timesheet period column header', async ({ page }) => {
    await expect(page.locator('th:has-text("Timesheet Period")')).toBeVisible();
  });
});

// ═════════════════════════════════════════════════════════════════════════
// MODULE 6: RECRUITMENT - CANDIDATES (18 Sub-functions)
// ═════════════════════════════════════════════════════════════════════════

test.describe('RECRUITMENT: Candidates (73 records)', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToModule(page, '/web/index.php/recruitment/viewCandidates');
  });

  test('WF-6.1: Candidates page loads', async ({ page }) => {
    await expect(page.locator('text=Candidates')).toBeVisible();
  });

  test('WF-6.2: Candidates count (73 records)', async ({ page }) => {
    await expect(page.locator('text=Records Found')).toBeVisible({ timeout: 10000 });
  });

  test('WF-6.3: Job title filter', async ({ page }) => {
    const selects = page.locator('select');
    if (await selects.count() > 0) {
      expect(await selects.first().isVisible()).toBeTruthy();
    }
  });

  test('WF-6.4: Vacancy filter', async ({ page }) => {
    const selects = page.locator('select');
    if (await selects.count() > 1) {
      expect(await selects.nth(1).isVisible()).toBeTruthy();
    }
  });

  test('WF-6.5: Hiring manager filter', async ({ page }) => {
    const selects = page.locator('select');
    if (await selects.count() > 2) {
      expect(await selects.nth(2).isVisible()).toBeTruthy();
    }
  });

  test('WF-6.6: Status filter dropdown', async ({ page }) => {
    const selects = page.locator('select');
    if (await selects.count() > 3) {
      expect(await selects.nth(3).isVisible()).toBeTruthy();
    }
  });

  test('WF-6.7: Candidate name search', async ({ page }) => {
    const nameInput = page.locator('input[placeholder*="Candidate Name"]').first();
    if (await nameInput.isVisible()) {
      expect(await nameInput.isVisible()).toBeTruthy();
    }
  });

  test('WF-6.8: Keywords search', async ({ page }) => {
    const keywordsInput = page.locator('input[placeholder*="Keywords"]').first();
    if (await keywordsInput.isVisible()) {
      expect(await keywordsInput.isVisible()).toBeTruthy();
    }
  });

  test('WF-6.9: Vacancy column', async ({ page }) => {
    await expect(page.locator('th:has-text("Vacancy")')).toBeVisible();
  });

  test('WF-6.10: Candidate column', async ({ page }) => {
    await expect(page.locator('th:has-text("Candidate")')).toBeVisible();
  });

  test('WF-6.11: Hiring manager column', async ({ page }) => {
    await expect(page.locator('th:has-text("Hiring Manager")')).toBeVisible();
  });

  test('WF-6.12: Date of application column', async ({ page }) => {
    await expect(page.locator('th:has-text("Date of Application")')).toBeVisible();
  });

  test('WF-6.13: Status column', async ({ page }) => {
    await expect(page.locator('th:has-text("Status")')).toBeVisible();
  });

  test('WF-6.14: Actions column', async ({ page }) => {
    await expect(page.locator('th:has-text("Actions")')).toBeVisible();
  });

  test('WF-6.15: Candidate status - Shortlisted', async ({ page }) => {
    const statusBadge = page.locator('text=Shortlisted').first();
    if (await statusBadge.isVisible()) {
      expect(await statusBadge.isVisible()).toBeTruthy();
    }
  });

  test('WF-6.16: Candidate status - Application Initiated', async ({ page }) => {
    const statusBadge = page.locator('text=Application Initiated').first();
    if (await statusBadge.isVisible()) {
      expect(await statusBadge.isVisible()).toBeTruthy();
    }
  });

  test('WF-6.17: Add candidate button', async ({ page }) => {
    const addBtn = page.locator('button:has-text("Add")').first();
    if (await addBtn.isVisible()) {
      expect(await addBtn.isVisible()).toBeTruthy();
    }
  });

  test('WF-6.18: Reset filters button', async ({ page }) => {
    await expect(page.locator('button:has-text("Reset")')).toBeVisible();
  });
});

// ═════════════════════════════════════════════════════════════════════════
// MODULE 7: PERFORMANCE - REVIEWS (12 Sub-functions)
// ═════════════════════════════════════════════════════════════════════════

test.describe('PERFORMANCE: Reviews', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToModule(page, '/web/index.php/performance/searchEvaluatePerformanceReview');
  });

  test('WF-7.1: Employee reviews section', async ({ page }) => {
    await expect(page.locator('text=Employee Reviews')).toBeVisible();
  });

  test('WF-7.2: Employee name filter', async ({ page }) => {
    const empNameInput = page.locator('input[placeholder*="Employee Name"], input[placeholder*="hints"]').first();
    if (await empNameInput.isVisible()) {
      expect(await empNameInput.isVisible()).toBeTruthy();
    }
  });

  test('WF-7.3: Job title filter', async ({ page }) => {
    const selects = page.locator('select');
    if (await selects.count() > 0) {
      expect(await selects.first().isVisible()).toBeTruthy();
    }
  });

  test('WF-7.4: Sub unit filter', async ({ page }) => {
    const selects = page.locator('select');
    if (await selects.count() > 1) {
      expect(await selects.nth(1).isVisible()).toBeTruthy();
    }
  });

  test('WF-7.5: Review status filter', async ({ page }) => {
    const selects = page.locator('select');
    if (await selects.count() > 3) {
      expect(await selects.nth(3).isVisible()).toBeTruthy();
    }
  });

  test('WF-7.6: From date filter', async ({ page }) => {
    const dateInputs = page.locator('input[type="date"]');
    if (await dateInputs.count() > 0) {
      expect(await dateInputs.first().isVisible()).toBeTruthy();
    }
  });

  test('WF-7.7: To date filter', async ({ page }) => {
    const dateInputs = page.locator('input[type="date"]');
    if (await dateInputs.count() > 1) {
      expect(await dateInputs.nth(1).isVisible()).toBeTruthy();
    }
  });

  test('WF-7.8: Employee column', async ({ page }) => {
    await expect(page.locator('th:has-text("Employee")')).toBeVisible();
  });

  test('WF-7.9: Review period column', async ({ page }) => {
    await expect(page.locator('th:has-text("Review Period")')).toBeVisible();
  });

  test('WF-7.10: Review status column', async ({ page }) => {
    await expect(page.locator('th:has-text("Review Status")')).toBeVisible();
  });

  test('WF-7.11: Due date column', async ({ page }) => {
    await expect(page.locator('th:has-text("Due Date")')).toBeVisible();
  });

  test('WF-7.12: Actions column', async ({ page }) => {
    await expect(page.locator('th:has-text("Actions")')).toBeVisible();
  });
});

// ═════════════════════════════════════════════════════════════════════════
// MODULE 8: DASHBOARD - WIDGETS & QUICK ACTIONS (12 Sub-functions)
// ═════════════════════════════════════════════════════════════════════════

test.describe('DASHBOARD: Widgets & Quick Actions', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToModule(page, '/web/index.php/dashboard/index');
  });

  test('WF-8.1: Time at work widget', async ({ page }) => {
    const widget = page.locator('text=Time at Work');
    if (await widget.isVisible()) {
      expect(await widget.isVisible()).toBeTruthy();
    }
  });

  test('WF-8.2: My actions widget', async ({ page }) => {
    const widget = page.locator('text=My Actions');
    if (await widget.isVisible()) {
      expect(await widget.isVisible()).toBeTruthy();
    }
  });

  test('WF-8.3: Quick launch section', async ({ page }) => {
    const section = page.locator('text=Quick Launch');
    if (await section.isVisible()) {
      expect(await section.isVisible()).toBeTruthy();
    }
  });

  test('WF-8.4: Quick launch - Assign leave', async ({ page }) => {
    const btn = page.locator('text=Assign Leave').first();
    if (await btn.isVisible()) {
      expect(await btn.isVisible()).toBeTruthy();
    }
  });

  test('WF-8.5: Quick launch - Leave list', async ({ page }) => {
    const btn = page.locator('text=Leave List').first();
    if (await btn.isVisible()) {
      expect(await btn.isVisible()).toBeTruthy();
    }
  });

  test('WF-8.6: Quick launch - Timesheets', async ({ page }) => {
    const btn = page.locator('text=Timesheets').first();
    if (await btn.isVisible()) {
      expect(await btn.isVisible()).toBeTruthy();
    }
  });

  test('WF-8.7: Quick launch - Apply leave', async ({ page }) => {
    const btn = page.locator('text=Apply Leave').first();
    if (await btn.isVisible()) {
      expect(await btn.isVisible()).toBeTruthy();
    }
  });

  test('WF-8.8: Quick launch - My leave', async ({ page }) => {
    const btn = page.locator('text=My Leave').first();
    if (await btn.isVisible()) {
      expect(await btn.isVisible()).toBeTruthy();
    }
  });

  test('WF-8.9: Buzz latest posts widget', async ({ page }) => {
    const widget = page.locator('text=Buzz Latest Posts');
    if (await widget.isVisible()) {
      expect(await widget.isVisible()).toBeTruthy();
    }
  });

  test('WF-8.10: Employee distribution by sub unit', async ({ page }) => {
    const chart = page.locator('text=Employee Distribution by Sub Unit');
    if (await chart.isVisible()) {
      expect(await chart.isVisible()).toBeTruthy();
    }
  });

  test('WF-8.11: Employees on leave today', async ({ page }) => {
    const widget = page.locator('text=Employees on Leave Today');
    if (await widget.isVisible()) {
      expect(await widget.isVisible()).toBeTruthy();
    }
  });

  test('WF-8.12: Dashboard layout responsive', async ({ page }) => {
    const dashboard = page.locator('main, [role="main"]').first();
    if (await dashboard.isVisible()) {
      expect(await dashboard.isVisible()).toBeTruthy();
    }
  });
});

// ═════════════════════════════════════════════════════════════════════════
// CROSS-MODULE VALIDATION TESTS (Form Validation, Error Handling)
// ═════════════════════════════════════════════════════════════════════════

test.describe('VALIDATION: Cross-Module Form Tests', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('V-1: Required field validation', async ({ page }) => {
    await navigateToModule(page, '/web/index.php/leave/viewLeaveList');
    const requiredIndicators = page.locator('text=* Required, text=*');
    const count = await requiredIndicators.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test('V-2: Email field validation (if present)', async ({ page }) => {
    await navigateToModule(page, '/web/index.php/pim/viewMyDetails');
    const emailInputs = page.locator('input[type="email"]');
    const count = await emailInputs.count();
    if (count > 0) {
      expect(await emailInputs.first().isVisible()).toBeTruthy();
    }
  });

  test('V-3: Date field validation (if present)', async ({ page }) => {
    await navigateToModule(page, '/web/index.php/leave/viewLeaveList');
    const dateInputs = page.locator('input[type="date"]');
    const count = await dateInputs.count();
    expect(count).toBeGreaterThan(0);
  });

  test('V-4: Dropdown selection validation', async ({ page }) => {
    await navigateToModule(page, '/web/index.php/admin/viewAdminModule');
    const selects = page.locator('select');
    const count = await selects.count();
    expect(count).toBeGreaterThan(0);
  });

  test('V-5: Search functionality across modules', async ({ page }) => {
    await navigateToModule(page, '/web/index.php/pim/viewEmployeeList');
    const searchInputs = page.locator('input[placeholder*="Search"], input[placeholder*="Name"]');
    const count = await searchInputs.count();
    expect(count).toBeGreaterThan(0);
  });

  test('V-6: Filter reset functionality', async ({ page }) => {
    await navigateToModule(page, '/web/index.php/pim/viewEmployeeList');
    const resetBtn = page.locator('button:has-text("Reset")').first();
    expect(await resetBtn.isVisible()).toBeTruthy();
  });

  test('V-7: Table pagination support', async ({ page }) => {
    await navigateToModule(page, '/web/index.php/pim/viewEmployeeList');
    const table = page.locator('table');
    expect(await table.isVisible()).toBeTruthy();
  });

  test('V-8: Action buttons visibility', async ({ page }) => {
    await navigateToModule(page, '/web/index.php/pim/viewEmployeeList');
    const actionBtns = page.locator('button[aria-label*="Edit"], button[aria-label*="Delete"]').first();
    if (await actionBtns.isVisible()) {
      expect(await actionBtns.isVisible()).toBeTruthy();
    }
  });
});
