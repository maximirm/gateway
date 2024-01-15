from uuid import UUID

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from app.clients import survey_service_client
from app.clients.schemas.survey_schemas import Survey, SurveyCreate, QuestionCreate, ResponseCreate
from app.decorator.has_role import has_role

router = APIRouter()


@router.get("/surveys/by_creator/{creator_id}/", response_model=list[Survey])
@has_role(["admin", "editor"])
async def get_surveys_by_creator_id(request: Request, creator_id: UUID):
    return await survey_service_client.fetch_surveys_by_creator_id(creator_id)


@router.delete("/surveys/by_creator/{creator_id}/", response_model=dict)
@has_role(["admin", "editor"])
async def delete_surveys_by_creator_id(request: Request, creator_id: UUID):
    await survey_service_client.delete_surveys_by_creator_id(creator_id)
    return JSONResponse(content=f"Surveys for creator-ID {str(creator_id)} deleted successfully", status_code=200)


@router.post("/surveys/")
@has_role(["editor"])
async def create_survey(request: Request, survey: SurveyCreate):
    await survey_service_client.create_survey(survey)
    return JSONResponse(content="Survey created", status_code=200)


@router.delete("/surveys/{survey_id}/")
@has_role(["editor"])
async def delete_survey(request: Request, survey_id: UUID):
    await survey_service_client.delete_survey(survey_id)
    return JSONResponse(content=f"Survey with ID {str(survey_id)} deleted successfully", status_code=200)


@router.post("/questions/")
@has_role(["editor"])
async def create_question(request: Request, question: QuestionCreate):
    await survey_service_client.create_question(question)
    return JSONResponse(content="Question created", status_code=200)


@router.post("/responses/")
async def create_response(response: ResponseCreate):
    await survey_service_client.create_response(response)
    return JSONResponse(content="Response created", status_code=200)
