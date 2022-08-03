import html
import logging
import random
import requests
from pprint import pformat
from sqlmodel import Session
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel
from fastapi.encoders import jsonable_encoder

from inquizitor import crud, models
from inquizitor.core.config import settings
from inquizitor.core.security import get_password_hash
from inquizitor.db import base  # noqa: F401
from inquizitor.models.user import UserCreate
from inquizitor.tests.factories import (
    AnswerFactory,
    QuizFactory,
    QuestionFactory,
    ChoiceFactory,
    UserFactory,
)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_users(db: Session) -> None:
    first_student = crud.user.get_by_email(db, email=settings.FIRST_STUDENT_EMAIL)
    if not first_student:
        user_in = UserCreate(
            username="student",
            email=settings.FIRST_STUDENT_EMAIL,
            password=settings.FIRST_STUDENT_PASSWORD,
            last_name=settings.FIRST_STUDENT_LASTNAME,
            first_name=settings.FIRST_STUDENT_FIRSTNAME,
            is_superuser=False,
            is_teacher=False,
            is_student=True,
        )
        first_student = crud.user.create(db, obj_in=user_in)  # noqa: F841

    first_teacher = crud.user.get_by_email(db, email=settings.FIRST_TEACHER_EMAIL)
    if not first_teacher:
        user_in = UserCreate(
            username="teacher",
            email=settings.FIRST_TEACHER_EMAIL,
            password=settings.FIRST_TEACHER_PASSWORD,
            last_name=settings.FIRST_TEACHER_LASTNAME,
            first_name=settings.FIRST_TEACHER_FIRSTNAME,
            is_superuser=False,
            is_teacher=True,
            is_student=False,
        )
        first_teacher = crud.user.create(db, obj_in=user_in)  # noqa: F841


def init_test_students(db: Session):
    test_students = [
        crud.user.get_by_email(db, email=settings.FIRST_STUDENT_EMAIL),
    ]
    for i in range(3):
        user_in = UserFactory.stub(schema_type="create", is_student=True)
        user_in = models.UserCreate(**user_in)
        user = crud.user.create(db, obj_in=user_in)
        test_students.append(user)

    return test_students


def dummy_quiz(db: Session, use_realistic_data: bool = False) -> None:
    NUM_QUESTIONS = 5
    test_students = init_test_students(db)
    first_teacher = crud.user.get_by_email(db, email=settings.FIRST_TEACHER_EMAIL)

    for i in range(10):
        realistic_data = list()
        if use_realistic_data:
            category = random.randint(9, 32) # available range of categories, see https://opentdb.com/api_config.php
            while not realistic_data:
                realistic_data = requests.get(
                    f'https://opentdb.com/api.php?amount={NUM_QUESTIONS}&type=multiple&category={category}'
                ).json()['results']

        quiz_in = QuizFactory.stub(
            schema_type="create",
            teacher=first_teacher,
            number_of_questions=NUM_QUESTIONS,
        )
        quiz_in['name'] = html.unescape(realistic_data[0]['category']) if use_realistic_data else quiz_in['name']
        quiz_in = models.QuizCreate(**quiz_in)
        quiz = crud.quiz.create(db, obj_in=quiz_in)

        for i in range(NUM_QUESTIONS):
            question_in = QuestionFactory.stub(
                schema_type="create", 
                quiz=quiz,
            )
            question_in['content'] = html.unescape(realistic_data[i]['question']) if use_realistic_data else question_in['content']
            question = crud.quiz_question.create(db, obj_in=question_in)

            index_correct = random.randrange(0, 4)
            for j in range(4):
                choice_in = ChoiceFactory.stub(
                    schema_type="create", 
                    question=question,
                )
                if j == index_correct:
                    choice_in['is_correct'] = True
                    if use_realistic_data:
                        choice_in['content'] = realistic_data[i]['correct_answer']
                else:
                    if use_realistic_data:
                        choice_in['content'] = realistic_data[i]['incorrect_answers'].pop()
                choice_in['content'] = html.unescape(choice_in['content'])
                # choice_in['content'] # required to call, bcs for some choice_in does not get updated
                choice = crud.quiz_choice.create(db, obj_in=choice_in)

        if quiz.id % 2 == 0:
            for student in test_students:
                user = UserFactory
                # First student accesses half the dummy quizzes
                quiz_student_link_in = models.QuizStudentLinkCreate(
                    student_id=student.id,
                    quiz_id=quiz.id,
                )
                quiz_attempt_in = models.QuizAttemptCreate(
                    student_id=student.id, quiz_id=quiz.id, is_done=True
                )
                link = crud.quiz_student_link.create(db, obj_in=quiz_student_link_in)
                attempt = crud.quiz_attempt.create(db, obj_in=quiz_attempt_in)

                # First student answers
                for question in quiz.questions:
                    choice = random.choices(question.choices)[0]
                    answer_in = AnswerFactory.stub(
                        schema_type="create",
                        content=choice.content,
                        student=student,
                        choice=choice,
                        attempt=attempt,
                        question=question,
                    )
                    answer = crud.quiz_answer.create(db, obj_in=answer_in)


def init_db(db: Session, engine: Engine, use_realistic_data: bool = False) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    SQLModel.metadata.create_all(bind=engine)

    # Example: init_db(db = SessionLocal(), engine)

    superuser = crud.user.get_by_username(
        db, username=settings.FIRST_SUPERUSER_USERNAME
    )
    if not superuser:
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            last_name=settings.FIRST_SUPERUSER_LASTNAME,
            first_name=settings.FIRST_SUPERUSER_FIRSTNAME,
            is_superuser=True,
            is_teacher=True,
            is_student=False,
        )
        superuser = crud.user.create(db, obj_in=user_in)  # noqa: F841

    init_users(db)
    dummy_quiz(db, use_realistic_data=use_realistic_data)


def drop_db(engine: Engine) -> None:
    SQLModel.metadata.drop_all(bind=engine)
