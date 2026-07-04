# 📋 TRICENTIS DEMO WEB SHOP - TESTING SCOPE DOCUMENT

**Status:** ⚠️ Created AFTER testing (should be BEFORE)  
**Date:** July 5, 2026  
**Application:** https://demowebshop.tricentis.com

---

## Part 1: Application Analysis

### 1.1 Core Features Inventory

```
✅ PRODUCTS & CATALOG
├─ Browse products by category
├─ View product details
├─ Search products
├─ Filter by price/attributes
├─ View product images
├─ Read product descriptions
├─ View stock status
└─ See product ratings/reviews

✅ SHOPPING CART
├─ Add items to cart
├─ Remove items from cart
├─ Update quantities
├─ View cart total
├─ Apply coupon codes
├─ See shipping cost
├─ See tax calculation
└─ Persist cart across sessions

✅ CHECKOUT & ORDERS
├─ Billing address entry
├─ Shipping address selection
├─ Shipping method selection
├─ Payment method selection
├─ Order review
├─ Order confirmation
├─ Order history
├─ Invoice download
├─ Order tracking
└─ Return/exchange requests

✅ USER ACCOUNTS
├─ User registration
├─ Email verification
├─ User login
├─ Password reset
├─ Profile management
├─ Address book
├─ Download orders
├─ Order history
├─ Wishlist/favorites
├─ Reward points
└─ Newsletter subscription

✅ PAYMENTS & BILLING
├─ Credit card processing
├─ Payment gateway integration
├─ Payment confirmation
├─ Refund processing
├─ Invoice generation
├─ Tax calculation
└─ Multiple payment methods

✅ NOTIFICATIONS
├─ Order confirmation email
├─ Account verification email
├─ Password reset email
├─ Order status updates
└─ Newsletter emails

✅ INTEGRATIONS
├─ Payment gateway (Stripe/PayPal)
├─ Email service
├─ Auth system
├─ Inventory management
├─ Shipping calculator
└─ Tax calculator
```

### 1.2 Critical Business Flows

```
FLOW #1: Guest to Customer Conversion
├─ Step 1: Browse products (no login required)
├─ Step 2: Add item to cart
├─ Step 3: Go to checkout
├─ Step 4: Register account (email entered)
├─ Step 5: Email verification sent ← CRITICAL
├─ Step 6: User clicks verification link
├─ Step 7: Account activated
├─ Step 8: User logs back in
├─ Step 9: Cart data persisted ← CRITICAL
└─ Success: Account created + Order completed

FLOW #2: Complete Purchase
├─ Step 1: Add item ($99) to cart
├─ Step 2: Go to cart
├─ Step 3: Verify subtotal = $99 ← CRITICAL
├─ Step 4: Select Standard Shipping (+$5)
├─ Step 5: Verify shipping = $5 ← CRITICAL
├─ Step 6: Set billing address (NY)
├─ Step 7: Verify tax calculated (8.875%) = $9.19 ← CRITICAL
├─ Step 8: Verify total = $113.19 ← CRITICAL
├─ Step 9: Go to checkout
├─ Step 10: Fill payment details
├─ Step 11: Process payment ← CRITICAL (money involved)
├─ Step 12: Order confirmation ← CRITICAL
├─ Step 13: Email sent ← CRITICAL
└─ Success: Order in database, money processed, confirmation sent

FLOW #3: Return to Order
├─ Step 1: User logs in
├─ Step 2: Goes to order history
├─ Step 3: Views past order
├─ Step 4: Clicks to request return
├─ Step 5: Selects reason for return
├─ Step 6: Return initiated
├─ Step 7: Email sent about return
└─ Success: Return request created, email confirmed

MOST CRITICAL: FLOW #2 (Complete Purchase)
└─ If this fails, no revenue generated
```

### 1.3 Data Dependencies

