# initial, todo

from sqlmodel import Session
from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from typing import List

from fastapi_tut import crud
from fastapi_tut.api import deps
from fastapi_tut.models.user import User, UserCreate, ShowUser

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

@router.get("/{id}", response_model=ShowUser)
async def read_user(
    id : int,
    db : Session = Depends(deps.get_db),
    Authorize : AuthJWT = Depends()
    ):

    # is_superuser
    Authorize.jwt_required()

    users = crud.user.get_user(id, db)

    # hindi dapat nakalabas yung pw lmao
    return users

@router.post("/", response_model=ShowUser)
async def create_user(
    user : UserCreate,
    db : Session = Depends(deps.get_db),
    Authorize : AuthJWT = Depends()
):
    # TODO
    # doesnt return query errors properly (duplicate username, etc)

    # is_superuser
    Authorize.jwt_required()
	
    user_in = UserCreate(**user.dict())

    crud.user.create(db, obj_in=user_in)
	
    return user_in

# @router.put("/")
# async def update_user(
#     user : UserCreate,
#     db : Session = Depends(deps.get_db),
#     Authorize : AuthJWT = Depends()
# ):
#     # TODO
#     # doesnt return query errors properly (duplicate username, etc)

#     # is_superuser
#     Authorize.jwt_required()
	
#     user_in = UserCreate(**user.dict())

#     crud.user.update(db, obj_in=user_in)
	
#     return {'msg' : 'Successfully update data.'}