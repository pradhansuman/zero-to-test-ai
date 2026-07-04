# 📋 TRICENTIS DEMO WEB SHOP - TESTING SCOPE DOCUMENT (FRESH START)

**Status:** DRAFT (Awaiting Approval)  
**Date:** July 5, 2026  
**Application:** https://demowebshop.tricentis.com  
**Approach:** SCOPE FIRST, TEST SECOND (Mandatory Framework)

---

## Part 1: Application Analysis

### 1.1 Core Features Inventory

```
✅ PRODUCT MANAGEMENT
├─ Browse products by category
├─ View product details with images
├─ Search for products
├─ Filter/sort products
├─ View stock status
└─ Read product descriptions

✅ SHOPPING CART
├─ Add items to cart
├─ Remove items from cart
├─ Update quantities
├─ View cart total
├─ Apply coupon codes (if available)
├─ View shipping estimate
└─ Persist cart across sessions

✅ USER ACCOUNTS
├─ User registration
├─ User login/logout
├─ Password reset
├─ Profile management
├─ Address management
├─ Order history
└─ Wishlist (if available)

✅ CHECKOUT & ORDERS
├─ Billing address entry
├─ Shipping address selection
├─ Shipping method selection
├─ Payment method selection
├─ Order confirmation
├─ Order tracking
└─ Invoice generation (if available)

✅ PAYMENTS
├─ Credit card processing
├─ Payment gateway integration
├─ Payment confirmation
└─ Transaction logging

✅ NOTIFICATIONS
├─ Order confirmation email
├─ Account verification email
├─ Password reset email
└─ Shipping notifications (if available)

✅ INTEGRATIONS
├─ Payment gateway (Stripe/PayPal/other)
├─ Email service
├─ User authentication system
└─ Inventory management system
```

### 1.2 Critical Business Flows

```
FLOW #1: Browse & Search
├─ User visits homepage
├─ Navigates to product category
├─ Searches for specific product
├─ Filters by price/attributes
└─ Views product details

FLOW #2: Add to Cart & Checkout (CRITICAL)
├─ User adds item to cart (quantity 1)
├─ Cart total updates
├─ User goes to checkout
├─ Selects shipping method
├─ Enters/confirms address
├─ Selects payment method
├─ Enters payment details
├─ Confirms order
├─ Receives confirmation ← CRITICAL
└─ Email sent ← CRITICAL

FLOW #3: User Registration (CRITICAL)
├─ User fills registration form
├─ Enters email
├─ Creates password
├─ Submits
├─ Email verification sent ← CRITICAL
├─ User verifies email
├─ Account activated
└─ Can login with credentials ← CRITICAL

FLOW #4: Order History
├─ User logs in
├─ Goes to account/orders
├─ Views past orders
├─ Can download invoice (if available)
└─ Can request return (if available)

MOST CRITICAL: FLOW #2 (Complete purchase with payment)
```

### 1.3 Data Entities

```
USERS TABLE:
├─ user_id (PK)
├─ email (UNIQUE)
├─ password_hash
├─ first_name, last_name
├─ addresses
└─ MUST PERSIST in database

ORDERS TABLE:
├─ order_id (PK)
├─ user_id (FK)
├─ order_date
├─ subtotal
├─ tax (if applicable)
├─ shipping
├─ total ← CRITICAL (must be accurate)
├─ status
├─ payment_status
└─ MUST PERSIST in database

ORDER ITEMS TABLE:
├─ order_item_id
├─ order_id (FK)
├─ product_id (FK)
├─ quantity
├─ unit_price
└─ line_total

CART TABLE:
├─ cart_id
├─ user_id (FK)
├─ product_id (FK)
├─ quantity
└─ MUST PERSIST across sessions

PAYMENTS TABLE:
├─ payment_id
├─ order_id (FK)
├─ amount
├─ status
├─ gateway_response
└─ MUST BE IDEMPOTENT (no double-charging)
```

---

## Part 2: Testing Scope Definition

### 2.1 What We WILL Test ✅

