from sqlalchemy import Boolean, Column, Integer, String

from fastapi_tut.db.base_class import Base

class RevokedToken(Base):
	"""ref https://indominusbyte.github.io/fastapi-jwt-auth/usage/revoking/"""
	id = Column(Integer, primary_key=True, index=True)
	jti = Column(String, index=True)
	
	# This could be made more complex, for example storing the token in Redis
	# with the value true if revoked and false if not revoked
	is_revoked = Column(Boolean(), default=False)