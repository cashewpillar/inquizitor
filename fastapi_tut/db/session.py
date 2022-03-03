from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from fastapi_tut.core.config import settings
from fastapi_tut.db.init_db import init_db

if settings.USE_SQLITE:
	engine = create_engine(
	    settings.SQLALCHEMY_DATABASE_URI, 
	    connect_args={"check_same_thread": False}
	)
else:
	engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def SessionLocal():
	with Session(engine) as session:
		# https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#fastapi-application
		# NOTE: above uses 'yield' instead of 'return'
		# i get errors with yield & currently i dont understand
		# same goes for below 
		return session 

	
def TestSession():
	engine = create_engine(
	    "sqlite://", 
	    connect_args={"check_same_thread": False},
	    poolclass=StaticPool
	)
	with Session(engine) as session:
		init_db(session, engine)
		return session
