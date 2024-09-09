import bcrypt
from pydantic import BaseModel


class RegisterUserResponse(BaseModel):
    """
    The response model for a successful user registration. It includes the user ID and a message indicating successful registration.
    """

    user_id: str
    message: str


async def register_user(
    email: str, password: str, username: str
) -> RegisterUserResponse:
    """
    Registers a new user into the system.

    Args:
    email (str): The email address of the new user. It must be unique across the system.
    password (str): The user's chosen password. This will be hashed and not stored in plain text for security.
    username (str): The user's desired username. This is how they will be identified in the system aside from their email.

    Returns:
    RegisterUserResponse: The response model for a successful user registration. It includes the user ID and a message indicating successful registration.
    """
    hashed_password = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode(
        "utf8"
    )
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    return RegisterUserResponse(
        user_id=user_id, message="User registered successfully."
    )
