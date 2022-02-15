from typing import Any
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
	id: Any = Column(Integer, primary_key=True, index=True)
	__name__: str

	# to generate table name from class name
	@declared_attr
	def __tablename__(cls) -> str:
		return cls.__name__.lower()