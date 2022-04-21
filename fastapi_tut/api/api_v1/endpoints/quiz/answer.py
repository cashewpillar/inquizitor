import logging
from sqlmodel import Session
from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException

from fastapi_tut import crud, models
from fastapi_tut.api import deps

router = APIRouter()

@router.get("/{quiz_index}/answers", response_model=List[models.QuizAnswer])
async def read_answers(
	*,
	db: Session = Depends(deps.get_db),
	quiz_index: Union[int, str],
	student_id: Optional[int] = None,
	current_user: models.User = Depends(deps.get_current_user)
) -> Any:
	"""
	Read answers of current student for the quiz.
	"""
	if crud.user.is_student(current_user):
		user_id = current_user.id
	elif crud.user.is_superuser(current_user) or crud.user.is_teacher(current_user):
		user_id = student_id

	quiz = crud.quiz.get(db, id=quiz_index)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")

	answers_of_current_user = crud.quiz_answer.get_all_by_quiz_and_student_ids(
		db, quiz_id=quiz.id, student_id=user_id
	)
	return answers_of_current_user

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

	answer = crud.quiz_answer.get_by_choice_and_user_ids(
		db, choice_id=answer_in.choice_id, student_id=answer_in.student_id
	)
	if answer:
		answer = crud.quiz_answer.update(db, db_obj=answer, obj_in=answer_in)
	else:
		answer = crud.quiz_answer.create(db, obj_in=answer_in)
		
	return answer


