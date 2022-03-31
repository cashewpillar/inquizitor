# initial, todo

from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from typing import List

from fastapi_tut import crud
from fastapi_tut.api import deps
from fastapi_tut.models.user import User, UserCreate, ShowUser, UserUpdate

router = APIRouter()


@router.get("/profile", response_model=ShowUser)
async def read_profile(
    db : Session = Depends(deps.get_db),
    Authorize : AuthJWT = Depends()
):
    Authorize.jwt_required()
    current_user = crud.user.get(db, id=Authorize.get_jwt_subject())
    
    return current_user

# Module 3: Exam
@router.get("/", response_model=List[User])
async def read_users(
    db : Session = Depends(deps.get_db),
    Authorize : AuthJWT = Depends()
):
    
    Authorize.jwt_required()
    deps.has_superuser_access(Authorize.get_jwt_subject(), db)

    users = crud.user.get_users(db)

    return users

@router.get("/{id}", response_model=ShowUser)
async def read_user(
    id : int,
    db : Session = Depends(deps.get_db),
    Authorize : AuthJWT = Depends()
):
    
    Authorize.jwt_required()
    deps.has_superuser_access(Authorize.get_jwt_subject(), db)

    users = crud.user.get_user(id, db)

    
    return users

@router.post("/", response_model=ShowUser)
async def create_user(
    user : UserCreate,
    db : Session = Depends(deps.get_db),
    Authorize : AuthJWT = Depends()
):
    """
    
    TODO
        - doesnt return query errors properly (duplicate username, etc)
    
    """

    Authorize.jwt_required()
    deps.has_superuser_access(Authorize.get_jwt_subject(), db)
	
    user_in = UserCreate(**user.dict())

    crud.user.create(db, obj_in=user_in)
	
    return user_in

@router.put("/{id}")
async def update_user(
    id : int,
    user : UserUpdate,
    db : Session = Depends(deps.get_db),
    Authorize : AuthJWT = Depends()
):
    """
    
    TODO
        - doesnt return query errors properly (duplicate username, etc)
    
    """

    Authorize.jwt_required()
    deps.has_superuser_access(Authorize.get_jwt_subject(), db)
	
    user_in = UserUpdate(**user.dict())

    result = crud.user.update_user_by_id(id, user_in, db)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {id} does not exist."
        )
	
    return {'msg' : 'Successfully updated user.'}