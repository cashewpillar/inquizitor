from sqlmodel import Session

from inquizitor.crud.base import CRUDBase
from inquizitor.models import QuizStudentLink, QuizStudentLinkCreate, QuizStudentLinkUpdate

class CRUDQuizStudentLink(CRUDBase[QuizStudentLink, QuizStudentLinkCreate, QuizStudentLinkUpdate]):
	pass

quiz_student_link = CRUDQuizStudentLink(QuizStudentLink)