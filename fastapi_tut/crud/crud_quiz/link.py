from sqlmodel import Session

from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import QuizStudentLink, QuizStudentLinkCreate, QuizStudentLinkUpdate

class CRUDQuizStudentLink(CRUDBase[QuizStudentLink, QuizStudentLinkCreate, QuizStudentLinkUpdate]):
	pass

quiz_student_link = CRUDQuizStudentLink(QuizStudentLink)