from sqlmodel import Session
from typing import Generator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT

from fastapi_tut import crud, models
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