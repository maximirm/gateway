from uuid import UUID

from fastapi import APIRouter


from app.clients.schemas import schemas


from app.services import analysis_service

router = APIRouter()


@router.get("/analyze/question/{question_id}", response_model=schemas.QuestionAnalyzed)
async def analyze_question(question_id: UUID):

    return await analysis_service.analyze_question(question_id)




