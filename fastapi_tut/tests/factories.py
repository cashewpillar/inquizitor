"""
Factories to help in tests.
"""

import datetime as dt
import factory
import random
from factory.alchemy import SQLAlchemyModelFactory
from typing import List, Optional, Union

from fastapi.encoders import jsonable_encoder

from fastapi_tut import models
from fastapi_tut.crud.base import CreateSchemaType, ModelType, UpdateSchemaType
from fastapi_tut.core.security import get_password_hash
from fastapi_tut.db.session import TestSession
from fastapi_tut.utils import fake, random_str
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


# TODO for update: check new attributes
class UserFactory(BaseFactory):
    """User factory."""

    class Meta:
        model = models.User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    full_name = factory.Faker('name') 
    last_name = factory.Faker('last_name') 
    first_name = factory.Faker('first_name') 
    password = factory.Faker('password')
    hashed_password = factory.LazyAttribute(lambda a: get_password_hash(a.password))

    model: ModelType = models.User
    create_schema: CreateSchemaType = models.UserCreate
    update_schema: UpdateSchemaType = models.UserUpdate

class QuizFactory(BaseFactory):
    """Quiz factory."""

    class Meta:
        model = models.Quiz

    name = factory.Faker('word')
    desc = factory.Faker('text')
    number_of_questions = factory.Faker("random_int", min=10, max=100, step=10)
    created_at = factory.LazyFunction(dt.datetime.utcnow)
    due_date = factory.LazyAttribute(lambda a: a.created_at + dt.timedelta(hours=5))
    quiz_code = factory.LazyFunction(random_str)
    # time_limit: int = factory.Faker("random_int", min=30*60, max=60*60, step=5*60)

    teacher: models.User = factory.SubFactory(UserFactory)
    # TODO
    # students: Optional[List[models.User]] = factory.SubFactory(UserFactory)
    questions: Optional[List[models.QuizQuestion]] = []
    attempts: Optional[List[models.QuizAttempt]] = []

    teacher_id: int = factory.LazyAttribute(lambda a: a.teacher.id if a.teacher is not None else None)
    
    model: ModelType = models.Quiz
    create_schema: CreateSchemaType = models.QuizCreate
    update_schema: UpdateSchemaType = models.QuizUpdate


