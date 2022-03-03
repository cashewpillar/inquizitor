from sqlmodel import Session

from typing import Dict, Any, Optional, Union

from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models.quiz import Quiz, QuizCreate, QuizUpdate

class CRUDQuiz(CRUDBase[Quiz, QuizCreate, QuizUpdate]):
	def create(self, db: Session, *, obj_in: QuizCreate) -> Quiz:
		db_obj = Quiz(
				name=obj_in.name,
				desc=obj_in.desc,
				number_of_questions=obj_in.number_of_questions,
				time=obj_in.time
				)
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj


	def update(
		self, db: Session, *, db_obj: Quiz, obj_in: Union[QuizUpdate, Dict[str, Any]]
	) -> Quiz:
		if isinstance(obj_in, dict):
			update_data = obj_in
		else:
			update_data = obj_in.dict(exclude_unset=True)

		if update_data["password"]:
			hashed_password = get_password_hash(update_data["password"])
			del update_data["password"]
			update_data["hashed_password"] = hashed_password
		return super().update(db, db_obj=db_obj, obj_in=update_data)


quiz = CRUDQuiz(Quiz)