import json
from datetime import datetime, timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from model import UserLoginSchema, UserSchema, Token
from utils import hash_password, sign_jwt, validate_user, verify_token


auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

revoked_tokens = set()


@auth_router.post("/user/signup", tags=["user"])
async def user_signup(user: UserSchema = Body(...)):
    """
    Handles user signup by adding the user data to the users.json file and 
    returning a JWT token upon successful creation. 
    :param user: UserSchema - the user data to be signed up
    :return: dict - a dictionary containing the JWT token
    """
    try:
        # Read existing users from the users.json file
        with open("file_store/users.json", "r") as file:
            users_data = json.load(file)
    except FileNotFoundError:
        users_data = {"users": []}

    # Hash the user's password before storing it
    hashed_password = await hash_password(user.password)
    user.password = hashed_password

    # Append the new user data to the existing user list
    users_data["users"].append(user.dict())

    # Write the updated user data back to the users.json file
    with open("file_store/users.json", "w") as file:
        json.dump(users_data, file, indent=4)

    # Return a JWT token upon successful user creation
    jwt_token = await sign_jwt(user.email)
    return {"token": jwt_token}


@auth_router.post("/user/signin", tags=["user"])
async def user_signin(user: UserLoginSchema = Body(...)):
    """ 
    Handles user login by checking if the provided credentials are valid. 
    :param user: UserLoginSchema - the user credentials
    :return: dict - a dictionary containing the JWT token
    """
    # If the user credentials are valid, return a JWT token
    if await validate_user(user.email, user.password):
        return {"token": await sign_jwt(user.email)}
    else:
        # If the user credentials are invalid, return an error message
        return {"error": "Wrong login details"}


@auth_router.get("/user/protected")
async def protected_route(payload: dict = Depends(verify_token)):
    """
	A protected route that requires a valid JWT token to access it. 
	:param payload: dict - the JWT token payload
	:return: dict - a dictionary containing the message and user data
	"""
    await is_token_revoked(payload[1])
    return {"message": "This is a protected route", "user": payload[0]}


@auth_router.post("/user/revoke-token/", response_model=Token)
async def revoke_token(token: Token):
    """
	Revoke a token. 
	:param token: Token - the JWT token
	:return: dict - a dictionary containing the access token
    """
    revoked_tokens.add(token.access_token)
    return {"access_token": token.access_token}


async def is_token_revoked(token: str = Depends(oauth2_scheme)):
    """
    Asynchronous function to check if a token is revoked. 
    Takes a token as input and raises an HTTPException if the token is revoked.
    """
        
    if token in revoked_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked"
        )
    

@auth_router.post("/user/refresh-token/")
async def refresh_token(request: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint to refresh an expired token.
    :param request: OAuth2PasswordRequestForm - form containing the refresh token
    :return: dict - a dictionary containing the new access token
    """
    try:
        # Verify the refresh token
        payload = await verify_token(request.refresh_token)
    except HTTPException as e:
        # Handle invalid refresh token
        raise HTTPException(
            status_code=e.status_code,
            detail="Invalid refresh token"
        )

    # Check if the token is expired or soon to expire
    expiration_delta = timedelta(minutes=15)
    if payload["exp"] - datetime.utcnow() > expiration_delta:
        # Token is not yet expired or soon to expire, return error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token is not expired or not soon to expire"
        )

    # Invalidate the old refresh token
    revoked_tokens.add(request.refresh_token)

    # Generate new access token
    new_access_token = await sign_jwt(payload["sub"])

    # Return the new access token
    return {"access_token": new_access_token}

    
@auth_router.post("/logout/")
async def logout(token: str = Depends(oauth2_scheme)):
    """
	Revoke a token. 
	:param token: str - the JWT token
	:return: dict - a dictionary containing the message
	"""
        
    # Revoke token
    await revoke_token(Token(access_token=token))
    return {"message": "Logout successful"}