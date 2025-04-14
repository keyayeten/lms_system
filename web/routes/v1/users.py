from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from web.core.auth import (
    get_current_user
)
from web.models.users import User
from web.schemas.users import (
    UserResponseSchema
)
from web.services.dependencies import get_user_service
from web.services.users_service import UserService


users = APIRouter(prefix="/users")


# User endpoints (require authentication)
@users.get("/", response_model=List[UserResponseSchema])
async def list_users(
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    """
    Get list of all users (requires authentication)
    """
    return await user_service.get_all_users()


@users.get("/me", response_model=UserResponseSchema)
async def read_current_user(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user
    """
    return current_user


@users.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    """
    Get user by ID (requires authentication)
    """
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@users.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    """
    Delete user by ID (requires authentication)
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own account"
        )

    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
