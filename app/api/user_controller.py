from fastapi import Header, APIRouter

from app.clients.schemas import user_schemas
from app.services import user_service

router = APIRouter()


@router.get("/users/", response_model=user_schemas.UserResponse)
async def get_user(
        authorization: str = Header(..., description="Authorization token")

):
    token = authorization.split("Bearer ")[1]
    return await user_service.get_user(token)
