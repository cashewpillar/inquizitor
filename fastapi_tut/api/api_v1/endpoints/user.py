# initial, todo

from sqlmodel import Session
from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from typing import List

from fastapi_tut import crud
from fastapi_tut.api import deps
from fastapi_tut.models.user import User, UserCreate

router = APIRouter()


# Module 3: Exam
@router.get("/", response_model=List[User])
async def read_users(
    db : Session = Depends(deps.get_db),
    Authorize : AuthJWT = Depends()
    ):

    # is_superuser
    Authorize.jwt_required()

    users = crud.user.get_users(db)

    return users

# @router.post("/")
# async def create_user(
#     user : UserCreate,
#     db : Session = Depends(deps.get_db),
#     Authorize : AuthJWT = Depends()
#     # arg schema
# ):
    
#     # is_superuser
#     Authorize.jwt_required()
	
#     user_in = UserCreate(**user.dict())

#     crud.user.create(db, obj_in=user_in)
	
#     return user_in

# @router.put("/{id}")
# async def update_user(exam_id: int, item_id: int):
# 	return {"message": f"Taking item [ID: {item_id}]"}