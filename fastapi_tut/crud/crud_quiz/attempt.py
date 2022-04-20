from sqlmodel import Session

from fastapi_tut import models
from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import QuizAttempt, QuizAttemptCreate, QuizAttemptUpdate

class CRUDQuizAttempt(CRUDBase[QuizAttempt, QuizAttemptCreate, QuizAttemptUpdate]):
	def get_by_quiz_and_user(
		self,
		db: Session,
		*,
		quiz_id: int,
		user_id: int
	) -> QuizAttempt:
		return (
			db.query(QuizAttempt)
			.filter(QuizAttempt.quiz_id == quiz_id, QuizAttempt.student_id == user_id)
		)

	# DOING
	# def get_score(
	# 	self,
	# 	db: Session, 
	# 	*,
	# 	quiz_id: int,
	# 	user_id: int
	# ) -> int:
	# 	score = 0
		# get answers of user for that quiz
quiz_attempt = CRUDQuizAttempt(QuizAttempt)
