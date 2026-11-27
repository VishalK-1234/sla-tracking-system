from datetime import datetime, timedelta, timezone
import pytest
from app.sla import calculate_due_at, is_overdue

BASE = datetime(2026, 11, 27, 10, 0, tzinfo=timezone.utc)

@pytest.mark.parametrize("priority,hours", [("High",24),("Medium",48),("Low",72)])
def test_due_date_by_priority(priority, hours):
    assert calculate_due_at(BASE, priority) == BASE + timedelta(hours=hours)

def test_weekends_are_included():
    friday = datetime(2026, 11, 27, 10, 0, tzinfo=timezone.utc)
    assert calculate_due_at(friday, "High") == datetime(2026, 11, 28, 10, 0, tzinfo=timezone.utc)

def test_invalid_priority_rejected():
    with pytest.raises(ValueError): calculate_due_at(BASE, "Urgent")

def test_not_overdue_at_exact_due_time():
    due = BASE + timedelta(hours=24)
    assert is_overdue(due, "Open", due) is False

def test_overdue_after_due_time():
    due = BASE + timedelta(hours=24)
    assert is_overdue(due, "In Progress", due + timedelta(seconds=1)) is True

@pytest.mark.parametrize("status", ["Resolved", "Closed"])
def test_completed_ticket_never_overdue(status):
    assert is_overdue(BASE, status, BASE + timedelta(days=10)) is False
