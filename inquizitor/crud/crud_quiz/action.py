from typing import Any, Dict, List, Union
from sqlmodel import Session
from inquizitor.crud.base import CRUDBase
from inquizitor.models import QuizAttempt, QuizAction, QuizActionCreate, QuizActionUpdate

class CRUDQuizAction(CRUDBase[QuizAction, QuizActionCreate, QuizActionUpdate]):
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

    def get_per_question_summary_by_attempt(
        self, db: Session, *, attempt_id: int
    ) -> Any:
        """Get per-question summary of actions for the given attempt"""
        summary = dict()
        actions = (
            db.query(QuizAction)
            .filter(QuizAction.attempt_id == attempt_id)
            .order_by(QuizAction.question_id)
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
            question_id = action.question_id
            summary.setdefault(question_id, dict(action_list))
            summary[question_id]['blur'] += action.blur
            summary[question_id]['focus'] += action.focus
            summary[question_id]['copy_'] += action.copy_
            summary[question_id]['paste'] += action.paste
            summary[question_id]['left_click'] += action.left_click
            summary[question_id]['right_click'] += action.right_click
            summary[question_id]['double_click'] += action.double_click

        return summary

quiz_action = CRUDQuizAction(QuizAction)
