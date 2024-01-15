from uuid import UUID

from fastapi import APIRouter, Request

from app.clients.schemas.survey_schemas import Survey
from app.decorator.has_role import has_role
from app.services import survey_service

router = APIRouter()


@router.get("/surveys/by_creator/{creator_id}/", response_model=list[Survey])
@has_role(["admin", "editor"])
async def get_surveys_by_creator_id(request: Request, creator_id: UUID):
    return await survey_service.get_surveys_by_creator_id(creator_id)


