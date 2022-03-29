from fastapi import APIRouter

from fastapi_tut.api.api_v1.endpoints.quiz import quiz, question

router = APIRouter()
router.include_router(quiz.router, tags=['quiz'])
router.include_router(question.router, prefix='/questions', tags=['question'])