```
SCOPE: IN (Explicitly Tested)

PHASE 1: FOUNDATION (UI & Navigation)
☑ Homepage loads and displays correctly
☑ Navigation menu works
☑ Product listing displays items
☑ Product detail page loads
☑ Search functionality works
☑ Category filtering works
Estimated tests: 15 tests

PHASE 2: CORE FUNCTIONALITY (Real User Actions)
☑ User can register with valid data
  └─ Verify user created in database
  └─ Verify email sent
☑ User registration rejects invalid data
☑ User can login with correct credentials
☑ User cannot login with wrong credentials
☑ User can logout
☑ Password reset flow works
☑ Add product to cart (verify count increases)
☑ Remove product from cart
☑ Update cart quantity
☑ Persist cart after page reload
Estimated tests: 20 tests

PHASE 3: CHECKOUT & PAYMENT (CRITICAL)
☑ Can proceed to checkout from cart
☑ Billing address form displays
☑ Shipping method selection works
☑ Order total calculates correctly
☑ Payment form displays
☑ Can submit payment
☑ Order created in database after payment ← CRITICAL
☑ Order appears in order history ← CRITICAL
☑ Email confirmation sent ← CRITICAL
☑ Order status is correct
Estimated tests: 15 tests

PHASE 4: DATA & INTEGRATION
☑ User data persists after logout/login
☑ Order data persists in database
☑ Cart persists across sessions
☑ Order history shows all past orders
☑ Email notifications work (mock/verify)
Estimated tests: 10 tests

PHASE 5: ERROR HANDLING & SECURITY
☑ Invalid product ID shows error
☑ Network errors handled gracefully
☑ Form validation works
☑ Password fields masked
☑ No hardcoded credentials visible
☑ Out of stock handling
Estimated tests: 10 tests

TOTAL PLANNED: 70 tests (not 40!)
```

### 2.2 What We WON'T Test ❌

```
SCOPE: OUT (Not Tested, with Reasons)

❌ LOAD TESTING (1000+ concurrent users)
   WHY: Requires k6/JMeter infrastructure
   WHEN: Later phase with performance team

❌ PENETRATION TESTING
   WHY: Requires security expert
   WHEN: Pre-launch security audit

❌ ACCESSIBILITY (WCAG 2.1 AA)
   WHY: Requires accessibility tools
   WHEN: Post-MVP accessibility audit

❌ LOCALIZATION (Multi-language)
   WHY: Only English version
   WHEN: After localization feature

❌ MOBILE APP (iOS/Android native)
   WHY: Testing web only
   WHEN: Mobile development phase

❌ ADVANCED INTEGRATIONS (Stripe internals)
   WHY: Third-party responsibility
   WHEN: Integration testing only

❌ DATABASE OPTIMIZATION
   WHY: DBA responsibility
   WHEN: Performance optimization phase

❌ OLD BROWSER SUPPORT (IE)
   WHY: Not supported
   WHEN: N/A
```

### 2.3 Test Distribution Matrix

```
TEST BREAKDOWN: 70 Total Tests

UI/Navigation Tests: 15 (21%)
├─ Homepage (2)
├─ Product pages (3)
├─ Search (2)
├─ Navigation (2)
├─ Cart display (2)
├─ Checkout display (2)
└─ Account pages (2)

Functional Tests: 20 (29%)
├─ Registration (3)
├─ Login/Logout (3)
├─ Add to cart (2)
├─ Remove from cart (2)
├─ Update quantity (2)
├─ Cart persistence (2)
├─ Password reset (2)
├─ Profile management (2)

Checkout & Payment: 15 (21%)
├─ Checkout flow (3)
├─ Billing address (2)
├─ Shipping selection (2)
├─ Order total calc (2)
├─ Payment processing (2)
├─ Order creation (2)

Integration Tests: 10 (14%)
├─ Order persistence (2)
├─ User data persistence (2)
├─ Order history (2)
├─ Email notifications (2)
├─ Database integrity (2)

Error/Edge Cases: 10 (14%)
├─ Invalid inputs (3)
├─ Error handling (3)
├─ Security basics (2)
├─ Out of stock (2)

TOTAL: 70 tests
```

### 2.4 Acceptance Criteria

```
TESTING COMPLETE WHEN:

Coverage: ≥80%
☐ UI Coverage: 90% (all main screens)
☐ Functional Coverage: 85% (key flows)
☐ Integration Coverage: 80% (critical integrations)
☐ Error Coverage: 75% (error scenarios)

Quality Gates:
☐ CRITICAL tests: 100% PASS
  └─ Payment processing must work
  └─ Order creation must succeed
  └─ User registration must work
☐ HIGH tests: 95%+ PASS
☐ MEDIUM tests: 90%+ PASS
☐ LOW tests: 80%+ PASS

Documentation:
☐ All tests documented
☐ Test matrix complete
☐ Gaps identified
☐ Professional report generated
```

---

## Part 3: Risk Assessment

### 3.1 Risk-Based Test Allocation

