import logging
from pprint import pformat
from sqlmodel import Session
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_jwt_auth import AuthJWT

from inquizitor import crud, models
from inquizitor.api import deps

router = APIRouter()

@router.post("/{quiz_index}/questions", response_model=models.QuizQuestion)
async def create_questions(
    *,
    db: Session = Depends(deps.get_db),
    quiz: models.Quiz = Depends(deps.get_quiz),
    question_in: models.QuizQuestionCreate, 
    current_author: models.User = Depends(deps.get_current_author),
) -> Any:
    """
    Create a question for the given quiz.
    """

    question_in.quiz_id = quiz.id
    question = crud.quiz_question.create(db, obj_in=question_in)
    return question

@router.get("/{quiz_index}/questions/{question_id}", response_model=models.QuizQuestionReadWithChoices)
async def read_question(
    *,
    db: Session = Depends(deps.get_db),
    question: models.QuizQuestion = Depends(deps.get_question),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve question by id.
    """

    return question

@router.put("/{quiz_index}/questions/{question_id}", response_model=models.QuizQuestion)
async def update_question(
    *,
    db: Session = Depends(deps.get_db),
    question_in: models.QuizQuestionUpdate,
    question: models.QuizQuestion = Depends(deps.get_question),
    current_author: models.User = Depends(deps.get_current_author),
) -> Any:
    """
    Update question by quiz_index and question id.
    """

    question = crud.quiz_question.update(db, db_obj=question, obj_in=question_in)
    return question


@router.delete("/{quiz_index}/questions/{question_id}", response_model=models.QuizQuestion)
async def delete_question(
    *,
    db: Session = Depends(deps.get_db),
    question: models.QuizQuestion = Depends(deps.get_question),
    current_author: models.User = Depends(deps.get_current_author),
) -> Any:
    """
    Delete question by id.
    """

    question = crud.quiz_question.remove(db, id=question.id)
    return question
