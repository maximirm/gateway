import json
from typing import List
from uuid import UUID

import httpx
from fastapi import HTTPException

from app.clients.schemas.user_schemas import UserResponse, UserCreate, UserLogin


async def create_user(user: UserCreate):
    url = "http://localhost:8003/users/register/"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=dict(user))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])


async def login(login_data: UserLogin):
    url = "http://localhost:8003/users/login/"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=dict(login_data))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])
    response_json = response.json()
    print(response_json)
    return response_json.get('token', None)


async def fetch_user_by_token(token: str) -> UserResponse:
    url = "http://localhost:8003/users/"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])
    user_data = response.json()
    return UserResponse(**user_data)


async def fetch_all_users() -> List[UserResponse]:
    url = "http://localhost:8003/users/all/"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])
    user_data = response.json()
    return [UserResponse(**user_data) for user_data in user_data]


async def delete_user(user_id: UUID):
    url = f"http://localhost:8003/users/{user_id}/"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])
