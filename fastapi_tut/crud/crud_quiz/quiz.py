from sqlmodel import Session
from typing import List

from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import Quiz, QuizCreate, QuizUpdate

class CRUDQuiz(CRUDBase[Quiz, QuizCreate, QuizUpdate]):
	# Read methods:
	# 1. Search by name (teacher)
	def get_multi_by_name(self, db:Session, *, name: str) -> List[Quiz]:
		"""Search quiz by name attribute only. (not unique)"""
		return db.query(Quiz).filter(Quiz.name == name).all()

quiz = CRUDQuiz(Quiz)