# Submission

## Repository

<<<<<<< HEAD
<<<<<<< HEAD
- Remote URL: `https://github.com/zayy-06/brewbox-billing-assessment`
=======
- Remote URL: https://github.com/zayy-06/brewbox-billing-assessment
>>>>>>> bugfix/BUG-102-calendar-proration
=======
- Remote URL: https://github.com/zayy-06/brewbox-billing-assessment
>>>>>>> origin/feature/FEAT-201-pause-resume
- Default branch: `main`

## Pull requests

| Ticket | Branch | PR link | Key commits |
|---|---|---|---|
<<<<<<< HEAD
<<<<<<< HEAD
| BUG-101 | `bugfix/BUG-101-discount-scope` | [PR #1](https://github.com/zayy-06/brewbox-billing-assessment/pull/1) | `bf0cd5e` |
| BUG-102 | `bugfix/BUG-102-calendar-proration` | | |
| BUG-103 | `bugfix/BUG-103-late-fee-grace` | | |
| FEAT-201 | `feature/FEAT-201-pause-resume` | | |
| FEAT-202 | `feature/FEAT-202-referral-credits` | | |
=======
| BUG-101 | `bugfix/BUG-101-discount-scope` | https://github.com/zayy-06/brewbox-billing-assessment/pull/1 | `bf0cd5e`, `464ca71` |
| BUG-102 | `bugfix/BUG-102-calendar-proration` | https://github.com/zayy-06/brewbox-billing-assessment/pull/2 | `b6a4439` |
| BUG-103 | `bugfix/BUG-103-late-fee-grace` | Pending |
| FEAT-201 | `feature/FEAT-201-pause-resume` | Pending |
| FEAT-202 | `feature/FEAT-202-referral-credits` | Pending |
>>>>>>> bugfix/BUG-102-calendar-proration

## Test evidence

- Command: `python -m pytest tests/test_reported_bugs.py -k bug_101 -v`
<<<<<<< HEAD
- Result:`2 passed, 2 deselected in 0.51s`
- Tests added: `None; verified the existing BUG-101 tests.`
=======
- Result: `2 passed, 2 deselected` on the BUG-101 branch.
- Command: `python -m pytest tests/test_reported_bugs.py -k bug_102 -v`
- Result: `1 passed, 3 deselected` on the BUG-102 branch.
- Full reported-bugs test file on the BUG-102 branch: `1 passed, 3 failed`. BUG-101 changes are on a separate branch, and BUG-103 remains pending.
- Tests added: No new tests added yet.
>>>>>>> bugfix/BUG-102-calendar-proration
=======
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
>>>>>>> origin/feature/FEAT-201-pause-resume

## Design notes

### BUG-101 — discount scope
Discount calculation was changed to apply to the subscription plan amount rather than the subtotal. Added validation to reject discounts greater than 30%. Tax calculation remains after the discount.

- Applied discounts to the plan amount only, not add-ons.
- Rejected discounts above 30%.
- Calculated tax after applying the discount.

- Restricted discounts to the plan amount rather than add-ons.
- Rejected discounts above 30%.
- Calculated tax after applying the discount.

### BUG-102 — proration

<<<<<<< HEAD
- Replaced the fixed 30-day convention with actual calendar-day proration.
- Used the number of days in the billing month.
=======
- Used actual calendar days in the billing month instead of a fixed 30-day month.
>>>>>>> origin/feature/FEAT-201-pause-resume
- Applied the proration factor to both plan and add-on charges.

### BUG-103 — late fee

<<<<<<< HEAD
- Pending implementation and verification.
- Expected behavior: no late fee on the due date plus five days; the fee starts on day six.

### FEAT-201 — pause/resume

- Pending implementation and verification.

### FEAT-202 — referral credits

- Pending implementation and verification.

## AI assistance

<<<<<<< HEAD
- Tools used: ChatGPT
- What I used them for: I used ChatGPT for help with BUG-101 implementation, understanding the discount calculation and validation, debugging guidance, test verification, writing the PR description, and Git/GitHub workflow.
- What I verified and can explain without assistance: I ran the BUG-101 tests myself and reviewed the code changes. I am working to understand the implementation so I can explain it clearly.
- I confirm I did not paste the entire repository or assignment into an AI tool: yes
=======
- Tools used: ChatGPT.
- What I used them for: Reviewing code, understanding the reported bugs, debugging test failures, and preparing implementation and documentation changes.
- What I verified and can explain without assistance: The BUG-101 and BUG-102 targeted tests passed on their respective branches; the full reported-bugs test file has not passed yet.
- I confirm I did not paste the entire repository or assignment into an AI tool: Yes, provided this accurately reflects my use of AI.
>>>>>>> bugfix/BUG-102-calendar-proration
=======
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
>>>>>>> origin/feature/FEAT-201-pause-resume
