from fastapi import APIRouter

from fastapi_tut.api.api_v1.endpoints import quiz, login

api_router = APIRouter()
api_router.include_router(login.router)
# api_router.include_router(quiz.router)