```
DATA ENTITIES:

Users Table:
├─ user_id (PK)
├─ email (UNIQUE, indexed)
├─ password_hash (bcrypt)
├─ first_name
├─ last_name
├─ phone
├─ dob
├─ created_at
├─ verified_at
└─ MUST PERSIST in database

Orders Table:
├─ order_id (PK)
├─ user_id (FK)
├─ order_date
├─ subtotal
├─ tax
├─ shipping
├─ total ← CRITICAL (must be accurate)
├─ status
├─ payment_status
├─ confirmation_sent
└─ MUST PERSIST in database after checkout

Order Items Table:
├─ order_item_id
├─ order_id (FK)
├─ product_id (FK)
├─ quantity
├─ unit_price
├─ line_total
└─ MUST PERSIST after order confirmation

Payments Table:
├─ payment_id
├─ order_id (FK)
├─ amount
├─ status (succeeded/failed)
├─ gateway_response
├─ processed_at
└─ MUST MATCH order total

Cart Table:
├─ cart_id
├─ user_id (FK)
├─ product_id (FK)
├─ quantity
├─ added_at
├─ updated_at
└─ MUST PERSIST across sessions

PERSISTENCE REQUIREMENTS:
├─ User data must survive browser close
├─ Cart must survive browser close
├─ Orders must survive server restart
├─ Payments must be idempotent (can't double-charge)
└─ Email logs must be auditable
```

---

## Part 2: Testing Scope Definition

### 2.1 What We WILL Test ✅

```
SCOPE: IN (These will be thoroughly tested)

PHASE 1: FOUNDATION (UI & Navigation)
☑ Homepage loads and renders correctly
☑ Main navigation menu works
☑ Search bar is functional
☑ Product listing page displays items
☑ Product detail page loads with correct info
☑ Footer content displays
☑ All links navigate correctly
Estimated tests: 20

PHASE 2: CORE FUNCTIONALITY (Real User Actions)
☑ User registration with valid data
  └─ Verify user created in database
  └─ Verify email verification sent
☑ User registration with invalid data
  └─ Verify rejection + error message
☑ User login with correct credentials
  └─ Verify session created
☑ User login with wrong credentials
  └─ Verify rejection
☑ Password reset flow
  └─ Verify reset email sent
  └─ Verify new password works
☑ Add product to cart
  └─ Verify cart count increases
  └─ Verify item in database
☑ Remove product from cart
  └─ Verify item removed from database
☑ Update cart quantity
  └─ Verify quantity updated in database
☑ Apply coupon code
  └─ Verify discount calculated correctly
  └─ Verify total updated
Estimated tests: 25

PHASE 3: CRITICAL BUSINESS LOGIC
☑ Tax calculation (verify correct by state)
  ├─ NY (8.875%): $100 → $108.88
  ├─ TX (8.25%): $100 → $108.25
  ├─ CA (7.25%): $100 → $107.25
  └─ FL (0%): $100 → $100
☑ Shipping calculation (verify by method)
  ├─ Standard: +$5
  ├─ Express: +$15
  └─ Overnight: +$25
☑ Order total = subtotal + tax + shipping
  ├─ $100 item + $10.00 tax + $5.00 shipping = $115.00
☑ Inventory management
  ├─ Can't add out-of-stock items
  ├─ Stock decreases after purchase
  └─ Can't oversell
☑ Coupon code application
  ├─ Valid code applies discount
  ├─ Invalid code rejected
  └─ Discount on multiple items
Estimated tests: 15

PHASE 4: INTEGRATION TESTING
☑ Payment processing
  ├─ Valid card succeeds (4111111111111111)
  ├─ Invalid card fails
  ├─ Declined card shows message
  └─ Payment data saved to database
☑ Order creation
  ├─ Order appears in order history
  ├─ Order items correctly stored
  ├─ Order status is "pending"
  └─ Order total matches cart
☑ Email notifications
  ├─ Registration confirmation sent
  ├─ Order confirmation sent
  ├─ Email contains order details
  └─ Password reset email sent
☑ Data persistence
  ├─ Cart persists after page reload
  ├─ Cart persists after browser close
  ├─ User data saves correctly
  └─ Order history shows past orders
Estimated tests: 20

PHASE 5: ERROR HANDLING & EDGE CASES
☑ Invalid product ID shows 404
☑ Network timeout shows error message
☑ Out of stock shows message (not button)
☑ Invalid address shows validation error
☑ Negative quantities rejected
☑ Empty cart message
☑ Payment gateway timeout handled
☑ Concurrent checkout (two users, last item)
☑ SQL injection attempts blocked
☑ XSS attempts blocked
Estimated tests: 15

TOTAL PLANNED: 95 tests (vs 40 we did!)
```

### 2.2 What We WON'T Test ❌

