from sqlmodel import Session
from typing import List

from fastapi_tut.crud.base import CRUDBase
from fastapi_tut.models import QuizChoice, QuizChoiceCreate, QuizChoiceUpdate

class CRUDQuizChoice(CRUDBase[QuizChoice, QuizChoiceCreate, QuizChoiceUpdate]):
	def get_multi_by_question(
		self, db: Session, *, question_id: int, skip: int = 0, limit: int = 100,
	) -> List[QuizChoice]:
		return (
			db.query(self.model)
            .filter(QuizChoice.question_id == question_id)
            .offset(skip)
            .limit(limit)
            .all()
		)

quiz_choice = CRUDQuizChoice(QuizChoice)