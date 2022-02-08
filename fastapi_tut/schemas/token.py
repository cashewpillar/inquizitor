from typing import Optional

from pydantic import BaseModel

class Token(BaseModel):
	access_token: str
	refresh_token: Optional[str] = None
	token_type: str

class TokenPayload(BaseModel):
	sub: Optional[int] = None