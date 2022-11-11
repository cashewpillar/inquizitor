import html
import logging
import random
import requests
from sqlmodel import Session, SQLModel
from sqlalchemy.engine import Engine

from inquizitor import crud, models
from inquizitor.core.config import settings
from inquizitor.db import base  # noqa: F401
from inquizitor.models.user import UserCreate
from inquizitor.utils import fake
from inquizitor.tests.factories import (
    ActionFactory,
    AnswerFactory,
    QuizFactory,
    QuestionFactory,
    ChoiceFactory,
    UserFactory,
)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

ALTER_FUNCTIONS = [str.upper, str.capitalize, str.lower, str.title]

def init_users(db: Session, secure_first_users: bool = False) -> None:
    superuser = crud.user.get_by_username(
        db, username=settings.FIRST_SUPERUSER_USERNAME
    )
    SUPERPASS = settings.SUPERUSER_PASSWORD if secure_first_users else 'secret'
    if not superuser:
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=SUPERPASS if secure_first_users else settings.FIRST_SUPERUSER_PASSWORD,
            last_name=settings.FIRST_SUPERUSER_LASTNAME,
            first_name=settings.FIRST_SUPERUSER_FIRSTNAME,
            is_superuser=True,
            is_teacher=True,
            is_student=False,
        )
        superuser = crud.user.create(db, obj_in=user_in)  # noqa: F841
    
    first_student = crud.user.get_by_email(db, email=settings.FIRST_STUDENT_EMAIL)
    if not first_student:
        user_in = UserCreate(
            username="student",
            email=settings.FIRST_STUDENT_EMAIL,
            password=SUPERPASS if secure_first_users else settings.FIRST_STUDENT_PASSWORD,
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
            password=SUPERPASS if secure_first_users else settings.FIRST_TEACHER_PASSWORD,
            last_name=settings.FIRST_TEACHER_LASTNAME,
            first_name=settings.FIRST_TEACHER_FIRSTNAME,
            is_superuser=False,
            is_teacher=True,
            is_student=False,
        )
        first_teacher = crud.user.create(db, obj_in=user_in)  # noqa: F841

def init_test_teachers(db: Session):
    global test_teachers
    test_teachers = [
        crud.user.get_by_email(db, email=settings.FIRST_TEACHER_EMAIL),
    ]
    for i in range(5):
        user_in = UserFactory.stub(schema_type="create", is_teacher=True, password="testteacher")
        user_in = models.UserCreate(**user_in)
        user = crud.user.create(db, obj_in=user_in)
        test_teachers.append(user)

    return test_teachers

def init_test_students(db: Session):
    global test_students
    test_students = [
        crud.user.get_by_email(db, email=settings.FIRST_STUDENT_EMAIL),
    ]
    for i in range(10):
        user_in = UserFactory.stub(schema_type="create", is_student=True, password="teststudent")
        user_in = models.UserCreate(**user_in)
        user = crud.user.create(db, obj_in=user_in)
        test_students.append(user)

    return test_students

def init_db(
    db: Session, 
    engine: Engine, 
    use_realistic_data: bool = False, 
    no_quizzes: bool = False, 
    has_attempts: bool = True,
    secure_first_users: bool = False
) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    SQLModel.metadata.create_all(bind=engine)

    # Example: init_db(db = SessionLocal(), engine)

    init_users(db, secure_first_users=secure_first_users)
    if not no_quizzes:
        generate_quizzes(db, use_realistic_data=use_realistic_data, has_attempts=has_attempts)

def drop_db(engine: Engine) -> None:
    SQLModel.metadata.drop_all(bind=engine)

def generate_attempts(db: Session, quiz: models.Quiz):
    for student in test_students:
        quiz_student_link_in = models.QuizStudentLinkCreate(
            student_id=student.id,
            quiz_id=quiz.id,
        )
        quiz_attempt_in = models.QuizAttemptCreate(
            student_id=student.id, quiz_id=quiz.id, is_done=True
        )
        link = crud.quiz_student_link.create(db, obj_in=quiz_student_link_in)
        attempt = crud.quiz_attempt.create(db, obj_in=quiz_attempt_in)

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

            # add a random number of input device actions
            for i in range(random.randint(3,15)): 
                action_in = ActionFactory.stub(
                    schema_type="create", attempt=attempt, question=question
                )
                action = crud.quiz_action.create(db, obj_in=action_in)

