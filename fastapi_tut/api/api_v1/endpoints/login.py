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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# NOTE: schemas validate & determine the JSON response of each request
# @router.post("/token", response_model=models.Token)
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
		db, email=form_data.username, password=form_data.password
	)
	if not user:
		raise HTTPException(status_code=400, detail="Incorrent email or password")
	if form_data.username != 'admin@admin.com':
		raise HTTPException(status_code=401, detail="Not authorized.")
	
	# user_id = 1

	# TODO: test time expiry
	access_token = Authorize.create_access_token(subject=user.id, fresh= True,
		expires_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
	refresh_token = Authorize.create_refresh_token(subject=user.id,
		expires_time=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))

	Authorize.set_access_cookies(access_token)
	Authorize.set_refresh_cookies(refresh_token)

	return {'msg':'Successfully logged in.'}

@router.post('/logout')
async def logout(Authorize: AuthJWT = Depends()):
	Authorize.unset_jwt_cookies()

	return {'msg':'Successfully logged out.'}

@router.post("/test-token", response_model=models.User)
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


# @router.post('/refresh', response_model=models.Token)
@router.post('/refresh')
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
	db: Session = Depends(deps.get_db),
	Authorize: AuthJWT = Depends()
) -> Any:
	"""
	Revoke access token of current user
	"""
	Authorize.jwt_required()

	jti = Authorize.get_raw_jwt()['jti']
	db_obj = models.RevokedToken(jti=jti, is_revoked=True)
	# TODO add the default token expiry (see core.config)
	# to remove token from denylist automatically
	db.add(db_obj)
	db.commit()
	db.refresh(db_obj)

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

	jti = Authorize.get_raw_jwt()['jti']
	db_obj = models.RevokedToken(jti=jti, is_revoked=True)
	# TODO add the default token expiry (see core.config)
	# to remove token from denylist automatically
	db.add(db_obj)
	db.commit()
	db.refresh(db_obj)

	return {'msg': "Refresh token has been revoked"}