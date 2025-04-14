from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status

from web.core.settings import settings
from web.core.security import (
    get_password_hash,
    verify_password,
)
from web.core.auth import create_access_token
from web.schemas.users import (
    UserCreateSchema,
    UserResponseSchema,
    TokenSchema,
    UserLoginSchema
)
from web.services.dependencies import get_user_service
from web.services.users_service import UserService


auth = APIRouter(prefix="/auth")


# Auth endpoints
@auth.post("/register", response_model=UserResponseSchema)
async def register_user(
    user_data: UserCreateSchema,
    user_service: UserService = Depends(get_user_service)
):
    """
    Register new user
    """
    existing_user = await user_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(user_data.password)
    user = await user_service.create_user(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password
    )
    return user


@auth.post("/login", response_model=TokenSchema)
async def login_user(
    login_data: UserLoginSchema,
    user_service: UserService = Depends(get_user_service)
):
    """
    Login user and get access token
    """
    user = await user_service.get_user_by_email(login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.auth.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
