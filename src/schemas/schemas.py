from typing import Optional
from pydantic import BaseModel,EmailStr


#properties required during user creation
class create_new_user(BaseModel):
    username: str
    email : EmailStr
    hashed_password : str


class user_login(BaseModel):
    email : str
    hashed_password : str


class Token(BaseModel):
    access_token: str
    token_type: str