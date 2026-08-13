from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    admin = "ADMIN"
    user = "USER"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    full_name: Optional[str] = None
    email: Optional[str] = Field(default=None, unique=True)
    role: UserRole = Field(default=UserRole.user,index=True)
    hashed_password: str
    is_active: bool = Field(default=True, index=True)




