from sqlmodel import Session
from typing import Any, List

from fastapi import APIRouter, Depends 
from fastapi_jwt_auth import AuthJWT

from fastapi_tut import crud, models
from fastapi_tut.api import deps

router = APIRouter()

# DOING
@router.get("/", response_model=List[models.Quiz])
async def read_quizzes(
	db: Session = Depends(deps.get_db),
	skip: int = 0,
	limit: int = 100,
	Authorize: AuthJWT = Depends()
) -> Any:
	"""
	Retrieve quizzes.
	"""
	Authorize.jwt_required()
	
	current_user = crud.user.get(db, id=Authorize.get_jwt_subject())

	# if crud.user.is_superuser(current_user):
	# 	quizzes = crud.quiz.get_multi(db, skip=skip, limit=limit)
	# 	pass
	# elif crud.user.is_student(current_user):
	quizzes = crud.quiz.get_multi_by_participant(
		# db=db, participant=current_user, skip=skip, limit=limit
		db=db, participant=current_user
	)
	# 	pass
	# elif crud.user.is_teacher(current_user):
	# 	quizzes = crud.quiz.get_multi_by_creator(
	# 		db=db, participant_id=current_user.id, skip=skip, limit=limit
	# 	)
	# 	pass
	return quizzes



