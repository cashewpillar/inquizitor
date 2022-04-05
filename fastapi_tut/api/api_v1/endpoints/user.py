# initial, todo

from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from typing import Any, List

from fastapi_tut import crud
from fastapi_tut.api import deps
from fastapi_tut.models import User, UserCreate, ShowUser, UserUpdate

router = APIRouter()

"""
NOTE
reordered path operations by endpoint 
@router.get("/")
@router.post("/")
@router.get("/{profile}")
@router.get("/{id}")
@router.put("/{id}")
"""

@router.get("/", response_model=List[ShowUser])
async def read_users(
    db : Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # NOTE User instead of ShowUser para available lahat ng properties for processing
    # mafifilter out naman yung response via response_model param
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=ShowUser)
async def create_user(
    *,
    db : Session = Depends(deps.get_db),
    user_in : UserCreate,
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """
    Create new user.
    """
    user = crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user

@router.get("/profile", response_model=ShowUser)
async def read_profile(
    db : Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.get("/{id}", response_model=ShowUser)
async def read_user(
    id : int,
    db : Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, 
            detail="The user doesn't have enough privileges"
        )
    return user

@router.put("/{id}", response_model=ShowUser)
async def update_user(
    *,
    db : Session = Depends(deps.get_db),
    id : int,
    user_in : UserUpdate,
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """
    Update a user.
    """
    user = crud.user.get(db, id=id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with {id} does not exist."
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
