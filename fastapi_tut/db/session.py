from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from fastapi_tut.core.config import settings

if settings.USE_SQLITE:
	engine = create_engine(
	    settings.SQLALCHEMY_DATABASE_URI, 
	    connect_args={"check_same_thread": False}
	)
else:
	engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

test_engine = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

def SessionLocal():
	with Session(engine) as session:
		# https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#fastapi-application
		# NOTE: above uses 'yield' instead of 'return'
		# i get errors with yield & currently i dont understand
		# same goes for below 
		return session 

# def TestSession():
# 	with Session(test_engine) as session:
# 		yield session

TestSession = Session(test_engine)