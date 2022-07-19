import logging
from sqlmodel import Session
from typing import Any, List, Tuple, Union

from fastapi import APIRouter, Depends, HTTPException

from inquizitor import crud, models
from inquizitor.api import deps

router = APIRouter()


@router.get("/{quiz_index}/finish", response_model=int)
async def finish_quiz(
    *,
    db: Session = Depends(deps.get_db),
    attempt: models.QuizAttempt = Depends(deps.get_attempt),
    current_student: models.User = Depends(deps.get_current_student)
) -> Any:
    """
    Finish the quiz and get the score for this attempt.
    """

    attempt_in = models.QuizAttemptUpdate(is_done=True)
    attempt = crud.quiz_attempt.update(db, db_obj=attempt, obj_in=attempt_in)

    return crud.quiz_attempt.get_score(db, id=attempt.id)


@router.put(
    "/{quiz_index}/questions/{question_id}/answer", response_model=models.QuizAnswer
)
async def update_answer(
    *,
    db: Session = Depends(deps.get_db),
    attempt_and_link: Tuple[models.QuizAttempt, models.QuizStudentLink] = Depends(
        deps.get_attempt_and_link
    ),
    question: models.QuizQuestion = Depends(deps.get_question),
    answer_in: Union[models.QuizAnswerCreate, models.QuizAnswerUpdate],
    current_student: models.User = Depends(deps.get_current_student)
) -> Any:
    """
    Update answer for the given question.
    """

    attempt = attempt_and_link[0]
    answer_in.attempt_id = attempt.id

    answer = crud.quiz_answer.get_by_question_and_attempt_ids(
        db, question_id=question.id, attempt_id=attempt.id
    )
    if answer:
        answer = crud.quiz_answer.update(db, db_obj=answer, obj_in=answer_in)
    else:
        answer = crud.quiz_answer.create(db, obj_in=answer_in)

    return answer


@router.get("/{quiz_index}/results", response_model=List[models.QuizReadWithQuestions])
async def get_quiz_results(
    *,
    db: Session = Depends(deps.get_db),
    quiz: models.Quiz = Depends(deps.get_quiz),
    current_author: models.User = Depends(deps.get_current_author)
) -> Any:
    """
    Get latest attempts of participants for this quiz
    """

    results = crud.quiz.get_multi_results_by_quiz_id(db, id=quiz.id)
    return results
