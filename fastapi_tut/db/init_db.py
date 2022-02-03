from sqlalchemy.orm import Session 

from fastapi_tut import crud, schemas
from fastapi_tut.utils import fake
from fastapi_tut.core.config import settings
from fastapi_tut.core.security import get_password_hash
from fastapi_tut.db.base import Base
from fastapi_tut.db.session import engine
from fastapi_tut.db import base # noqa: F401
from fastapi_tut.models import User

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

def init_users(db: Session) -> None:
	for i in range(10):
		user = User(full_name=fake.name(),
					email=fake.email(),
					hashed_password=get_password_hash("secret")
				)
		db.add(user)
		db.commit()
		db.refresh(user)

def init_db(db: Session) -> None:
	# Tables should be created with Alembic migrations
	# But if you don't want to use migrations, create
	# the tables un-commenting the next line
	Base.metadata.create_all(bind=engine)

	user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
	if not user:
		user_in = schemas.UserCreate(
			full_name=settings.FIRST_SUPERUSER_FULLNAME,
			email=settings.FIRST_SUPERUSER_EMAIL,
			password=settings.FIRST_SUPERUSER_PASSWORD,
			is_superuser=True,
		)
		user = crud.user.create(db, obj_in=user_in) # noqa: F841

	init_users(db)
	

def drop_db() -> None:
	Base.metadata.drop_all(bind=engine)