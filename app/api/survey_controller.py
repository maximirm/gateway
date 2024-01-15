from uuid import UUID

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from app.clients.schemas.survey_schemas import Survey
from app.decorator.has_role import has_role
from app.services import survey_service

router = APIRouter()


@router.get("/surveys/by_creator/{creator_id}/", response_model=list[Survey])
@has_role(["admin", "editor"])
async def get_surveys_by_creator_id(request: Request, creator_id: UUID):
    return await survey_service.get_surveys_by_creator_id(creator_id)

@router.delete("/surveys/by_creator/{creator_id}/", response_model=dict)
@has_role(["admin", "editor"])
async def delete_surveys_by_creator_id(request: Request, creator_id: UUID):
    await survey_service.delete_surveys_by_creator_id(creator_id)
    return JSONResponse(content=f"Surveys for creator-ID {str(creator_id)} deleted successfully", status_code=200)
