from app.clients import user_service_client
from app.clients.schemas.user_schemas import UserResponse


async def get_user(token: str) -> UserResponse:
    return await user_service_client.fetch_user_by_token(token)
