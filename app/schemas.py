from datetime import datetime
from tokenize import String
from pydantic import BaseModel, EmailStr
from typing import Optional

from pydantic.types import conint

class UserCreate(BaseModel):
    email: EmailStr  # pip install email-validator
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:  # pydentic converts class to dictionary
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):  # validate payload format . This is the schema
    title: str              # https://pydantic-docs.helpmanual.io/usage/validators/
    content: str
    published: bool = True  # set default value  # the users is not obliged to provide with it


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class UpdatePost(PostBase):
    title: str
    content: str
    published: bool  # no default value


class Post(PostBase):  # the response will have this schema
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut  # it automatically retrives the information of the owner

    class Config:  # converts class to dictionary
        orm_mode = True

    # title: str
    # content: str
    # published: bool
    # owner_id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class Vote(BaseModel):
    post_id: int 
    dir: conint(le = 1) # max = 1, but it takes negative numbers
    