from uuid import UUID

from fastapi import APIRouter, Request

from app.clients.schemas import schemas
from app.decorator.user_validation import has_role
from app.services import analysis_service

router = APIRouter()


@router.get("/analyze/question/{question_id}", response_model=schemas.QuestionAnalyzed)
@has_role(["admin", "editor"])
async def analyze_question(request: Request, question_id: UUID):
    return await analysis_service.analyze_question(question_id)
