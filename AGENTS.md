# SLA Desk Agent Guide

## Project
Full-stack SLA ticket dashboard. Read `docs/spec.md` before changing behavior.

## Architecture
- `backend/app/main.py`: FastAPI routes and application lifespan.
- `backend/app/models.py`: SQLAlchemy ticket model.
- `backend/app/sla.py`: SLA targets, UTC deadline calculation, overdue rules.
- `backend/app/seed.py`: demo data.
- `frontend/src/App.jsx`: dashboard and ticket interactions.
- `frontend/src/components/`: reusable UI components.
- `frontend/src/api.js`: frontend API client.

## SLA rules
- High: 24h; Medium: 48h; Low: 72h.
- Calendar hours include weekends and holidays.
- Store/return UTC timestamps. `is_overdue` is derived at read time.
- Resolved and Closed tickets are not overdue. Status changes never reset the SLA clock.

## Commands
- Backend from `backend/`: `python -m pip install -r requirements.txt`
- Backend from `backend/`: `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
- Backend tests from `backend/`: `python -m pytest -v`
- Frontend from `frontend/`: `npm install`, `npm run dev`
- Frontend checks from `frontend/`: `npm test`, `npm run build`
- E2E from `frontend/`: `npx playwright install chromium`, `npm run test:e2e`

## Conventions
Keep API, domain rules, persistence, and UI separate. Validate input server-side. Add tests for behavior changes. Do not store production secrets. This training app has no authentication.
