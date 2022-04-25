from sqlmodel import Session
from typing import List

from inquizitor import crud
from inquizitor.crud.base import CRUDBase
from inquizitor.models import QuizAnswer, QuizAnswerCreate, QuizAnswerUpdate

class CRUDQuizAnswer(CRUDBase[QuizAnswer, QuizAnswerCreate, QuizAnswerUpdate]):
	def get_by_choice_and_user_ids(
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

	def get_all_by_quiz_and_student_ids(
		self,
		db: Session,
		*,
		quiz_id: int,
		student_id: int
	) -> List[QuizAnswer]:
		student = crud.user.get(db, id=student_id)
		return [answer for answer in student.answers if answer.choice.question.quiz_id == quiz_id]

quiz_answer = CRUDQuizAnswer(QuizAnswer)
