from typing import Any, Dict, List, Union
from sqlmodel import Session
from inquizitor.crud.base import CRUDBase
from inquizitor.models import QuizAttempt, QuizAction, QuizActionCreate, QuizActionUpdate

class CRUDQuizAction(CRUDBase[QuizAction, QuizActionCreate, QuizActionUpdate]):
    """
    Reporting Scenarios:
    - [ ] Reports > Quiz > Aggregate Latest Attempt Actions By Student
    - [ ] Reports > Quiz > Aggregate Student's Latest Attempt Actions By Question
    Detection Scenarios:
    - [x] Attempt Log == get_multi_by_attempt
    - [x] Attempt's Question Log == get_multi_by_question_attempt
    """

    def update(self, db: Session, *, db_obj: QuizAction, obj_in: Union[QuizActionUpdate, Dict[str, Any]]) -> None:
        raise Exception('QuizAction does not allow updating of records')

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

    def get_multi_by_attempt(
        self, db: Session, *, attempt_id: int
    ) -> List[QuizAction]:
        return (
            db.query(QuizAction)
            .filter(QuizAction.attempt_id == attempt_id)
            .all()
        )

    def get_multi_by_question(
        self, db: Session, *, question_id: int
    ) -> List[QuizAction]:
        return (
            db.query(QuizAction)
            .filter(QuizAction.question_id == question_id)
            .all()
        )

    # DOING: do the aggregate part
    def get_multi_by_quiz_order_by_student(
        self, db: Session, *, quiz_id: int
    ) -> List[QuizAction]:
        """Get aggregated quiz actions per student"""
        return (
            db.query(QuizAction)
            .join(QuizAttempt)
            .filter(QuizAttempt.quiz_id == quiz_id)
            .order_by(QuizAttempt.student_id)
            .all()
        )

quiz_action = CRUDQuizAction(QuizAction)
