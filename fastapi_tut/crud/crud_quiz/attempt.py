from sqlmodel import Session

from fastapi_tut import models
from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import QuizAttempt, QuizAttemptCreate, QuizAttemptUpdate

class CRUDQuizAttempt(CRUDBase[QuizAttempt, QuizAttemptCreate, QuizAttemptUpdate]):
	def get_by_quiz_and_user(
		self,
		db: Session,
		*,
		quiz: models.Quiz,
		user: models.User
	) -> QuizAttempt:
		return (
			db.query(QuizAttempt)
			.filter(QuizAttempt.quiz_id == quiz.id, QuizAttempt.student_id == user.id)
		)

	def create

quiz_attempt = CRUDQuizAttempt(QuizAttempt)
