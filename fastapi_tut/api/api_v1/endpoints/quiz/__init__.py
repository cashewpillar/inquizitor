from fastapi import APIRouter

from fastapi_tut.api.api_v1.endpoints.quiz import choice, quiz, question

router = APIRouter()
router.include_router(choice.router, tags=['choice'])
router.include_router(quiz.router, tags=['quiz'])
router.include_router(question.router, tags=['question'])