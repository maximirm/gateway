from typing import List
from uuid import UUID

from app.clients import user_service_client
from app.clients.schemas.user_schemas import UserResponse, UserCreate


async def register_user(user: UserCreate):

    await user_service_client.create_user(user)

async def get_user(token: str) -> UserResponse:
    return await user_service_client.fetch_user_by_token(token)


async def get_all_users() -> List[UserResponse]:
    return await user_service_client.fetch_all_users()


async def delete_user(user_id: UUID):
    await user_service_client.delete_user(user_id)
