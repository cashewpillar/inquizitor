import logging
from pprint import pformat
from sqlmodel import Session
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_jwt_auth import AuthJWT

from inquizitor import crud, models
from inquizitor.api import deps

router = APIRouter()

# @router.post("/{quiz_index}/questions/{question_id}/actions", response_model=models.QuizAction)
# async def create_action(
#     *,
#     action_in: models.QuizActionCreate,
#     db: Session = Depends(deps.get_db),
#     current_student: models.User = Depends(deps.get_current_student),
#     attempt: models.QuizAttempt = Depends(deps.get_attempt),
#     quiz: models.Quiz = Depends(deps.get_quiz),
#     question: models.QuizQuestion = Depends(deps.get_question),
# ) -> Any:
#     """
#     Store the current student's action for the given attempt and quiz question.
#     """

#     action_in.student_id = student.id
#     action_in.attempt_id = attempt.id
#     action_in.quiz_id = quiz.id
#     action_in.question_id = question.id

#     action = crud.quiz_action.create(db, obj_in=action_in)

#     return action


# @router.get(
#     "/{quiz_index}/questions/{question_id}",
#     response_model=models.QuizQuestionReadWithChoices,
# )
# async def read_question(
#     *,
#     db: Session = Depends(deps.get_db),
#     question: models.QuizQuestion = Depends(deps.get_question),
#     current_user: models.User = Depends(deps.get_current_user),
# ) -> Any:
#     """
#     Retrieve question by id.
#     """

#     return question


# @router.put("/{quiz_index}/questions/{question_id}", response_model=models.QuizQuestion)
# async def update_question(
#     *,
#     db: Session = Depends(deps.get_db),
#     question_in: models.QuizQuestionUpdate,
#     question: models.QuizQuestion = Depends(deps.get_question),
#     current_author: models.User = Depends(deps.get_current_author),
# ) -> Any:
#     """
#     Update question by quiz_index and question id.
#     """

#     question = crud.quiz_question.update(db, db_obj=question, obj_in=question_in)
#     return question


# @router.delete(
#     "/{quiz_index}/questions/{question_id}", response_model=models.QuizQuestion
# )
# async def delete_question(
#     *,
#     db: Session = Depends(deps.get_db),
#     question: models.QuizQuestion = Depends(deps.get_question),
#     current_author: models.User = Depends(deps.get_current_author),
# ) -> Any:
#     """
#     Delete question by id.
#     """

#     question = crud.quiz_question.remove(db, id=question.id)
#     return question
