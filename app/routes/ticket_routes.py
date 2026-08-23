from fastapi import APIRouter, Depends,HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import Ticket, User, UserRole
from app.auth import get_current_active_user
from app.schemas import TicketCreate,TicketUpdate

from typing import Annotated


router = APIRouter(tags=["Ticket"])

@router.get("/ticket", response_model=list[Ticket])
def list_tickets(
        current_user: Annotated[User, Depends(get_current_active_user)],
        session: Session = Depends(get_session)):

    statement = select(Ticket)
    if current_user.role == UserRole.admin:
        pass
    else:
        statement = statement.where(Ticket.owner_id==current_user.id)
    statement = statement.order_by(Ticket.created_at.desc())
    return session.exec(statement).all()

@router.get("/ticket/{ticket_id}", response_model=Ticket)
def list_ticket(
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
        session: Session = Depends(get_session)):

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
        payload: TicketUpdate,
        ticket_id: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        session: Session = Depends(get_session)):

    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    if current_user.role == UserRole.admin:
        pass

    elif ticket.owner_id == current_user.id:
        if payload.resolution or payload.status:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action not allowed")

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action not allowed")

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(ticket, key, value)

    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

@router.delete("/ticket/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
        ticket_id: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        session: Session = Depends(get_session)):

    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    if current_user.role == UserRole.admin:
        pass

    elif current_user.id == ticket.owner_id:
        pass

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action not allowed")

    session.delete(ticket)
    session.commit()
    return





























