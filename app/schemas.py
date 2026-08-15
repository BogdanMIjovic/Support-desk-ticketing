from pydantic import BaseModel
from typing import Optional
from app.models import UserBase

class TicketCreate(BaseModel):
    title: str
    description: str

class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: str

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    resolution: Optional[str] = None

class UserOut(UserBase):
    pass

class TokenData(BaseModel):
    username: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str


