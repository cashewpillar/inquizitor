# havent understood v well, see:
# https://fastapi.tiangolo.com/advanced/async-tests/

# TODO BUT NOT URGENT annotate the parameter 'app'

import pytest
from httpx import AsyncClient
from typing import Dict

from fastapi_tut.core.config import settings

@pytest.mark.anyio
async def test_get_access_token(app) -> None:
	login_data = {
		"username": settings.FIRST_SUPERUSER_EMAIL,
		"password": settings.FIRST_SUPERUSER_PASSWORD,
	}
	async with AsyncClient(app=app, base_url="http://test") as ac:
		r = await ac.post(
			"/login/access-token", data=login_data)
	tokens = r.json()
	assert r.status_code == 200
	assert "access_token" in tokens
	assert tokens["access_token"]

@pytest.mark.anyio
async def test_use_access_token(
	app, superuser_token_headers: Dict[str, str]
) -> None:
	async with AsyncClient(app=app, base_url="http://test") as ac:
		r = await ac.post(
			"/login/test-token", headers=await superuser_token_headers
		)
	result = r.json()
	assert r.status_code == 200
	assert "email" in result
