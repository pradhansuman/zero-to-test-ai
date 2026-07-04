# ⚡ QUICK REFERENCE CARD - Testing Scope Framework

## For When You're Starting a NEW Application

**Status:** Quick lookup guide  
**Use:** Before writing ANY tests

---

## The 30-Second Version

```
1. Complete TESTING_SCOPE_FRAMEWORK.md
2. Get stakeholder approval
3. Then test per scope
4. Report against scope

Done.
```

---

## The 5-Minute Version

### Step 1: ANALYZE (What does the app do?)
- [ ] List all features
- [ ] Document user flows
- [ ] Identify integrations
- [ ] Map data entities

### Step 2: SCOPE (What will we test?)
- [ ] List what we WILL test
- [ ] List what we WON'T test
- [ ] Create test matrix
- [ ] Assess risks

### Step 3: APPROVE (Who agrees?)
- [ ] Product Owner ✓
- [ ] Engineering ✓
- [ ] QA ✓
- [ ] Business ✓

### Step 4: TEST (Per the scope)
- [ ] Phase 1: UI tests (15-20%)
- [ ] Phase 2: Functional tests (25-30%)
- [ ] Phase 3: Integration tests (15-20%)
- [ ] Phase 4: Business logic (15-20%)
- [ ] Phase 5: Error/Edge cases (10-15%)

### Step 5: REPORT (Professional format)
- [ ] Generate dashboard
- [ ] Compare to scope
- [ ] Document gaps
- [ ] Get sign-off

---

## Test Distribution (Must Follow)

```
TOTAL TESTS: 100%
├─ UI Tests: 15-20%
├─ Functional Tests: 25-30%
├─ Integration Tests: 15-20%
├─ Business Logic: 15-20%
└─ Error/Edge Cases: 10-15%

DON'T SKIP ANY CATEGORY
```

---

## Red Flags (Stop If You See These)

```
🔴 No scope document
🔴 No stakeholder approval
🔴 Only UI tests (no functional)
🔴 Skipping critical features
🔴 No integration testing
🔴 No business logic testing
🔴 No gaps documented
🔴 Wrong report format

Fix before proceeding.
```

---

## Critical Features to Always Test

```
PAYMENT PROCESSING
├─ Valid card works
├─ Invalid card fails
├─ Amount correct
└─ Transaction logged

ORDER CREATION
├─ Order in database
├─ Items correct
├─ Total accurate
└─ Status tracked

USER DATA
├─ Password hashed
├─ Email verified
├─ Data persists
└─ Sessions managed

CHECKOUT FLOW
├─ All fields required
├─ Address validated
├─ Total calculated
└─ Email sent

Never skip these!
```

---

## Risk-Based Testing

```
🔴 CRITICAL (5+ tests)
├─ Payment processing
├─ Order creation
├─ User authentication
└─ Data persistence

🟠 HIGH (3-4 tests)
├─ Checkout flow
├─ Calculations (tax, shipping)
├─ Inventory management
└─ Email notifications

🟡 MEDIUM (2-3 tests)
├─ Product browsing
├─ Search/filtering
├─ Form validation
└─ Error messages

🟢 LOW (1-2 tests)
├─ UI rendering
├─ Navigation
├─ Static content
└─ Help text
```

---

## What NOT to Do

```
❌ Test without scope
❌ Only test UI presence
❌ Skip critical features
❌ No stakeholder approval
❌ Mix test categories
❌ Unbalanced distribution
❌ Missing integrations
❌ Wrong report format
❌ No gaps documented

Fix any of these → STOP testing
```

---

## Professional Report (MANDATORY)

```
EVERY test MUST generate:

✅ KPI Cards
  ├─ Total Tests
  ├─ Passed (✅ Green)
  ├─ Failed (❌ Red)
  └─ Skipped (⚠️ Yellow)

✅ Analytics
  ├─ Pass Rate Pie Chart
  └─ Browser Coverage

✅ Suite Breakdown
  ├─ Per-suite metrics
  └─ Pass rates

✅ Test Results Table
  ├─ Test name
  ├─ Suite
  ├─ Browser
  └─ Status

File: [app-name]-qa-dashboard.html

NO EXCEPTIONS.
```

---

## Templates to Use

```
Copy-paste template file:
→ TESTING_SCOPE_FRAMEWORK.md

Rename to:
→ [APPLICATION_NAME]_SCOPE_DOCUMENT.md

Fill in all 5 parts:
1. Application Analysis
2. Testing Scope Definition
3. Risk Assessment
4. Test Execution Plan
5. Sign-Off

Get approval before testing!
```

