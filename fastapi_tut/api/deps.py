from typing import Generator

from fastapi.templating import Jinja2Templates

from fastapi_tut.db.session import SessionLocal

# might remove staticfiles once vue is implemented
templates = Jinja2Templates(directory="fastapi_tut/templates")

def get_db() -> Generator:
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close()