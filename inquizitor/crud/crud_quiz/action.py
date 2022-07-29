from typing import Any, Dict, List, Union
from sqlmodel import Session
from inquizitor.crud.base import CRUDBase
from inquizitor.models import QuizAction, QuizActionCreate, QuizActionUpdate

class CRUDQuizAction(CRUDBase[QuizAction, QuizActionCreate, QuizActionUpdate]):
    def update(self, db: Session, *, db_obj: QuizAction, obj_in: Union[QuizActionUpdate, Dict[str, Any]]) -> None:
        raise Exception('QuizAction does not allow updating of records')

    def get_multi_by_student_question_attempt(
        self, db: Session, *, student_id: int, question_id: int, attempt_id: int
    ) -> List[QuizAction]:
        return (
            db.query(QuizAction)
            .filter(
                QuizAction.student_id == student_id,
                QuizAction.question_id == question_id,
                QuizAction.attempt_id == attempt_id
            )
            .all()
        )

    def get_multi_by_student_quiz_attempt(
        self, db: Session, *, student_id: int, quiz_id: int, attempt_id: int
    ) -> List[QuizAction]:
        return (
            db.query(QuizAction)
            .filter(
                QuizAction.student_id == student_id,
                QuizAction.quiz_id == quiz_id,
                QuizAction.attempt_id == attempt_id
            )
            .all()
        )

    def get_multi_by_question_attempt(
        self, db: Session, *, question_id: int, attempt_id: int
    ) -> List[QuizAction]:
        return (
            db.query(QuizAction)
            .filter(
                QuizAction.question_id == question_id,
                QuizAction.attempt_id == attempt_id
            )
            .all()
        )

    def get_multi_by_question_attempt(
        self, db: Session, *, question_id: int, attempt_id: int
    ) -> List[QuizAction]:
        return (
            db.query(QuizAction)
            .filter(
                QuizAction.question_id == question_id,
                QuizAction.attempt_id == attempt_id
            )
            .all()
        )

    def get_multi_by_question(
        self, db: Session, *, question_id: int
    ) -> List[QuizAction]:
        return (
            db.query(QuizAction)
            .filter(
                QuizAction.question_id == question_id,
            )
            .all()
        )

    def get_multi_by_quiz_attempt(
        self, db: Session, *, quiz_id: int, attempt_id: int
    ) -> List[QuizAction]:
        return (
            db.query(QuizAction)
            .filter(
                QuizAction.quiz_id == quiz_id,
                QuizAction.attempt_id == attempt_id
            )
            .all()
        )

    def get_multi_by_quiz(
        self, db: Session, *, quiz_id: int
    ) -> List[QuizAction]:
        return (
            db.query(QuizAction)
            .filter(
                QuizAction.quiz_id == quiz_id,
            )
            .all()
        )

    def get_multi_by_student(
        self, db: Session, *, student_id: int
    ) -> List[QuizAction]:
        return (
            db.query(QuizAction)
            .filter(
                QuizAction.student_id == student_id,
            )
            .all()
        )

quiz_action = CRUDQuizAction(QuizAction)
