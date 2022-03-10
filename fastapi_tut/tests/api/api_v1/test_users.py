# TODO

import pytest
from httpx import AsyncClient

@pytest.mark.skip(reason="switching from fixtures to factories & adding student + teacher")
@pytest.mark.anyio
async def test_get_users_superuser_me(
	client: AsyncClient
) -> None:
	pass