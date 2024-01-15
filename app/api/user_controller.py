from typing import List
from uuid import UUID

from fastapi import Header, APIRouter, Request
from starlette.responses import JSONResponse

from app.clients.schemas.user_schemas import UserResponse, UserCreate, UserLogin
from app.decorator.has_role import has_role
from app.services import user_service

router = APIRouter()


@router.post("/users/register/")
async def register_user(user: UserCreate):
    await user_service.register_user(user)
    return JSONResponse(content="User created successfully", status_code=200)


@router.post("/users/login/")
async def login_user(login_data: UserLogin):
    token = await user_service.login(login_data)
    return JSONResponse(content={"token": token}, status_code=200)


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
async def delete_user(request: Request, user_id: UUID):
    await user_service.delete_user(user_id)
    return JSONResponse(content=f"User with id {user_id} deleted successfully", status_code=200)
