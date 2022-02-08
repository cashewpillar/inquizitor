from typing import Generator
from jose import jwt
from pydantic import ValidationError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from fastapi_tut import crud, models, schemas
from fastapi_tut.core import security
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

# TODO: unused
def get_current_user(
	db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
	try:
		payload = jwt.decode(
			token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
		)
		token_data = schemas.TokenPayload(**payload)
	except (jwt.JWTError, ValidationError):
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Could not validate credentials",
		)
	user = crud.user.get(db, id=token_data.sub)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	return user

	
# def refresh_access_token(
# 	db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
# ) -> str:
# 	try:
# 		payload = jwt.decode(
# 			token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
# 		)
# 		token_data = schemas.TokenPayload(**payload)
# 	except (jwt.JWTError, ValidationError):
# 		raise HTTPException(
# 			status_code=status.HTTP_403_FORBIDDEN,
# 			detail="Could not validate credentials",
# 		)
# 	user = crud.user.get(db, id=token_data.sub)
	