import datetime as dt
import logging
import random
from unicodedata import is_normalized
from inquizitor.crud.crud_quiz import question
import pytest
from httpx import AsyncClient
from pprint import pformat
from sqlmodel import Session
from typing import Dict
from fastapi.encoders import jsonable_encoder

from inquizitor import crud
from inquizitor.models import QuizActions
from inquizitor.tests.factories import (
    ActionFactory, AttemptFactory, QuestionFactory, QuizFactory, UserFactory
)
logging.basicConfig(level=logging.INFO)

@pytest.mark.anyio
class TestCreateAction:
    async def test_create_action_superuser(
        self, db: Session, client: AsyncClient, superuser_cookies: Dict[str, str]
    ) -> None:
        superuser_cookies = await superuser_cookies
        r = await client.get("/users/profile", cookies=superuser_cookies)
        result = r.json()
        user = crud.user.get(db, id=result["id"])
        attempt = AttemptFactory()
        question = QuestionFactory(quiz_id=attempt.quiz_id)
        action_in = ActionFactory.stub(schema_type="create", attempt=attempt, question=question)
        r = await client.post(
            f"/quizzes/{attempt.quiz_id}/questions/{question.id}/actions", 
            cookies=superuser_cookies, 
            json=action_in
        )
        result = r.json()
        assert r.status_code == 400

    async def test_create_action_teacher(
        self, db: Session, client: AsyncClient, teacher_cookies: Dict[str, str]
    ) -> None:
        teacher_cookies = await teacher_cookies
        r = await client.get("/users/profile", cookies=teacher_cookies)
        result = r.json()
        user = crud.user.get(db, id=result["id"])
        attempt = AttemptFactory()
        question = QuestionFactory(quiz_id=attempt.quiz_id)
        action_in = ActionFactory.stub(schema_type="create", attempt=attempt, question=question)
        r = await client.post(
            f"/quizzes/{attempt.quiz_id}/questions/{question.id}/actions", 
            cookies=teacher_cookies, 
            json=action_in
        )
        result = r.json()
        assert r.status_code == 400

    async def test_create_action_student(
        self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
    ) -> None:
        student_cookies = await student_cookies
        r = await client.get("/users/profile", cookies=student_cookies)
        result = r.json()
        user = crud.user.get(db, id=result["id"])
        attempt = AttemptFactory(student=user)
        question = QuestionFactory(quiz_id=attempt.quiz_id)
        action_in = ActionFactory.stub(schema_type="create", attempt=attempt, question=question)
        r = await client.post(
            f"/quizzes/{attempt.quiz_id}/questions/{question.id}/actions", 
            cookies=student_cookies, 
            json=action_in
        )
        result = r.json()
        assert r.status_code == 200
        assert result["time"] == action_in["time"]
        assert result["blur"] == action_in["blur"]
        assert result["focus"] == action_in["focus"]
        assert result["copy_"] == action_in["copy_"]
        assert result["paste"] == action_in["paste"]
        assert result["left_click"] == action_in["left_click"]
        assert result["right_click"] == action_in["right_click"]
        assert result["double_click"] == action_in["double_click"]

