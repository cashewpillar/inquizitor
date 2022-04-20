import logging
from sqlmodel import Session
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException

from fastapi_tut import crud, models
from fastapi_tut.api import deps

router = APIRouter()

# TODO FOR TESTING
@router.put("/{quiz_index}/questions/{question_id}/answer", response_model=models.QuizAnswer)
async def update_answer(
	*,
	db: Session = Depends(deps.get_db),
	quiz_index: Union[int, str],
	question_id: int,
	answer_in: Union[models.QuizAnswerCreate, models.QuizAnswerUpdate],
	current_user: models.User = Depends(deps.get_current_user)
) -> Any:
	"""
	Update answer for question.
	"""
	if not crud.user.is_student(current_user):
		raise HTTPException(status_code=400, detail="User must be a student")

	quiz = crud.quiz.get(db, id=quiz_index)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")

	question = crud.quiz_question.get(db, id=question_id)
	if not crud.quiz.has_question(db, quiz_index=quiz_index, question_id=question.id):
		raise HTTPException(status_code=404, detail="Question does not belong to the specified quiz")

	answer = crud.quiz_answer.get_by_choice_and_user(
		db, choice_id=answer_in.choice_id, student_id=answer_in.student_id
	)
	if answer:
		answer = crud.quiz_answer.update(db, db_obj=answer, obj_in=answer_in)
	else:
		answer = crud.quiz_answer.create(db, obj_in=answer_in)
		
	return answer