# havent understood v well, see:
# https://fastapi.tiangolo.com/advanced/async-tests/

# havent tested/ studied multiple logins

import logging
import pytest
from httpx import AsyncClient
from pprint import pformat
from typing import Dict

from fastapi_tut.core.config import settings

logging.basicConfig(level=logging.INFO)

LOGIN_DATA = {
	"username": settings.FIRST_SUPERUSER_EMAIL,
	"password": settings.FIRST_SUPERUSER_PASSWORD,
}

@pytest.mark.anyio
async def test_get_tokens(client: AsyncClient) -> None:
	r = await client.post(
		"/login/token", data=LOGIN_DATA)
	assert r.status_code == 200
	assert "access_token_cookie" in r.cookies
	assert "refresh_token_cookie" in r.cookies
	assert r.cookies["access_token_cookie"]
	assert r.cookies["refresh_token_cookie"]


@pytest.mark.skip("Doing: access token missing")
@pytest.mark.anyio
async def test_use_access_token(
	client: AsyncClient, superuser_access_token_headers: Dict[str, str]
) -> None:
	r = await client.post(
		"/login/test-token", headers=await superuser_access_token_headers
	)
	logging.info(f"{pformat(r.headers)}")
	result = r.json()
	assert r.status_code == 200
	assert result["email"] == settings.FIRST_SUPERUSER_EMAIL
	assert result["is_superuser"] == True


@pytest.mark.skip()
@pytest.mark.anyio
async def test_use_refresh_token(
	client: AsyncClient, superuser_refresh_token_headers: Dict[str, str],
) -> None:
	r = await client.post(
		"/login/refresh", headers=await superuser_refresh_token_headers
	)
	tokens = r.json()
	assert r.status_code == 200
	assert "access_token" in tokens
	assert tokens["access_token"]


@pytest.mark.skip()
@pytest.mark.anyio
async def test_access_revoke(
	production_client: AsyncClient, superuser_access_token_headers: Dict[str, str]
) -> None:
	headers = await superuser_access_token_headers
	r = await production_client.delete(
		"/login/access-revoke", headers=headers
	)
	assert r.status_code == 200
	assert "msg" in r.json()
	assert "Access" in r.json()["msg"]

	r = await production_client.post(
		"/login/test-token", headers=headers
	)
	result = r.json()
	assert r.status_code == 401


@pytest.mark.skip()
@pytest.mark.anyio
async def test_refresh_revoke(
	production_client: AsyncClient, superuser_refresh_token_headers: Dict[str, str]
) -> None:
	headers = await superuser_refresh_token_headers
	r = await production_client.delete(
		"/login/refresh-revoke", headers=headers
	)
	assert r.status_code == 200
	assert "msg" in r.json()
	assert "Refresh" in r.json()["msg"]

	r = await production_client.post(
		"/login/refresh", headers=headers
	)
	result = r.json()
	assert r.status_code == 401