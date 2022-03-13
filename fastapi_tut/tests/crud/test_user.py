import logging
import pytest
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from sqlmodel import Session

from fastapi_tut import crud, models
from fastapi_tut.db.session import test_engine
from fastapi_tut.db.init_db import init_db
from fastapi_tut.models.user import UserCreate, UserUpdate
from fastapi_tut.tests.factories import RoleFactory, UserFactory
from fastapi_tut.utils import fake, fake_user

logging.basicConfig(level=logging.INFO)

class TestUserFactory:
	def setUp(self, db: Session):
		init_db(db, test_engine)

	def test_initial_data(self, db: Session):
		user_2 = crud.user.get(db, id=2) # user-1 is admin
		student_role = crud.role.get(db, id="student")
		teacher_role = crud.role.get(db, id="Teacher")
		assert user_2
		assert user_2.role
		assert student_role
		assert teacher_role

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

class TestRole:
	def test_create_role(self, db: Session) -> None:
		name = "Role-rcoaster"
		role_in = models.RoleCreate(id=name)
		role = crud.role.create(db, obj_in=role_in)
		assert role.id == name

	def test_get_role(self, db: Session) -> None:
		role = RoleFactory(id="Russian-Role-ette")
		role_in_db = crud.role.get(db, id=role.id)
		assert role_in_db
		assert role.id == role_in_db.id
		assert jsonable_encoder(role) == jsonable_encoder(role_in_db)

	def test_update_role(self, db: Session) -> None:
		role = RoleFactory()
		data = RoleFactory.stub(schema_type="update")
		role_in_update = models.RoleUpdate(**data)
		# NOTE i have to call a function on the role object 
		# or get an attribute before the object can be used as a Role instance
		# in the update call below 
		# https://github.com/FactoryBoy/factory_boy/issues/913
		repr(role)
		crud.role.update(db, db_obj=role, obj_in=role_in_update)
		role_in_db = crud.role.get(db, id=role.id)
		assert role_in_db.id == role_in_update.id

class TestUser:
	def test_create_user(self, db: Session) -> None:
		data = UserFactory.stub(schema_type="create", password="secret")
		user_in = UserCreate(**data)
		user = crud.user.create(db, obj_in=user_in)
		assert crud.user.authenticate(db, email=data["email"], password=data["password"])
		assert user.email == data["email"]
		assert hasattr(user, "hashed_password")

	def test_authenticate_user(self, db: Session) -> None:
		data = UserFactory.stub(schema_type="create", password="secret")
		user = UserFactory(**data)
		authenticated_user = crud.user.authenticate(db, email=user.email, password=data["password"])
		assert authenticated_user
		assert user.email == authenticated_user.email

	def test_not_authenticate_user(self, db: Session) -> None:
		data = UserFactory.stub(schema_type="create", password="secret")
		user = crud.user.authenticate(db, email=data["email"], password=data["password"])
		assert user is None

	def test_check_if_user_is_superuser(self, db: Session) -> None:
		user = UserFactory(is_superuser=True)
		is_superuser = crud.user.is_superuser(user)
		assert is_superuser is True

	def test_check_if_user_is_superuser_normal_user(self, db: Session) -> None:
		user = UserFactory(is_superuser=False)
		is_superuser = crud.user.is_superuser(user)
		assert is_superuser is False

	def test_get_user(self, db: Session) -> None:
		user = UserFactory()
		user_in_db = crud.user.get(db, id=user.id)
		assert user_in_db
		assert user.email == user_in_db.email
		assert jsonable_encoder(user) == jsonable_encoder(user_in_db)

	# TODO add marks
	def test_get_user_relations(self, db: Session) -> None:
		teacher_role = crud.role.get(db, id="teacher")
		user = UserFactory(role=teacher_role)
		assert user.role 

	def test_update_user(self, db: Session) -> None:
		user = UserFactory()
		data = UserFactory.stub(schema_type="update")	
		user_in_update = UserUpdate(**data)
		repr(user)
		crud.user.update(db, db_obj=user, obj_in=user_in_update)
		user_in_db = crud.user.get(db, id=user.id)
		assert user_in_db
		assert user.email == user_in_db.email
		assert crud.user.authenticate(db, email=data["email"], password=data["password"])

class TestUserRole:
	def test_create_user_role(self, db: Session):
		student_role = crud.role.get(db, id="Student")
		user = UserFactory(role=student_role)
		assert user.role_id == student_role.id

	def test_add_user_role(self, db: Session):
		teacher_role = crud.role.get(db, id="teacher")
		user = UserFactory()
		user.role = teacher_role 

		user = crud.user.get(db, id=user.id)
		assert user.role == teacher_role

	def test_update_user_role(self, db: Session):
		student_role = crud.role.get(db, id="Student")
		user = UserFactory()
		data = UserFactory.stub(schema_type="update", role=student_role)
		user_in_update = UserUpdate(**data)
		repr(user)
		crud.user.update(db, db_obj=user, obj_in=user_in_update)
		user = crud.user.get(db, id=user.id)
		assert user.role == student_role