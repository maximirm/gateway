from uuid import UUID

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from app.clients import user_service_client, survey_service_client
from app.clients.schemas.user_schemas import UserResponse, UserCreate, UserLogin
from app.decorator.has_role import has_role

router = APIRouter()


@router.post("/users/register/")
async def register_user(user: UserCreate):
    await user_service_client.create_user(user)
    return JSONResponse(content="User created successfully", status_code=200)


@router.post("/users/login/")
async def login_user(login_data: UserLogin):
    return await user_service_client.login(login_data)


@router.get("/users/all/", response_model=list[UserResponse])
@has_role(["admin"])
async def get_all_users(request: Request):
    return await user_service_client.fetch_all_users()


@router.delete("/users/{user_id}/", response_model=str)
@has_role(["admin"])
async def delete_user(request: Request, user_id: UUID):
    await user_service_client.delete_user(user_id)
    await survey_service_client.delete_surveys_by_creator_id(user_id)
    return JSONResponse(content=f"User with id {user_id} deleted successfully", status_code=200)
