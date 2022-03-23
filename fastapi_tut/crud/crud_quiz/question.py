from sqlmodel import Session

from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import QuizQuestion, QuizQuestionCreate, QuizQuestionUpdate

class CRUDQuizQuestion(CRUDBase[QuizQuestion, QuizQuestionCreate, QuizQuestionUpdate]):
	pass

quiz_question = CRUDQuizQuestion(QuizQuestion)
