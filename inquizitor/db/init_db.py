import logging
import random
from pprint import pformat
from sqlmodel import Session 
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel
from fastapi.encoders import jsonable_encoder

from inquizitor import crud, models
from inquizitor.core.config import settings
from inquizitor.core.security import get_password_hash
from inquizitor.db import base # noqa: F401
from inquizitor.models.user import UserCreate
from inquizitor.tests.factories import (
	AnswerFactory, QuizFactory, QuestionFactory, ChoiceFactory
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
		first_student = crud.user.create(db, obj_in=user_in) # noqa: F841

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
		first_teacher = crud.user.create(db, obj_in=user_in) # noqa: F841


def dummy_quiz(db: Session) -> None:
	first_teacher = crud.user.get_by_email(db, email=settings.FIRST_TEACHER_EMAIL)
	first_student = crud.user.get_by_email(db, email=settings.FIRST_STUDENT_EMAIL)
	NUM_QUESTIONS = 5
	for i in range(10):
		quiz_in = QuizFactory.stub(
			schema_type="create", 
			teacher=first_teacher, 
			number_of_questions=NUM_QUESTIONS
		)
		quiz_in = models.QuizCreate(**quiz_in)
		quiz = crud.quiz.create(db, obj_in=quiz_in)

		for i in range(NUM_QUESTIONS):
			question_in = QuestionFactory.stub(schema_type="create", quiz=quiz)
			question = crud.quiz_question.create(db, obj_in=question_in)

			index_correct = random.randrange(0, 4)
			for i in range(4):
				choice_in = ChoiceFactory.stub(schema_type="create", question=question)
				if i == index_correct:
					choice_in["is_correct"] = True
				choice = crud.quiz_choice.create(db, obj_in=choice_in)

		if quiz.id % 2 == 0:
			# First student accesses half the dummy quizzes
			quiz_student_link_in = models.QuizStudentLinkCreate(
				student_id=first_student.id,	
				quiz_id=quiz.id,
			)
			quiz_attempt_in = models.QuizAttemptCreate(
				student_id=first_student.id,	
				quiz_id=quiz.id,
			)
			link = crud.quiz_student_link.create(db, obj_in=quiz_student_link_in)
			attempt = crud.quiz_attempt.create(db, obj_in=quiz_attempt_in)

			# First student answers
			for question in quiz.questions:
				choice = random.choices(question.choices)[0]
				answer_in = AnswerFactory.stub(
					schema_type="create", 
					content=choice.content, 
					student=first_student, 
					choice=choice,
					attempt=attempt,
					question=question
				)
				answer = crud.quiz_answer.create(db, obj_in=answer_in)


def init_db(db: Session, engine: Engine) -> None:
	# Tables should be created with Alembic migrations
	# But if you don't want to use migrations, create
	# the tables un-commenting the next line
	SQLModel.metadata.create_all(bind=engine)

	# Example: init_db(db = SessionLocal(), engine) 
	
	superuser = crud.user.get_by_username(db, username=settings.FIRST_SUPERUSER_USERNAME)
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
		superuser = crud.user.create(db, obj_in=user_in) # noqa: F841	

	init_users(db)
	dummy_quiz(db)
	

def drop_db(engine: Engine) -> None:
	SQLModel.metadata.drop_all(bind=engine)