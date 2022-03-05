# initial, todo

from fastapi import APIRouter

router = APIRouter()

# Module 3: Exam
@router.get("/exams/{exam_id}")
async def take_exam(exam_id: int):
	# [Module 3] if logged in, redirect to instructions page of examination module
	return {"message": f"Taking exam [ID: {exam_id}]"}

@router.get("/exams/{exam_id}/items/{item_id}")
async def take_exam(exam_id: int, item_id: int):
	return {"message": f"Taking item [ID: {item_id}]"}