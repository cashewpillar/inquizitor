import logging
from pprint import pformat
from sqlmodel import Session
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_jwt_auth import AuthJWT

from fastapi_tut import crud, models
from fastapi_tut.api import deps

router = APIRouter()

@router.get("/", response_model=List[models.Quiz])
async def read_quizzes(
	db: Session = Depends(deps.get_db),
	skip: int = 0,
	limit: int = 100,
	current_user: models.User = Depends(deps.get_current_user)
) -> Any:
	"""
	Retrieve quizzes.
	"""
	if crud.user.is_superuser(current_user):
		quizzes = crud.quiz.get_multi(db, skip=skip, limit=limit)
	elif crud.user.is_student(current_user):
		quizzes = crud.quiz.get_multi_by_participant(
			# NOTE change to line below when feature is needed
			# db=db, participant=current_user, skip=skip, limit=limit
			db=db, student=current_user
		)
	elif crud.user.is_teacher(current_user):
		quizzes = crud.quiz.get_multi_by_author(
			db=db, teacher_id=current_user.id, skip=skip, limit=limit
		)

	return quizzes

@router.get("/{index}", response_model=models.Quiz)
async def read_quiz(
	*,
	db: Session = Depends(deps.get_db),
	index: Union[int, str] = Path(..., description="ID or Code of quiz to retrieve"),
	current_user: models.User = Depends(deps.get_current_user)
) -> Any:
	"""
	Retrieve quiz by id or quiz_code.
	"""
	quiz = crud.quiz.get_by_index(db, index)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")
	# if crud.user.is_student(current_user) or (crud.user.is_teacher(current_user) and quiz.teacher_id != current_user.id):
	# 	raise HTTPException(status_code=400, detail="Not enough permissions")
	return quiz

@router.put("/{id}", response_model=models.Quiz)
async def update_quiz(
	*,
	db: Session = Depends(deps.get_db),
	id: int,
	quiz_in: models.QuizUpdate,
	current_user: models.User = Depends(deps.get_current_user)
) -> Any:
	"""
	Update quiz by id.
	"""
	quiz = crud.quiz.get(db, id=id)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")
		
	if not crud.user.is_superuser(current_user) and \
		not crud.quiz.is_author(db, user_id=current_user.id, quiz_index=id):
		raise HTTPException(status_code=400, detail="Not enough permissions")
	quiz = crud.quiz.update(db, db_obj=quiz, obj_in=quiz_in)
	return quiz

@router.delete("/{id}", response_model=models.Quiz)
async def delete_quiz(
	*,
	db: Session = Depends(deps.get_db),
	id: int,
	current_user: models.User = Depends(deps.get_current_user)
) -> Any:
	"""
	Delete quiz by id.
	"""
	quiz = crud.quiz.get(db, id=id)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")
	if not crud.user.is_superuser(current_user) and \
		not crud.quiz.is_author(db, user_id=current_user.id, quiz_index=id):
		raise HTTPException(status_code=400, detail="Not enough permissions")
	quiz = crud.quiz.remove(db, id=id)
	return quiz