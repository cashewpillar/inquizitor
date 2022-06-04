import logging
from sqlmodel import Session
from typing import Any, List, Tuple, Union

from fastapi import APIRouter, Depends, HTTPException

from inquizitor import crud, models
from inquizitor.api import deps

router = APIRouter()

@router.get("/{quiz_index}/finish", response_model=int)
async def finish_quiz(
	*,
	db: Session = Depends(deps.get_db),
	quiz: models.Quiz = Depends(deps.get_quiz),
	current_student: models.User = Depends(deps.get_current_student)
) -> Any:
	"""
	Finish the quiz and get the score for this attempt.
	"""

	return crud.quiz_attempt.get_score(db, quiz_id=quiz.id, student_id=current_student.id)

@router.put("/{quiz_index}/questions/{question_id}/answer", response_model=models.QuizAnswer)
async def update_answer(
	*,
	db: Session = Depends(deps.get_db),
	attempt_and_link: Tuple[models.QuizAttempt, models.QuizStudentLink] = Depends(deps.get_attempt_and_link),
	answer_in: Union[models.QuizAnswerCreate, models.QuizAnswerUpdate]
) -> Any:
	"""
	Update answer for the given question.
	"""

	answer = crud.quiz_answer.get_by_choice_and_user_ids(
		db, choice_id=answer_in.choice_id, student_id=answer_in.student_id
	)
	if answer:
		answer = crud.quiz_answer.update(db, db_obj=answer, obj_in=answer_in)
	else:
		answer = crud.quiz_answer.create(db, obj_in=answer_in)
		
	return answer


