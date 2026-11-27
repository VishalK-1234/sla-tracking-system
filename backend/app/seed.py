from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from .models import Ticket
from .sla import calculate_due_at

SAMPLES = [
    ("VPN access unavailable", "Remote employee cannot connect to the corporate VPN.", "Maya Chen", "High", "Open", -30),
    ("Payroll export mismatch", "Monthly payroll export contains mismatched totals.", "Daniel Reed", "High", "In Progress", -8),
    ("Laptop battery replacement", "Laptop battery drains within one hour.", "Ava Patel", "Medium", "Open", -12),
    ("Update design software", "Install the approved design software update.", "Noah Kim", "Low", "Open", -18),
    ("Email access restored", "Mailbox access issue has been resolved.", "Olivia Jones", "Medium", "Resolved", -60),
    ("Printer queue blocked", "The third-floor printer queue is stuck.", "Ethan Brooks", "Medium", "Open", -55),
    ("New starter account", "Create access for a new team member.", "Sophia Garcia", "Low", "In Progress", -4),
    ("Suspicious login alert", "Investigate an unusual sign-in notification.", "Liam Wilson", "High", "Closed", -50),
]

def seed_demo(db: Session):
    if db.query(Ticket).count():
        return
    now = datetime.now(timezone.utc)
    for title, description, requester, priority, status, age_hours in SAMPLES:
        created = now + timedelta(hours=age_hours)
        db.add(Ticket(title=title, description=description, requester=requester,
                      priority=priority, status=status, created_at=created,
                      due_at=calculate_due_at(created, priority)))
    db.commit()

def reset_demo(db: Session):
    db.query(Ticket).delete()
    db.commit()
    seed_demo(db)
