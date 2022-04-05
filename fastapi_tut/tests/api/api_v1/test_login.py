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
	"username": settings.FIRST_SUPERUSER_USERNAME,
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


# READ: https://stackoverflow.com/questions/61302281/if-the-jwt-token-for-auth-is-saved-in-the-http-only-cookie-how-do-you-read-it-f 
@pytest.mark.anyio
async def test_use_access_token(
	client: AsyncClient, superuser_cookies: Dict[str, str]
) -> None:
	r = await client.get(
		"/users/profile", cookies=await superuser_cookies
	)
	result = r.json()
	assert r.status_code == 200
	assert result["username"] == settings.FIRST_SUPERUSER_USERNAME
	assert result["is_superuser"] == True

@pytest.mark.anyio
async def test_use_refresh_token(
	client: AsyncClient, superuser_cookies: Dict[str, str],
) -> None:
	r = await client.post(
		"/login/refresh", cookies=await superuser_cookies
	)
	result = r.json()
	assert r.status_code == 200
	assert "access_token_cookie" in r.cookies
	assert r.cookies["access_token_cookie"]

@pytest.mark.anyio
async def test_access_revoke(
	client: AsyncClient, superuser_cookies: Dict[str, str]
) -> None:
	cookies = await superuser_cookies
	r = await client.delete(
		"/login/access-revoke", cookies=cookies
	)
	assert r.status_code == 200
	assert "msg" in r.json()
	assert "Access" in r.json()["msg"]

	r = await client.get(
		"/users/profile", cookies=cookies
	)
	result = r.json()
	assert r.status_code == 401

@pytest.mark.anyio
async def test_refresh_revoke(
	client: AsyncClient, superuser_cookies: Dict[str, str]
) -> None:
	cookies = await superuser_cookies
	r = await client.delete(
		"/login/refresh-revoke", cookies=cookies
	)
	assert r.status_code == 200
	assert "msg" in r.json()
	assert "Refresh" in r.json()["msg"]

	r = await client.post(
		"/login/refresh", cookies=cookies
	)
	result = r.json()
	assert r.status_code == 401