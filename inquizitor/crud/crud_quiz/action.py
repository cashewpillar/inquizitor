from typing import Any, Dict, Union
from sqlmodel import Session
from inquizitor.crud.base import CRUDBase
from inquizitor.models import QuizAction, QuizActionCreate, QuizActionUpdate

class CRUDQuizAction(CRUDBase[QuizAction, QuizActionCreate, QuizActionUpdate]):
    def update(self, db: Session, *, db_obj: QuizAction, obj_in: Union[QuizActionUpdate, Dict[str, Any]]) -> None:
        raise Exception('QuizAction does not allow updating of records')

quiz_action = CRUDQuizAction(QuizAction)
