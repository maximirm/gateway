from uuid import UUID

from fastapi import APIRouter, Request

from app.clients import survey_service_client, analysis_service_client
from app.clients.schemas.survey_schemas import AnalyzedQuestion, AnalyzedSurvey
from app.decorator.has_role import has_role


router = APIRouter()


@router.get("/analyze/question/{question_id}/", response_model=AnalyzedQuestion)
@has_role(["editor"])
async def analyze_question(request: Request, question_id: UUID):
    question = await survey_service_client.fetch_question(question_id)
    analyzed_question = await analysis_service_client.fetch_analyzed_question(question)
    return analyzed_question


@router.get("/analyze/survey/{survey_id}/", response_model=AnalyzedSurvey)
@has_role(["editor"])
async def analyze_survey(request: Request, survey_id: UUID):
    survey = await survey_service_client.fetch_survey(survey_id)
    analyzed_survey = await analysis_service_client.fetch_analyzed_survey(survey)
    return analyzed_survey



