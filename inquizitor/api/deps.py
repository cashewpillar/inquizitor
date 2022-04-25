from sqlmodel import Session
from sqlalchemy import and_
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError

from inquizitor import crud, models
from inquizitor.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/login/access-token"
)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> models.User:
    try:
        Authorize.jwt_required()
    except JWTDecodeError as err:
        # https://github.com/IndominusByte/fastapi-jwt-auth/issues/20
        status_code = err.status_code
        if err.message == "Signature verification failed":
            status_code = 401
        raise HTTPException(status_code=status_code, detail="User not logged in")
    
    user = crud.user.get(db, id=Authorize.get_jwt_subject())
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user