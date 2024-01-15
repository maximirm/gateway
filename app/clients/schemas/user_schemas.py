from typing import Optional

from pydantic import BaseModel, UUID4


class UserResponse(BaseModel):
    role: str
    token: Optional[str]
    id: UUID4

    class Config:
        from_attributes = True
