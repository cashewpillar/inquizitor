# TODO use factories instead of fixtures

from typing import List
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from fastapi_tut import crud, models
from fastapi_tut.core.security import verify_password
from fastapi_tut.models.user import UserCreate, UserUpdate
from fastapi_tut.utils import fake, fake_user
from fastapi_tut.tests.factories import UserFactory

def test_create_user(db: Session) -> None:
	data = fake_user()
	user_in = UserCreate(**data)
	user = crud.user.create(db, obj_in=user_in)
	assert user.username == data["username"]
	assert hasattr(user, "hashed_password")

def test_authenticate_user(db: Session) -> None:
	data = fake_user()
	user_in = UserCreate(**data)
	user = crud.user.create(db, obj_in=user_in)
	authenticated_user = crud.user.authenticate(db, username=data["username"], password=data["password"])
	assert authenticated_user
	assert data["username"] == authenticated_user.username

def test_not_authenticate_user(db: Session) -> None:
	data = fake_user()
	user = crud.user.authenticate(db, username=data["username"], password=data["password"])
	assert user is None

def test_check_if_user_is_superuser(db: Session, user: models.User) -> None:
	data = fake_user(**{"is_superuser": True})
	user_in = UserCreate(**data)
	user = crud.user.create(db, obj_in=user_in)
	is_superuser = crud.user.is_superuser(user)
	assert is_superuser is True

def test_check_if_user_is_superuser_normal_user(db: Session) -> None:
	user = UserFactory()
	is_superuser = crud.user.is_superuser(user)
	assert is_superuser is False

def test_get_user(db: Session) -> None:
	user = UserFactory()
	user_2 = crud.user.get(db, id=user.id)
	assert user_2
	assert user.username == user_2.username
	assert jsonable_encoder(user) == jsonable_encoder(user_2)

# TODO rename the model marks of user first, relationship attributes here
# def test_get_user_relations(db: Session, user: models.User, marks_of_users: List[models.MarksOfUser]) -> None:
# 	pass

def test_update_user(db: Session) -> None:
	user = UserFactory()
	repr(user)
	new_password = fake.password()
	user_in_update = UserUpdate(password=new_password)
	crud.user.update(db, db_obj=user, obj_in=user_in_update)
	user_2 = crud.user.get(db, id=user.id)
	assert user_2
	assert user.username == user_2.username
	assert verify_password(new_password, user_2.hashed_password)