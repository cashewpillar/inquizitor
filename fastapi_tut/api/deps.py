from sqlmodel import Session
from sqlalchemy import and_
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT

from fastapi_tut import crud, models
from fastapi_tut.models.user import User
from fastapi_tut.db.session import SessionLocal

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
	Authorize.jwt_required()
	
	current_user = crud.user.get(db, id=Authorize.get_jwt_subject())

	return current_user

def has_superuser_access(subject, db: Session):
	superuser = db.query(User).filter(and_(User.id == subject, User.is_superuser == True)).first()

	if not superuser:
		raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with {id} does not exist."
        )

	return True