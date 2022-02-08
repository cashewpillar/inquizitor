from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_tut import crud, schemas
from fastapi_tut.core.config import settings
from fastapi_tut.db.base import Base

if settings.USE_SQLITE:
	engine = create_engine(
	    settings.SQLALCHEMY_DATABASE_URI, 
	    connect_args={"check_same_thread": False}
	)
else:
	engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def SessionLocal():
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

	return SessionLocal()

	
def TestSession():
	engine = create_engine(
	    "sqlite://", 
	    connect_args={"check_same_thread": False}
	)
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
	Base.metadata.create_all(bind=engine)
	db = SessionLocal()

	user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
	if not user:
		user_in = schemas.UserCreate(
			full_name=settings.FIRST_SUPERUSER_FULLNAME,
			email=settings.FIRST_SUPERUSER_EMAIL,
			password=settings.FIRST_SUPERUSER_PASSWORD,
			is_superuser=True,
		)
		user = crud.user.create(db, obj_in=user_in) # noqa: F841

	return db