@pytest.mark.anyio
class TestReadQuestionActions:
    async def test_read_question_actions_students(
        self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
    ) -> None:
        question_actions = []
        quiz = QuizFactory()
        question = QuestionFactory(quiz=quiz)
        for i in range(3): # three students
            student = UserFactory(student=True)
            user = crud.user.get(db, id=student.id)
            attempt = AttemptFactory(quiz=quiz, student=user, is_done=True)
            actions = []
            for j in range(5): # five question actions each
                action = ActionFactory(attempt=attempt, question=question)
                action = jsonable_encoder(crud.quiz_action.get(db, id=action.id))
                actions.append(action)
            question_actions.append(
                {"student_id":user.id, "student_name":user.full_name, "actions":actions}
            )

        student_cookies = await student_cookies
        r = await client.get(
            f"/quizzes/{question.quiz_id}/questions/{question.id}/actions",
            cookies=student_cookies,
        )
        result = r.json()
        assert r.status_code == 400

    async def test_read_question_actions_teacher_superuser(
        self, db:Session, client: AsyncClient, teacher_cookies: Dict[str, str], superuser_cookies: Dict[str, str] 
    ) -> None:
        teacher_cookies = await teacher_cookies
        superuser_cookies = await superuser_cookies
        r = await client.get("/users/profile", cookies=teacher_cookies)
        result = r.json()
        teacher = crud.user.get(db, id=result["id"])
        quiz = QuizFactory(teacher=teacher)
        question = QuestionFactory(quiz=quiz)

        question_actions = []
        for i in range(3): # three students
            student = UserFactory(student=True)
            user = crud.user.get(db, id=student.id)
            attempt = AttemptFactory(quiz=quiz, student=user, is_done=True)
            actions = []
            for j in range(5): # five question actions each
                action = ActionFactory(attempt=attempt, question=question)
                action = jsonable_encoder(crud.quiz_action.get(db, id=action.id))
                actions.append(action)
            question_actions.append(
                {"actions":actions, "student_id":user.id, "student_name":user.full_name}
            )

        r = await client.get(
            f"/quizzes/{question.quiz_id}/questions/{question.id}/actions",
            cookies=teacher_cookies,
        )
        result = r.json()
        assert r.status_code == 200
        student_ids = [student["student_id"] for student in question_actions]
        student_names = [student["student_name"] for student in question_actions]
        actions = {student["student_id"]: student["actions"] for student in question_actions}
        for student_in_db in result:
            assert student_in_db["student_id"] in student_ids
            assert student_in_db["student_name"] in student_names
            for action_in_db in student_in_db["actions"]:
                assert action_in_db in actions[student_in_db["student_id"]]

        r = await client.get(
            f"/quizzes/{question.quiz_id}/questions/{question.id}/actions",
            cookies=superuser_cookies,
        )
        result = r.json()
        assert r.status_code == 200
        for student_in_db in result:
            assert student_in_db["student_id"] in student_ids
            assert student_in_db["student_name"] in student_names
            for action_in_db in student_in_db["actions"]:
                assert action_in_db in actions[student_in_db["student_id"]]

@pytest.mark.anyio
class TestReadQuizActions:
    async def test_read_quiz_actions_students(
        self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
    ) -> None:
        quiz_actions = []
        quiz = QuizFactory()
        questions = [QuestionFactory(quiz=quiz) for i in range(3)]
        for i in range(3): # three students
            student = UserFactory(student=True)
            user = crud.user.get(db, id=student.id)
            attempt = AttemptFactory(quiz=quiz, student=user, is_done=True)
            actions = []
            for q in questions:
                for j in range(3): # three actions each
                    action = ActionFactory(attempt=attempt, question=q)
                    action = jsonable_encoder(crud.quiz_action.get(db, id=action.id))
                    actions.append(action)
                quiz_actions.append(
                    {"student_id":user.id, "student_name":user.full_name, "actions":actions}
                )

        student_cookies = await student_cookies
        r = await client.get(
            f"/quizzes/{quiz.id}/actions",
            cookies=student_cookies,
        )
        result = r.json()
        assert r.status_code == 400

    async def test_read_quiz_actions_teacher_superuser(
        self, db:Session, client: AsyncClient, teacher_cookies: Dict[str, str], superuser_cookies: Dict[str, str] 
    ) -> None:
        teacher_cookies = await teacher_cookies
        superuser_cookies = await superuser_cookies
        r = await client.get("/users/profile", cookies=teacher_cookies)
        result = r.json()
        teacher = crud.user.get(db, id=result["id"])
        quiz = QuizFactory(teacher=teacher)
        questions = [QuestionFactory(quiz=quiz) for i in range(3)]

        quiz_actions = []
        for i in range(3): # three students
            student = UserFactory(student=True)
            user = crud.user.get(db, id=student.id)
            attempt = AttemptFactory(quiz=quiz, student=user, is_done=True)
            actions = []
            for q in questions:
                for j in range(3): # three actions each
                    action = ActionFactory(attempt=attempt, question=q)
                    action = jsonable_encoder(crud.quiz_action.get(db, id=action.id))
                    actions.append(action)
                quiz_actions.append(
                    {"student_id":user.id, "student_name":user.full_name, "actions":actions}
                )

        r = await client.get(
            f"/quizzes/{quiz.id}/actions",
            cookies=teacher_cookies,
        )
        result = r.json()
        assert r.status_code == 200
        student_ids = [student["student_id"] for student in quiz_actions]
        student_names = [student["student_name"] for student in quiz_actions]
        actions = {student["student_id"]: student["actions"] for student in quiz_actions}
        for student_in_db in result:
            assert student_in_db["student_id"] in student_ids
            assert student_in_db["student_name"] in student_names
            for action_in_db in student_in_db["actions"]:
                assert action_in_db in actions[student_in_db["student_id"]]

        r = await client.get(
            f"/quizzes/{quiz.id}/actions",
            cookies=superuser_cookies,
        )
        result = r.json()
        assert r.status_code == 200
        for student_in_db in result:
            assert student_in_db["student_id"] in student_ids
            assert student_in_db["student_name"] in student_names
            for action_in_db in student_in_db["actions"]:
                assert action_in_db in actions[student_in_db["student_id"]]

