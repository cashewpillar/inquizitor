from typing import Generator

from fastapi.security import OAuth2PasswordBearer

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