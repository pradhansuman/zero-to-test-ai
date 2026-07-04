# 📋 TESTING SCOPE FRAMEWORK

## 🔴 MANDATORY: Complete This BEFORE Writing Any Tests

**DO NOT start testing until this document is completed and approved.**

This framework prevents the mistakes we made with Tricentis (40 UI tests, 0 functional tests).

---

## Part 1: Application Analysis

### Step 1.1: Core Features Inventory

List ALL features the application has:

```
APPLICATION: [Name]
URL: [URL]
ANALYSIS DATE: [Date]

CORE FEATURES:
☐ Feature 1: [Description]
  - SubFeature 1a
  - SubFeature 1b
☐ Feature 2: [Description]
☐ Feature 3: [Description]
...

INTEGRATIONS:
☐ Payment Gateway (Stripe, PayPal, etc.)
☐ Email Service (SendGrid, etc.)
☐ SMS Service (Twilio, etc.)
☐ Analytics (Google Analytics, etc.)
☐ Third-party APIs
☐ Database
☐ File Storage
...

USER ROLES:
☐ Guest
☐ Customer
☐ Admin
☐ Support
...
```

### Step 1.2: Critical Business Flows

Document the most important user journeys:

```
PRIMARY FLOW #1: [Name]
├─ Step 1: [Action]
├─ Step 2: [Action]
├─ Step 3: [Action] ← Data stored in DB
├─ Step 4: [Action] ← Email sent
├─ Step 5: [Action] ← Payment processed
└─ Success Criteria: [What proves it worked]

PRIMARY FLOW #2: [Name]
...

CRITICAL PATH: [The flow that must work at all costs]
```

### Step 1.3: Data Dependencies

What data is created/modified/deleted:

```
DATA ENTITIES:
☐ Users (created, updated, deleted)
☐ Orders (created, updated, cancelled)
☐ Payments (processed, refunded)
☐ Emails (sent, tracked)
☐ Products (inventory updated)
☐ Sessions (created, destroyed)
...

PERSISTENCE:
☐ Database records must survive page reload
☐ Cart must persist across sessions
☐ User state must be maintained
☐ Order history must be accurate
...
```

---

## Part 2: Testing Scope Definition

### Step 2.1: What We WILL Test

**Explicitly list every type of test we'll create:**

```
SCOPE: IN (These will be tested)

UI & NAVIGATION:
☑ Page loads without errors
☑ Navigation menus work
☑ Buttons/links are clickable
☑ Forms display correctly

FUNCTIONAL:
☑ Add item to cart (verify count increases)
☑ Submit checkout form (verify order created)
☑ Process payment (verify transaction succeeds)
☑ Create user account (verify in database)
☑ Login with valid credentials (verify session)
☑ Password reset flow (verify email sent)

BUSINESS LOGIC:
☑ Tax calculation (verify correct by state)
☑ Shipping cost (verify by method)
☑ Coupon application (verify discount applied)
☑ Inventory depletion (verify can't oversell)
☑ Order totals (verify item+tax+shipping=correct)

DATA PERSISTENCE:
☑ Cart survives page reload
☑ User data saves in database
☑ Order history is accurate
☑ Login session persists

SECURITY:
☑ Password fields masked
☑ No hardcoded API keys
☑ HTTPS enforced
☑ XSS prevention (basic)
☑ SQL injection prevention (basic)

ERROR HANDLING:
☑ Invalid product ID shows 404
☑ Network error shows message
☑ Form validation errors display
☑ Payment failure handled

INTEGRATION:
☑ Email notifications sent
☑ Payment gateway processes card
☑ User creation in auth system
```

### Step 2.2: What We WON'T Test (and Why)

**Be explicit about what's OUT OF SCOPE:**

