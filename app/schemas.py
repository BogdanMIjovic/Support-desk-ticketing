from pydantic import BaseModel, Field
from typing import Optional

class TicketCreate(BaseModel):
    title: str
    description: str
    resolution: Optional[str] = None

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    resolution: Optional[str] = None

class Token(BaseModel):
    token: str
    type: str


