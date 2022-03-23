from sqlmodel import Session

from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import Quiz, QuizCreate, QuizUpdate

class CRUDQuiz(CRUDBase[Quiz, QuizCreate, QuizUpdate]):
	pass
	
quiz = CRUDQuiz(Quiz)