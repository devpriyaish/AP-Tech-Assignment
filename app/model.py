from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    full_name: str = Field(default=None, description="User's full name")
    email: str = Field(..., description="User's email address")
    username: str = Field(default=None, description="User's username")
    password: str = Field(..., description="User's password")

    class Config:
        schema_demo = {
            "full_name": "Demo User",
            "email": "demo@sample.com",
            "username": "demo4u",
            "password": "demo123",
        }


class UserLoginSchema(BaseModel):
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
		
    class Config:
        schema_demo = {
            "email": "demo@sample.com",
            "password": "demo123",
        }


class Token(BaseModel):
    access_token: str