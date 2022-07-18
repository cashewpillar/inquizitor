from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

from inquizitor.core.config import settings

# sqlite cascade delete https://github.com/tiangolo/sqlmodel/issues/213
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

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