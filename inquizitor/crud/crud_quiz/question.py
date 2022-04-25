from sqlmodel import Session

from inquizitor.crud.base import CRUDBase
from inquizitor.models import QuizQuestion, QuizQuestionCreate, QuizQuestionUpdate

class CRUDQuizQuestion(CRUDBase[QuizQuestion, QuizQuestionCreate, QuizQuestionUpdate]):
	def has_choice(self, db: Session, question_id: int, choice_id: int):
		"""Verify if choice belongs to the question"""
		question = self.get(db, question_id)
		choice_ids = [choice.id for choice in question.choices]
		return choice_id in choice_ids

quiz_question = CRUDQuizQuestion(QuizQuestion)
