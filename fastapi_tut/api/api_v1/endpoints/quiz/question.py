import logging
from pprint import pformat
from sqlmodel import Session
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_jwt_auth import AuthJWT

from fastapi_tut import crud, models
from fastapi_tut.api import deps

router = APIRouter()

@router.post("/{quiz_index}/questions", response_model=models.QuizQuestion)
async def create_questions(
	*,
    quiz_index: Union[int, str],
    question_in: models.QuizQuestionCreate, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    quiz = crud.quiz.get_by_index(db, quiz_index)
    if not quiz: #return error if quiz doesn't exist
        raise HTTPException(status_code=404, detail="Quiz not found")

    #check if user is student
    #check if teacher owns the quiz
    if crud.user.is_student(current_user) or current_user.id != quiz.teacher_id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    question_in.quiz_id = quiz.id
    question = crud.quiz_question.create(db, obj_in=question_in)
    return question

@router.get("/{quiz_index}/questions/{question_id}", response_model=models.QuizQuestionReadWithChoices)
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
	quiz = crud.quiz.get_by_index(db, quiz_index)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")

	question = crud.quiz_question.get(db, id=question_id)
	if not question:
		raise HTTPException(status_code=404, detail="Question not found")
	if not crud.quiz.has_question(db, quiz_index=quiz_index, question_id=question.id):
		raise HTTPException(status_code=404, detail="Question does not belong to the specified quiz")
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
	quiz = crud.quiz.get_by_index(db, quiz_index)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")

	if not crud.user.is_superuser(current_user) and \
		not crud.quiz.is_author(db, user_id=current_user.id, quiz_index=quiz_index):
		raise HTTPException(status_code=400, detail="Not enough permissions")

	question = crud.quiz_question.get(db, id=question_id)
	if not crud.quiz.has_question(db, quiz_index=quiz_index, question_id=question.id):
		raise HTTPException(status_code=404, detail="Question does not belong to the specified quiz")

	question = crud.quiz_question.update(db, db_obj=question, obj_in=question_in)
	if not question:
		raise HTTPException(status_code=404, detail="Question not found")
	return question


@router.delete("/{quiz_index}/questions/{question_id}", response_model=models.QuizQuestion)
async def delete_question(
	*,
	db: Session = Depends(deps.get_db),
	quiz_index: Union[int, str] = Path(..., description="ID or Code of quiz to retrieve"),
	question_id: int,
	current_user: models.User = Depends(deps.get_current_user)
) -> Any:
	# """
	# Delete question by id.
	# """
	quiz = crud.quiz.get_by_index(db, quiz_index)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")

	if not crud.user.is_superuser(current_user) and \
		not crud.quiz.is_author(db, user_id=current_user.id, quiz_index=quiz_index):
		raise HTTPException(status_code=400, detail="Not enough permissions")

	question = crud.quiz_question.get(db, id=question_id)
	if not crud.quiz.has_question(db, quiz_index=quiz_index, question_id=question.id):
		raise HTTPException(status_code=404, detail="Question does not belong to the specified quiz")

	question = crud.quiz_question.remove(db, id=question_id)
	return question
