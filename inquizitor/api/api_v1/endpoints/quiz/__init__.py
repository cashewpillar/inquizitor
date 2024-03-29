from fastapi import APIRouter

from inquizitor.api.api_v1.endpoints.quiz import answer, choice, quiz, question, action, attempt

router = APIRouter()
router.include_router(answer.router, tags=["answer"])
router.include_router(choice.router, tags=["choice"])
router.include_router(quiz.router, tags=["quiz"])
router.include_router(question.router, tags=["question"])
router.include_router(action.router, tags=["action"])
router.include_router(attempt.router, tags=["action"])
