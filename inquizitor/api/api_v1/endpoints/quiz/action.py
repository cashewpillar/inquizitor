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
    response_model=models.QuizAction
)
async def create_action(
    *,
    action_in: models.QuizActionCreate,
    db: Session = Depends(deps.get_db),
    attempt: models.QuizAttempt = Depends(deps.get_attempt),
    question: models.QuizQuestion = Depends(deps.get_question),
) -> Any:
    """
    Store the current student's action for the given attempt and quiz question.
    User is validated through get_attempt (see api/deps.py)
    """

    action_in.attempt_id = attempt.id
    action_in.question_id = question.id

    action = crud.quiz_action.create(db, obj_in=action_in)

    return action

@router.get(
    "/{quiz_index}/questions/{question_id}/actions",
    response_model=List[models.QuizActions],
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

    question_actions = []
    attempts = crud.quiz_attempt.get_multi_latest_by_quiz_id(db, id=quiz.id)
    for attempt in attempts:
        actions = crud.quiz_action.get_multi_by_question_attempt(
            db, question_id=question.id, attempt_id=attempt.id
        )
        student = crud.user.get(db, attempt.student_id)
        question_actions.append(models.QuizActions(
            student_id=student.id, student_name=student.full_name, actions=actions
        ))

    return question_actions

@router.get(
    "/{quiz_index}/actions",
    response_model=List[models.QuizActions],
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

    quiz_actions = []
    attempts = crud.quiz_attempt.get_multi_latest_by_quiz_id(db, id=quiz.id)
    for attempt in attempts:
        actions = crud.quiz_action.get_multi_by_attempt(
            db, attempt_id=attempt.id
        )
        student = crud.user.get(db, attempt.student_id)
        quiz_actions.append(models.QuizActions(
            student_id=student.id, student_name=student.full_name, actions=actions
        ))

    return quiz_actions

@router.get(
    "/{quiz_index}/{student_id}/actions",
    response_model=List[models.QuizAction],
)
async def read_attempt_actions(
    *,
    db: Session = Depends(deps.get_db),
    quiz: models.Quiz = Depends(deps.get_quiz),
    student_id: int,
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
    student_id: int,
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

@router.get(
    "/{quiz_index}/{student_id}/actions-per-question",
    response_model=Dict[int, Dict],
)
async def read_per_question_attempt_actions(
    *,
    db: Session = Depends(deps.get_db),
    quiz: models.Quiz = Depends(deps.get_quiz),
    student_id: int,
    current_author: models.User = Depends(deps.get_current_author),
) -> Any:
    """
    Retrieve student's actions for the given quiz, aggregated per question
    """

    attempt = crud.quiz_attempt.get_latest_by_quiz_and_student_ids(
        db, quiz_id=quiz.id, student_id=student_id
    )
    actions = crud.quiz_action.get_per_question_summary_by_attempt(
        db, attempt_id=attempt.id
    )

    return actions

@router.get(
    "/{quiz_index}/actions-per-question",
    response_model=Dict[int, Dict],
)
async def read_per_question_attempts_actions(
    *,
    db: Session = Depends(deps.get_db),
    quiz: models.Quiz = Depends(deps.get_quiz),
    current_author: models.User = Depends(deps.get_current_author),
) -> Any:
    """
    Retrieve all the students' aggregated actions (per question) for the given quiz

    {student_id: dict_student_action_aggregate_per_question}
    """

    attempts_with_actions = dict()
    attempts = crud.quiz_attempt.get_multi_latest_by_quiz_id(
        db, id=quiz.id
    )
    total_points = crud.quiz.get_total_points(db, id=quiz.id)
    for attempt in attempts:
        student_actions = crud.quiz_action.get_per_question_summary_by_attempt(
            db, attempt_id=attempt.id, get_predictions=True
        )
        score = crud.quiz_attempt.get_score(db, id=attempt.id)
        student = crud.user.get(db, attempt.student_id)
        record = {
            'student_name': student.full_name,
            'username': student.username,
            'score': f"{score}/{total_points}",
            'actions': student_actions
        }
        attempts_with_actions.setdefault(student.id, record)

    return attempts_with_actions

@router.get(
    "/{quiz_index}/actions-per-question/filter-by-cheating",
    response_model=Dict[str, Dict[int, Dict[int, Dict]]],
)
async def read_per_question_attempts_actions_filter_by_cheating(
    *,
    db: Session = Depends(deps.get_db),
    quiz: models.Quiz = Depends(deps.get_quiz),
    current_author: models.User = Depends(deps.get_current_author),
) -> Any:
    """
    Retrieve all the students' aggregated actions (per question) for the given quiz,
    filtered by cheating status, for dataset creation purposes

    {
        'is_cheater_dataset': {student_id: dict_student_action_aggregate_per_question},
        'is_not_cheater_dataset': {student_id: dict_student_action_aggregate_per_question}
    }
    """

    attempts_with_actions = {
        'is_cheater_dataset': dict(),
        'is_not_cheater_dataset': dict(),
    }
    attempts = crud.quiz_attempt.get_multi_latest_by_quiz_id(
        db, id=quiz.id
    )
    for attempt in attempts:
        student_actions = crud.quiz_action.get_per_question_summary_by_attempt(
            db, attempt_id=attempt.id
        )
        student = crud.user.get(db, id=attempt.student_id)
        if student.is_cheater_dataset:
            attempts_with_actions['is_cheater_dataset'].setdefault(student.id, student_actions)
        else:
            attempts_with_actions['is_not_cheater_dataset'].setdefault(student.id, student_actions)

    return attempts_with_actions