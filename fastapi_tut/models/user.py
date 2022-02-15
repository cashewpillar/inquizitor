from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from fastapi_tut.db.base_class import Base

class User(Base):
	# TODO UNUSED
	# id = Column(Integer, primary_key=True, index=True)
	full_name = Column(String, index=True)
	email = Column(String, unique=True, index=True, nullable=False)
	hashed_password = Column(String, nullable=False)
	is_superuser = Column(Boolean(), default=False)

	def __repr__(self):
		"""Represent instance as a unique string."""
		return f"<User({self.email!r})>"
