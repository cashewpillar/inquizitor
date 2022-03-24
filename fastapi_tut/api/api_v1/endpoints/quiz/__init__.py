from fastapi import APIRouter

from fastapi_tut.api.api_v1.endpoints.quiz import quiz

router = APIRouter()
router.include_router(quiz.router, tags=['quiz'])