from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from web.core.settings import settings
from web.models.users import User
from web.services.dependencies import get_user_service
from web.services.users_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.auth.secret_key,
        algorithm=settings.auth.algorithm
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.auth.secret_key,
            algorithms=[settings.auth.algorithm]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_service.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user