```
SCOPE: OUT (These will NOT be tested)

PERFORMANCE & LOAD:
❌ Load testing (1000+ concurrent users)
   WHY: Requires load testing infrastructure (k6, JMeter)
   WHEN: Later phase or dedicated performance team

ADVANCED SECURITY:
❌ Penetration testing (OWASP Top 10)
   WHY: Requires security expert, not QA automation
   WHEN: After launch with professional pen tester

ACCESSIBILITY:
❌ WCAG 2.1 AA compliance
   WHY: Requires accessibility audit tools (axe, WAVE)
   WHEN: Separate accessibility testing phase

LOCALIZATION:
❌ Multi-language testing
   WHY: Out of scope for English-only release
   WHEN: After localization feature implemented

MOBILE:
❌ Native mobile app testing
   WHY: Only testing web app, not iOS/Android
   WHEN: Mobile apps developed separately

THIRD-PARTY:
❌ Payment gateway internals
   WHY: Stripe/PayPal responsibility, not ours
   WHEN: Integration testing only (test our side)

BACKEND ONLY:
❌ Database optimization
   WHY: DBA/backend engineer responsibility
   WHEN: Performance review later

OLD BROWSERS:
❌ Internet Explorer support
   WHY: Not supported by business
   WHEN: N/A (won't support IE)
```

### Step 2.3: Test Type Matrix

**Define exactly what kinds of tests and how many:**

```
TEST MATRIX:

UI TESTS: 20 tests
├─ Homepage rendering (2)
├─ Navigation (3)
├─ Form rendering (4)
├─ Button/Link clicks (5)
├─ Modal/Dialog display (3)
├─ Responsive design (3)
└─ Error states (2)

FUNCTIONAL TESTS: 30 tests
├─ User registration (5)
├─ User login (4)
├─ Shopping cart (6)
├─ Checkout (6)
├─ Product management (5)
├─ Order management (4)
└─ Account management (4)

INTEGRATION TESTS: 15 tests
├─ Email notifications (4)
├─ Payment processing (4)
├─ Database persistence (4)
├─ Auth system (3)
└─ API endpoints (3)

SECURITY TESTS: 8 tests
├─ Password masking (1)
├─ XSS prevention (2)
├─ SQL injection prevention (2)
├─ CSRF protection (2)
├─ Credential handling (1)
└─ Session security (1)

ERROR HANDLING TESTS: 10 tests
├─ Network errors (3)
├─ Invalid input (3)
├─ Not found errors (2)
├─ Permission errors (2)
└─ Server errors (2)

EDGE CASES: 12 tests
├─ Boundary values (4)
├─ Concurrent operations (3)
├─ Race conditions (2)
├─ Data validation (3)
└─ State transitions (2)

TOTAL: 95 tests (not 40!)
```

### Step 2.4: Acceptance Criteria

**Define what "done" means:**

```
ACCEPTANCE CRITERIA FOR TESTING:

Coverage Threshold: ≥ 80%
├─ UI Coverage: ≥ 90% (critical screens)
├─ Functional Coverage: ≥ 85% (main flows)
├─ Integration Coverage: ≥ 75% (APIs, DB)
└─ Error Coverage: ≥ 70% (error paths)

Quality Gates:
☐ All CRITICAL tests pass
☐ All HIGH priority tests pass
☐ ≤ 5% of MEDIUM tests fail (must document)
☐ ≤ 10% of LOW tests fail (must document)

Documentation:
☐ Scope document signed off
☐ All tests documented
☐ Test matrix complete
☐ Known limitations documented

Artifacts:
☐ Test report generated
☐ Coverage metrics shown
☐ Gaps identified and planned
☐ Regression testing plan created
```

---

## Part 3: Risk Assessment

### Step 3.1: High-Risk Areas (Test More)

