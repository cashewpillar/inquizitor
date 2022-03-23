from sqlmodel import Session

from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import QuizAttempt, QuizAttemptCreate, QuizAttemptUpdate

class CRUDQuizAttempt(CRUDBase[QuizAttempt, QuizAttemptCreate, QuizAttemptUpdate]):
	pass

quiz_attempt = CRUDQuizAttempt(QuizAttempt)
