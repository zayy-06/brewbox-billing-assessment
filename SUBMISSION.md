# Submission

## Repository

- Remote URL: https://github.com/zayy-06/brewbox-billing-assessment
- Default branch: `main`

## Pull requests

| Ticket | Branch | PR link | Key commits |
|---|---|---|---|
| BUG-101 | `bugfix/BUG-101-discount-scope` | https://github.com/zayy-06/brewbox-billing-assessment/pull/1 | `bf0cd5e`, `464ca71` |
| BUG-102 | `bugfix/BUG-102-calendar-proration` | https://github.com/zayy-06/brewbox-billing-assessment/pull/2 | `b6a4439`, `a10ea03` |
| BUG-103 | `bugfix/BUG-103-late-fee-grace` | https://github.com/zayy-06/brewbox-billing-assessment/pull/3 | `4760903` |
| FEAT-201 | `feature/FEAT-201-pause-resume` | https://github.com/zayy-06/brewbox-billing-assessment/pull/4 | `c4852ec`, `b4a5e6f` |
| FEAT-202 | `feature/FEAT-202-referral-credits` | https://github.com/zayy-06/brewbox-billing-assessment/pull/5 | `c035b99` |

## Test evidence

- BUG-101: `python -m pytest tests/test_reported_bugs.py -k bug_101 -v`
  - Result: `2 passed, 2 deselected`
- BUG-102: `python -m pytest tests/test_reported_bugs.py -k bug_102 -v`
  - Result: `1 passed, 3 deselected`
- BUG-103: `python -m pytest tests/test_reported_bugs.py -k bug_103 -v`
  - Result: `1 passed, 3 deselected`
- FEAT-201: `python -m pytest tests/test_feat_201_pause_resume.py -v`
  - Result: `23 passed`
- FEAT-202: `python -m pytest tests/test_feat_202_referral_credits.py -v`
  - Result: `19 passed`

The targeted tests above passed on their respective branches. Record a full-suite result only if you verified it on the combined implementation.

## Design notes

### BUG-101 — Discount scope

- Applied discounts to the plan amount rather than add-on charges.
- Rejected discounts above 30%.
- Calculated tax after applying the discount.

### BUG-102 — Calendar-day proration

- Replaced fixed 30-day proration with actual calendar-day calculations.
- Used the number of days in the billing month as the denominator.
- Applied proration to both plan and add-on charges.
- Preserved full-month billing for subscriptions active from the first day of the month.

### BUG-103 — Late-fee grace period

- Enforced five full grace days after the invoice due date.
- Prevented late fees during the grace period.
- Allowed late fees to apply starting on day six.

### FEAT-201 — Subscription pause and resume

- Implemented subscription pause and resume functionality.
- Validated pause duration, dates, overlapping pauses, and overdue invoices.
- Accounted for paused days when calculating proration.
- Kept existing invoices unchanged when a subscription pause was applied.

### FEAT-202 — Referral credits

- Implemented a referral credit ledger with original amounts, remaining balances, source invoices, and expiry dates.
- Calculated referral rewards at 10% of the eligible invoice base, capped at $50.
- Applied available credits to subsequent invoices in earliest-expiry-first order.
- Prevented invoice amounts due from becoming negative.
- Handled referral eligibility, invalid codes, self-referrals, and credit application.
- Excluded tax from the referral reward calculation and prevented a reward from being applied to the invoice that generated it.

## AI assistance

- Tool used: ChatGPT.
- Purpose: Understanding requirements, reviewing implementation, debugging test failures, and preparing documentation.
- Verification: Targeted tests were run for BUG-101, BUG-102, BUG-103, FEAT-201, and FEAT-202 on their respective branches.
- I confirm I did not paste the entire repository or assignment into an AI tool: Yes, if accurate.
