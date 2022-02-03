import logging
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_tut import models, schemas, crud, utils
from fastapi_tut.api import deps
from fastapi_tut.core import security
from fastapi_tut.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Module 2: Login
@router.get("/login")
async def login(request: Request):
	# if user is logged in, redirect to exam page
	# [Module 3] if logged in, redirect to instructions page of examination module
	return utils.templates.TemplateResponse("login.html", {"request": request})

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
	"""
	"""
	return {
		"access_token": security.create_access_token(
			user.id, expires_delta=access_token_expires
		),
		"token_type": "bearer",
	}
	"""
	token = {
		"access_token": security.create_access_token(
			user.id, expires_delta=access_token_expires
		),
		"token_type": "bearer",
	}
	"""
	# DOING
	# https://stackoverflow.com/questions/62119138/how-to-do-a-post-redirect-get-prg-in-fastapi
	# https://devforum.okta.com/t/fastapi-redirectresponse-lost-authorization-header-when-getting-authorization-code-from-the-authorize-endpoint/12907
	# https://stackoverflow.com/questions/14707345/oauth2-query-string-vs-fragment
	# logger.info(f"Bearer {token['access_token']}")
	
	# return RedirectResponse(url="/login/test-token")

@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
	"""
	Test access token
	"""
	return current_user