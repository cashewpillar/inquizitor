from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_tut import schemas, crud
from fastapi_tut.api import deps
from fastapi_tut.core import security
from fastapi_tut.core.config import settings

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
	db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
	"""
	OAuth2 compatible token login, get an access token for future requests
	"""
	user = crud.user.authenticate(
		db, email=form_data.username, password=form_data.password
	)
	if not user:
		raise HTTPException(status_code=400, detail="Incorrent email or password")
	access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	return {
		"access_token": security.create_access_token(
			user.id, expires_delta=access_token_expires
		),
		"token_type": "bearer",
	}