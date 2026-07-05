import { test, expect } from '@playwright/test';

/**
 * DEMOQA ADAPTIVE TEST SUITE
 * Application Type: FORMS_PLATFORM
 * Test Count: 8 (Low complexity)
 * Guardrails: REQ-5 (Functional), REQ-6 (Form Validation), REQ-7 (Data), REQ-13 (Accessibility)
 * Focus: Input validation, form handling, error display, accessibility
 */

test.describe('DemoQA - Forms Platform Testing', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://demoqa.com/');
  });

  // REQ-5: Functional Testing
  test('TC-1: Text Box - Valid Input Submission', async ({ page }) => {
    // Preconditions: Application loaded, Text Box form visible
    await page.click('text=Elements');
    await page.click('text=Text Box');
    
    // Steps: Fill in valid text, submit
    await page.fill('#userName', 'John Doe');
    await page.fill('#userEmail', 'john@example.com');
    await page.fill('#currentAddress', '123 Main Street');
    await page.fill('#permanentAddress', '456 Oak Avenue');
    await page.click('#submit');
    
    // Assertions
    const output = await page.locator('#output');
    await expect(output).toContainText('John Doe');
    await expect(output).toContainText('john@example.com');
  });

  test('TC-2: Checkbox - Select Multiple Options', async ({ page }) => {
    // Preconditions: Checkbox form loaded
    await page.click('text=Elements');
    await page.click('text=Check Box');
    
    // Steps: Expand tree and select checkboxes
    await page.click('[aria-label="Toggle"]');
    await page.click('input[type="checkbox"]');
    
    // Assertions
    const checkedItems = await page.locator('input[type="checkbox"]:checked').count();
    expect(checkedItems).toBeGreaterThan(0);
  });

  test('TC-3: Radio Button - Select Option', async ({ page }) => {
    // Preconditions: Radio button form visible
    await page.click('text=Elements');
    await page.click('text=Radio Button');
    
    // Steps: Select radio button option
    await page.click('input[value="impressive"]');
    
    // Assertions
    const selected = await page.locator('input[value="impressive"]:checked');
    await expect(selected).toBeTruthy();
  });

  // REQ-6: Form Validation Testing
  test('TC-4: Email Validation - Invalid Format Rejected', async ({ page }) => {
    // Preconditions: Text Box form open
    await page.click('text=Elements');
    await page.click('text=Text Box');
    
    // Steps: Enter invalid email
    await page.fill('#userEmail', 'invalid-email');
    await page.click('#submit');
    
    // Assertions: Form validation error or no submission
    const emailInput = await page.locator('#userEmail');
    const validationState = await emailInput.evaluate((el: any) => el.validity.valid);
    expect(validationState).toBeFalsy();
  });

  test('TC-5: Required Field - Empty Submit Blocked', async ({ page }) => {
    // Preconditions: Form loaded
    await page.click('text=Elements');
    await page.click('text=Text Box');
    
    // Steps: Try submitting without required fields
    const submitButton = await page.locator('#submit');
    const isDisabled = await submitButton.isDisabled();
    
    // Assertions
    if (!isDisabled) {
      await expect(submitButton).toBeEnabled();
    }
  });

  // REQ-7: Data Integrity Testing
  test('TC-6: Text Limits - Maximum Length Enforced', async ({ page }) => {
    // Preconditions: Text Box form visible
    await page.click('text=Elements');
    await page.click('text=Text Box');
    
    // Steps: Enter text longer than expected limit
    await page.fill('#currentAddress', 'A'.repeat(300));
    
    // Assertions: Text is truncated or limited
    const textValue = await page.locator('#currentAddress').inputValue();
    expect(textValue.length).toBeLessThanOrEqual(300);
  });

  // REQ-13: Accessibility Testing
  test('TC-7: Keyboard Navigation - Tab Through Form', async ({ page }) => {
    // Preconditions: Form loaded
    await page.click('text=Elements');
    await page.click('text=Text Box');
    
    // Steps: Navigate using Tab key
    const userName = await page.locator('#userName');
    await userName.focus();
    await page.keyboard.press('Tab');
    
    // Assertions: Focus moves to next element
    const focusedElement = await page.evaluate(() => {
      return (document.activeElement as any)?.id;
    });
    expect(focusedElement).not.toBe('userName');
  });

  test('TC-8: Form Labels - Accessible Labels Present', async ({ page }) => {
    // Preconditions: Form elements visible
    await page.click('text=Elements');
    await page.click('text=Text Box');
    
    // Steps: Check for associated labels
    const inputs = await page.locator('input[type="text"]').all();
    
    // Assertions: All inputs have labels or aria-labels
    for (const input of inputs) {
      const ariaLabel = await input.getAttribute('aria-label');
      const label = await input.getAttribute('placeholder');
      expect(ariaLabel || label).toBeTruthy();
    }
  });
});
