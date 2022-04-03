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
    current_user: ShowUser = Depends(deps.get_current_user)
):
    
    return current_user

# Module 3: Exam
@router.get("/", response_model=List[User])
async def read_users(
    db : Session = Depends(deps.get_db),
    current_user: ShowUser = Depends(deps.get_current_user)
):
    
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, details='Not enough permissions.')

    users = crud.user.get_users(db)

    return users

@router.get("/{id}", response_model=ShowUser)
async def read_user(
    id : int,
    db : Session = Depends(deps.get_db),
    current_user: ShowUser = Depends(deps.get_current_user)
):
    
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, details='Not enough permissions.')

    users = crud.user.get_user(id, db)

    
    return users

@router.post("/", response_model=ShowUser)
async def create_user(
    user : UserCreate,
    db : Session = Depends(deps.get_db),
    current_user: ShowUser = Depends(deps.get_current_user)
):
    """
    
    TODO
        - doesnt return query errors properly (duplicate username, etc)
    
    """

    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, details='Not enough permissions.')
	
    user_in = UserCreate(**user.dict())

    crud.user.create(db, obj_in=user_in)
	
    return user_in

@router.put("/{id}")
async def update_user(
    id : int,
    user_in : UserUpdate,
    db : Session = Depends(deps.get_db),
    current_user: ShowUser = Depends(deps.get_current_user)
):
    """
    
    TODO
        - doesnt return query errors properly (duplicate username, etc)
    
    """

    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, details='Not enough permissions.')
	
    user_in = UserUpdate(**user_in.dict())

    user = crud.user.get(db, id=id)

    result = crud.user.update(db, db_obj=user, obj_in=user_in)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {id} does not exist."
        )

    return {'msg' : 'Successfully updated user.'}