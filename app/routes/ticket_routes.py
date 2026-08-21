from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select, Field
from app.models import Ticket, User, UserRole
from app.database import get_session
from app.auth import get_current_active_user, get_current_admin_user
from typing import Optional, Annotated


router = APIRouter(tags=["Ticket"])

@router.get("/ticket", response_model=list[Ticket])
def list_tickets(current_user: Annotated[User, Depends(get_current_active_user)],
                 session: Session = Depends(get_session)):

    statement = select(Ticket)
    if current_user.role == UserRole.admin:
        pass

    else:
        statement = statement.where(Ticket.owner_id == current_user.id)

    statement = statement.order_by(Ticket.created_at.desc())
    return session.exec(statement).all()



