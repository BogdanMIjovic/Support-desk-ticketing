from jwt import InvalidTokenError
from pwdlib import PasswordHash
from app.database import get_session
from app.models import User, UserRole
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timezone, timedelta
from typing import Optional, Annotated
from fastapi.security import OAuth2PasswordBearer
from app.schemas import TokenData
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
password_hash = PasswordHash.recommended()

def get_hashed_password(password:str):
    return password_hash.hash(password)

def get_user(username: str, session: Session = Depends(get_session)):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user

def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)

def authenticate_user(username:str, password:str, session: Session = Depends(get_session)):
    user = get_user(username, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_schema)], session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(token_data.username, session)
    if not user:
        raise credentials_exception
    return user

async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]):

    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not active!")

    return current_user


async def get_current_admin_user(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permission!")

    return current_user













