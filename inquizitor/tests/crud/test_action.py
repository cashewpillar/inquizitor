import logging
import factory
import pytest
from sqlmodel import Session
from pprint import pformat

from inquizitor import crud, models
from inquizitor.tests import factories 

def test_create_action(db: Session) -> None:
    focus = 1
    quiz = factories.QuizFactory()
    question = factories.QuestionFactory(quiz=quiz)
    student = crud.user.get_by_username(db, username="student")
    attempt = factories.AttemptFactory(quiz=quiz, student=student)

    action_in = models.QuizActionCreate(focus=focus, attempt_id=attempt.id, question_id=question.id)
    action = crud.quiz_action.create(db=db, obj_in=action_in)
    assert action.attempt == attempt
    assert action.question == question
    assert action.focus == focus

def test_create_multiple_actions(db: Session) -> None:
    student = crud.user.get_by_username(db, username="student")
    with pytest.raises(Exception) as e_info:
        action_in = models.QuizActionCreate(focus=1, blur=1, double_click=1, student_id=student.id)
        action = crud.quiz_action.create(db=db, obj_in=action_in)

def test_get_action(db: Session) -> None:
    double_click = 1
    quiz = factories.QuizFactory()
    question = factories.QuestionFactory(quiz=quiz)
    student = crud.user.get_by_username(db, username="student")
    attempt = factories.AttemptFactory(quiz=quiz, student=student)

    action_in = models.QuizActionCreate(double_click=double_click, attempt_id=attempt.id, question_id=question.id)
    action = crud.quiz_action.create(db=db, obj_in=action_in)
    action_in_db = crud.quiz_action.get(db=db, id=action.id)
    assert action_in_db.id == action.id
    assert action_in_db.attempt == attempt
    assert action_in_db.question == question
    assert action_in_db.double_click == double_click

def test_get_multi_action_by_question_attempt(db: Session) -> None:
    actions = []
    quiz = factories.QuizFactory()
    question = factories.QuestionFactory(quiz=quiz)
    student = factories.UserFactory(is_student=True)
    attempt = factories.AttemptFactory(student=student, quiz=quiz)
    for i in range(3):
        action = factories.ActionFactory(question=question, attempt=attempt)
        actions.append(action)

    actions_in_db = crud.quiz_action.get_multi_by_question_attempt(
        db, question_id=question.id, attempt_id=attempt.id
    )
    assert actions == actions_in_db

def test_get_multi_action_by_attempt(db: Session) -> None:
    actions = []
    quiz = factories.QuizFactory()
    for i in range(3):
        question = factories.QuestionFactory(quiz=quiz)
    student = factories.UserFactory(is_student=True)
    attempt = factories.AttemptFactory(student=student, quiz=quiz)
    quiz_in_db = crud.quiz.get(db, id=quiz.id)
    for question in quiz_in_db.questions:
        action = factories.ActionFactory(question=question, attempt=attempt)
        actions.append(action)

    actions_in_db = crud.quiz_action.get_multi_by_attempt(
        db, attempt_id=attempt.id
    )
    assert actions == actions_in_db

def test_get_multi_action_by_question(db: Session) -> None:
    actions = []
    quiz = factories.QuizFactory()
    question = factories.QuestionFactory(quiz=quiz)
    for i in range(3):
        student = factories.UserFactory(is_student=True)
        attempt = factories.AttemptFactory(student=student, quiz=quiz)
        action = factories.ActionFactory(question=question, attempt=attempt)
        actions.append(action)

    actions_in_db = crud.quiz_action.get_multi_by_question(
        db, question_id=question.id
    )
    assert actions == actions_in_db

def test_get_multi_by_quiz_order_by_student(db: Session) -> None:
    actions = []
    quiz = factories.QuizFactory()
    for i in range(3):
        question = factories.QuestionFactory(quiz=quiz)
    quiz_in_db = crud.quiz.get(db, id=quiz.id)
    for i in range(3):
        student = factories.UserFactory(is_student=True)
        attempt = factories.AttemptFactory(student=student, quiz=quiz)
        for question in quiz_in_db.questions:
            for i in range(5):
                action = factories.ActionFactory(question=question, attempt=attempt)
                actions.append(action)

    actions_in_db = crud.quiz_action.get_multi_by_quiz_order_by_student(
        db, quiz_id=quiz.id
    )
    assert actions == actions_in_db

