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

    def get_multi_by_quiz_order_by_student(
        self, db: Session, *, quiz_id: int
    ) -> List[QuizAction]:
        """Get quiz actions, order by student"""
        return (
            db.query(QuizAction)
            .join(QuizAttempt)
            .filter(QuizAttempt.quiz_id == quiz_id)
            .order_by(QuizAttempt.student_id)
            .all()
        )

    def get_multi_by_attempt_order_by_question(
        self, db: Session, *, attempt_id: int
    ) -> List[QuizAction]:
        """Get quiz actions for the given student attempt, order by question"""
        return (
            db.query(QuizAction)
            .filter(QuizAction.attempt_id == attempt_id)
            .order_by(QuizAction.question_id)
            .all()
        )

    def get_per_student_summary_by_quiz(
        self, db: Session, *, quiz_id: int
    ) -> Any:
        """Get per-student summary of actions for the given quiz"""
        summary = dict()
        actions = (
            db.query(QuizAction)
            .join(QuizAttempt)
            .filter(QuizAttempt.quiz_id == quiz_id)
            .order_by(QuizAttempt.student_id)
            .all()
        )
        action_list = {
            'blur': 0,
            'focus': 0,
            'copy_': 0,
            'paste': 0,
            'left_click': 0,
            'right_click': 0,
            'double_click': 0,
        }
        for action in actions:
            student_name = action.attempt.student.username
            summary.setdefault(student_name, dict(action_list))
            summary[student_name]['blur'] += action.blur
            summary[student_name]['focus'] += action.focus
            summary[student_name]['copy_'] += action.copy_
            summary[student_name]['paste'] += action.paste
            summary[student_name]['left_click'] += action.left_click
            summary[student_name]['right_click'] += action.right_click
            summary[student_name]['double_click'] += action.double_click

        return summary

quiz_action = CRUDQuizAction(QuizAction)
