from fastapi import FastAPI

from app.api import analysis_controller, user_controller, survey_controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Erlaubt alle Methoden (GET, POST, etc.)
    allow_headers=["*"],  # Erlaubt alle Header
)

app.include_router(analysis_controller.router, tags=["Analysis"])
app.include_router(user_controller.router, tags=["Users"])
app.include_router(survey_controller.router, tags=["Surveys"])
