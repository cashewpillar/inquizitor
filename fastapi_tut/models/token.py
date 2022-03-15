from typing import Optional
from sqlmodel import Field, SQLModel

from fastapi_tut.db.base_class import TableBase

class RevokedToken(TableBase, table=True):
	"""ref https://indominusbyte.github.io/fastapi-jwt-auth/usage/revoking/"""
	jti: str = Field(index=True)
	
	# This could be made more complex, for example storing the token in Redis
	# with the value true if revoked and false if not revoked
	is_revoked: bool = Field(default=False)

class Token(SQLModel):
	access_token: str
	refresh_token: Optional[str] = None
	token_type: str

class TokenPayload(SQLModel):
	sub: Optional[int] = None