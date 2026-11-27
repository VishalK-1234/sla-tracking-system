from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .database import Base, engine, get_db
from .models import Ticket
from .schemas import TicketCreate, TicketOut, StatusUpdate, DashboardOut
from .sla import SLA_HOURS, COMPLETED_STATUSES, calculate_due_at, serialize_ticket
from .seed import seed_demo, reset_demo

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with next(get_db()) as db:
        seed_demo(db)
    yield

app = FastAPI(title="SLA Desk API", version="1.0.0", description="Priority-based SLA tracking API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "SLA Desk API"}

@app.get("/api/tickets", response_model=list[TicketOut])
def list_tickets(search: str = Query(default="", max_length=120), priority: str | None = None,
                 status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Ticket)
    if priority:
        if priority not in SLA_HOURS: raise HTTPException(422, "Invalid priority filter")
        query = query.filter(Ticket.priority == priority)
    if status:
        if status not in {"Open", "In Progress", "Resolved", "Closed"}: raise HTTPException(422, "Invalid status filter")
        query = query.filter(Ticket.status == status)
    if search.strip():
        term = f"%{search.strip()}%"
        query = query.filter((Ticket.title.ilike(term)) | (Ticket.requester.ilike(term)) | (Ticket.description.ilike(term)))
    return [serialize_ticket(t) for t in query.order_by(desc(Ticket.created_at)).all()]

@app.post("/api/tickets", response_model=TicketOut, status_code=201)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    created = datetime.now(timezone.utc)
    ticket = Ticket(**payload.model_dump(), status="Open", created_at=created,
                    due_at=calculate_due_at(created, payload.priority))
    db.add(ticket); db.commit(); db.refresh(ticket)
    return serialize_ticket(ticket)

@app.patch("/api/tickets/{ticket_id}/status", response_model=TicketOut)
def update_status(ticket_id: int, payload: StatusUpdate, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket: raise HTTPException(404, "Ticket not found")
    ticket.status = payload.status
    db.commit(); db.refresh(ticket)
    return serialize_ticket(ticket)

@app.get("/api/dashboard", response_model=DashboardOut)
def dashboard(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    items = [serialize_ticket(t) for t in tickets]
    total = len(items)
    overdue = sum(x["is_overdue"] for x in items)
    completed = sum(x["status"] in COMPLETED_STATUSES for x in items)
    compliant = total - overdue
    return {"total": total, "open": sum(x["status"] == "Open" for x in items),
            "in_progress": sum(x["status"] == "In Progress" for x in items),
            "resolved": completed, "overdue": overdue,
            "sla_compliance": round((compliant / total * 100) if total else 100.0, 1)}

@app.post("/api/demo/reset")
def demo_reset(db: Session = Depends(get_db)):
    reset_demo(db)
    return {"message": "Demo tickets restored", "count": db.query(Ticket).count()}
