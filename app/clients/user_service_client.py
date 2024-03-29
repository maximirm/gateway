import json
from uuid import UUID

import httpx
from fastapi import HTTPException

from app.clients.schemas.user_schemas import UserResponse, UserCreate, UserLogin

BASE_URL = "user:8003"


async def create_user(user: UserCreate):
    url = f"http://{BASE_URL}/users/register/"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=dict(user))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])


async def login(login_data: UserLogin):
    url = f"http://{BASE_URL}/users/login/"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=dict(login_data))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])
    user_data = response.json()
    return UserResponse(**user_data)


async def fetch_user_by_token(token: str) -> UserResponse:
    url = f"http://{BASE_URL}/users/"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])
    user_data = response.json()
    return UserResponse(**user_data)


async def fetch_all_users() -> list[UserResponse]:
    url = f"http://{BASE_URL}/users/all/"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])
    user_data = response.json()
    return [UserResponse(**user) for user in user_data]


async def delete_user(user_id: UUID):
    url = f"http://{BASE_URL}/users/{user_id}/"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])
