# TODO setup database for tests, also configure app factory for tests

import pytest
from typing import Dict, Generator

from sqlalchemy.orm import Session

from fastapi_tut import create_app, crud
from fastapi_tut.utils import fake_user
from fastapi_tut.db.session import SessionLocal
from fastapi_tut.tests.utils.utils import get_superuser_token_headers
from fastapi_tut.schemas.user import UserCreate

@pytest.fixture(scope="session")
def db() -> Generator:
	yield SessionLocal()

@pytest.fixture(scope="module")
def app():
	"""Create application for the tests"""
	_app = create_app()
	yield _app

@pytest.fixture
def user(db: Session):
	"""Create user for the tests"""
	data = fake_user()
	user_in = UserCreate(**data)
	user = crud.user.create(db, obj_in=user_in)
	return user

@pytest.fixture
def superuser_token_headers(app) -> Dict[str, str]:
	return get_superuser_token_headers(app)