@pytest.mark.anyio
class TestReadAttemptActions:
    async def test_read_attempt_actions_students(
        self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
    ) -> None:
        quiz = QuizFactory()
        questions = [QuestionFactory(quiz=quiz) for i in range(3)]
        student = UserFactory(student=True)
        user = crud.user.get(db, id=student.id)
        attempt = AttemptFactory(quiz=quiz, student=user, is_done=True)

        actions = []
        for q in questions:
            for j in range(3): # three actions each
                action = ActionFactory(attempt=attempt, question=q)
                action = jsonable_encoder(crud.quiz_action.get(db, id=action.id))
                actions.append(action)

        student_cookies = await student_cookies
        r = await client.get(
            f"/quizzes/{quiz.id}/{student.id}/actions",
            cookies=student_cookies,
        )
        result = r.json()
        assert r.status_code == 400

    async def test_read_attempt_actions_teacher_superuser(
        self, db:Session, client: AsyncClient, teacher_cookies: Dict[str, str], superuser_cookies: Dict[str, str] 
    ) -> None:
        teacher_cookies = await teacher_cookies
        superuser_cookies = await superuser_cookies
        r = await client.get("/users/profile", cookies=teacher_cookies)
        result = r.json()
        teacher = crud.user.get(db, id=result["id"])

        quiz = QuizFactory(teacher=teacher)
        questions = [QuestionFactory(quiz=quiz) for i in range(3)]
        student = UserFactory(student=True)
        attempt = AttemptFactory(quiz=quiz, student=student)

        actions = []
        for q in questions:
            for j in range(3): # three actions each
                action = ActionFactory(attempt=attempt, question=q)
                action = jsonable_encoder(crud.quiz_action.get(db, id=action.id))
                actions.append(action)

        r = await client.get(
            f"/quizzes/{quiz.id}/{student.id}/actions",
            cookies=teacher_cookies,
        )
        result = r.json()
        assert r.status_code == 200
        for action_in_db in result:
            assert action_in_db in actions

        r = await client.get(
            f"/quizzes/{quiz.id}/{student.id}/actions",
            cookies=superuser_cookies,
        )
        result = r.json()
        assert r.status_code == 200
        for action_in_db in result:
            assert action_in_db in actions