def generate_quizzes(
    db: Session, use_realistic_data: bool = False, has_attempts: bool = True
) -> None:
    NUM_QUESTIONS = 5
    init_test_teachers(db)
    init_test_students(db)
    teacher_set = list(test_teachers)

    for i in range(50): # fifty quizzes
        logging.info(f"Generating quiz #{i+1}")
        realistic_data = []
        if use_realistic_data:
            category = random.randint(9, 32) # available range of categories, see https://opentdb.com/api_config.php
            while not realistic_data:
                realistic_data = requests.get(
                    f'https://opentdb.com/api.php?amount={NUM_QUESTIONS}&type=multiple&category={category}'
                ).json()['results']

                for q in realistic_data: # fill in incomplete values for standard initial data structure
                    if type(q['correct_answer']) != type('str'):
                        q['correct_answer'] = fake.word()
                    if type(q['incorrect_answers']) != type([list]):
                        q['incorrect_answers'] = [fake.word() for i in range(4)]
                    if len(q['incorrect_answers']) < 4:
                        for i in range(4 - len(q['incorrect_answers'])):
                            q['incorrect_answers'].append(fake.word())

        if not len(teacher_set):
            teacher_set = list(test_teachers)
        
        quiz_in = QuizFactory.stub(
            schema_type="create",
            teacher=teacher_set.pop(),
            number_of_questions=NUM_QUESTIONS,
        )
        quiz_in['name'] = html.unescape(realistic_data[0]['category']) if use_realistic_data else quiz_in['name']
        quiz_in = models.QuizCreate(**quiz_in)
        quiz = crud.quiz.create(db, obj_in=quiz_in)

        for i in range(NUM_QUESTIONS): # use set amount of questions
            question_in = QuestionFactory.stub(
                schema_type="create", 
                points=1,
                quiz=quiz,
            )
            question_in['content'] = html.unescape(realistic_data[i]['question']) if use_realistic_data else question_in['content']
            question = crud.quiz_question.create(db, obj_in=question_in)

            index_correct = random.randrange(0, 4)
            for j in range(4): # four choices/ options OR accepted answers for fill-in-the-blanks
                choice_in = ChoiceFactory.stub(
                    schema_type="create", 
                    question=question,
                )

                if question.question_type == models.QuestionType.blank:
                    if use_realistic_data:
                        choice_in['content'] = ALTER_FUNCTIONS[j](realistic_data[i]['correct_answer'])
                    choice_in['is_correct'] = True
                elif question.question_type == models.QuestionType.choice:
                    if j == index_correct:
                        choice_in['is_correct'] = True
                        if use_realistic_data:
                            choice_in['content'] = realistic_data[i]['correct_answer']
                    else:
                        if use_realistic_data:
                            choice_in['content'] = realistic_data[i]['incorrect_answers'].pop()

                choice_in['content'] = html.unescape(choice_in['content'])
                choice = crud.quiz_choice.create(db, obj_in=choice_in)

        if has_attempts and quiz.id % 2 == 0: # even numbered quiz ids are answered by test students as initialized above
            generate_attempts(db, quiz)

def add_quiz(
    db: Session, dict_quiz: dict, has_attempts: bool = False, blanks_case_sensitive: bool = True
) -> None:
    assert type(dict_quiz) == dict
    first_superuser = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)

    quiz_in = QuizFactory.stub(
        schema_type="create",
        name=dict_quiz.setdefault('name', ''),
        desc=dict_quiz.setdefault('desc', ''),
        number_of_questions=len(dict_quiz['items']),
        teacher_id=first_superuser.id,
    )
    quiz_in = models.QuizCreate(**quiz_in)
    quiz = crud.quiz.create(db, obj_in=quiz_in)
    for i, item in enumerate(dict_quiz['items']):
        question_in = QuestionFactory.stub(
            schema_type="create", 
            content=item['question'],
            points=1,
            order=i,
            quiz_id=quiz.id,
            question_type=item['question_type']
        )
        question = crud.quiz_question.create(db, obj_in=question_in)

        if question.question_type == models.QuestionType.blank:
            answers = [item['correct_answer']] if blanks_case_sensitive else [ALTER_FUNCTIONS[i](item['correct_answer']) for i in range(len(ALTER_FUNCTIONS))]
            for answer in answers:
                choice_in = ChoiceFactory.stub(
                    schema_type="create", 
                    content=answer,
                    is_correct=True,
                    question_id=question.id,
                )
                crud.quiz_choice.create(db, obj_in=choice_in)
        elif question.question_type == models.QuestionType.choice:
            for j, choice in enumerate([item['correct_answer'],] + item['incorrect_answers']):
                choice_in = ChoiceFactory.stub(
                    schema_type="create", 
                    content=choice,
                    is_correct=True if j == 0 else False,
                    question_id=question.id,
                )
                crud.quiz_choice.create(db, obj_in=choice_in)

    if has_attempts:
        generate_attempts(db, quiz)