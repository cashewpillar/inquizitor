from sqlmodel import Session
from sqlalchemy import and_
from typing import Generator, Tuple, Union

from fastapi import Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError

from inquizitor import crud, models
from inquizitor.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/login/access-token")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> models.User:
    try:
        Authorize.jwt_required()
    except JWTDecodeError as err:
        # NOTE https://github.com/IndominusByte/fastapi-jwt-auth/issues/20
        status_code = err.status_code
        if err.message == "Signature verification failed":
            status_code = 401
        raise HTTPException(status_code=status_code, detail="User not logged in")

    user = crud.user.get(db, id=Authorize.get_jwt_subject())
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_teacher(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not (crud.user.is_superuser(current_user) or crud.user.is_teacher(current_user)):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_student(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_student(current_user):
        raise HTTPException(status_code=400, detail="User must be a student")
    return current_user


def get_quiz(
    *,
    db: Session = Depends(get_db),
    quiz_index: Union[int, str] = Path(
        ..., description="ID or Code of quiz to retrieve"
    ),
) -> models.Quiz:
    quiz = crud.quiz.get_by_index(db, quiz_index=quiz_index)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return quiz


def get_question(
    *,
    db: Session = Depends(get_db),
    question_id: int,
    quiz: models.Quiz = Depends(get_quiz),
) -> models.QuizQuestion:
    question = crud.quiz_question.get(db, id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    if not crud.quiz.has_question(db, quiz_index=quiz.id, question_id=question.id):
        raise HTTPException(
            status_code=404, detail="Question does not belong to the specified quiz"
        )

    return question


def get_choice(
    *,
    db: Session = Depends(get_db),
    choice_id: int,
    question: models.QuizQuestion = Depends(get_question),
) -> models.QuizChoice:
    choice = crud.quiz_choice.get(db, id=choice_id)
    if not choice:
        raise HTTPException(status_code=404, detail="Choice not found")
    if not crud.quiz_question.has_choice(
        db, question_id=question.id, choice_id=choice.id
    ):
        raise HTTPException(
            status_code=404, detail="Question does not belong to the specified quiz"
        )

    return choice


def get_attempt(
    *,
    db: Session = Depends(get_db),
    quiz: models.Quiz = Depends(get_quiz),
    current_student: models.User = Depends(get_current_student),
) -> models.QuizAttempt:
    attempt = crud.quiz_attempt.get_latest_by_quiz_and_student_ids(
        db, quiz_id=quiz.id, student_id=current_student.id
    )
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt for this quiz not found.")

    return attempt


def get_attempt_and_link(
    *,
    db: Session = Depends(get_db),
    quiz: models.Quiz = Depends(get_quiz),
    question: models.QuizQuestion = Depends(get_question),
    current_student: models.User = Depends(get_current_student),
) -> Tuple[models.QuizAttempt, models.QuizStudentLink]:
    attempt = crud.quiz_attempt.get_latest_by_quiz_and_student_ids(
        db, quiz_id=quiz.id, student_id=current_student.id
    )
    if not attempt or attempt.is_done:
        quiz_attempt_in = models.QuizAttemptCreate(
            student_id=current_student.id,
            quiz_id=quiz.id,
            recent_question_id=question.id,
        )
        attempt = crud.quiz_attempt.create(db, obj_in=quiz_attempt_in)
    else:
        attempt = crud.quiz_attempt.update(
            db, db_obj=attempt, obj_in={"recent_question_id": question.id}
        )

    link = crud.quiz_student_link.get_by_quiz_and_student_ids(
        db, quiz_id=quiz.id, student_id=current_student.id
    )
    if not link:
        quiz_student_link_in = models.QuizStudentLinkCreate(
            student_id=current_student.id,
            quiz_id=quiz.id,
        )
        link = crud.quiz_student_link.create(db, obj_in=quiz_student_link_in)

    return (attempt, link)


def get_current_author(
    *,
    db: Session = Depends(get_db),
    quiz: models.Quiz = Depends(get_quiz),
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not (
        crud.user.is_superuser(current_user)
        or crud.quiz.is_author(db, user_id=current_user.id, quiz_index=quiz.id)
    ):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
