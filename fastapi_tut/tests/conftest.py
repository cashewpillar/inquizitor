from httpx import AsyncClient
from typing import Dict, Generator, List

import pytest
import random

from fastapi import FastAPI
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from fastapi_tut import create_app, crud, models, utils
from fastapi_tut.tests import common
from fastapi_tut.api.deps import get_db
from fastapi_tut.db.init_db import init_db, drop_db
from fastapi_tut.db.session import TestSession, test_engine
from fastapi_tut.tests import common
from fastapi_tut.tests.utils.utils import (
	get_superuser_cookies,
)

@pytest.fixture(scope="session")
def db() -> Generator:
	"""Create database for the tests."""

	# https://factoryboy.readthedocs.io/en/v2.6.1/orms.html#managing-sessions
	common.Session.configure(bind=test_engine)
	init_db(common.Session(), test_engine)

	yield common.Session()

	# Rollback the session => no changes to the database
	common.Session.rollback()
	# Remove it, so that the next test gets a new Session()
	common.Session.remove()

@pytest.fixture(scope="module")
def app(db: Session):
	"""Create application for the tests"""
	_app = create_app(db)
	yield _app



@pytest.fixture
@pytest.mark.anyio
async def client(app: FastAPI, db: Session) -> Generator:
	"""Client for making asynchronous requests (?)"""
	# See https://fastapi.tiangolo.com/advanced/async-tests/
	def get_session_override():
		return db

	app.dependency_overrides[get_db] = get_session_override
	async with AsyncClient(app=app, base_url="http://test") as ac:
		yield ac
	app.dependency_overrides.clear()



@pytest.fixture
def user(db: Session) -> models.User:
	"""Create user for the tests"""
	data = utils.fake_user()
	user_in = models.UserCreate(**data)
	user = crud.user.create(db, obj_in=user_in)
	return user

@pytest.fixture
def superuser_cookies(app: FastAPI) -> Dict[str, str]:
	return get_superuser_cookies(app)