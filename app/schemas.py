from typing import Optional
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True

class PostRequest(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    uid: Optional[str] = None
