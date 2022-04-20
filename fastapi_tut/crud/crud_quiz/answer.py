from sqlmodel import Session

from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import QuizAnswer, QuizAnswerCreate, QuizAnswerUpdate

class CRUDQuizAnswer(CRUDBase[QuizAnswer, QuizAnswerCreate, QuizAnswerUpdate]):
	def get_by_choice_and_user(
		self,
		db: Session,
		*,
		choice_id: int,
		student_id: int
	) -> QuizAnswer:
		return (
			db.query(QuizAnswer)
			.filter(QuizAnswer.choice_id == choice_id, QuizAnswer.student_id == student_id)
			.first()
		)

quiz_answer = CRUDQuizAnswer(QuizAnswer)