```
SCOPE: OUT (These are NOT tested, with reasons)

PERFORMANCE & LOAD TESTING:
❌ 1000 concurrent users
   WHY: Requires k6, JMeter, load testing infrastructure
   OWNED BY: DevOps/Performance team
   TIMELINE: After MVP launch

❌ API response times < 200ms
   WHY: Requires dedicated performance testing
   OWNED BY: Backend/DevOps
   TIMELINE: Performance optimization phase

ADVANCED SECURITY:
❌ Penetration testing
   WHY: Requires security expert
   OWNED BY: Security team
   TIMELINE: Pre-launch security audit

❌ SSL/TLS certificate validation
   WHY: DevOps/infrastructure responsibility
   OWNED BY: Infrastructure team
   TIMELINE: Infrastructure setup

ACCESSIBILITY:
❌ WCAG 2.1 AA compliance
   WHY: Requires accessibility tools (axe, WAVE)
   OWNED BY: Accessibility specialist
   TIMELINE: Post-MVP accessibility audit

❌ Screen reader compatibility
   WHY: Manual testing by accessibility expert
   OWNED BY: QA accessibility specialist
   TIMELINE: Later phase

LOCALIZATION:
❌ Multi-language support
   WHY: Only English version at launch
   OWNED BY: Localization team
   TIMELINE: After launch

❌ Currency conversion
   WHY: USD only for MVP
   OWNED BY: Localization team
   TIMELINE: Multi-currency phase

MOBILE TESTING:
❌ Native iOS/Android apps
   WHY: Testing web only, apps separate
   OWNED BY: Mobile team
   TIMELINE: Mobile development phase

❌ Responsive design comprehensive test
   WHY: Quick spot-check only, dedicated mobile phase later
   OWNED BY: Mobile/QA team
   TIMELINE: Mobile optimization phase

BACKEND-ONLY:
❌ Database query optimization
   WHY: DBA/Backend responsibility
   OWNED BY: Backend team
   TIMELINE: Performance optimization

❌ API rate limiting
   WHY: Backend implementation responsibility
   OWNED BY: Backend team
   TIMELINE: Security hardening phase

❌ Backup/disaster recovery
   WHY: Infrastructure/DevOps responsibility
   OWNED BY: DevOps team
   TIMELINE: Infrastructure setup

OLD BROWSERS:
❌ Internet Explorer support
   WHY: Not supported by modern standards
   OWNED BY: N/A
   TIMELINE: N/A
```

### 2.3 Test Type Breakdown

```
BREAKDOWN BY TEST TYPE:

UI TESTS (20):
├─ Page rendering (5)
├─ Navigation (5)
├─ Form display (4)
├─ Button/Link clicks (4)
├─ Layout responsiveness (2)
└─ Error message display (3)

FUNCTIONAL TESTS (30):
├─ User registration (4)
├─ User authentication (4)
├─ Shopping cart operations (6)
├─ Checkout flow (6)
├─ Product management (5)
├─ Order creation (3)
└─ Account management (2)

INTEGRATION TESTS (20):
├─ Payment gateway (5)
├─ Email service (4)
├─ Database persistence (5)
├─ Auth system (3)
├─ API endpoints (3)
└─ Order processing (2)

BUSINESS LOGIC TESTS (15):
├─ Tax calculation (4)
├─ Shipping calculation (3)
├─ Inventory management (3)
├─ Coupon application (3)
├─ Order total validation (2)
└─ Price calculations (2)

SECURITY TESTS (5):
├─ Password masking (1)
├─ XSS prevention (2)
├─ SQL injection prevention (2)
└─ CSRF protection (1)

ERROR HANDLING TESTS (10):
├─ 404 errors (2)
├─ Network errors (3)
├─ Validation errors (2)
├─ Payment failures (2)
├─ Timeout handling (1)
└─ State error (1)

EDGE CASES (5):
├─ Empty cart (1)
├─ Out of stock (1)
├─ Invalid quantities (1)
├─ Concurrent purchases (1)
└─ Data validation (1)

TOTAL: 95 tests
```

---

## Part 3: Risk Assessment

### 3.1 High-Risk Areas (Must Test Thoroughly)

