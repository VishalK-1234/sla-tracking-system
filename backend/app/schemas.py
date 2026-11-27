from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

Priority = Literal["High", "Medium", "Low"]
Status = Literal["Open", "In Progress", "Resolved", "Closed"]

class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=5, max_length=2000)
    requester: str = Field(min_length=2, max_length=100)
    priority: Priority

    @field_validator("title", "description", "requester")
    @classmethod
    def trim_and_reject_blank(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be blank")
        return value

class StatusUpdate(BaseModel):
    status: Status

class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    requester: str
    priority: str
    status: str
    created_at: datetime
    due_at: datetime
    is_overdue: bool
    sla_hours: int
    hours_remaining: float

class DashboardOut(BaseModel):
    total: int
    open: int
    in_progress: int
    resolved: int
    overdue: int
    sla_compliance: float
