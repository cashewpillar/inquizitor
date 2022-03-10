import pytest
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from fastapi_tut import crud, models
from fastapi_tut.core.security import verify_password
from fastapi_tut.models.user import UserCreate, UserUpdate
from fastapi_tut.tests.factories import RoleFactory, UserFactory
from fastapi_tut.utils import fake, fake_user

# DOING
class TestUserFactory:
	def test_role_factory(self, db: Session):
		role = RoleFactory(id="RandomRole")
		role_in_db = crud.role.get(db, id=role.id)
		assert role_in_db.id
		assert not role_in_db.users

	def test_user_factory(self, db: Session):
		user = UserFactory(password="secret")
		user_in_db = crud.user.get(db, id=user.id)
		assert user_in_db.full_name
		assert user_in_db.email
		assert user_in_db.is_superuser is False
		assert user_in_db.role_id is None 
		assert user_in_db.email
		assert crud.user.authenticate(db, email=user_in_db.email, password="secret")


# DOING
@pytest.mark.skip(reason="will be using factories & haven't edited boilerplate")
class TestRole:
	pass
	# def test_create_role(self, db: Session) -> None:
	# 	name = random_str()
	# 	role_in = models.QuestionTypeCreate(name=name)
	# 	role = crud.role.create(db, obj_in=role_in)
	# 	assert role.name == name

	# def test_get_role(self, db: Session) -> None:
	# 	role_in = models.QuestionType(name=random_str())
	# 	role = crud.role.create(db, obj_in=role_in)
	# 	role_2 = crud.role.get(db, id=role.id)
	# 	assert role_2
	# 	assert role.name == role_2.name
	# 	assert jsonable_encoder(role) == jsonable_encoder(role_2)

	# def test_update_role(self, db: Session, role: models.QuestionType) -> None:
	# 	name = random_str()
	# 	role_in_update = models.QuestionTypeUpdate(name=name)
	# 	crud.role.update(db, db_obj=role, obj_in=role_in_update)
	# 	role_2 = crud.role.get(db, id=role.id)
	# 	assert role_2
	# 	assert role.name == role_2.name

class TestUser:
	def test_create_user(self, db: Session) -> None:
		data = fake_user()
		user_in = UserCreate(**data)
		user = crud.user.create(db, obj_in=user_in)
		assert user.email == data["email"]
		assert hasattr(user, "hashed_password")

	def test_authenticate_user(self, db: Session) -> None:
		data = fake_user()
		user_in = UserCreate(**data)
		user = crud.user.create(db, obj_in=user_in)
		authenticated_user = crud.user.authenticate(db, email=data["email"], password=data["password"])
		assert authenticated_user
		assert data["email"] == authenticated_user.email

	def test_not_authenticate_user(self, db: Session) -> None:
		data = fake_user()
		user = crud.user.authenticate(db, email=data["email"], password=data["password"])
		assert user is None

	def test_check_if_user_is_superuser(self, db: Session, user: models.User) -> None:
		data = fake_user(**{"is_superuser": True})
		user_in = UserCreate(**data)
		user = crud.user.create(db, obj_in=user_in)
		is_superuser = crud.user.is_superuser(user)
		assert is_superuser is True

	def test_check_if_user_is_superuser_normal_user(self, db: Session, user: models.User) -> None:
		is_superuser = crud.user.is_superuser(user)
		assert is_superuser is False

	def test_get_user(self, db: Session, user: models.User) -> None:
		user_2 = crud.user.get(db, id=user.id)
		assert user_2
		assert user.email == user_2.email
		assert jsonable_encoder(user) == jsonable_encoder(user_2)

	# DOING rename the model marks of user first
	# def test_get_user_relations(self, db: Session, user: models.User, marks_of_students: List[models.MarksOfStudent]) -> None:
		# assert user.marks == marks_of_students 

	def test_update_user(self, db: Session, user: models.User) -> None:
		new_password = fake.password()
		user_in_update = UserUpdate(password=new_password)
		crud.user.update(db, db_obj=user, obj_in=user_in_update)
		user_2 = crud.user.get(db, id=user.id)
		assert user_2
		assert user.email == user_2.email
		assert verify_password(new_password, user_2.hashed_password)