@pytest.mark.anyio
class TestReadAttemptQuestionActions:
    async def test_read_attempt_question_actions_students(
        self, db: Session, client: AsyncClient, student_cookies: Dict[str, str]
    ) -> None:
        quiz = QuizFactory()
        question = QuestionFactory(quiz=quiz)
        student = UserFactory(student=True)
        user = crud.user.get(db, id=student.id)
        attempt = AttemptFactory(quiz=quiz, student=user, is_done=True)

        actions = []
        for j in range(3):
            action = ActionFactory(attempt=attempt, question=question)
            action = jsonable_encoder(crud.quiz_action.get(db, id=action.id))
            actions.append(action)

        student_cookies = await student_cookies
        r = await client.get(
            f"/quizzes/{quiz.id}/questions/{question.id}/{student.id}/actions",
            cookies=student_cookies,
        )
        result = r.json()
        assert r.status_code == 400

    async def test_read_attempt_question_actions_teacher_superuser(
        self, db:Session, client: AsyncClient, teacher_cookies: Dict[str, str], superuser_cookies: Dict[str, str] 
    ) -> None:
        teacher_cookies = await teacher_cookies
        superuser_cookies = await superuser_cookies
        r = await client.get("/users/profile", cookies=teacher_cookies)
        result = r.json()
        teacher = crud.user.get(db, id=result["id"])

        quiz = QuizFactory(teacher=teacher)
        question = QuestionFactory(quiz=quiz)
        student = UserFactory(student=True)
        attempt = AttemptFactory(quiz=quiz, student=student)

        actions = []
        for j in range(3):
            action = ActionFactory(attempt=attempt, question=question)
            action = jsonable_encoder(crud.quiz_action.get(db, id=action.id))
            actions.append(action)

        r = await client.get(
            f"/quizzes/{quiz.id}/questions/{question.id}/{student.id}/actions",
            cookies=teacher_cookies,
        )
        result = r.json()
        assert r.status_code == 200
        for action_in_db in result:
            assert action_in_db in actions

        r = await client.get(
            f"/quizzes/{quiz.id}/questions/{question.id}/{student.id}/actions",
            cookies=superuser_cookies,
        )
        result = r.json()
        assert r.status_code == 200
        for action_in_db in result:
            assert action_in_db in actions

@pytest.mark.anyio
class TestReadPerQuestionAttemptActionsFilterByCheating:
    async def test_read_attempt_actions_teacher_superuser(
        self, db:Session, client: AsyncClient, teacher_cookies: Dict[str, str], superuser_cookies: Dict[str, str] 
    ) -> None:
        teacher_cookies = await teacher_cookies
        superuser_cookies = await superuser_cookies
        r = await client.get("/users/profile", cookies=teacher_cookies)
        result = r.json()
        teacher = crud.user.get(db, id=result["id"])

        quiz = QuizFactory(teacher=teacher)
        questions = [QuestionFactory(quiz=quiz) for i in range(3)]
        attempts_with_actions = {
            'is_cheater_dataset': dict(),
            'is_not_cheater_dataset': dict(),
        }
        action_list = {
            'blur': 0,
            'focus': 0,
            'copy_': 0,
            'paste': 0,
            'left_click': 0,
            'right_click': 0,
            'double_click': 0,
        }

        for s in range(3): # three students
            is_cheater_dataset = bool(random.randint(0,1))
            student = UserFactory(student=True, is_cheater_dataset=is_cheater_dataset)
            attempt = AttemptFactory(quiz=quiz, student=student, is_done=True)
            attempt_actions = dict()
            
            for q in questions:
                question_actions = dict(action_list)
                for j in range(3): # three actions each
                    action = ActionFactory(attempt=attempt, question=q)
                    if action.blur:
                        question_actions['blur'] += 1
                    elif action.focus:
                        question_actions['focus'] += 1
                    elif action.copy_:
                        question_actions['copy_'] += 1
                    elif action.paste:
                        question_actions['paste'] += 1
                    elif action.left_click:
                        question_actions['left_click'] += 1
                    elif action.right_click:
                        question_actions['right_click'] += 1
                    elif action.double_click:
                        question_actions['double_click'] += 1
                attempt_actions.setdefault(str(q.id), question_actions)
            
            if is_cheater_dataset:
                attempts_with_actions['is_cheater_dataset'].setdefault(str(student.id), attempt_actions)
            else:
                attempts_with_actions['is_not_cheater_dataset'].setdefault(str(student.id), attempt_actions)
        
        r = await client.get(
            f"/quizzes/{quiz.id}/actions-per-question/filter-by-cheating",
            cookies=teacher_cookies,
        )
        result = r.json()
        assert r.status_code == 200
        # logging.info(f"""
        # {pformat(result)}
        # =================================
        # {pformat(attempts_with_actions)}\n\n
        # """)
        assert result == attempts_with_actions
        
        r = await client.get(
            f"/quizzes/{quiz.id}/actions-per-question/filter-by-cheating",
            cookies=superuser_cookies,
        )
        result = r.json()
        assert r.status_code == 200
        assert result == attempts_with_actions