from sqlmodel import Session

from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import QuizAnswer, QuizAnswerCreate, QuizAnswerUpdate

class CRUDQuizAnswer(CRUDBase[QuizAnswer, QuizAnswerCreate, QuizAnswerUpdate]):
	pass

quiz_answer = CRUDQuizAnswer(QuizAnswer)
