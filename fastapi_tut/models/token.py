from typing import Optional
from sqlmodel import Field, SQLModel

from fastapi_tut.db.base_class import TableBase

class RevokedToken(SQLModel, table=True):
	"""ref https://indominusbyte.github.io/fastapi-jwt-auth/usage/revoking/"""
	id: Optional[int] = Field(default=None, primary_key=True)
	jti: str = Field(index=True)
	# This could be made more complex, for example storing the token in Redis
	# with the value true if revoked and false if not revoked

class Token(SQLModel):
	access_token: str
	refresh_token: Optional[str] = None
	token_type: str

class TokenPayload(SQLModel):
	sub: Optional[int] = None