```
RISK LEVEL: CRITICAL
├─ Payment processing (money involved)
├─ User authentication (security)
├─ Data deletion (data loss)
├─ Order creation (customer impact)
└─ Admin functions (system stability)

ACTION: Write 3-5 tests for each critical area

RISK LEVEL: HIGH
├─ Product catalog
├─ Inventory management
├─ Email notifications
├─ Report generation
└─ API integrations

ACTION: Write 2-3 tests for each high-risk area

RISK LEVEL: MEDIUM
├─ UI rendering
├─ Form validation
├─ Search functionality
└─ Filtering/sorting

ACTION: Write 1-2 tests for each medium-risk area

RISK LEVEL: LOW
├─ Help text
├─ Footer links
├─ Static content
└─ Documentation pages

ACTION: Write spot checks, not comprehensive tests
```

### Step 3.2: Known Limitations

```
SCOPE LIMITATIONS:

Limitation #1: We can't test real payment processing
├─ Mitigation: Use Stripe test cards
├─ Risk: Payment flow might have bugs
├─ Acceptance: Acceptable risk

Limitation #2: We can't test email delivery to real inbox
├─ Mitigation: Mock email service or use test email
├─ Risk: Email template bugs might not be caught
├─ Acceptance: Acceptable risk

Limitation #3: We can't test 1000+ concurrent users
├─ Mitigation: Manual load testing later
├─ Risk: Performance issues at scale
├─ Acceptance: Acceptable for MVP

Limitation #4: We can't pen test the application
├─ Mitigation: Security review by expert
├─ Risk: Security vulnerabilities missed
├─ Acceptance: Will do pen test pre-launch
```

---

## Part 4: Test Execution Plan

### Step 4.1: Test Phases

```
PHASE 1: FOUNDATION (Week 1)
└─ 20 tests: UI, navigation, basic rendering
   Target: ✅ All tests pass
   Time: 5 days

PHASE 2: CORE FUNCTIONALITY (Week 2)
└─ 30 tests: Registration, login, cart, checkout
   Target: ✅ 95%+ pass rate
   Time: 5 days

PHASE 3: INTEGRATION (Week 3)
└─ 15 tests: Email, payments, database, APIs
   Target: ✅ All critical tests pass
   Time: 5 days

PHASE 4: EDGE CASES & ERRORS (Week 4)
└─ 30 tests: Security, errors, edge cases
   Target: ✅ 90%+ pass rate
   Time: 5 days

PHASE 5: REGRESSION (Ongoing)
└─ Re-run all 95 tests
   Target: ✅ Maintain 80%+ pass rate
   Time: Continuous
```

### Step 4.2: Dependencies & Blockers

```
DEPENDENCIES:

Before testing cart:
└─ Need product catalog working

Before testing checkout:
├─ Need cart functional
├─ Need payment gateway configured
└─ Need shipping calculation working

Before testing payment:
├─ Need Stripe account (test mode)
└─ Need test card numbers

Before testing email:
├─ Need email service configured
└─ Need test email account

BLOCKERS:

Blocker #1: Database not accessible
└─ Mitigation: Setup test database
└─ Owner: Backend team
└─ Timeline: Day 1

Blocker #2: Payment gateway not configured
└─ Mitigation: Use Stripe test mode
└─ Owner: Backend team
└─ Timeline: Day 2

Blocker #3: Test data not available
└─ Mitigation: Create test data setup script
└─ Owner: QA team
└─ Timeline: Day 1
```

---

## Part 5: Sign-Off

### Step 5.1: Stakeholder Review

```
SCOPE REVIEWED BY:

☐ Product Owner
  └─ Date: __/__/____
  └─ Approved: YES / NO
  └─ Comments: _________________

☐ Engineering Lead
  └─ Date: __/__/____
  └─ Approved: YES / NO
  └─ Comments: _________________

☐ QA Lead
  └─ Date: __/__/____
  └─ Approved: YES / NO
  └─ Comments: _________________

☐ Business Stakeholder
  └─ Date: __/__/____
  └─ Approved: YES / NO
  └─ Comments: _________________

SCOPE APPROVED: ☐ YES ☐ NO

If NO, list required changes:
1. _______________________
2. _______________________
3. _______________________

Once approved, testing can begin.
```

### Step 5.2: Scope Change Process

