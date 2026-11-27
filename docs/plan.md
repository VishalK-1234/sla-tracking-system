# Implementation Plan

1. **Backend foundation:** SQLAlchemy model, SQLite session, Pydantic schemas, startup initialization and demo seeding.
2. **SLA domain service:** single priority-to-hours mapping; UTC due-date calculation; derived overdue calculation; dashboard aggregation.
3. **API layer:** health, ticket list/filter/search, ticket creation, status update, dashboard, demo reset.
4. **Frontend foundation:** Vite + React, API client, reusable status/priority badges, responsive layout.
5. **Dashboard:** KPI cards, SLA compliance visualization, filters/search, ticket table, ticket detail drawer, create-ticket modal.
6. **Verification:** pytest service/API tests, Vitest component tests, Playwright create-and-status-update flow, production build.
7. **Submission:** document decisions, test commands/results, AI usage, and demo walkthrough.

## Key technical decisions
- UTC-aware ISO-8601 timestamps across API boundaries.
- `due_at` stored for auditability; `is_overdue` derived at response time.
- Calendar-hour SLA policy, explicitly including weekends.
- SQLite for a portable training environment; SQLAlchemy keeps persistence isolated.
- No authentication in this training scope.
