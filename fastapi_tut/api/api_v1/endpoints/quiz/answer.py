# TODO
# remove unused imports by ctrl+D-ing

import logging
import random
import string
from pprint import pformat
from sqlmodel import Session
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_jwt_auth import AuthJWT

from fastapi_tut import crud, models
from fastapi_tut.api import deps

router = APIRouter()

# DOING
@router.put("/quizzes/{quiz_index}/questions/{question_id}/answer", response_model=models.QuizAnswer)
async def update_quiz(
	*,
	db: Session = Depends(deps.get_db),
	quiz_index: Union[int, str],
	question_id: int,
	answer_in: models.QuizAnswer,
	current_user: models.User = Depends(deps.get_current_user)
) -> Any:
	"""
	Update answer for question.
	"""
	if not crud.user.is_student(current_user):
		raise HTTPException(status_code=400, detail="User must be a student")

	quiz = crud.quiz.get(db, id=id)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")

	question = crud.quiz_question.get(db, id=question_id)
	if not crud.quiz.has_question(db, quiz_index=quiz_index, question_id=question.id):
		raise HTTPException(status_code=404, detail="Question does not belong to the specified quiz")

	answer = crud.quiz_answer.get(db, id=answer_in.id)
	if answer:
		answer = crud.quiz_answer.update(db, db_obj=answer, obj_in=answer_in)
	else:
		answer = crud.quiz_answer.create(db, obj_in=answer_in)
		
	return answer