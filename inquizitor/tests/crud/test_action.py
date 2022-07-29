import pytest
from sqlmodel import Session

from inquizitor import crud, models
from inquizitor.tests.factories import ActionFactory 

def test_create_action(db: Session) -> None:
    focus = 1
    student = crud.user.get_by_username(db, username="student")
    action_in = models.QuizActionCreate(focus=focus, student_id=student.id)
    action = crud.quiz_action.create(db=db, obj_in=action_in)
    assert action.student == student
    assert action.focus == focus

def test_get_action(db: Session) -> None:
    double_click = 1
    student = crud.user.get_by_username(db, username="student")
    action_in = models.QuizActionCreate(double_click=double_click, student_id=student.id)
    action = crud.quiz_action.create(db=db, obj_in=action_in)
    action_in_db = crud.quiz_action.get(db=db, id=action.id)
    assert action_in_db.double_click == double_click
    assert action_in_db.student == student

def test_update_action(db: Session) -> None:
    student = crud.user.get_by_username(db, username="student")
    action_in = models.QuizActionCreate(blur=1, student_id=student.id)
    action = crud.quiz_action.create(db=db, obj_in=action_in)

    action_update = models.QuizActionUpdate(left_click=1, blur=0, student_id=student.id)
    with pytest.raises(Exception) as e_info:
        crud.quiz_action.update(db=db, db_obj=item, obj_in=item_update)

def test_remove_action(db: Session) -> None:
    focus = 1
    student = crud.user.get_by_username(db, username="student")
    action_in = models.QuizActionCreate(focus=focus, student_id=student.id)
    action = crud.quiz_action.create(db=db, obj_in=action_in)
    action2 = crud.quiz_action.remove(db=db, id=action.id)
    action3 = crud.quiz_action.get(db=db, id=action.id)
    assert action3 is None
    assert action2.id == action.id
    assert action2.student == action.student
    assert action2.focus == action.focus

def test_factory(db: Session) -> None:
    action = ActionFactory()
    assert sum([
        action.blur,
        action.focus,
        action.copy_,
        action.paste,
        action.left_click,
        action.right_click,
        action.double_click,
    ]) == 1

    # DOING
    # action2 = ActionFactory(blur=1)
    # assert sum([
    #     action2.blur,
    #     action2.focus,
    #     action2.copy_,
    #     action2.paste,
    #     action2.left_click,
    #     action2.right_click,
    #     action2.double_click,
    # ]) == 1