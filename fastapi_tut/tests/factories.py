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
from factory.alchemy import SQLAlchemyModelFactory

from fastapi_tut import models
from fastapi_tut.core.security import get_password_hash
from fastapi_tut.utils import fake
from fastapi_tut.db.session import TestSession

class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = TestSession()
        sqlalchemy_session_persistence = 'commit'

# Boiler
# 
# class ThisFactory(BaseFactory):
#     """ThisFactory"""

#     class Meta:
#         model = models.This

class RoleFactory(BaseFactory):
    """RoleFactory"""

    class Meta:
        model = models.Role

    id = random.choice(["Student", "Teacher"])

class UserFactory(BaseFactory):
    """User factory."""

    class Meta:
        model = models.User

    # full_name = factory.Sequence(lambda a: fake.name()) 
    # email = factory.Sequence(lambda a: fake.email())
    # password = factory.Sequence(lambda a: fake.password())
    full_name = factory.Faker('name') 
    email = factory.Faker('email')
    password = factory.Faker('password')
    hashed_password = factory.LazyAttribute(lambda a: get_password_hash(a.password))

# class QuizFactory(BaseFactory):
#     """Quiz factory."""


