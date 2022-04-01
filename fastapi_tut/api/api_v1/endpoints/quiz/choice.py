import logging
from pprint import pformat
from sqlmodel import Session
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_jwt_auth import AuthJWT

from fastapi_tut import crud, models
from fastapi_tut.api import deps

router = APIRouter()

# NOTE MIGHT NOT BE NEEDED
# @router.get("/{quiz_index}/questions/{question_id}/choices/{choice_id}", response_model=models.QuizChoice)
# async def read_choice(
# 	*,
# 	db: Session = Depends(deps.get_db),
# 	quiz_index: Union[int, str] = Path(..., description="ID or Code of quiz to retrieve"),
# 	question_id: int,
# 	choice_id: int,
# 	current_user: models.User = Depends(deps.get_current_user)
# ) -> Any:
# 	"""
# 	Retrieve choice by id.
# 	"""
# 	quiz = crud.quiz.get_by_index(db, quiz_index)
# 	if not quiz:
# 		raise HTTPException(status_code=404, detail="Quiz not found")

# 	question = crud.quiz_question.get(db, id=question_id)
# 	if not question:
# 		raise HTTPException(status_code=404, detail="Question not found")
# 	if not crud.quiz.has_question(db, quiz_index=quiz_index, question_id=question.id):
# 		raise HTTPException(status_code=404, detail="Question does not belong to the specified quiz")

# 	choice = crud.quiz_choice.get(db, id=choice_id)
# 	if not choice:
# 		raise HTTPException(status_code=404, detail="Choice not found")
# 	if not crud.question.has_choice(db, question_id=question.id, choice_id=choice.id):
# 		raise HTTPException(status_code=404, detail="Choice does not belong to the specified question")

# 	return question

@router.put("/{quiz_index}/questions/{question_id}/choices/{choice_id}", response_model=models.QuizChoice)
async def update_choice(
	*,
	db: Session = Depends(deps.get_db),
	quiz_index: Union[int, str] = Path(..., description="ID or Code of quiz to retrieve"),
	question_id: int,
	choice_id: int,
	choice_in: models.QuizChoiceUpdate,
	current_user: models.User = Depends(deps.get_current_user)
) -> Any:
	"""
	Update choice by quiz_index, question id, and choice id.
	"""
	quiz = crud.quiz.get_by_index(db, quiz_index)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")

	if not crud.user.is_superuser(current_user) and \
		not crud.quiz.is_author(db, user_id=current_user.id, quiz_index=quiz_index):
		raise HTTPException(status_code=400, detail="Not enough permissions")

	question = crud.quiz_question.get(db, id=question_id)
	if not question:
		raise HTTPException(status_code=404, detail="Question not found")
	if not crud.quiz.has_question(db, quiz_index=quiz_index, question_id=question.id):
		raise HTTPException(status_code=404, detail="Question does not belong to the specified quiz")

	choice = crud.quiz_choice.get(db, id=choice_id)
	if not choice:
		raise HTTPException(status_code=404, detail="Choice not found")
	if not crud.quiz_question.has_choice(db, question_id=question_id, choice_id=choice.id):
		raise HTTPException(status_code=404, detail="Question does not belong to the specified quiz")

	choice = crud.quiz_choice.update(db, db_obj=choice, obj_in=choice_in)
	return choice


@router.delete("/{quiz_index}/questions/{question_id}/choices/{choice_id}", response_model=models.QuizChoice)
async def delete_choice(
	*,
	db: Session = Depends(deps.get_db),
	quiz_index: Union[int, str] = Path(..., description="ID or Code of quiz to retrieve"),
	question_id: int,
	choice_id: int,
	current_user: models.User = Depends(deps.get_current_user)
) -> Any:
	"""
	Delete choice by id.
	"""
	quiz = crud.quiz.get_by_index(db, quiz_index)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")

	if not crud.user.is_superuser(current_user) and \
		not crud.quiz.is_author(db, user_id=current_user.id, quiz_index=quiz_index):
		raise HTTPException(status_code=400, detail="Not enough permissions")

	question = crud.quiz_question.get(db, id=question_id)
	if not question:
		raise HTTPException(status_code=404, detail="Question not found")
	if not crud.quiz.has_question(db, quiz_index=quiz_index, question_id=question.id):
		raise HTTPException(status_code=404, detail="Question does not belong to the specified quiz")

	choice = crud.quiz_choice.get(db, id=choice_id)
	if not choice:
		raise HTTPException(status_code=404, detail="Choice not found")
	if not crud.quiz_question.has_choice(db, question_id=question_id, choice_id=choice.id):
		raise HTTPException(status_code=404, detail="Question does not belong to the specified quiz")

	choice = crud.quiz_choice.remove(db, id=choice_id)
	return choice
