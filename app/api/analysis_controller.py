from uuid import UUID

from fastapi import APIRouter, Request

from app.clients import survey_service_client, analysis_service_client
from app.clients.schemas.survey_schemas import QuestionAnalyzed
from app.decorator.has_role import has_role


router = APIRouter()


@router.get("/analyze/question/{question_id}/", response_model=QuestionAnalyzed)
@has_role(["editor"])
async def analyze_question(request: Request, question_id: UUID):
    question = await survey_service_client.fetch_question(question_id)
    analyzed_question = await analysis_service_client.fetch_analyzed_question(question)
    return analyzed_question