```
🔴 CRITICAL RISK: Payment Processing
├─ Severity: CRITICAL (money involved)
├─ Impact: Revenue loss, customer trust loss
├─ Tests Required: 5-6 tests minimum
├─ Coverage:
│  ├─ Valid card succeeds
│  ├─ Invalid card fails gracefully
│  ├─ Declined card shows message
│  ├─ Amount matches order total
│  ├─ Transaction logged
│  └─ Idempotency (can't double charge)
└─ Acceptance: 100% pass rate REQUIRED

🔴 CRITICAL RISK: Order Creation & Persistence
├─ Severity: CRITICAL (data integrity)
├─ Impact: Lost orders, missing revenue
├─ Tests Required: 5-6 tests minimum
├─ Coverage:
│  ├─ Order created in database
│  ├─ Order items stored correctly
│  ├─ Order total accurate
│  ├─ Status transitions correct
│  ├─ Order appears in history
│  └─ Survives server restart
└─ Acceptance: 100% pass rate REQUIRED

🔴 CRITICAL RISK: User Data Integrity
├─ Severity: CRITICAL (security/privacy)
├─ Impact: Data breach, lost user trust
├─ Tests Required: 5 tests minimum
├─ Coverage:
│  ├─ Password properly hashed
│  ├─ Email verified before access
│  ├─ Personal data encrypted
│  ├─ Sessions managed securely
│  └─ Data persists correctly
└─ Acceptance: 100% pass rate REQUIRED

🟠 HIGH RISK: Checkout Flow
├─ Severity: HIGH (customer experience)
├─ Impact: Cart abandonment, lost sales
├─ Tests Required: 4-5 tests minimum
├─ Coverage:
│  ├─ All fields required
│  ├─ Address validation
│  ├─ Shipping selection works
│  ├─ Payment method selection
│  └─ Order review accurate
└─ Acceptance: 95%+ pass rate

🟠 HIGH RISK: Tax & Shipping Calculation
├─ Severity: HIGH (legal/financial)
├─ Impact: Wrong charges, legal issues
├─ Tests Required: 4-5 tests minimum
├─ Coverage:
│  ├─ Tax by state/region
│  ├─ Shipping by method
│  ├─ Calculations accurate
│  ├─ Total correct
│  └─ Discounts applied properly
└─ Acceptance: 100% accuracy required

🟠 HIGH RISK: Inventory Management
├─ Severity: HIGH (overselling)
├─ Impact: Fulfillment issues, customer complaints
├─ Tests Required: 3 tests minimum
├─ Coverage:
│  ├─ Stock decreases after purchase
│  ├─ Can't buy out-of-stock
│  ├─ Concurrent purchase handling
│  └─ Stock level accurate
└─ Acceptance: 100% pass rate

🟡 MEDIUM RISK: Email Notifications
├─ Severity: MEDIUM (customer communication)
├─ Impact: Customer confusion, support burden
├─ Tests Required: 3-4 tests
├─ Coverage:
│  ├─ Confirmation sent
│  ├─ Correct email address
│  ├─ Content accurate
│  └─ Tracking works
└─ Acceptance: 90%+ pass rate

🟡 MEDIUM RISK: Authentication
├─ Severity: MEDIUM (security)
├─ Impact: Unauthorized access
├─ Tests Required: 2-3 tests
├─ Coverage:
│  ├─ Login works
│  ├─ Logout works
│  ├─ Session management
│  └─ Password reset
└─ Acceptance: 100% pass rate

🟢 LOW RISK: UI/Navigation
├─ Severity: LOW (cosmetic)
├─ Impact: User confusion (minor)
├─ Tests Required: 1-2 tests
├─ Coverage:
│  ├─ Pages load
│  ├─ Navigation works
│  └─ Forms display
└─ Acceptance: 80%+ pass rate
```

### 3.2 Known Limitations

