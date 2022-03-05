from httpx import AsyncClient
from typing import Dict
import pytest

from fastapi import FastAPI

from fastapi_tut.core.config import settings

@pytest.mark.anyio
async def get_superuser_access_token_headers(app: FastAPI) -> Dict[str, str]:
	login_data = {
		"username": settings.FIRST_SUPERUSER_EMAIL,
		"password": settings.FIRST_SUPERUSER_PASSWORD,
	}
	
	async with AsyncClient(app=app, base_url="http://test") as ac:
		r = await ac.post(
				"/login/access-token", data=login_data)
	tokens = r.json()
	a_token = tokens["access_token"]
	headers = {"Authorization": f"Bearer {a_token}"}

	return headers	


@pytest.mark.anyio
async def get_superuser_refresh_token_headers(app: FastAPI) -> Dict[str, str]:
	login_data = {
		"username": settings.FIRST_SUPERUSER_EMAIL,
		"password": settings.FIRST_SUPERUSER_PASSWORD,
	}
	
	async with AsyncClient(app=app, base_url="http://test") as ac:
		r = await ac.post(
				"/login/access-token", data=login_data)
	tokens = r.json()
	r_token = tokens["refresh_token"]
	headers = {"grant_type": "refresh_token", 
	"Authorization":f"Bearer {r_token}"}

	return headers
