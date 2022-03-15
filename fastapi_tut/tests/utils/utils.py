import logging
import pytest
from httpx import AsyncClient
from pprint import pformat
from typing import Dict

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from fastapi_tut.core.config import settings

logging.basicConfig(level=logging.INFO)

@pytest.mark.anyio
async def get_superuser_cookies(app: FastAPI) -> Dict[str, str]:
	login_data = {
		"username": settings.FIRST_SUPERUSER_EMAIL,
		"password": settings.FIRST_SUPERUSER_PASSWORD,
	}
	
	async with AsyncClient(app=app, base_url="http://test") as ac:
		r = await ac.post(
				"/login/token", data=login_data)
	return r.cookies