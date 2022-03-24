from sqlmodel import Session
from typing import List

from fastapi.encoders import jsonable_encoder

from fastapi_tut import models
from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import Quiz, QuizCreate, QuizUpdate

class CRUDQuiz(CRUDBase[Quiz, QuizCreate, QuizUpdate]):
	# Read methods:
	# 1. Search by name (teacher)
	def get_multi_by_name(self, db:Session, *, name: str) -> List[Quiz]:
		"""Search quiz by name attribute only. (not unique)"""
		return db.query(Quiz).filter(Quiz.name == name).all()

	def get_multi_by_participant(self, db:Session, *, participant: models.User) -> List[Quiz]:
		"""Search quizzes participated by the student."""
		return [jsonable_encoder(quiz) for quiz in participant.student_quizzes]

quiz = CRUDQuiz(Quiz)