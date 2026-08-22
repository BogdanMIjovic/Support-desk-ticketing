from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select, Field
from app.models import Ticket, User, UserRole
from app.database import get_session
from app.auth import get_current_active_user, get_current_admin_user
from app.schemas import TicketCreate, TicketUpdate
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

@router.get("/ticket/{ticket_id}", response_model=Ticket)
def get_ticket(
        ticket_id: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        session: Session = Depends(get_session)):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    if current_user.role == UserRole.admin:
        return ticket
    elif current_user.id == ticket.owner_id:
        return ticket
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access not granted")

@router.post("/ticket", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def create_ticket(
        payload: TicketCreate,
        current_user: Annotated[User, Depends(get_current_active_user)],
        session: Session = Depends(get_session)
        ):

    payload_for_validation = {
        "title": payload.title,
        "description": payload.description,
        "owner_id": current_user.id
    }

    ticket = Ticket.model_validate(payload_for_validation)
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

@router.patch("/ticket/{ticket_id}", response_model=Ticket)
def update_ticket(
        ticket_id: int,
        payload: TicketUpdate,
        current_user: Annotated[User, Depends(get_current_active_user)],
        session: Session = Depends(get_session)):

    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    updates = payload.model_dump(exclude_unset=True)

    if current_user.role == UserRole.admin:
        pass

    elif current_user.id == ticket.owner_id:
        if  payload.resolution or payload.status:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access not granted")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access not granted")

    for key, value in updates.items():
        setattr(ticket, key, value)

    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket




















