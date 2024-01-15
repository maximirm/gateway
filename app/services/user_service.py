from typing import List
from uuid import UUID

from fastapi import HTTPException

from app.clients import user_service_client
from app.clients.schemas.user_schemas import UserResponse, UserCreate, UserLogin


async def register_user(user: UserCreate):
    await user_service_client.create_user(user)


async def login(login_data: UserLogin):
    token = await user_service_client.login(login_data)
    if token is None:
        raise HTTPException(
            status_code=500, detail="Token not found in response")
    return token


async def get_user(token: str) -> UserResponse:
    return await user_service_client.fetch_user_by_token(token)


async def get_all_users() -> List[UserResponse]:
    return await user_service_client.fetch_all_users()


async def delete_user(user_id: UUID):
    await user_service_client.delete_user(user_id)
