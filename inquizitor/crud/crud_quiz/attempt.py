import logging
from pprint import pformat
from sqlmodel import Session
from typing import List

from inquizitor import crud, models
from inquizitor.crud.base import CRUDBase
from inquizitor.models import QuizAttempt, QuizAttemptCreate, QuizAttemptUpdate


class CRUDQuizAttempt(CRUDBase[QuizAttempt, QuizAttemptCreate, QuizAttemptUpdate]):
    def get_latest_by_quiz_and_student_ids(
        self, db: Session, *, quiz_id: int, student_id: int
    ) -> QuizAttempt:
        """Read latest attempt of student for the given quiz"""

        return (
            db.query(QuizAttempt)
            .filter(
                QuizAttempt.quiz_id == quiz_id, QuizAttempt.student_id == student_id
            )
            # NOTE cant make ordering by date to work YET, maybe should stringify but ehh
            # all methods prepended w/ `get_latest` currently use ID instead of STARTED at
            .order_by(QuizAttempt.id.desc())
            .first()
        )

    def get_multi_by_quiz_and_student_ids(
        self, db: Session, *, quiz_id: int, student_id: int
    ) -> List[QuizAttempt]:
        """Read all attempts of student for the given quiz"""

        return (
            db.query(QuizAttempt)
            .filter(
                QuizAttempt.quiz_id == quiz_id, QuizAttempt.student_id == student_id
            )
            .order_by(QuizAttempt.id.desc())
            .all()
        )

    def get_multi_latest_by_student_id(
        self, db: Session, *, student_id: int
    ) -> List[QuizAttempt]:
        """Read all latest attempts of student for all quizzes taken"""
        unique_attempts = []
        attempts = (
            db.query(QuizAttempt)
            .filter(QuizAttempt.student_id == student_id)
            .order_by(QuizAttempt.id.desc())
            .all()
        )
        unique_quiz_ids = [attempt.quiz_id for attempt in unique_attempts]
        for attempt in attempts:
            if attempt.quiz_id not in unique_quiz_ids:
                unique_attempts.append(attempt)

        return unique_attempts

    def get_multi_latest_by_quiz_id(self, db: Session, *, id: int) -> List[QuizAttempt]:
        """Read all latest student attempts on a given quiz"""
        unique_attempts = []
        attempts = (
            db.query(QuizAttempt)
            .filter(QuizAttempt.quiz_id == id)
            .order_by(QuizAttempt.id.desc())
            .all()
        )
        unique_student_ids = [attempt.student_id for attempt in unique_attempts]
        for attempt in attempts:
            if attempt.student_id not in unique_student_ids:
                unique_attempts.append(attempt)

        return unique_attempts

    def get_score(self, db: Session, *, id: int) -> int:
        """Compute the score for the given attempt ID."""
        attempt = crud.quiz_attempt.get(db, id=id)

        score = 0
        answers = crud.quiz_answer.get_all_by_attempt(db, attempt_id=attempt.id)
        for answer in answers:
            choice = crud.quiz_choice.get(db, id=answer.choice_id)
            question = crud.quiz_question.get(db, id=choice.question_id)
            answer_in = models.QuizAnswerUpdate(is_correct=choice.is_correct)
            answer = crud.quiz_answer.update(db, db_obj=answer, obj_in=answer_in)
            if answer.is_correct:
                score += question.points

        return score


quiz_attempt = CRUDQuizAttempt(QuizAttempt)
