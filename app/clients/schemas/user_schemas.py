from typing import Optional

from pydantic import BaseModel, UUID4


class UserResponse(BaseModel):
    id: UUID4
    name: str
    role: str
    token: Optional[str]

    class Config:
        from_attributes = True
