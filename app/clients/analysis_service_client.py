import json

import httpx
from fastapi import HTTPException

from app.clients.schemas.survey_schemas import AnalyzedQuestion, Question
from app.clients.util import custom_serializer

BASE_URL = "analysis:8001"


async def fetch_analyzed_question(question: Question) -> AnalyzedQuestion:
    url = f"http://{BASE_URL}/analyze/question/"
    async with httpx.AsyncClient() as client:
        json_question = json.dumps(dict(question), default=custom_serializer)
        response = await client.post(url, data=json_question)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])

    analyzed_question_data = response.json()
    return AnalyzedQuestion(**analyzed_question_data)