```
🔴 CRITICAL (5+ tests each):
├─ Payment Processing
├─ Order Creation & Persistence
└─ User Registration & Authentication

🟠 HIGH (3-4 tests each):
├─ Checkout Flow
├─ Shopping Cart
├─ User Data Persistence
└─ Email Notifications

🟡 MEDIUM (2-3 tests each):
├─ Product Browsing
├─ Search/Filtering
├─ Form Validation
└─ Navigation

🟢 LOW (1-2 tests each):
├─ UI Rendering
├─ Static Content
└─ Help Text
```

### 3.2 Known Limitations

```
LIMITATION #1: Real Payment Processing
├─ Can't charge real cards
├─ MITIGATION: Use Stripe/PayPal test cards
├─ RISK: Payment bugs possible
└─ ACCEPTANCE: Acceptable (use test mode)

LIMITATION #2: Email Verification
├─ Can't access external inbox
├─ MITIGATION: Mock email service
├─ RISK: Email template bugs
└─ ACCEPTANCE: Acceptable (manual email audit later)

LIMITATION #3: No Load Testing
├─ Can't test 1000+ concurrent users
├─ MITIGATION: Manual load test later
├─ RISK: Performance issues at scale
└─ ACCEPTANCE: Acceptable (MVP launch with limited users)

LIMITATION #4: No Pen Testing
├─ Can't do security audit
├─ MITIGATION: Professional pen test pre-launch
├─ RISK: Security vulnerabilities
└─ ACCEPTANCE: Acceptable (schedule pre-launch audit)
```

---

## Part 4: Test Execution Plan

### 4.1 Timeline

```
PHASE 1: FOUNDATION (3 days)
└─ 15 UI tests
   └─ Target: All tests pass

PHASE 2: CORE FUNCTIONALITY (3 days)
└─ 20 functional tests
   └─ Target: 95%+ pass rate

PHASE 3: CHECKOUT & PAYMENT (3 days)
└─ 15 payment/order tests
   └─ Target: 100% critical tests pass

PHASE 4: INTEGRATION (2 days)
└─ 10 integration tests
   └─ Target: 80%+ pass rate

PHASE 5: ERROR & EDGE CASES (2 days)
└─ 10 error/edge tests
   └─ Target: 75%+ pass rate

TOTAL: ~13 days (can parallelize to ~7 days)
```

### 4.2 Dependencies & Blockers

```
DEPENDENCIES:

Before Phase 2:
└─ Phase 1 (UI tests) must be done

Before Phase 3:
├─ Phase 2 (functional tests) must be done
└─ Payment gateway must be configured (test mode)

Before Phase 4:
└─ Phase 3 must be done

BLOCKERS:

Blocker #1: Payment gateway not in test mode
└─ FIX: Configure Stripe/PayPal test credentials

Blocker #2: Test data not available
└─ FIX: Create test user setup script

Blocker #3: Database not accessible
└─ FIX: Setup test database
```

---

## Part 5: Sign-Off

### Stakeholder Approval

```
SCOPE DOCUMENT: Tricentis Demo Web Shop (Fresh Start)
VERSION: 1.0
DATE: July 5, 2026

APPROVALS REQUIRED:

☐ Product Owner
  └─ Name: _____________
  └─ Date: __/__/____
  └─ Approved: ☐ YES  ☐ NO

☐ Engineering Lead
  └─ Name: _____________
  └─ Date: __/__/____
  └─ Approved: ☐ YES  ☐ NO

☐ QA Lead
  └─ Name: _____________
  └─ Date: __/__/____
  └─ Approved: ☐ YES  ☐ NO

SCOPE STATUS: 
☐ APPROVED - Ready to test
☐ NEEDS CHANGES - Update scope first
☐ REJECTED - Rewrite scope

APPROVED BY: (Initial when approved)
___________________

APPROVED DATE: __/__/____
```

---

## Summary

**Application:** https://demowebshop.tricentis.com  
**Tests Planned:** 70 (breakdown: 15 UI + 20 Functional + 15 Payment + 10 Integration + 10 Error)  
**Coverage Target:** ≥80%  
**Status:** DRAFT (Awaiting Approval)

**Next Steps:**
1. Review this scope document
2. Get stakeholder approvals above ↑
3. Once approved, proceed to test creation per this scope
4. Generate professional dashboard after each test run
5. Compare results to scope at completion

---

**This document MUST be approved before testing begins.**

**Per MANDATORY_SCOPE_ENFORCEMENT.md: NO TESTING WITHOUT SCOPE APPROVAL.**
