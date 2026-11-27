from datetime import datetime, timedelta, timezone

SLA_HOURS = {"High": 24, "Medium": 48, "Low": 72}
COMPLETED_STATUSES = {"Resolved", "Closed"}

def ensure_utc(value: datetime) -> datetime:
    # SQLite may return naive datetimes; persisted values are interpreted as UTC.
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)

def calculate_due_at(created_at: datetime, priority: str) -> datetime:
    if priority not in SLA_HOURS:
        raise ValueError(f"Unsupported priority: {priority}")
    return ensure_utc(created_at) + timedelta(hours=SLA_HOURS[priority])

def is_overdue(due_at: datetime, status: str, now: datetime | None = None) -> bool:
    if status in COMPLETED_STATUSES:
        return False
    current = ensure_utc(now or datetime.now(timezone.utc))
    return current > ensure_utc(due_at)

def serialize_ticket(ticket, now: datetime | None = None) -> dict:
    current = ensure_utc(now or datetime.now(timezone.utc))
    due = ensure_utc(ticket.due_at)
    created = ensure_utc(ticket.created_at)
    return {
        "id": ticket.id, "title": ticket.title, "description": ticket.description,
        "requester": ticket.requester, "priority": ticket.priority, "status": ticket.status,
        "created_at": created, "due_at": due,
        "is_overdue": is_overdue(due, ticket.status, current),
        "sla_hours": SLA_HOURS[ticket.priority],
        "hours_remaining": round((due-current).total_seconds()/3600, 2),
    }
