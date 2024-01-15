from uuid import UUID

from fastapi import APIRouter, Request, Depends

from app.clients.schemas import schemas
from app.decorator.has_role import has_role, get_current_user_id
from app.services import analysis_service

router = APIRouter()


@router.get("/analyze/question/{question_id}/", response_model=schemas.QuestionAnalyzed)
@has_role(["admin", "editor"])
async def analyze_question(request: Request, question_id: UUID):

    return await analysis_service.analyze_question(question_id)