---

## Common Mistakes (Don't Make These)

```
❌ Mistake: Only testing UI
   ✅ Fix: Test functionality, integrations, logic

❌ Mistake: No risk assessment
   ✅ Fix: Identify critical features (5+ tests each)

❌ Mistake: Same tests for all features
   ✅ Fix: More tests for critical features

❌ Mistake: No integration testing
   ✅ Fix: Test APIs, databases, email

❌ Mistake: Skipping business logic
   ✅ Fix: Test calculations, rules, constraints

❌ Mistake: No error scenario testing
   ✅ Fix: Test validation, security, edge cases

❌ Mistake: No gaps documented
   ✅ Fix: Explicitly list what's out-of-scope and why

❌ Mistake: Wrong report format
   ✅ Fix: Use mandatory dashboard format
```

---

## Files You'll Create

```
1. [APP_NAME]_SCOPE_DOCUMENT.md
   → Use TESTING_SCOPE_FRAMEWORK.md as template
   → Complete all 5 parts
   → Get approvals

2. [APP_NAME]_TEST_MATRIX.md
   → Detailed test breakdown
   → By category and risk level

3. [APP_NAME]_TEST_SUITE.ts
   → All test cases
   → Per approved scope

4. [APP_NAME]-qa-dashboard.html
   → Generated report
   → Mandatory format
   → Auto-generated after tests

5. [APP_NAME]_FINAL_REPORT.md
   → Scope vs actual comparison
   → Gaps documented
   → Sign-off
```

---

## Decision Tree

```
Starting a NEW application?

        ↓ NO scope document yet?
        ├─ Create TESTING_SCOPE_FRAMEWORK.md
        └─ Go to next step

        ↓ Got stakeholder approval?
        ├─ If NO: Get approval first
        └─ If YES: Go to next step

        ↓ Test matrix created?
        ├─ If NO: Create test matrix
        └─ If YES: Go to next step

        ↓ Tests written?
        ├─ If NO: Write tests per scope
        └─ If YES: Go to next step

        ↓ Tests executed?
        ├─ If NO: Run tests
        └─ If YES: Go to next step

        ↓ Dashboard generated?
        ├─ If NO: Generate dashboard
        └─ If YES: Go to next step

        ↓ COMPLETE!
        └─ Report ready for sign-off
```

---

## Checklist: Am I Ready to Test?

```
PRE-TESTING CHECKLIST:

□ Scope document completed
□ All 5 parts filled in
□ Features analyzed
□ Tests defined (IN + OUT)
□ Risk assessment done
□ Test matrix created
□ Execution plan ready
□ Product Owner approved
□ Engineering approved
□ QA approved
□ Business approved
□ Timeline set
□ Blockers identified
□ Dependencies clear

If any unchecked → STOP and fix before testing

All checked? → YOU'RE READY TO TEST!
```

---

## During Testing: Watch For

```
EXECUTION PHASE:

✓ Following test matrix distribution
✓ Critical features heavily tested
✓ Medium/low features appropriately tested
✓ All test phases represented
✓ Tests are independent
✓ No flaky tests
✓ Clear test names
✓ Clear assertions

If something wrong → Fix immediately
```

---

## Final Report: What to Include

```
REPORT MUST HAVE:

✓ Mandatory dashboard (KPI cards, charts, tables)
✓ Coverage metrics (by category)
✓ Gaps vs scope (what we didn't test)
✓ Known issues (with links to tickets)
✓ Recommendations (for next phase)
✓ Sign-off section (approvals)

NO EXCEPTIONS ON FORMAT.
```

---

## One-Liner Rules

```
NO TESTING WITHOUT SCOPE
NO SCOPE WITHOUT APPROVAL
NO APPROVAL WITHOUT ANALYSIS
NO WRONG REPORT FORMAT
NO SKIPPED CRITICAL FEATURES
NO UNBALANCED TEST DISTRIBUTION
NO UNDOCUMENTED GAPS
NO EXCEPTIONS
```

---

## For Questions

```
"How do I scope test?"
→ See: TESTING_SCOPE_FRAMEWORK.md

"What's the right approach?"
→ See: TRICENTIS_SCOPE_DOCUMENT.md

"What did we do wrong?"
→ See: TEST_GAP_ANALYSIS.md

"What's the new standard?"
→ See: MANDATORY_SCOPE_ENFORCEMENT.md

"What's the report format?"
→ See: MANDATORY_REPORT_FORMAT.md
```

---

**That's it. Apply this framework to every new application.**

**No scope = No testing.**

**Scope first, test second, report always.**
