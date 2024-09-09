from datetime import datetime, timedelta

import prisma
import prisma.models
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    Model to return the JWT token after successful authentication.
    """

    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed version.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password is correct, else False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=15)
) -> str:
    """
    Generates a JWT token with specified expiry.

    Args:
        data (dict): The payload to encode in the JWT token.
        expires_delta (timedelta, optional): Time until expiration of the token. Defaults to 15 minutes.

    Returns:
        str: The generated JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "SECRET_KEY", algorithm="HS256")
    return encoded_jwt


async def login_user(email: str, password: str) -> LoginResponse:
    """
    Authenticates a user and returns a JWT token.

    Args:
        email (str): The email address associated with the user's account.
        password (str): The password for the user's account.

    Returns:
        LoginResponse: Model to return the JWT token after successful authentication if credentials are valid.
                       Returns None if authentication fails.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user and verify_password(password, user.password):
        access_token = create_access_token(data={"sub": user.email})
        return LoginResponse(access_token=access_token, token_type="bearer")
    else:
        return LoginResponse(access_token="", token_type="")
