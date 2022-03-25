# initial, todo
import random
import string

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from fastapi_jwt_auth import AuthJWT

from fastapi_tut import crud
from fastapi_tut.models.quiz.quiz import Quiz, QuizCreate, QuizRead
from fastapi_tut.api import deps

router = APIRouter()

# Module 3: Exam
@router.get("/exams/{exam_id}")
async def take_exam(exam_id: int):
	# [Module 3] if logged in, redirect to instructions page of examination module
	return {"message": f"Taking exam [ID: {exam_id}]"}

@router.get("/exams/{exam_id}/items/{item_id}")
async def take_exam(exam_id: int, item_id: int):
	return {"message": f"Taking item [ID: {item_id}]"}



# Teacher Quiz CRUD

# Create a quiz
@router.post("/create/", response_model=QuizRead)
async def create_quiz(
    quiz: QuizCreate, 
    db: Session = Depends(deps.get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()

    current_user = crud.user.get(db, id=Authorize.get_jwt_subject())
    # quiz_obj = Quiz.from_orm(quiz)

# generate random characters
    while True:
        characters = string.ascii_letters + string.digits
        quiz_code = ''.join(random.choice(characters) for i in range(6))
        #check if generated quiz_code already exists
        existing_code = db.query(Quiz).filter(Quiz.quiz_code == quiz_code).first()
        if not existing_code:
            break

    quiz_object = Quiz(**quiz.dict(), quiz_code=quiz_code, teacher_id=current_user.id)

    db.add(quiz_object)
    db.commit()
    db.refresh(quiz_object)
    return quiz_object


#Create questions