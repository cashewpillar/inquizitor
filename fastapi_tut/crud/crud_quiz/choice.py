from sqlmodel import Session

from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import QuizChoice, QuizChoiceCreate, QuizChoiceUpdate

class CRUDQuizChoice(CRUDBase[QuizChoice, QuizChoiceCreate, QuizChoiceUpdate]):
	pass

quiz_choice = CRUDQuizChoice(QuizChoice)