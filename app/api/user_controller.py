from typing import List

from fastapi import Header, APIRouter, Request

from app.clients.schemas.user_schemas import UserResponse
from app.decorator.has_role import has_role
from app.services import user_service

router = APIRouter()


@router.get("/users/", response_model=UserResponse)
async def get_user(
        authorization: str = Header(..., description="Authorization token")

):
    token = authorization.split("Bearer ")[1]
    return await user_service.get_user(token)


@router.get("/users/all", response_model=List[UserResponse])
@has_role(["admin"])
async def get_all_users(request: Request):
    return await user_service.get_all_users()
