# initial, todo

from fastapi import APIRouter

router = APIRouter()

# Module 1: Admin
@router.get("/admin")
async def admin():
	return {"message": """TODO: Admin login page, 
	Admin login form data handling (POST),
	Make similar to read_users endpoint of ref repo """}
