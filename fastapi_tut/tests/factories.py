"""
Factories to help in tests.

DOING
https://factoryboy.readthedocs.io/en/stable/introduction.html
https://factoryboy.readthedocs.io/en/stable/orms.html?highlight=sqlalchemy_session#sqlalchemy
https://factoryboy.readthedocs.io/en/stable/recipes.html
https://github.com/tiangolo/sqlmodel/issues/82
https://factoryboy.readthedocs.io/en/stable/index.html#reproducible-random-values
"""

import factory
import random
from fastapi.encoders import jsonable_encoder
from factory.alchemy import SQLAlchemyModelFactory
from typing import Any, Union

from fastapi_tut import models
from fastapi_tut.core.security import get_password_hash
from fastapi_tut.db.session import TestSession
from fastapi_tut.crud.base import CreateSchemaType, ModelType, UpdateSchemaType
from fastapi_tut.tests import common

# Boiler
# 
# class ThisFactory(BaseFactory):
#     """ThisFactory"""

#     class Meta:
#         model = models.This

class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = common.Session
        sqlalchemy_session_persistence = 'commit'

    # custom override to get dict values based on model
    # might also override stub_batch depending on test cases
    @classmethod
    def stub(cls, schema_type: Union["create", "update"] = None,**kwargs):
        if schema_type == "create":
            cls._meta.model = cls.create_schema
        elif schema_type == "update":
            cls._meta.model = cls.update_schema

        x = cls.build(**kwargs)
        cls._meta.model = cls.model
        return jsonable_encoder(x)

class RoleFactory(BaseFactory):
    """RoleFactory"""

    class Meta:
        model = models.Role

    id: str = factory.Faker('word')

    model: ModelType = models.Role
    create_schema: CreateSchemaType = models.RoleCreate
    update_schema: UpdateSchemaType = models.RoleUpdate

class UserFactory(BaseFactory):
    """User factory."""

    class Meta:
        model = models.User

    full_name: str = factory.Faker('name') 
    email: str = factory.Faker('email')
    password: str = factory.Faker('password')
    is_superuser: bool = False
    role: models.Role = None 

    role_id: str = factory.LazyAttribute(lambda a: a.role.id if a.role is not None else None)
    hashed_password: str = factory.LazyAttribute(lambda a: get_password_hash(a.password))

    model: ModelType = models.User
    create_schema: CreateSchemaType = models.UserCreate
    update_schema: UpdateSchemaType = models.UserUpdate

# class QuizFactory(BaseFactory):
#     """Quiz factory."""


