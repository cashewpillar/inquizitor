import logging
from pprint import pformat
from sqlmodel import Session
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from fastapi_tut import crud, models
from fastapi_tut.api import deps

router = APIRouter()

# DOING
# /quizzes/{quiz_id}/questions/{question_id}
# @route.get("/{quiz_id}/questions/{question_id}", response_model=models.QuizQuestion)
# async def read_question(
# 	*,
# 	db: Session = Depends(deps.get_db),
# 	quiz_id: int,
# 	question_id: int,
# 	current_user: models.User = Depends(deps.get_current_user)
# ) -> Any:
# 	"""
# 	Retrieve question belonging to a quiz by id.
# 	"""
# 	question = crud.question.get(db, id=id)
# 	if not question:
# 		raise HTTPException(status_code=404, detail="Question not found")
# 	if crud.user.is_student(current_user) or (crud.user.is_teacher(current_user) and question.teacher_id != current_user.id):
# 		raise HTTPException(status_code=400, detail="Not enough permissions")
# 	return question