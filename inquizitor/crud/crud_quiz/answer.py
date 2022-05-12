import logging
from sqlmodel import Session
from typing import List

from inquizitor import crud
from inquizitor.crud.base import CRUDBase
from inquizitor.models import QuizAnswer, QuizAnswerCreate, QuizAnswerUpdate

class CRUDQuizAnswer(CRUDBase[QuizAnswer, QuizAnswerCreate, QuizAnswerUpdate]):
	def get_by_question_and_attempt_ids(
		self,
		db: Session,
		*,
		question_id: int,
		attempt_id: int
	) -> QuizAnswer:
		return (
			db.query(QuizAnswer)
			.filter(QuizAnswer.question_id == question_id, QuizAnswer.attempt_id == attempt_id)
			.first()
		)

	def get_all_by_attempt(
		self,
		db: Session,
		*,
		attempt_id: int
	) -> List[QuizAnswer]:
		attempt = crud.quiz_attempt.get(db, id=attempt_id)
		student = crud.user.get(db, id=attempt.student_id)

		# logging.info(f"A{attempt.id}S{student.id} ANS: {[answer for answer in student.answers if answer.attempt_id == attempt.id]}")
		return [answer for answer in student.answers if answer.attempt_id == attempt.id]

quiz_answer = CRUDQuizAnswer(QuizAnswer)
