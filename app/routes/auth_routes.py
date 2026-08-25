from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta
from app.schemas import Token, UserOut, UserCreate
from app.database import get_session
from app.auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_hashed_password
from app.models import User

router = APIRouter(tags=["Auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
        login_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_session)
):
    user = authenticate_user(login_data.username, login_data.password, session)
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    data = {"sub": user.username}
    expire_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data, expire_delta)

    return Token(access_token=access_token, token_type="bearer")

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == payload.username)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    hashed_password = get_hashed_password(payload.password)
    base_user={
        "username": payload.username,
        "full_name": payload.full_name,
        "email": payload.email,
        "hashed_password": hashed_password
    }

    user = User.model_validate(base_user)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user