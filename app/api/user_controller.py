from typing import List

from fastapi import Header, APIRouter, Request, Depends
from starlette.responses import JSONResponse

from app.clients.schemas.user_schemas import UserResponse
from app.decorator.has_role import has_role, get_current_user_id
from app.services import user_service

router = APIRouter()


@router.get("/users/", response_model=UserResponse)
async def get_user(
        authorization: str = Header(..., description="Authorization token")

):
    token = authorization.split("Bearer ")[1]
    return await user_service.get_user(token)


@router.get("/users/all/", response_model=List[UserResponse])
@has_role(["admin"])
async def get_all_users(request: Request):
    return await user_service.get_all_users()

@router.delete("/users/{user_id}/", response_model=str)
@has_role(["admin"])
async def delete_user(request: Request, user_id=Depends(get_current_user_id)):
    await user_service.delete_user(user_id)
    return JSONResponse(content=f"User with id {user_id} deleted successfully", status_code=200)
