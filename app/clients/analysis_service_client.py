import json
from uuid import UUID

import httpx
from fastapi import HTTPException

from app.clients.schemas.survey_schemas import QuestionAnalyzed, Question
from app.clients.util import custom_serializer


async def fetch_analyzed_question(question: Question) -> QuestionAnalyzed:
    url = f"http://localhost:8001/analyze/question/"
    async with httpx.AsyncClient() as client:
        json_question = json.dumps(dict(question), default=custom_serializer)
        response = await client.post(url, data=json_question)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])

    analyzed_question_data = response.json()
    return QuestionAnalyzed(**analyzed_question_data)
