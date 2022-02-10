import logging
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from fastapi_tut import schemas, crud, utils
from fastapi_tut.models import RevokedToken	
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


# NOTE: schemas validate & determine the JSON response of each request
@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(
	db: Session = Depends(deps.get_db), 
	form_data: OAuth2PasswordRequestForm = Depends(),
	Authorize: AuthJWT = Depends()
) -> Any:
	"""
	OAuth2 compatible token login, get an access token for future requests
	"""
	user = crud.user.authenticate(
		db, email=form_data.username, password=form_data.password
	)
	if not user:
		raise HTTPException(status_code=400, detail="Incorrent email or password")

	# TODO: test time expiry
	access_token = Authorize.create_access_token(subject=user.id,
		expires_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
	refresh_token = Authorize.create_refresh_token(subject=user.id,
		expires_time=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))

	return {"access_token": access_token,
			"refresh_token": refresh_token,
			"token_type": "bearer"}


@router.post("/login/test-token", response_model=schemas.User)
async def test_token(
	db: Session = Depends(deps.get_db),
	Authorize: AuthJWT = Depends()
) -> Any:
	"""
	Test access token
	"""
	Authorize.jwt_required()

	current_user = crud.user.get(db, id=Authorize.get_jwt_subject())
	return current_user


@router.post('/login/refresh', response_model=schemas.Token)
async def refresh(
	Authorize: AuthJWT = Depends()
) -> Any:
	"""
	Get an access token using a refresh token
	"""
	Authorize.jwt_refresh_token_required()

	current_user = Authorize.get_jwt_subject()
	new_access_token = Authorize.create_access_token(subject=current_user,
		expires_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
	
	return {"access_token": new_access_token,
			"token_type": "bearer"}


@router.delete('/login/access-revoke', response_model=schemas.Msg)
async def revoke_access(
	db: Session = Depends(deps.get_db),
	Authorize: AuthJWT = Depends()
) -> Any:
	"""
	Revoke access token of current user
	"""
	Authorize.jwt_required()

	jti = Authorize.get_raw_jwt()['jti']
	db_obj = RevokedToken(jti=jti, is_revoked=True)
	# TODO add the default token expiry (see core.config)
	# to remove token from denylist
	db.add(db_obj)
	db.commit()
	db.refresh(db_obj)

	return {'msg': "Access token has been revoked"}


@router.delete('/login/refresh-revoke', response_model=schemas.Msg)
async def revoke_refresh(
	db: Session = Depends(deps.get_db),
	Authorize: AuthJWT = Depends()
) -> Any:
	"""
	Revoke refresh token of current user
	"""
	Authorize.jwt_refresh_token_required()

	jti = Authorize.get_raw_jwt()['jti']
	db_obj = RevokedToken(jti=jti, is_revoked=True)
	# TODO add the default token expiry (see core.config)
	# to remove token from denylist
	db.add(db_obj)
	db.commit()
	db.refresh(db_obj)

	return {'msg': "Refresh token has been revoked"}