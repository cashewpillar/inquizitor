from sqlmodel import Session
from typing import List, Union

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

	def get_by_index(
		self, db: Session, quiz_index: Union[int, str]
	) -> Quiz:
		"""Read quiz by quiz_code or int"""
		if isinstance(quiz_index, str):
			quiz = self.get_by_code(db, code=quiz_index)
		else:
			quiz = self.get(db, id=quiz_index)
		return quiz

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

	def has_question(self, db: Session, quiz_index: Union[int, str], question_id: int):
		"""Verify if question belongs to the quiz"""
		quiz = self.get_by_index(db, quiz_index)
		question_ids = [question.id for question in quiz.questions]
		return question_id in question_ids

	def is_author(self, db: Session, user_id: int, quiz_index: Union[int, str]):
		quiz = self.get_by_index(db, quiz_index)
		return quiz.teacher_id == user_id

quiz = CRUDQuiz(Quiz)