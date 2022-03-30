import logging
from pprint import pformat
from sqlmodel import Session
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_jwt_auth import AuthJWT

from fastapi_tut import crud, models
from fastapi_tut.api import deps

router = APIRouter()

# DOING
# /quizzes/{quiz_id}/questions/{question_id}
@router.get("/{quiz_index}/questions/{question_id}", response_model=models.QuizQuestion)
async def read_question(
	*,
	db: Session = Depends(deps.get_db),
	quiz_index: Union[int, str] = Path(..., description="ID or Code of quiz to retrieve"),
	question_id: int,
	current_user: models.User = Depends(deps.get_current_user)
) -> Any:
	"""
	Retrieve question by id.
	What-ifs:
	1. Users without access to quiz reads a question [solved using quiz_index]
	"""

	if isinstance(quiz_index, str):
		quiz = crud.quiz.get_by_code(db, code=quiz_index)
	else:
		quiz = crud.quiz.get(db, id=quiz_index)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")

	question = crud.quiz_question.get(db, id=question_id)
	if not question:
		raise HTTPException(status_code=404, detail="Question not found")
	return question

@router.put("/{quiz_index}/questions/{question_id}", response_model=models.QuizQuestion)
async def update_question(
	*,
	db: Session = Depends(deps.get_db),
	quiz_index: Union[int, str] = Path(..., description="ID or Code of quiz to retrieve"),
	question_id: int,
	question_in: models.QuizQuestionUpdate,
	current_user: models.User = Depends(deps.get_current_user)
) -> Any:
	"""
	Update question by quiz_index and question id.
	"""

	if isinstance(quiz_index, str):
		quiz = crud.quiz.get_by_code(db, code=quiz_index)
	else:
		quiz = crud.quiz.get(db, id=quiz_index)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")
	# TODO add validation method to quiz to check if question belongs??

	if not crud.user.is_superuser(current_user) and \
		not (crud.user.is_teacher(current_user) and quiz.teacher_id == current_user.id):
		raise HTTPException(status_code=400, detail="Not enough permissions")

	question = crud.quiz_question.get(db, id=question_id)
	crud.quiz_question.update(db, db_obj=question, obj_in=question_in)
	if not question:
		raise HTTPException(status_code=404, detail="Question not found")
	return question