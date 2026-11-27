# Feature Specification: SLA Tracking

## Problem
Support teams need to see whether tickets are within their agreed response window, identify overdue work, and understand workload at a glance.

## Scope
Extend a support-ticket workflow with priority-based due dates, an automatically derived overdue flag, and dashboard counts.

## SLA policy
- High: 24 calendar hours.
- Medium: 48 calendar hours.
- Low: 72 calendar hours.
- Clock starts at ticket creation (`created_at`).
- Calendar hours are continuous: weekends and holidays count.
- Timestamps are stored and returned in UTC.
- A ticket is overdue when `now > due_at` and status is neither `Resolved` nor `Closed`. At the exact due instant it is not yet overdue.
- Changing priority recalculates `due_at` from the original `created_at`; status changes do not reset the SLA clock.

## User stories and acceptance criteria

### US1 — View SLA-aware ticket list (P1)
As a support agent, I can see each ticket's priority, status, created time, due time, remaining time, and overdue state.
- List returns tickets newest first.
- Overdue state is computed on each read.
- Resolved and closed tickets are never marked overdue.
- Search matches title, requester, and ticket ID; priority and status filters can be combined.

### US2 — Create a ticket with an SLA (P1)
As a support agent, I can create a ticket and have its deadline assigned automatically.
- Required: title (3–120 chars), description (5–2000 chars), requester (2–100 chars), priority.
- Priority must be High, Medium, or Low.
- `created_at` is assigned by the server; clients cannot supply `due_at` or `overdue`.
- `due_at = created_at + priority target`.

### US3 — Track ticket status (P1)
As a support agent, I can move a ticket through Open, In Progress, Resolved, and Closed.
- Only supported statuses are accepted.
- Resolved/Closed tickets are excluded from overdue counts.
- Status changes do not alter created_at or due_at.

### US4 — Monitor SLA dashboard (P1)
As a team lead, I can see total, open, in-progress, resolved, overdue, and SLA compliance metrics.
- Counts reflect the same ticket dataset as the list.
- SLA compliance = (non-overdue active tickets + completed tickets) / all tickets × 100; empty dataset returns 100%.
- Dashboard values are calculated server-side.

### US5 — Reset demo data (P2)
As a learner, I can restore deterministic sample tickets for demonstrations.
- Reset removes existing tickets and inserts the documented sample set.

## API contract
- `GET /api/health`
- `GET /api/tickets?search=&priority=&status=`
- `POST /api/tickets`
- `PATCH /api/tickets/{ticket_id}/status`
- `GET /api/dashboard`
- `POST /api/demo/reset`

## Non-functional requirements
- API validation returns useful 4xx responses.
- SQLite persistence survives backend restarts.
- Frontend shows loading, empty, and error states.
- Layout works on desktop and mobile widths.
- No secrets or production personal data are included.

## Out of scope
Authentication, email notifications, business-hour calendars, holiday calendars, ticket assignment, multi-tenant access, and integrations.
