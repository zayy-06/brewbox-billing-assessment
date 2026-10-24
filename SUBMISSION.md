# Submission

## Repository

- Remote URL: https://github.com/zayy-06/brewbox-billing-assessment
- Default branch: `main`

## Pull requests

| Ticket | Branch | PR link | Key commits |
|---|---|---|---|
| BUG-101 | `bugfix/BUG-101-discount-scope` | https://github.com/zayy-06/brewbox-billing-assessment/pull/1 | `bf0cd5e`, `464ca71` |
| BUG-102 | `bugfix/BUG-102-calendar-proration` | https://github.com/zayy-06/brewbox-billing-assessment/pull/2 | `b6a4439` |
| BUG-103 | `bugfix/BUG-103-late-fee-grace` | Pending |
| FEAT-201 | `feature/FEAT-201-pause-resume` | Pending |
| FEAT-202 | `feature/FEAT-202-referral-credits` | Pending |

## Test evidence

- Command: `python -m pytest tests/test_reported_bugs.py -k bug_101 -v`
- Result: `2 passed, 2 deselected` on the BUG-101 branch.
- Command: `python -m pytest tests/test_reported_bugs.py -k bug_102 -v`
- Result: `1 passed, 3 deselected` on the BUG-102 branch.
- Full reported-bugs test file on the BUG-102 branch: `1 passed, 3 failed`. BUG-101 changes are on a separate branch, and BUG-103 remains pending.
- Tests added: No new tests added yet.

## Design notes

### BUG-101 — discount scope

- Applied discounts to the plan amount only, not add-ons.
- Rejected discounts above 30%.
- Calculated tax after applying the discount.

### BUG-102 — proration

- Replaced the fixed 30-day convention with actual calendar-day proration.
- Used the number of days in the billing month.
- Applied the proration factor to both plan and add-on charges.

### BUG-103 — late fee

- Pending implementation and verification.
- Expected behavior: no late fee on the due date plus five days; the fee starts on day six.

### FEAT-201 — pause/resume

- Pending implementation and verification.

### FEAT-202 — referral credits

- Pending implementation and verification.

## AI assistance

- Tools used: ChatGPT.
- What I used them for: Reviewing code, understanding the reported bugs, debugging test failures, and preparing implementation and documentation changes.
- What I verified and can explain without assistance: The BUG-101 and BUG-102 targeted tests passed on their respective branches; the full reported-bugs test file has not passed yet.
- I confirm I did not paste the entire repository or assignment into an AI tool: Yes, provided this accurately reflects my use of AI.
