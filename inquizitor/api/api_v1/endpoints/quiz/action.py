import logging
from pprint import pformat
from sqlmodel import Session
from typing import Any, Dict, List, Tuple, Union

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_jwt_auth import AuthJWT

from inquizitor import crud, models
from inquizitor.api import deps

router = APIRouter()

@router.post(
    "/{quiz_index}/questions/{question_id}/actions", 
    response_model=List[models.QuizAction]
)
async def create_actions(
    *,
    action_ins: List[models.QuizActionCreate],
    db: Session = Depends(deps.get_db),
    attempt: models.QuizAttempt = Depends(deps.get_attempt),
    question: models.QuizQuestion = Depends(deps.get_question),
) -> Any:
    """
    Store the current student's actions for the given attempt and quiz question.
    User is validated through get_attempt
    """

    actions = []
    for action_in in action_ins:
        action_in.attempt_id = attempt.id
        action_in.question_id = question.id

        action = crud.quiz_action.create(db, obj_in=action_in)
        actions.append(action)

    return actions

@router.get(
    "/{quiz_index}/questions/{question_id}/actions",
    response_model=Dict[Tuple[int, str], List[models.QuizAction]],
)
async def read_question_actions(
    *,
    db: Session = Depends(deps.get_db),
    quiz: models.Quiz = Depends(deps.get_quiz),
    question: models.QuizQuestion = Depends(deps.get_question),
    current_author: models.User = Depends(deps.get_current_author),
) -> Any:
    """
    Retrieve actions for the given quiz question.
    """

    question_actions = {}
    attempts = crud.quiz_attempt.get_multi_latest_by_quiz_id(db, quiz.id)
    for attempt in attempts:
        actions = crud.quiz_action.get_multi_by_question_attempt(
            db, question_id=question.id, attempt_id=attempt.id
        )
        student = crud.user.get(db, attempt.student_id)
        question_actions[(student.id, student.full_name)] = actions

    return question_actions

@router.get(
    "/{quiz_index}/actions",
    response_model=Dict[Tuple[int, str], List[models.QuizAction]],
)
async def read_quiz_actions(
    *,
    db: Session = Depends(deps.get_db),
    quiz: models.Quiz = Depends(deps.get_quiz),
    current_author: models.User = Depends(deps.get_current_author),
) -> Any:
    """
    Retrieve actions for the given quiz.
    """

    quiz_actions = {}
    attempts = crud.quiz_attempt.get_multi_latest_by_quiz_id(db, quiz.id)
    for attempt in attempts:
        actions = crud.quiz_action.get_multi_by_attempt(
            db, attempt_id=attempt.id
        )
        student = crud.user.get(db, attempt.student_id)
        quiz_actions[(student.id, student.full_name)] = actions

    return quiz_actions

@router.get(
    "/{quiz_index}/{student_id}/actions",
    response_model=List[models.QuizAction],
)
async def read_attempt_actions(
    *,
    db: Session = Depends(deps.get_db),
    quiz: models.Quiz = Depends(deps.get_quiz),
    current_author: models.User = Depends(deps.get_current_author),
) -> Any:
    """
    Retrieve student's actions for the given quiz.
    """

    attempt = crud.quiz_attempt.get_latest_by_quiz_and_student_ids(
        db, quiz_id=quiz.id, student_id=student_id
    )
    actions = crud.quiz_action.get_multi_by_attempt_order_by_question(
        db, attempt_id=attempt.id
    )

    return actions

@router.get(
    "/{quiz_index}/questions/{question_id}/{student_id}/actions",
    response_model=List[models.QuizAction],
)
async def read_attempt_question_actions(
    *,
    db: Session = Depends(deps.get_db),
    quiz: models.Quiz = Depends(deps.get_quiz),
    question: models.QuizQuestion = Depends(deps.get_question),
    current_author: models.User = Depends(deps.get_current_author),
) -> Any:
    """
    Retrieve student's actions for the given quiz question.
    """

    attempt = crud.quiz_attempt.get_latest_by_quiz_and_student_ids(
        db, quiz_id=quiz.id, student_id=student_id
    )
    actions = crud.quiz_action.get_multi_by_question_attempt(
        db, question_id=question.id, attempt_id=attempt.id
    )

    return actions