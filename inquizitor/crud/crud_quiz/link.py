from sqlmodel import Session

from inquizitor.crud.base import CRUDBase
from inquizitor.models import QuizStudentLink, QuizStudentLinkCreate, QuizStudentLinkUpdate

class CRUDQuizStudentLink(CRUDBase[QuizStudentLink, QuizStudentLinkCreate, QuizStudentLinkUpdate]):
	def get_by_quiz_and_student_ids(
		self,
		db: Session,
		*,
		quiz_id: int,
		student_id: int
	) -> QuizStudentLink:
		return (
			db.query(QuizStudentLink)
			.filter(QuizStudentLink.quiz_id == quiz_id, QuizStudentLink.student_id == student_id)
			.first()
		)

quiz_student_link = CRUDQuizStudentLink(QuizStudentLink)