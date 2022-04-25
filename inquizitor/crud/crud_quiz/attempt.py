from sqlmodel import Session

from inquizitor import crud, models
from inquizitor.crud.base import CRUDBase
from inquizitor.models import QuizAttempt, QuizAttemptCreate, QuizAttemptUpdate

class CRUDQuizAttempt(CRUDBase[QuizAttempt, QuizAttemptCreate, QuizAttemptUpdate]):
	def get_by_quiz_and_student_ids(
		self,
		db: Session,
		*,
		quiz_id: int,
		student_id: int
	) -> QuizAttempt:
		return (
			db.query(QuizAttempt)
			.filter(QuizAttempt.quiz_id == quiz_id, QuizAttempt.student_id == student_id)
			.first()
		)

	def get_score(
		self,
		db: Session, 
		*,
		quiz_id: int,
		student_id: int
	) -> int:
		score = 0
		answers = crud.quiz_answer.get_all_by_quiz_and_student_ids(
			db, quiz_id=quiz_id, student_id=student_id 
		)
		for answer in answers:
			choice = crud.quiz_choice.get(db, id=answer.choice_id)
			answer_in = models.QuizAnswerUpdate(is_correct=choice.is_correct)
			answer = crud.quiz_answer.update(db, db_obj=answer, obj_in=answer_in)
			if answer.is_correct:
				score += 1

		return score

quiz_attempt = CRUDQuizAttempt(QuizAttempt)
