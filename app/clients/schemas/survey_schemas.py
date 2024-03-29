from typing import Optional, List

from pydantic import BaseModel, UUID4


class ResponseCreate(BaseModel):
    question_id: UUID4
    respondent_id: Optional[UUID4] = None
    response_text: List[str]


class Response(ResponseCreate):
    id: UUID4


class QuestionCreate(BaseModel):
    survey_id: UUID4
    order: int
    question_text: str
    type: int
    options: Optional[List[str]] = None


class Question(QuestionCreate):
    id: UUID4
    responses: list[Response] = []


class AnalyzedQuestion(Question):
    analysis_responses: Optional[dict] = None
    analysis_respondents: Optional[dict] = None


class SurveyCreate(BaseModel):
    creator_id: UUID4
    title: str
    description: str
    is_public: bool


class Survey(SurveyCreate):
    id: UUID4
    questions: list[Question] = []


class AnalyzedSurvey(SurveyCreate):
    id: UUID4
    analyzed_questions: list[AnalyzedQuestion] = []
