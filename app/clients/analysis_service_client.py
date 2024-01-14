import json
from uuid import UUID

import httpx
from fastapi import HTTPException

from app.clients.schemas.schemas import QuestionAnalyzed, Question


def custom_serializer(obj):
    if isinstance(obj, UUID):
        return str(obj)
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


async def fetch_analyzed_question(question: Question) -> QuestionAnalyzed:
    url = f"http://localhost:8001/analyze/question"
    async with httpx.AsyncClient() as client:
        json_question = json.dumps(dict(question), default=custom_serializer)
        response = await client.post(url, data=json_question, headers={"Content-Type": "application/json"})

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])

    analyzed_question_data = response.json()
    return QuestionAnalyzed(**analyzed_question_data)
