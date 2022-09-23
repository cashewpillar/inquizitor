from sqlmodel import Session
from sqlalchemy import and_
from typing import Any, Callable, Generator, Tuple, Union

from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.types import DecoratedCallable
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError

from inquizitor import crud, models
from inquizitor.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/login/access-token")

# https://github.com/tiangolo/fastapi/issues/2060#issuecomment-974527690
class HandleTrailingSlashRouter(APIRouter):
    """
    Registers endpoints for both a non-trailing-slash and a trailing slash. In regards to the exported API schema only the non-trailing slash will be included.

    Examples:

        @router.get("", include_in_schema=False) - not included in the OpenAPI schema, responds to both the naked url (no slash) and /

        @router.get("/some/path") - included in the OpenAPI schema as /some/path, responds to both /some/path and /some/path/

        @router.get("/some/path/") - included in the OpenAPI schema as /some/path, responds to both /some/path and /some/path/

    Co-opted from https://github.com/tiangolo/fastapi/issues/2060#issuecomment-974527690
    """

    def api_route(
            self, path: str, *, include_in_schema: bool = True, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        given_path = path
        path_no_slash = given_path[:-1] if given_path.endswith("/") else given_path

        add_nontrailing_slash_path = super().api_route(
            path_no_slash, include_in_schema=include_in_schema, **kwargs
        )

        add_trailing_slash_path = super().api_route(
            path_no_slash + "/", include_in_schema=False, **kwargs
        )

        def add_path_and_trailing_slash(func: DecoratedCallable) -> DecoratedCallable:
            add_trailing_slash_path(func)
            return add_nontrailing_slash_path(func)

        return add_trailing_slash_path if given_path == "/" else add_path_and_trailing_slash

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
        # https://github.com/IndominusByte/fastapi-jwt-auth/issues/20
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

    question_ids = [q.id for q in quiz.questions]
    next_question_index = question_ids.index(question.id) + 1
    next_question_id = question_ids[next_question_index] if next_question_index < len(question_ids) else None

    attempt = crud.quiz_attempt.get_latest_by_quiz_and_student_ids(
        db, quiz_id=quiz.id, student_id=current_student.id
    )
    if not attempt or attempt.is_done:
        quiz_attempt_in = models.QuizAttemptCreate(
            student_id=current_student.id,
            quiz_id=quiz.id,
            recent_question_id=next_question_id,
        )
        attempt = crud.quiz_attempt.create(db, obj_in=quiz_attempt_in)
    else:
        attempt = crud.quiz_attempt.update(
            db, db_obj=attempt, obj_in={"recent_question_id": next_question_id}
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
    current_teacher: models.User = Depends(get_current_teacher),
) -> models.User:
    if not (
        crud.user.is_superuser(current_teacher)
        or crud.quiz.is_author(db, user_id=current_teacher.id, quiz_index=quiz.id)
    ):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_teacher
