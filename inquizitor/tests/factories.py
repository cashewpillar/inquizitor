import datetime as dt
import factory
import random
from factory.alchemy import SQLAlchemyModelFactory
from typing import List, Optional, Union

from fastapi.encoders import jsonable_encoder

from inquizitor import models
from inquizitor.crud.base import CreateSchemaType, ModelType, UpdateSchemaType
from inquizitor.core.security import get_password_hash
from inquizitor.db.session import TestSession
from inquizitor.utils import fake, random_str
from inquizitor.tests import common

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
        sqlalchemy_session_persistence = "commit"

    # custom override to get dict values based on model
    # might also override stub_batch depending on test cases
    @classmethod
    def stub(cls, schema_type: Union["create", "update"] = None, **kwargs):
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

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    full_name = factory.Faker("name")
    last_name = factory.Faker("last_name")
    first_name = factory.Faker("first_name")
    password = factory.Faker("password")
    hashed_password = factory.LazyAttribute(lambda a: get_password_hash(a.password))
    is_student = False
    is_teacher = False

    model: ModelType = models.User
    create_schema: CreateSchemaType = models.UserCreate
    update_schema: UpdateSchemaType = models.UserUpdate


class QuizFactory(BaseFactory):
    """Quiz factory."""

    class Meta:
        model = models.Quiz

    class Params:
        # TODO
        # students: Optional[List[models.User]] = factory.SubFactory(UserFactory)
        teacher: models.User = factory.SubFactory(UserFactory)
        questions: Optional[List[models.QuizQuestion]] = []
        attempts: Optional[List[models.QuizAttempt]] = []

    name = factory.Faker("word")
    desc = factory.Faker("text")
    number_of_questions = factory.Faker("random_int", min=10, max=100, step=10)
    created_at = factory.LazyFunction(dt.datetime.now)
    due_date = factory.LazyAttribute(lambda a: a.created_at + dt.timedelta(hours=5))
    quiz_code = None
    # time_limit: int = factory.Faker("random_int", min=30*60, max=60*60, step=5*60)
    teacher_id: int = factory.LazyAttribute(
        lambda a: a.teacher.id if a.teacher is not None else None
    )

    model: ModelType = models.Quiz
    create_schema: CreateSchemaType = models.QuizCreate
    update_schema: UpdateSchemaType = models.QuizUpdate


class QuestionFactory(BaseFactory):
    """Question factory."""

    class Meta:
        model = models.QuizQuestion

    class Params:
        quiz: models.Quiz = factory.SubFactory(QuizFactory)

    content: str = factory.LazyAttribute(lambda a: fake.sentence().replace(".", "?"))
    points: int = factory.Faker("random_int", min=1, max=5)
    order: int = factory.Sequence(lambda n: n)
    quiz_id: int = factory.LazyAttribute(
        lambda a: a.quiz.id if a.quiz is not None else None
    )

    model: ModelType = models.QuizQuestion
    create_schema: CreateSchemaType = models.QuizQuestionCreate
    update_schema: UpdateSchemaType = models.QuizQuestionUpdate


class ChoiceFactory(BaseFactory):
    """Choice factory."""

    class Meta:
        model = models.QuizChoice

    class Params:
        question: models.QuizQuestion = factory.SubFactory(QuestionFactory)

    content: str = factory.Faker("word")
    is_correct: bool = False
    question_id: int = factory.LazyAttribute(
        lambda a: a.question.id if a.question is not None else None
    )

    model: ModelType = models.QuizChoice
    create_schema: CreateSchemaType = models.QuizChoiceCreate
    update_schema: UpdateSchemaType = models.QuizChoiceUpdate


class AttemptFactory(BaseFactory):
    """Attempt factory."""

    class Meta:
        model = models.QuizAttempt

    class Params:
        recent_question: models.QuizQuestion = factory.SubFactory(QuestionFactory)
        student: models.User = factory.SubFactory(UserFactory)
        quiz: models.User = factory.SubFactory(QuizFactory)
        answers: Optional[List[models.QuizAnswer]] = []

    is_done: bool = False
    recent_question_id: int = factory.LazyAttribute(
        lambda a: a.recent_question.id if a.recent_question is not None else None
    )
    student_id: int = factory.LazyAttribute(
        lambda a: a.student.id if a.student is not None else None
    )
    quiz_id: int = factory.LazyAttribute(
        lambda a: a.quiz.id if a.quiz is not None else None
    )
    started_at = factory.LazyFunction(dt.datetime.now)

    model: ModelType = models.QuizAttempt
    create_schema: CreateSchemaType = models.QuizAttemptCreate
    update_schema: UpdateSchemaType = models.QuizAttemptUpdate


class AnswerFactory(BaseFactory):
    """Answer factory."""

    class Meta:
        model = models.QuizAnswer

    class Params:
        choice: models.QuizChoice = factory.SubFactory(ChoiceFactory)
        student: models.User = factory.SubFactory(UserFactory)
        attempt: models.QuizAttempt = factory.SubFactory(AttemptFactory)
        question: models.QuizQuestion = factory.SubFactory(QuestionFactory)

    content: str = factory.LazyAttribute(lambda a: a.choice.content)
    is_correct: bool = factory.LazyAttribute(lambda a: a.choice.is_correct)
    choice_id: int = factory.LazyAttribute(
        lambda a: a.choice.id if a.choice is not None else None
    )
    student_id: int = factory.LazyAttribute(
        lambda a: a.student.id if a.student is not None else None
    )
    attempt_id: int = factory.LazyAttribute(
        lambda a: a.attempt.id if a.attempt is not None else None
    )
    question_id: int = factory.LazyAttribute(
        lambda a: a.question.id if a.question is not None else None
    )

    model: ModelType = models.QuizAnswer
    create_schema: CreateSchemaType = models.QuizAnswerCreate
    update_schema: UpdateSchemaType = models.QuizAnswerUpdate
