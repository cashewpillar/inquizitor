from sqlmodel import Session
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from pydantic.networks import EmailStr
from typing import Any, List

from inquizitor import crud
from inquizitor.api import deps
from inquizitor.models import User, UserCreate, ShowUser, UserUpdate

router = APIRouter()

@router.get("/", response_model=List[ShowUser])
async def read_users(
    db : Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # NOTE User instead of ShowUser para available lahat ng properties for processing
    # mafifilter out naman yung response via response_model param
    current_user: User = Depends(deps.get_current_superuser)
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
    current_user: User = Depends(deps.get_current_superuser)
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

# DOING
@router.put("/profile", response_model=ShowUser)
def update_profile(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user

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
    current_user: User = Depends(deps.get_current_superuser)
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
