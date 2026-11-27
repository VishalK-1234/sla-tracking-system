# SLA Tracking System - Submission Evidence

## Project
SLA-based support ticket tracking application built with React, FastAPI and SQLite.

## Implemented Features
- Create and manage support tickets.
- Priority-based SLA deadlines:
  - High: 24 hours
  - Medium: 48 hours
  - Low: 72 hours
- Overdue ticket detection.
- Dashboard metrics.
- Ticket search and filtering.
- Ticket status management.
- Resolved and Closed tickets excluded from active overdue tracking.

## Automated Verification

| Verification | Result |
|---|---|
| Backend Pytest | 18 passed |
| Frontend Vitest | 2 passed |
| Frontend production build | Passed |
| Playwright Chromium E2E | Passed |

## AI Usage
AI assistance was used for specification, planning, implementation, debugging and test development. Generated code was reviewed and verified through automated tests and manual inspection.

## Demonstration
See `demo-script.md` for the three-minute project demonstration.

## Review
See `peer-review-checklist.md` for the reviewer checklist.
