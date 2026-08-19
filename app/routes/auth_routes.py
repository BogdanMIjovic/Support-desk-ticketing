from fastapi.security import OAuth2PasswordRequestForm
from app.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlmodel import Session
from app.database import get_session
from datetime import timedelta
from app.schemas import Token

router = APIRouter(tags=["Auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_session)
):
    user = authenticate_user(user_data.username, user_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"})

    expire_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    data = {"sub": user.username}

    access_token = create_access_token(data=data, expire_delta=expire_delta)

    return Token(access_token=access_token, token_type="bearer")














