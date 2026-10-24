# Submission

## Repository

- Remote URL: https://github.com/zayy-06/brewbox-billing-assessment
- Default branch: `main`

## Pull requests

| Ticket | Branch | PR link | Key commits |
|---|---|---|---|
| BUG-101 | `bugfix/BUG-101-discount-scope` | https://github.com/zayy-06/brewbox-billing-assessment/pull/1 | `bf0cd5e`, `464ca71` |
| BUG-102 | `bugfix/BUG-102-calendar-proration` | https://github.com/zayy-06/brewbox-billing-assessment/pull/2 | `b6a4439` |
| BUG-103 | `bugfix/BUG-103-late-fee-grace` | https://github.com/zayy-06/brewbox-billing-assessment/pull/3 | `4760903` |
| FEAT-201 | `feature/FEAT-201-pause-resume` | https://github.com/zayy-06/brewbox-billing-assessment/pull/4 | `c4852ec` |
| FEAT-202 | `feature/FEAT-202-referral-credits` | Pending | Pending |

## Test evidence

- BUG-101 command: `python -m pytest tests/test_reported_bugs.py -k bug_101 -v`
  - Result: `2 passed, 2 deselected`
- BUG-102 command: `python -m pytest tests/test_reported_bugs.py -k bug_102 -v`
  - Result: `1 passed, 3 deselected`
- BUG-103 command: `python -m pytest tests/test_reported_bugs.py -k bug_103 -v`
  - Result: `1 passed, 3 deselected`
- FEAT-201 tests: `23 passed` on the FEAT-201 branch.
- Full test suite: `56 passed`.
- Tests added: No new tests added so far.

## Design notes

### BUG-101 — discount scope

- Restricted discounts to the plan amount rather than add-ons.
- Rejected discounts above 30%.
- Calculated tax after applying the discount.

### BUG-102 — proration

- Used actual calendar days in the billing month instead of a fixed 30-day month.
- Applied the proration factor to both plan and add-on charges.

### BUG-103 — late fee

- Enforced five full grace days after the invoice due date.
- Prevented late fees during the grace period.
- Allowed the late fee to apply starting on day six.

### FEAT-201 — pause/resume

- Implemented subscription pause and resume functionality.
- Handled subscription state changes for pausing and resuming.
- Added safeguards to prevent unsupported state transitions.
- Verified the feature with targeted tests; `23 passed`.

### FEAT-202 — referral credits

- Pending implementation and testing.

## AI assistance

- Tools used: ChatGPT.
- What I used them for: Understanding requirements, reviewing code, debugging test failures, and preparing implementation and documentation.
- What I verified and can explain without assistance: The targeted tests for BUG-101, BUG-102, BUG-103, and FEAT-201 passed on their respective branches. The full test suite passed with `56 passed`.
- I confirm I did not paste the entire repository or assignment into an AI tool: Yes, if accurate.
