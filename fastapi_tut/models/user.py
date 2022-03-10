from typing import Any, List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, String

from fastapi_tut.db.base_class import TableBase
from fastapi_tut.models import MarksOfStudent, Quiz

# DOING: crud & test of marks & quiz
# WENT with individual models instead of using roles bcs of role specific attributes 
# WILL GO with role models bcs i want to store users all in db
# class Student(User, table=True):
# 	marks: Optional[List[MarksOfStudent]] = Relationship(back_populates="student")

# 	def __repr__(self):
# 		return f"<Student({self.email!r})>"

# class Teacher(User, table=True):
# 	quizzes: Optional[List[Quiz]] = Relationship(back_populates="teacher")

# 	def __repr__(self):
# 		return f"<Teacher({self.email!r})>"

# Shared Properties
class UserBase(SQLModel):
	full_name: Optional[str] = Field(index=True)
	email: Optional[EmailStr]
	is_superuser: bool = Field(default=False)
	role_id: int = Field(default=None, foreign_key="role.id")

# Properties to receive via API on creation
class UserCreate(UserBase):
	email: EmailStr
	password: str

class UserUpdate(UserBase):
	full_name: Optional[str] = None
	email: Optional[EmailStr] = None
	is_superuser: bool = False
	password: Optional[str] = None
	role_id: int = None

class UserInDBBase(UserBase, TableBase):
	class Config:
		orm_mode = True

# Additional properties  to return via API
class User(UserInDBBase, table=True):
	email: EmailStr = Field(sa_column=Column(String, unique=True, index=True, nullable=False))
	hashed_password: str = Field(nullable=False)

	marks: Optional[List[MarksOfStudent]] = Relationship(back_populates="student")
	quizzes: Optional[List[Quiz]] = Relationship(back_populates="teacher")
	role: Optional["Role"] = Relationship(back_populates="users")

	def __repr__(self):
		"""Represent instance as a unique string."""
		return f"<User({self.email!r})>"


class RoleBase(SQLModel):
	id: str = Field(primary_key=True)

class RoleCreate(RoleBase):
	pass

class RoleUpdate(RoleBase):
	id: Optional[str] = None

class RoleInDBBase(RoleBase):
	pass

# Todo role specific attributes
class Role(RoleInDBBase, table=True):
	"""One to Many Design: Users can only have one role"""
	users: Optional[List[User]] = Relationship(back_populates="role")

	def __repr__(self):
		return f"Role({self.id!r})"