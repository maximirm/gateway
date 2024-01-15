from typing import Optional, List

from pydantic import BaseModel, UUID4


class Response(BaseModel):
    id: UUID4
    question_id: UUID4
    respondent_id: Optional[UUID4] = None
    response_text: List[str]


class Question(BaseModel):
    id: UUID4
    survey_id: UUID4
    order: int
    question_text: str
    type: int
    options: Optional[List[str]] = None
    responses: list[Response] = []


class QuestionAnalyzed(Question):
    analysis_responses: Optional[dict] = None
    analysis_respondents: Optional[dict] = None


class SurveyCreate(BaseModel):
    creator_id: UUID4
    title: str
    description: str


class Survey(SurveyCreate):
    id: UUID4
    questions: list[Question] = []
