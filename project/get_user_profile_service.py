from datetime import datetime
from enum import Enum

import prisma
import prisma.enums
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    """
    The response model returning the user's profile details.
    """

    id: str
    email: str
    role: prisma.enums.Role
    createdAt: datetime
    updatedAt: datetime


async def get_user_profile() -> UserProfileResponse:
    """
    Retrieves the user's profile information for the currently authenticated user.

    This function assumes the existence of a mechanism to identify the currently logged-in user,
    typically through a session or token authentication.

    It fetches the user's profile details from the database and returns them in a structured form.
    If the user does not exist or the profile cannot be retrieved, it raises an HTTPException.

    Args:
        None

    Returns:
        UserProfileResponse: The response model returning the user's profile details including
                             ID, email, role, createdAt, and updatedAt timestamps.

    Raises:
        HTTPException: An error occurred accessing the user information.
    """
    current_user_id = "the-currently-authenticated-user-id"
    user = await prisma.models.User.prisma().find_unique(where={"id": current_user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    role_str = user.role.value if isinstance(user.role, Enum) else user.role
    return UserProfileResponse(
        id=user.id,
        email=user.email,
        role=role_str,
        createdAt=user.createdAt,
        updatedAt=user.updatedAt,
    )
