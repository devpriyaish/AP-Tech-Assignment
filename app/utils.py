import json
import bcrypt
from fastapi import HTTPException, Header, status
import jwt

from decouple import config
from datetime import datetime, timedelta


JWT_SECRET = config('JWT_SECRET')
JWT_ALGORITHM = config('JWT_ALGORITHM')


async def hash_password(password: str) -> str:
    """
    A function to hash a password using bcrypt.

    Parameters:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password as a string.
    """

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Return the hashed password as a string
    return hashed_password.decode('utf-8')


async def sign_jwt(email: str) -> str:
    """
    Asynchronously signs a JWT token using the provided email.

    Parameters:
        email (str): The email for which the token is being signed.

    Returns:
        str: The signed JWT token.
    """
        
    # Define the expiration time for the token
    expires_delta = timedelta(days=1)
    expires_at = datetime.utcnow() + expires_delta

    # Create the payload containing the email and expiration time
    payload = {
        "email": email,
        "exp": expires_at
    }

    # Generate the JWT token
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token.decode("utf-8")


async def validate_user(email: str, password: str) -> bool:
    """
    Validate user's email and password by loading user data from users.json 
    file.
    
    Args:
        email (str): The user's email.
        password (str): The user's password.
        
    Returns:
        bool: True if the user is validated, False otherwise.
    """
        
    # Load user data from users.json file
    with open("file_store/users.json", "r") as file:
        users_data = json.load(file)

    # Find the user by email
    user = next(
        (user for user in users_data["users"] if user["email"] == email), None
    )

    if user:
        # Check if the provided password matches the hashed password
        hashed_password = user.get("password")
        if hashed_password and bcrypt.checkpw(
            password.encode("utf-8"), hashed_password.encode("utf-8")
        ):
            return True

    return False


async def verify_token(authorization: str = Header(...)):
    """
    An asynchronous function to verify the token from the Authorization header.

    Args:
        authorization (str): The Authorization header containing the token.

    Returns:
        dict: The payload extracted from the token.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        # Extract the token from the Authorization header
        token = authorization.split()[1]
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload, token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