def test_get_multi_by_attempt_order_by_question(db: Session) -> None:
    actions = []
    quiz = factories.QuizFactory()
    for i in range(3):
        question = factories.QuestionFactory(quiz=quiz)
    student = factories.UserFactory(is_student=True)
    attempt = factories.AttemptFactory(student=student, quiz=quiz)
    quiz_in_db = crud.quiz.get(db, id=quiz.id)
    for question in quiz_in_db.questions:
        for i in range(5):
            action = factories.ActionFactory(question=question, attempt=attempt)
            actions.append(action)

    actions_in_db = crud.quiz_action.get_multi_by_attempt_order_by_question(
        db, attempt_id=attempt.id
    )
    assert actions == actions_in_db

def test_get_per_student_summary_by_quiz(db: Session) -> None:
    quiz = factories.QuizFactory()
    for i in range(3):
        question = factories.QuestionFactory(quiz=quiz)
    quiz_in_db = crud.quiz.get(db, id=quiz.id)
    for i in range(5):
        student = factories.UserFactory(is_student=True)
        attempt = factories.AttemptFactory(student=student, quiz=quiz)
        for question in quiz_in_db.questions:
            for i in range(15):
                action = factories.ActionFactory(question=question, attempt=attempt)

    summary = crud.quiz_action.get_per_student_summary_by_quiz(
        db, quiz_id=quiz.id
    )
    for student in summary:
        action_count = 0
        for action in summary[student].keys():
            action_count += summary[student][action]
        assert action_count == 45 # 3 questions, 15 actions each

def test_get_per_question_summary_by_attempt(db: Session) -> None:
    quiz = factories.QuizFactory()
    for i in range(5):
        question = factories.QuestionFactory(quiz=quiz)
    student = factories.UserFactory(is_student=True)
    attempt = factories.AttemptFactory(student=student, quiz=quiz)

    quiz_in_db = crud.quiz.get(db, id=quiz.id)
    for question in quiz_in_db.questions:
        for i in range(20):
            action = factories.ActionFactory(question=question, attempt=attempt)

    summary = crud.quiz_action.get_per_question_summary_by_attempt(
        db, attempt_id=attempt.id
    )
    for question in summary:
        action_count = 0
        for action in summary[question].keys():
             # exclude the items "label" and "inactive_duration" from checks
            if not action in ("label", "inactive_duration"):
                action_count += summary[question][action]
        assert action_count == 20 # 20 actions each

def test_update_action(db: Session) -> None:
    quiz = factories.QuizFactory()
    question = factories.QuestionFactory(quiz=quiz)
    student = crud.user.get_by_username(db, username="student")
    attempt = factories.AttemptFactory(quiz=quiz, student=student)

    action_in = models.QuizActionCreate(blur=1, question_id=question.id, attempt_id=attempt.id)
    action = crud.quiz_action.create(db=db, obj_in=action_in)
    action_update = models.QuizActionUpdate(left_click=1, blur=0, student_id=student.id)
    with pytest.raises(Exception) as e_info:
        crud.quiz_action.update(db=db, db_obj=item, obj_in=item_update)

def test_remove_action(db: Session) -> None:
    focus = 1
    quiz = factories.QuizFactory()
    question = factories.QuestionFactory(quiz=quiz)
    student = crud.user.get_by_username(db, username="student")
    attempt = factories.AttemptFactory(quiz=quiz, student=student)

    action_in = models.QuizActionCreate(focus=focus, attempt_id=attempt.id, question_id=question.id)
    action = crud.quiz_action.create(db=db, obj_in=action_in)
    action2 = crud.quiz_action.remove(db=db, id=action.id)
    action3 = crud.quiz_action.get(db=db, id=action.id)
    assert action3 is None
    assert action2.id == action.id
    assert action2.attempt == action.attempt
    assert action2.question == action.question
    assert action2.focus == action.focus

def test_factory(db: Session) -> None:
    action = factories.ActionFactory()
    action2 = factories.ActionFactory(custom=True, focus=1)
    assert sum([
        action.blur,
        action.focus,
        action.copy_,
        action.paste,
        action.left_click,
        action.right_click,
        action.double_click,
    ]) == 1
    assert sum([
        action2.blur,
        action2.focus,
        action2.copy_,
        action2.paste,
        action2.left_click,
        action2.right_click,
        action2.double_click,
    ]) == 1
    with pytest.raises(Exception) as e_info:
        action2 = factories.ActionFactory(custom=True, blur=1, copy_=1)