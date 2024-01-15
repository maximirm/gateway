from typing import Optional

from pydantic import BaseModel, UUID4


class UserResponse(BaseModel):
    id: UUID4
    name: str
    role: str
    token: Optional[str]


class UserCreate(BaseModel):
    name: str
    password: str
    role: str


class UserLogin(BaseModel):
    name: str
    password: str
