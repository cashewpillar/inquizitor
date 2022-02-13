from typing import Generator
from jose import jwt
from pydantic import ValidationError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from fastapi_tut import crud, models, schemas
from fastapi_tut.core.config import settings
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