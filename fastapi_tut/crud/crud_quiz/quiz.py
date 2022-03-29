from sqlmodel import Session
from typing import List

from fastapi.encoders import jsonable_encoder

from fastapi_tut import crud, models
from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import Quiz, QuizCreate, QuizUpdate

class CRUDQuiz(CRUDBase[Quiz, QuizCreate, QuizUpdate]):
	def get_by_code(
		self, db: Session, code: str
	) -> Quiz:
		"""Read quiz by quiz_code"""
		return db.query(Quiz).filter(Quiz.quiz_code == code).first()

	def get_multi_by_name(
		self, db:Session, *, name: str, skip: int = 0, limit: int = 100
	) -> List[Quiz]:
		"""Read quiz by name attribute only. (not unique)"""
		return (
			db.query(Quiz)
			.filter(Quiz.name == name)
			.offset(skip)
			.limit(limit)
			.all()
		)

	# NOTE might need query with offset and limit here
	def get_multi_by_participant(
		self, db:Session, *, student: models.User
		# self, db:Session, *, student: models.User, skip: int = 0, limit: int = 100
	) -> List[Quiz]:
		"""Read quizzes participated by the student."""
		return [jsonable_encoder(crud.quiz.get(db, id=link.quiz_id)) for link in student.student_quizzes]

	def get_multi_by_author(
		self, db:Session, *, teacher_id: int, skip: int = 0, limit: int = 100
	) -> List[Quiz]:
		"""Read quizzes participated by the student."""
		return (
			db.query(Quiz)
			.filter(Quiz.teacher_id == teacher_id)
			.offset(skip)
			.limit(limit)
			.all()
		)

quiz = CRUDQuiz(Quiz)