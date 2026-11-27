def test_health(client):
    assert client.get("/api/health").json()["status"] == "ok"

def test_seeded_dashboard_has_tickets(client):
    data = client.get("/api/dashboard").json()
    assert data["total"] == 8
    assert data["overdue"] >= 1
    assert 0 <= data["sla_compliance"] <= 100

def test_create_ticket_assigns_due_date(client):
    response = client.post("/api/tickets", json={"title":"Cannot access VPN", "description":"VPN connection fails on startup", "requester":"Jamie Lee", "priority":"High"})
    assert response.status_code == 201
    ticket = response.json()
    assert ticket["sla_hours"] == 24
    assert ticket["is_overdue"] is False
    assert ticket["due_at"] > ticket["created_at"]

def test_reject_blank_ticket(client):
    response = client.post("/api/tickets", json={"title":"  ", "description":"Something is broken", "requester":"Jamie Lee", "priority":"Low"})
    assert response.status_code == 422

def test_invalid_priority_rejected(client):
    response = client.post("/api/tickets", json={"title":"Broken laptop", "description":"Laptop will not start", "requester":"Jamie Lee", "priority":"Urgent"})
    assert response.status_code == 422

def test_filters_and_search(client):
    assert all(t["priority"] == "High" for t in client.get("/api/tickets?priority=High").json())
    assert len(client.get("/api/tickets?search=VPN").json()) >= 1

def test_status_update_preserves_due_date(client):
    ticket = client.get("/api/tickets").json()[0]
    due = ticket["due_at"]
    updated = client.patch(f"/api/tickets/{ticket['id']}/status", json={"status":"Resolved"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "Resolved"
    assert updated.json()["due_at"] == due
    assert updated.json()["is_overdue"] is False

def test_missing_ticket_returns_404(client):
    assert client.patch("/api/tickets/99999/status", json={"status":"Closed"}).status_code == 404

def test_demo_reset(client):
    client.post("/api/demo/reset")
    assert client.get("/api/dashboard").json()["total"] == 8
