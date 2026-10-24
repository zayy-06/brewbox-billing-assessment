# Submission

## Repository

- **Remote URL:** https://github.com/zayy-06/brewbox-billing-assessment
- **Default branch:** `main`

## Pull requests

| Ticket | Branch | PR link | Key commits |
|---|---|---|---|
| BUG-101 | `bugfix/BUG-101-discount-scope` | https://github.com/zayy-06/brewbox-billing-assessment/pull/1 | `bf0cd5e`, `464ca71` |
| BUG-102 | `bugfix/BUG-102-calendar-proration` | https://github.com/zayy-06/brewbox-billing-assessment/pull/2 | `b6a4439`, `a10ea03` |
| BUG-103 | `bugfix/BUG-103-late-fee-grace` | https://github.com/zayy-06/brewbox-billing-assessment/pull/3 | `4760903` |
| FEAT-201 | `feature/FEAT-201-pause-resume` | https://github.com/zayy-06/brewbox-billing-assessment/pull/4 | `c4852ec`, `b4a5e6f` |
| FEAT-202 | `feature/FEAT-202-referral-credits` | https://github.com/zayy-06/brewbox-billing-assessment/pull/5 | `1e5ef28`, `ba3fb40` |

*Note: The PRs remain open and unmerged on their respective branches. Combined integration is verified on `test/all-tickets-integration`.*

## Test evidence

### Individual ticket test results (run on their respective branches)

- **BUG-101:** `python -m pytest tests/test_reported_bugs.py -k bug_101 -v`
  - Result: `2 passed, 2 deselected`
- **BUG-102:** `python -m pytest tests/test_reported_bugs.py -k bug_102 -v`
  - Result: `1 passed, 3 deselected`
- **BUG-103:** `python -m pytest tests/test_reported_bugs.py -k bug_103 -v`
  - Result: `1 passed, 3 deselected`
- **FEAT-201:** `python -m pytest tests/test_feat_201_pause_resume.py -v`
  - Result: `23 passed`
- **FEAT-202:** `python -m pytest tests/test_feat_202_referral_credits.py -v`
  - Result: `19 passed`

### Combined integration test results (verified on `test/all-tickets-integration`)

- **Full test suite command:** `python -m pytest -v`
- **Result:** `56 passed in 0.41s`
  - `tests/test_basic_billing.py`: `4 passed`
  - `tests/test_feat_201_pause_resume.py`: `23 passed`
  - `tests/test_feat_202_referral_credits.py`: `19 passed`
  - `tests/test_integrity_bubble.py`: `6 passed`
  - `tests/test_reported_bugs.py`: `4 passed`

## Design notes

### BUG-101 — Discount scope

- Applied discounts strictly to the recurring plan amount rather than add-on charges.
- Enforced the configured maximum discount using the existing `MAX_DISCOUNT_PERCENT` constant (`Decimal("30")`) rather than hardcoding.
- Rejected discounts strictly greater than 30% with a `ValueError`.
- Calculated sales tax on taxable amount after applying the discount.

### BUG-102 — Calendar-day proration

- Replaced fixed 30-day proration with actual calendar-day calculations (`calendar.monthrange(year, month)[1]`).
- Counted active billable days inclusively from `max(period_start, start_date)` through `period_end`.
- Applied proration to both plan and add-on charges.
- Preserved full-month billing (factor = `1`) for subscriptions active for the entire calendar month to eliminate rounding drift.

### BUG-103 — Late-fee grace period

- Enforced five full calendar grace days after the invoice due date (`day <= invoice.due_on + timedelta(days=5)`).
- Late fee applies only starting on day six after due date.
- Preserved idempotent application (fee added once, untaxed, non-positive due or non-issued invoices skipped).

### FEAT-201 — Subscription pause and resume

- Implemented `pause_subscription`, `resume_subscription`, and `list_pauses`.
- Validated pause durations between 7 and 90 days inclusive.
- Enforced that pauses cannot start in the past or prior to subscription activation.
- Prevented overlapping pause windows using `PausePeriod.overlaps`.
- Blocked scheduling pauses if any invoice for the subscription is overdue with a positive balance as of the request date.
- Shortened active pauses on early resume such that the resume date is active again and remaining pause duration is at least 7 days.
- Updated `_active_days` to subtract overlapping paused days. Fully-paused months (0 active days) generate no invoice.

### FEAT-202 — Referral credits

- Implemented customer referral validation in `create_customer` (rejecting self-referral and unknown referral codes).
- Implemented referral credit ledger entries tracking original amount, remaining amount, source customer/invoice, and 365-day expiry (`CREDIT_VALID_DAYS`).
- Awarded 10% credit capped at $50 (`MAX_REFERRAL_CREDIT`) upon full payment of the referee's first invoice, calculated on pre-tax subtotal minus discount (including add-ons, excluding tax, late fees, and credit-paid amounts).
- Enforced one credit per referee.
- Implemented `credit_balance` (non-expired balance as-of a given date) and `list_credits` (ordered by earliest expiry).
- Applied credits after tax during invoice generation in earliest-expiry-first order, never allowing invoice amount due to become negative, and leaving zero-due invoices in `ISSUED` status without auto-paying.

## AI assistance

- **Tools used:** ChatGPT and Antigravity AI coding assistant.
- **Purpose:** Requirements understanding, implementation guidance, debugging, integration review, and documentation.
- **Verification:** Targeted tests were run and passed on their respective branches (BUG-101: 2 passed; BUG-102: 1 passed; BUG-103: 1 passed; FEAT-201: 23 passed; FEAT-202: 19 passed), and the combined full test suite (56 passed) was verified on `test/all-tickets-integration`.
- **Understanding:** I understand some of the implementation logic but need to revise certain details before explaining everything independently.
- **Repository/assignment disclosure:** I confirm I did not paste the entire repository or assignment into an AI tool: **Yes.**
