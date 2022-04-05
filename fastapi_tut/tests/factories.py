"""
Factories to help in tests.
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

class UserFactory(BaseFactory):
    """User factory."""

    class Meta:
        model = models.User

    full_name = factory.Faker('name') 
    email = factory.Faker('email')
    password = factory.Faker('password')
    hashed_password = factory.LazyAttribute(lambda a: get_password_hash(a.password))

# class QuizFactory(BaseFactory):
#     """Quiz factory."""


