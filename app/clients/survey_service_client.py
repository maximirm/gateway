import json
from uuid import UUID

import httpx
from fastapi import HTTPException

from app.clients.schemas.survey_schemas import Question, Survey, SurveyCreate
from app.clients.util import custom_serializer


async def create_survey(survey: SurveyCreate):
    url = "http://localhost:8000/surveys/"
    async with httpx.AsyncClient() as client:
        json_survey = json.dumps(dict(survey), default=custom_serializer)
        response = await client.post(url, data=json_survey)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])


async def fetch_surveys_by_creator_id(creator_id: UUID) -> list[Survey]:
    url = f"http://localhost:8000/surveys/by_creator/{creator_id}/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])

    survey_data = response.json()
    return [Survey(**survey) for survey in survey_data]


async def delete_survey(survey_id: UUID):
    url = f"http://localhost:8000/surveys/{survey_id}/"
    async with httpx.AsyncClient() as client:
        response = await client.delete(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])


async def delete_surveys_by_creator_id(creator_id: UUID):
    url = f"http://localhost:8000/surveys/by_creator/{creator_id}/"
    async with httpx.AsyncClient() as client:
        response = await client.delete(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])


async def fetch_question(question_id: UUID) -> Question:
    url = f"http://localhost:8000/questions/{question_id}/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])

    question_data = response.json()
    return Question(**question_data)
