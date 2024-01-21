from uuid import UUID

from fastapi import APIRouter, Request, Depends
from starlette.responses import JSONResponse

from app.clients import survey_service_client
from app.clients.schemas.survey_schemas import Survey, SurveyCreate, QuestionCreate, ResponseCreate
from app.decorator.has_role import has_role, get_current_user_id

router = APIRouter()


@router.get("/surveys/all/", response_model=list[Survey])
async def get_all_surveys():
    return await survey_service_client.fetch_all_surveys()


@router.get("/surveys/{survey_id}/", response_model=Survey)
@has_role(["editor"])
async def get_survey(request: Request, survey_id: UUID):
    return await survey_service_client.fetch_survey(survey_id)


@router.get("/surveys/by_creator/{creator_id}/", response_model=list[Survey])
@has_role(["admin", "editor"])
async def get_surveys_by_creator_id(request: Request, creator_id: UUID):
    return await survey_service_client.fetch_surveys_by_creator_id(creator_id)


@router.delete("/surveys/by_creator/{creator_id}/", response_model=dict)
@has_role(["admin", "editor"])
async def delete_surveys_by_creator_id(request: Request, creator_id: UUID):
    await survey_service_client.delete_surveys_by_creator_id(creator_id)
    return JSONResponse(content=f"Surveys for creator-ID {str(creator_id)} deleted successfully", status_code=200)


@router.post("/surveys/", response_model=Survey)
@has_role(["editor"])
async def create_survey(request: Request, survey: SurveyCreate, user_id: str = Depends(get_current_user_id)):
    return await survey_service_client.create_survey(survey, user_id)


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


@router.delete("/questions/{question_id}/")
@has_role(["editor"])
async def delete_question(request: Request, question_id: UUID):
    await survey_service_client.delete_question(question_id)
    return JSONResponse(content="Question deleted", status_code=200)


@router.post("/responses/")
async def create_response(response: ResponseCreate):
    await survey_service_client.create_response(response)
    return JSONResponse(content="Response created", status_code=200)
