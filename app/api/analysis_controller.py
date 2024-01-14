from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.clients.exceptions.no_responses_exception import NoResponsesException
from app.clients.exceptions.question_not_found_exception import QuestionNotFoundException
from app.clients.exceptions.wrong_question_type_exception import WrongQuestionTypeException
from app.clients.schemas import schemas


from app.services import gateway_service

router = APIRouter()


@router.get("/analyze/question/{question_id}", response_model=schemas.QuestionAnalyzed)
async def analyze_question(question_id: UUID):
    try:
        return await gateway_service.get_analyzed_question(question_id)
    except WrongQuestionTypeException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NoResponsesException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except QuestionNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))



