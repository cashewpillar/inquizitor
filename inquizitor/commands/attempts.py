import click
import logging
import secrets
from typing import Optional, Union

from inquizitor import crud, models
from inquizitor.commands.initial_data import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.argument('email')
@click.argument('quiz_index')
def invalidate_attempt(email: str, quiz_index: Union[str, int]):
    """Manually nullify record for attempt that (1) had technical difficulties 
    by marking them as not done"""

    quiz = crud.quiz.get_by_index(db, quiz_index=quiz_index)
    student = crud.user.get_by_email(db, email=email)
    attempt = crud.quiz_attempt.get_latest_by_quiz_and_student_ids(
        db, quiz_id=quiz.id, student_id=student.id
    )
    attempt_in = models.QuizAttemptUpdate(is_done=False)
    crud.quiz_attempt.update(db, db_obj=attempt, obj_in=attempt_in)

    logger.info(f"Attempt by {email} for quiz {quiz.quiz_code} has been invalidated!")