import logging
from sqlmodel import Session
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException

from fastapi_tut import crud, models
from fastapi_tut.api import deps

router = APIRouter()

@router.get("/{quiz_index}/finish", response_model=int)
async def finish_quiz(
	*,
	db: Session = Depends(deps.get_db),
	quiz_index: Union[int, str],
	current_user: models.User = Depends(deps.get_current_user)
) -> Any:
	"""
	Finish the quiz and get scores for this attempt.
	"""
	quiz = crud.quiz.get(db, id=quiz_index) # NOTE can be made a dependency function for ease of reuse
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")

	return crud.quiz_attempt.get_score(db, quiz_id=quiz.id, student_id=current_user.id)

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

	attempt = crud.quiz_attempt.get_by_quiz_and_student_ids(db, quiz_id=quiz.id, student_id=current_user.id)
	# crud.quiz_attempt.update(
	# 	db, db_obj=attempt, obj_in={"recent_question_id": question_id}
	# )
	if not attempt:
		quiz_attempt_in = models.QuizAttemptCreate(
			student_id=current_user.id,	
			quiz_id=quiz.id,
			recent_question_id=question_id
		)
		attempt = crud.quiz_attempt.create(db, obj_in=quiz_attempt_in)
	else:
		crud.quiz_attempt.update(
			db, db_obj=attempt, obj_in={"recent_question_id": question_id}
		)

	answer = crud.quiz_answer.get_by_choice_and_user(
		db, choice_id=answer_in.choice_id, student_id=answer_in.student_id
	)
	if answer:
		answer = crud.quiz_answer.update(db, db_obj=answer, obj_in=answer_in)
	else:
		answer = crud.quiz_answer.create(db, obj_in=answer_in)
		
	return answer


