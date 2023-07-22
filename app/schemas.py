from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    # This is for pydantic response model
    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    # owner: UserOut

    # This is for pydantic response model
    class Config:
        orm_mode = True


class PostVote(BaseModel):
    id: int
    content: str
    created_at: datetime
    published: bool
    title: str
    owner_id: int


class PostOut(BaseModel):
    Post: Post
    votes: int

    # class Config:
    #     orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
