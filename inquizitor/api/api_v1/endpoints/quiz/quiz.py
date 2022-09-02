import datetime as dt
import logging
import random
import string
from pprint import pformat
from sqlmodel import Session
from typing import Any, List, Union

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_jwt_auth import AuthJWT

from inquizitor import crud, models
from inquizitor.api import deps

router = APIRouter()


@router.post("/", response_model=models.QuizReadWithQuestions)
async def create_quiz(
    *,
    db: Session = Depends(deps.get_db),
    quiz_in: models.QuizCreate,
    current_teacher: models.User = Depends(deps.get_current_teacher)
) -> Any:
    """
    Create a quiz.
    """

    quiz = crud.quiz.create(db, obj_in=quiz_in)
    return quiz


@router.get("/", response_model=List[models.QuizReadWithQuestions])
async def read_quizzes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve quizzes.
    """
    if crud.user.is_superuser(current_user):
        quizzes = crud.quiz.get_multi(db, skip=skip, limit=limit)
    elif crud.user.is_student(current_user):
        quizzes = crud.quiz.get_multi_by_participant(
            db=db, student=current_user, skip=skip, limit=limit
        )
    elif crud.user.is_teacher(current_user):
        quizzes = crud.quiz.get_multi_by_author(
            db=db, teacher_id=current_user.id, skip=skip, limit=limit
        )

    return quizzes


@router.get("/results", response_model=List[List[models.QuizReadWithQuestions]])
async def read_quizzes_results(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_teacher: models.User = Depends(deps.get_current_teacher),
) -> Any:
    """
    Retrieve results for all student attempt for each quiz authored by the current teacher.
    """
    quizzes = crud.quiz.get_multi_by_author(
        db=db, teacher_id=current_teacher.id, skip=skip, limit=limit
    )
    quizzes_results = []
    for quiz in quizzes:
        results = crud.quiz.get_multi_results_by_quiz_id(db, id=quiz.id)
        quizzes_results.append(results)

    return quizzes_results


@router.get("/{quiz_index}", response_model=models.QuizReadWithQuestions)
async def read_quiz(
    *,
    db: Session = Depends(deps.get_db),
    quiz: models.Quiz = Depends(deps.get_quiz),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve quiz by id or quiz_code.
    """
    if crud.user.is_student(current_user):
        if dt.datetime.now() > quiz.due_date:
            raise HTTPException(
                status_code=400, detail="Quiz due date has already passed"
            )

        attempt = crud.quiz_attempt.get_latest_by_quiz_and_student_ids(
            db, quiz_id=quiz.id, student_id=current_user.id
        )
        if not attempt or attempt.is_done:
            # TODO ensure that quiz-user combination is unique
            quiz_attempt_in = models.QuizAttemptCreate(
                student_id=current_user.id, quiz_id=quiz.id
            )
            attempt = crud.quiz_attempt.create(db, obj_in=quiz_attempt_in)

        link = crud.quiz_student_link.get_by_quiz_and_student_ids(
            db, quiz_id=quiz.id, student_id=current_user.id
        )
        if not link:
            quiz_student_link_in = models.QuizStudentLinkCreate(
                student_id=current_user.id,
                quiz_id=quiz.id,
            )
            link = crud.quiz_student_link.create(db, obj_in=quiz_student_link_in)

    return quiz


@router.put("/{quiz_index}", response_model=models.Quiz)
async def update_quiz(
    *,
    db: Session = Depends(deps.get_db),
    quiz_in: models.QuizUpdate,
    quiz: models.Quiz = Depends(deps.get_quiz),
    current_author: models.User = Depends(deps.get_current_author)
) -> Any:
    """
    Update quiz by index.
    """
    quiz = crud.quiz.update(db, db_obj=quiz, obj_in=quiz_in)
    return quiz


@router.delete("/{quiz_index}", response_model=models.Quiz)
async def delete_quiz(
    *,
    db: Session = Depends(deps.get_db),
    quiz: models.Quiz = Depends(deps.get_quiz),
    current_author: models.User = Depends(deps.get_current_author)
) -> Any:
    """
    Delete quiz by index.
    """

    quiz = crud.quiz.remove(db, id=quiz.id)
    return quiz
