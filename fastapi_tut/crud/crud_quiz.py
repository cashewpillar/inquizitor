from sqlmodel import Session

from typing import Dict, Any, Optional, Union

from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import (
	Quiz, 
	QuizCreate, 
	QuizUpdate,
	QuestionType, 
	QuestionTypeCreate, 
	QuestionTypeUpdate,
	Question, 
	QuestionCreate, 
	QuestionUpdate,
)

class CRUDQuiz(CRUDBase[Quiz, QuizCreate, QuizUpdate]):
	def create(self, db: Session, *, obj_in: QuizCreate) -> Quiz:
		# retained explicit assignment courtesy of https://www.python.org/dev/peps/pep-0020/#id2
		db_obj = Quiz(
				name=obj_in.name,
				desc=obj_in.desc,
				number_of_questions=obj_in.number_of_questions,
				time=obj_in.time
				)
		return super().create(db, obj_in=db_obj)

	def update(
		self, db: Session, *, db_obj: Quiz, obj_in: Union[QuizUpdate, Dict[str, Any]]
	) -> Quiz:
		if isinstance(obj_in, dict):
			update_data = obj_in
		else:
			update_data = obj_in.dict(exclude_unset=True)

		return super().update(db, db_obj=db_obj, obj_in=update_data)


class CRUDQuestionType(CRUDBase[QuestionType, QuestionTypeCreate, QuestionTypeUpdate]):
	# get_questions() - skipped since will not be using

	def create(self, db: Session, *, obj_in: QuestionTypeCreate) -> QuestionType:
		db_obj = QuestionType(
				name=obj_in.name
				)
		return super().create(db, obj_in=db_obj)


	def update(
		self, db: Session, *, db_obj: QuestionType, obj_in: Union[QuestionTypeUpdate, Dict[str, Any]]
	) -> QuestionType:
		if isinstance(obj_in, dict):
			update_data = obj_in
		else:
			update_data = obj_in.dict(exclude_unset=True)

		return super().update(db, db_obj=db_obj, obj_in=update_data)


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
	def create(self, db: Session, *, obj_in: QuestionCreate) -> Question:
		db_obj = Question(
				content=obj_in.content,
				quiz_id=obj_in.quiz_id,
				question_type_id=obj_in.question_type_id,
				)
		return super().create(db, obj_in=db_obj)


	def update(
		self, db: Session, *, db_obj: Question, obj_in: Union[QuestionUpdate, Dict[str, Any]]
	) -> Question:
		if isinstance(obj_in, dict):
			update_data = obj_in
		else:
			update_data = obj_in.dict(exclude_unset=True)

		return super().update(db, db_obj=db_obj, obj_in=update_data)


question_type = CRUDQuestionType(QuestionType)
question = CRUDQuestion(Question)
quiz = CRUDQuiz(Quiz)