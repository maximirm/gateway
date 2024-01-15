from fastapi import FastAPI

from app.api import analysis_controller, user_controller, survey_controller

app = FastAPI()

app.include_router(analysis_controller.router, tags=["Analysis"])
app.include_router(user_controller.router, tags=["Users"])
app.include_router(survey_controller.router, tags=["Surveys"])
