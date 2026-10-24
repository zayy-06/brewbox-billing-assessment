# Submission

> Replace the placeholders before submitting. Be concise and honest.

## Repository

- Remote URL: `https://github.com/zayy-06/brewbox-billing-assessment`
- Default branch: `main`

## Pull requests

| Ticket | Branch | PR link | Key commits |
|---|---|---|---|
| BUG-101 | `bugfix/BUG-101-discount-scope` | [PR #1](https://github.com/zayy-06/brewbox-billing-assessment/pull/1) | `bf0cd5e` |
| BUG-102 | `bugfix/BUG-102-calendar-proration` | | |
| BUG-103 | `bugfix/BUG-103-late-fee-grace` | | |
| FEAT-201 | `feature/FEAT-201-pause-resume` | | |
| FEAT-202 | `feature/FEAT-202-referral-credits` | | |

## Test evidence

- Command: `python -m pytest tests/test_reported_bugs.py -k bug_101 -v`
- Result:`2 passed, 2 deselected in 0.51s`
- Tests added: `None; verified the existing BUG-101 tests.`

## Design notes

### BUG-101 — discount scope
Discount calculation was changed to apply to the subscription plan amount rather than the subtotal. Added validation to reject discounts greater than 30%. Tax calculation remains after the discount.

### BUG-102 — proration

### BUG-103 — late fee

### FEAT-201 — pause/resume

### FEAT-202 — referral credits

## AI assistance

- Tools used: ChatGPT
- What I used them for: I used ChatGPT for help with BUG-101 implementation, understanding the discount calculation and validation, debugging guidance, test verification, writing the PR description, and Git/GitHub workflow.
- What I verified and can explain without assistance: I ran the BUG-101 tests myself and reviewed the code changes. I am working to understand the implementation so I can explain it clearly.
- I confirm I did not paste the entire repository or assignment into an AI tool: yes
