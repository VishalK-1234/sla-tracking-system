# SLA Desk — Full-Stack SLA Tracking System

A spec-first support-ticket SLA application built with FastAPI, SQLAlchemy, SQLite, React, and Vite.

## Features
- Priority-based SLA deadlines: High 24h, Medium 48h, Low 72h.
- Calendar-hour calculation (weekends included).
- Automatic overdue detection using UTC timestamps.
- Dashboard metrics: total, open, in progress, resolved, overdue, and SLA compliance.
- Ticket search, priority/status filters, sorting, ticket creation, and status updates.
- Responsive dashboard with seeded demo tickets.
- Backend unit/API tests, frontend component tests, and Playwright E2E test.

## Requirements
- Python 3.10+
- Node.js 18+
- npm

## Run the backend (PowerShell)
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
API docs: http://127.0.0.1:8000/docs

## Run the frontend (second terminal)
```powershell
cd frontend
npm install
npm run dev
```
Open http://localhost:5173.

## Run tests
Backend:
```powershell
cd backend
pytest -v
```
Frontend:
```powershell
cd frontend
npm install
npm test
npm run build
```
Playwright E2E (after installing frontend dependencies):
```powershell
cd frontend
npx playwright install chromium
npm run test:e2e
```

## SLA policy
| Priority | Target |
|---|---:|
| High | 24 calendar hours |
| Medium | 48 calendar hours |
| Low | 72 calendar hours |

Deadlines are calculated from ticket creation time in UTC. Weekends and holidays are included. A ticket is overdue only when its due time has passed and its status is not `Resolved` or `Closed`. The overdue flag is derived at read time, not stored as a stale database value.

## Demo data
The backend seeds sample tickets on first startup. Use the `Reset demo data` action in the UI to restore the sample set.

## Notes
This is a training project. It intentionally has no production authentication or authorization. Do not deploy it with real employee/customer data without adding authentication, authorization, rate limiting, secrets management, and operational safeguards.
