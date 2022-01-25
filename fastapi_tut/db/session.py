from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_tut.core.config import settings

if settings.USE_SQLITE:
	SQLALCHEMY_DATABASE_URL = "sqlite:///fastapi_tut/data.db"
	engine = create_engine(
	    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
	)
else:
	SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
	engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)