```
CHANGE REQUEST PROCESS:

If scope changes mid-testing:

1. Document the change request
   ├─ What: [Description of change]
   ├─ Why: [Reason for change]
   ├─ Impact: [How it affects testing]
   └─ Effort: [How many new tests]

2. Get approval from stakeholders
   ├─ Product Owner ✓
   ├─ Engineering ✓
   └─ QA Lead ✓

3. Update this document
   └─ Add change request section

4. Re-baseline tests
   └─ Adjust test count if needed

5. Continue testing
   └─ All changes documented

NO SCOPE CREEP WITHOUT APPROVAL.
```

---

## Template: Before Testing ANY Application

### Use This Checklist:

```
APPLICATION: ___________________
DATE: ___________________

STEP 1: ANALYSIS ✓
☐ List all features
☐ Document all user flows
☐ Identify all integrations
☐ Map all data entities
☐ Identify user roles

STEP 2: SCOPE DEFINITION ✓
☐ List what we WILL test
☐ List what we WON'T test
☐ Create test matrix
☐ Define acceptance criteria
☐ Identify gaps

STEP 3: RISK ASSESSMENT ✓
☐ Identify critical areas
☐ Identify high-risk features
☐ Document limitations
☐ Plan mitigations
☐ Get stakeholder buy-in

STEP 4: EXECUTION PLAN ✓
☐ Break into phases
☐ Identify dependencies
☐ List blockers
☐ Assign owners
☐ Set timelines

STEP 5: SIGN-OFF ✓
☐ Product Owner approved
☐ Engineering Lead approved
☐ QA Lead approved
☐ Scope document finalized
☐ Ready to test

ONLY AFTER ALL 5 STEPS: Begin writing tests
```

---

## Real Example: Tricentis (What We Should Have Done)

### BEFORE Writing Tests:

```
APPLICATION: Tricentis Demo Web Shop

ANALYSIS:
✓ 10 core features identified (products, cart, checkout, accounts, etc.)
✓ 15 user flows documented
✓ 5 integrations found (payment, email, auth, inventory, shipping)
✓ 8 data entities identified
✓ 3 user roles defined (guest, customer, admin)

SCOPE: IN
✓ 95 tests planned (not 40!)
  ├─ 20 UI tests
  ├─ 30 functional tests
  ├─ 15 integration tests
  ├─ 8 security tests
  ├─ 10 error tests
  └─ 12 edge case tests

SCOPE: OUT
✓ Load testing (no infrastructure)
✓ Pen testing (no security expert)
✓ Mobile testing (only web)
✓ Accessibility (separate phase)

RISKS:
✓ CRITICAL: Payment processing (needs real testing)
✓ CRITICAL: Order creation (must verify in DB)
✓ HIGH: Tax/shipping calculations (financial impact)

LIMITATIONS:
✓ Can't test 1000+ users (will do later)
✓ Can't test real payment processing (use test cards)
✓ Can't test email delivery (will mock)

SIGN-OFF:
✓ Product Owner: APPROVED
✓ Engineering: APPROVED
✓ QA Lead: APPROVED

NOW BEGIN TESTING WITH CLEAR SCOPE
```

### THEN Write Tests:

Instead of:
- 40 random UI tests
- No functional testing
- No integration testing
- No security testing

We'd have:
- 95 comprehensive tests
- Functional coverage
- Integration coverage
- Security coverage
- Clear test matrix

---

## Summary

**BEFORE YOU WRITE ANY TEST:**

1. ✅ Analyze the application (all features, all flows)
2. ✅ Define what you WILL test (explicit list)
3. ✅ Define what you WON'T test (explicit list + reasons)
4. ✅ Assess risks (what matters most?)
5. ✅ Get approval (all stakeholders signed off)

**ONLY THEN:** Write tests

This prevents:
- ❌ Testing wrong things
- ❌ Missing critical features
- ❌ Surprises mid-testing
- ❌ Scope creep
- ❌ Wasted effort

---

**This framework is MANDATORY for all future applications.**
