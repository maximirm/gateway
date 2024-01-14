from uuid import UUID

from app.clients.schemas.schemas import QuestionAnalyzed
from app.clients.analysis_service_client import fetch_analyzed_question


async def get_analyzed_question(question_id: UUID) -> QuestionAnalyzed:

    return await fetch_analyzed_question(question_id)