```
LIMITATION #1: Real Payment Processing
├─ Issue: Can't charge real credit cards in testing
├─ Mitigation: Use Stripe test cards
│  ├─ 4111 1111 1111 1111 (visa success)
│  ├─ 4000 0000 0000 0002 (visa decline)
│  └─ 5555 5555 5555 4444 (mastercard success)
├─ Risk: Payment gateway integration bugs
├─ Acceptance: Acceptable risk (use test cards)

LIMITATION #2: Email Verification
├─ Issue: Can't access external email inbox
├─ Mitigation: Use test email service (Mailhog)
├─ Risk: Email templates might have bugs
├─ Acceptance: Acceptable (manual email audit planned)

LIMITATION #3: High-Load Testing
├─ Issue: Can't test 1000+ concurrent users
├─ Mitigation: Manual load testing later (k6/JMeter)
├─ Risk: Performance issues at scale
├─ Acceptance: Acceptable (MVP launching with limited users)

LIMITATION #4: Real Tax Rates
├─ Issue: Tax rates are complex, vary by location
├─ Mitigation: Test major states (NY, TX, CA, FL)
├─ Risk: Might miss edge case tax rules
├─ Acceptance: Acceptable (can be updated)

LIMITATION #5: Security Pen Testing
├─ Issue: QA can't do professional pen testing
├─ Mitigation: Security team does pre-launch audit
├─ Risk: Advanced attacks might not be caught
├─ Acceptance: Acceptable (plan pre-launch security audit)

LIMITATION #6: Accessibility Testing
├─ Issue: Needs accessibility specialist
├─ Mitigation: Basic accessibility checks only
├─ Risk: WCAG violations might be missed
├─ Acceptance: Acceptable (plan post-launch accessibility audit)
```

---

## Part 4: Acceptance Criteria

```
TESTING COMPLETE WHEN:

Coverage Threshold Met:
☐ UI Coverage: 90% (20/22 main screens)
☐ Functional Coverage: 85% (key user flows)
☐ Integration Coverage: 80% (critical integrations)
☐ Error Coverage: 75% (major error paths)
☐ Overall Coverage: 80%+ (combined)

Quality Gates Met:
☐ All CRITICAL priority tests: 100% PASS
  └─ Payment processing (must work perfectly)
  └─ Order creation (must be accurate)
  └─ User data (must be secure)
  └─ Checkout flow (must complete)
☐ All HIGH priority tests: 95%+ PASS
  └─ Can be documented if failed
☐ MEDIUM priority tests: 90%+ PASS
  └─ Can fail with justification
☐ LOW priority tests: 80%+ PASS
  └─ Can fail with documentation

Test Quality:
☐ All tests documented
☐ All tests repeatable
☐ All tests independent
☐ No flaky tests
☐ Clear test names
☐ Clear assertions
☐ Test matrix completed
☐ Test report generated

Documentation Complete:
☐ Scope document signed off
☐ Test cases documented
☐ Known issues documented
☐ Limitations documented
☐ Coverage report generated
☐ Test summary provided
☐ Gaps identified
☐ Regression plan created
```

---

## Part 5: Sign-Off

### Stakeholder Approval

```
SCOPE DOCUMENT: Tricentis Demo Web Shop
VERSION: 1.0
DATE: July 5, 2026
STATUS: ⚠️ Created AFTER testing (should be before)

APPROVAL REQUIRED FROM:

☐ Product Owner
  └─ Name: _______________
  └─ Date: __/__/____
  └─ Approved: ☐ YES  ☐ NO
  └─ Comments: _________________

☐ Engineering Lead
  └─ Name: _______________
  └─ Date: __/__/____
  └─ Approved: ☐ YES  ☐ NO
  └─ Comments: _________________

☐ QA Lead
  └─ Name: _______________
  └─ Date: __/__/____
  └─ Approved: ☐ YES  ☐ NO
  └─ Comments: _________________

SCOPE STATUS: 
☐ APPROVED - Ready to test
☐ NEEDS CHANGES - Update scope
☐ REJECTED - Rewrite

REQUIRED CHANGES (if any):
1. _____________________________
2. _____________________________
3. _____________________________
```

---

## Lessons Learned

```
WHAT WE DID WRONG:
❌ Wrote 40 tests without scope document
❌ Tested UI presence, not functionality
❌ No payment testing at all
❌ No order creation testing
❌ No email testing
❌ No tax/shipping calculation testing
❌ No business logic testing
❌ No integration testing
❌ No error scenario testing
❌ No security testing

WHAT WE SHOULD DO NEXT TIME:
✅ Create scope document FIRST
✅ Get stakeholder approval
✅ Identify critical paths
✅ Test functionality not just presence
✅ Test business logic
✅ Test integrations
✅ Test error scenarios
✅ Test security basics
✅ Write 95 tests, not 40
✅ Cover 80%+ of features
```

---

**This document should have been written BEFORE we created any tests.**

**For all future applications: Complete this scope document first, get approvals, then test.**
