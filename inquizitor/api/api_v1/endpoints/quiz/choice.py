import logging
from pprint import pformat
from sqlmodel import Session
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_jwt_auth import AuthJWT

from inquizitor import crud, models
from inquizitor.api import deps

router = APIRouter()


@router.post("/{quiz_index}/questions/{question_id}", response_model=models.QuizChoice)
async def create_choices(
    *,
    db: Session = Depends(deps.get_db),
    choice_in: models.QuizChoiceCreate,
    question: models.QuizQuestion = Depends(deps.get_question),
    current_author: models.User = Depends(deps.get_current_author),
) -> Any:
    """
    Create a choice for the given question.
    """

    choice_in.question_id = question.id
    choice = crud.quiz_choice.create(db, obj_in=choice_in)
    return choice


@router.put(
    "/{quiz_index}/questions/{question_id}/choices/{choice_id}",
    response_model=models.QuizChoice,
)
async def update_choice(
    *,
    db: Session = Depends(deps.get_db),
    choice_in: models.QuizChoiceUpdate,
    choice: models.QuizChoice = Depends(deps.get_choice),
    current_author: models.User = Depends(deps.get_current_author),
) -> Any:
    """
    Update choice by quiz_index, question id, and choice id.
    """

    choice = crud.quiz_choice.update(db, db_obj=choice, obj_in=choice_in)
    return choice


@router.delete(
    "/{quiz_index}/questions/{question_id}/choices/{choice_id}",
    response_model=models.QuizChoice,
)
async def delete_choice(
    *,
    db: Session = Depends(deps.get_db),
    choice: models.QuizChoice = Depends(deps.get_choice),
    current_author: models.User = Depends(deps.get_current_author),
) -> Any:
    """
    Delete choice by id.
    """

    choice = crud.quiz_choice.remove(db, id=choice.id)
    return choice
