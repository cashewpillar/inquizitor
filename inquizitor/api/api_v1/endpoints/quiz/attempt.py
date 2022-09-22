from sqlmodel import Session
from typing import Any, List

from fastapi import APIRouter, Depends

from inquizitor import crud, models
from inquizitor.api import deps

router = APIRouter()

@router.get(
    "/{quiz_index}/attempt",
    response_model=models.QuizAttempt,
)
async def get_attempt(
    *,
    db: Session = Depends(deps.get_db),
    quiz: models.Quiz = Depends(deps.get_quiz),
    current_student: models.User = Depends(deps.get_current_student),
) -> Any:
    """
    Retrieve student's latest attempt for the given quiz.
    """

    attempt = crud.quiz_attempt.get_latest_by_quiz_and_student_ids(
        db, quiz_id=quiz.id, student_id=current_student.id
    )

    return attempt