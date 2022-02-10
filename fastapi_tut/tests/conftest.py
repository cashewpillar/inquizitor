# TODO setup database for tests, also configure app factory for tests
# TODO BUT NOT URGENTO annotate the parameter 'app' of the client fixture

import pytest
from httpx import AsyncClient
from typing import Dict, Generator

from sqlalchemy.orm import Session

from fastapi_tut import create_app, crud, models
from fastapi_tut.utils import fake_user
from fastapi_tut.db.session import TestSession
from fastapi_tut.tests.utils.utils import (
	get_superuser_access_token_headers,
	get_superuser_refresh_token_headers,
)
from fastapi_tut.schemas.user import UserCreate

@pytest.fixture(scope="session")
def db() -> Generator:
	"""Create database for the tests."""
	yield TestSession()


@pytest.fixture(scope="module")
def app():
	"""Create application for the tests"""
	_app = create_app()
	yield _app


@pytest.fixture
@pytest.mark.anyio
async def client(app) -> Generator:
	"""Client for making asynchronous requests (?)"""
	# See https://fastapi.tiangolo.com/advanced/async-tests/
	async with AsyncClient(app=app, base_url="http://test") as ac:
		yield ac


@pytest.fixture
def user(db: Session) -> models.User:
	"""Create user for the tests"""
	data = fake_user()
	user_in = UserCreate(**data)
	user = crud.user.create(db, obj_in=user_in)
	return user


@pytest.fixture
def superuser_access_token_headers(app) -> Dict[str, str]:
	return get_superuser_access_token_headers(app)


@pytest.fixture
def superuser_refresh_token_headers(app) -> Dict[str, str]:
	return get_superuser_refresh_token_headers(app)