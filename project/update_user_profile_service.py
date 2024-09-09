from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    Response object, including the updated profile info for the user.
    """

    id: str
    email: str
    username: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


async def update_user_profile(
    email: Optional[str],
    username: Optional[str],
    bio: Optional[str],
    avatar_url: Optional[str],
) -> UpdateUserProfileResponse:
    """
    Updates the user's profile information. The function identifies the user by the given email,
    and then updates the user's profile with provided values. Fields not provided (i.e., None)
    will not be updated. The email is used as the identifier to find the user.

    Args:
      email (Optional[str]): The user's new email address.
      username (Optional[str]): The new username for the user.
      bio (Optional[str]): A new bio for the user, describing self in a short paragraph.
      avatar_url (Optional[str]): URL to the new avatar image for the user profile.

    Returns:
      UpdateUserProfileResponse: An object including the updated profile info for the user.

    Raises:
      ValueError: If email is not provided or the user is not found.
    """
    if email is None:
        raise ValueError("Email is required for identifying the user to update.")
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user is None:
        raise ValueError("User not found with the provided email.")
    update_data = {}
    if username is not None:
        update_data["username"] = username
    if bio is not None:
        update_data["bio"] = bio
    if avatar_url is not None:
        update_data["avatar_url"] = avatar_url
    updated_user = await prisma.models.User.prisma().update(
        where={"email": email}, data=update_data
    )
    return UpdateUserProfileResponse(
        id=updated_user.id,
        email=updated_user.email,
        username=updated_user.username,
        bio=updated_user.bio,
        avatar_url=updated_user.avatar_url,
    )  # TODO(autogpt): Cannot access attribute "username" for class "User"


#     Attribute "username" is unknown. reportAttributeAccessIssue
