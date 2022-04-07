# might use extension when have time
# https://github.com/fastapi-users/fastapi-users
# https://github.com/MushroomMaula/fastapi_login

import logging
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlmodel import Session

from fastapi_tut import models, crud, utils
from fastapi_tut.api import deps
from fastapi_tut.core import security
from fastapi_tut.core.config import settings
from fastapi_tut import crud

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/token")
async def login_access_token(
	db: Session = Depends(deps.get_db), 
	form_data: OAuth2PasswordRequestForm = Depends(),
	Authorize: AuthJWT = Depends()
) -> Any:
	"""
	OAuth2 compatible token login, get an access token for future requests
	"""
	user = crud.user.authenticate(
		db, username=form_data.username, password=form_data.password
	)
	if not user:
		raise HTTPException(status_code=400, detail="Incorrent user or password")
		
	access_token = Authorize.create_access_token(subject=user.id, fresh= True,
		expires_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
	refresh_token = Authorize.create_refresh_token(subject=user.id,
		expires_time=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))

	Authorize.set_access_cookies(access_token)
	Authorize.set_refresh_cookies(refresh_token)

	return {'msg':'Successfully logged in.'}

@router.post('/logout', response_model=models.Msg)
async def logout(
	Authorize: AuthJWT = Depends(),
	db: Session = Depends(deps.get_db)
	):

	Authorize.jwt_required()
	crud.token.revoke_access(Authorize, db)
	
	Authorize.jwt_refresh_token_required()
	crud.token.revoke_refresh(Authorize, db)

	Authorize.unset_jwt_cookies()

	return {'msg':'Successfully logged out.'}

@router.post('/refresh', response_model=models.Msg)
async def refresh(
	Authorize: AuthJWT = Depends()
) -> Any:
	"""
	Get an access token using a refresh token
	"""
	Authorize.jwt_refresh_token_required()

	current_user = Authorize.get_jwt_subject()
	
	new_access_token = Authorize.create_access_token(subject=current_user, fresh=False,
		expires_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
	
	Authorize.set_access_cookies(new_access_token)

	return {'msg':'Successfully refreshed the access token.'}

@router.delete('/access-revoke', response_model=models.Msg)
async def revoke_access(
	Authorize: AuthJWT = Depends(),
	db: Session = Depends(deps.get_db)
) -> Any:
	"""
	Revoke access token of current user
	"""
	Authorize.jwt_required()
	
	crud.token.revoke_access(Authorize, db)

	return {'msg': "Access token has been revoked"}


@router.delete('/refresh-revoke', response_model=models.Msg)
async def revoke_refresh(
	db: Session = Depends(deps.get_db),
	Authorize: AuthJWT = Depends()
) -> Any:
	"""
	Revoke refresh token of current user
	"""
	Authorize.jwt_refresh_token_required()

	crud.token.revoke_refresh(Authorize, db)

	return {'msg': "Refresh token has been revoked"}