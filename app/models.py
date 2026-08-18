from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from enum import Enum
from datetime import datetime, timezone

class UserRole(str, Enum):
    admin = "ADMIN"
    user = "USER"

class TicketStatus(str, Enum):
    open = "OPEN"
    in_progress = "IN_PROGRESS"
    solved = "SOLVED"

class TicketPriority(str, Enum):
    low = "LOW"
    medium = "MEDIUM"
    high = "HIGH"

class UserBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    full_name: Optional[str] = None
    email: Optional[str] = Field(default=None, unique=True)
    role: UserRole = Field(default=UserRole.user,index=True)
    is_active: bool = Field(default=True, index=True)


class User(UserBase, table=True):
    hashed_password: str
    tickets: list["Ticket"] = Relationship(back_populates="user")


class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    status: TicketStatus = Field(default=TicketStatus.open, index=True)
    priority: TicketPriority = Field(default=TicketPriority.medium, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
    resolution: Optional[str] = None
    owner_id: int = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="tickets")








