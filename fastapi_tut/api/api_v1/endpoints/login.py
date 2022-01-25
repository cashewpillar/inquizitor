from fastapi import APIRouter, Request, Depends	
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from fastapi_tut import schemas
from fastapi_tut.api import deps

router = APIRouter()

# Module 2: Login
@router.get("/login")
async def login(request: Request):
	# if user is logged in, redirect to exam page
	# [Module 3] if logged in, redirect to instructions page of examination module
	return deps.templates.TemplateResponse("login.html", {"request": request})

# doing
@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
	db: Session = Depends(deps.get_db)
):
	pass