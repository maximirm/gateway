from uuid import UUID

from app.clients.schemas.schemas import QuestionAnalyzed, Question
from app.clients import analysis_service_client, survey_service_client


async def get_question(question_id: UUID) -> Question:
    return await survey_service_client.fetch_question(question_id)


async def analyze_question(question_id: UUID) -> QuestionAnalyzed:
    question = await survey_service_client.fetch_question(question_id)
    analyzed_question = await analysis_service_client.fetch_analyzed_question(question)
    return analyzed_question
