from email.policy import default
from enum import unique
from typing import Optional, List

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, String

from fastapi_tut.db.base_class import PKModel
from fastapi_tut.models.quiz.link import QuizStudentLink

# Shared Properties
class UserBase(SQLModel):
	username : str
	email: Optional[EmailStr]
	full_name: Optional[str] = Field(index=True)
	is_superuser: bool = False
	last_name : str
	first_name : str
	is_teacher : bool = False
	is_student : bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
	email: EmailStr
	password: str


class UserUpdate(UserBase):
	username : Optional[str]
	email: Optional[EmailStr]
	is_superuser: Optional[bool]
	last_name : Optional[str]
	first_name : Optional[str]
	password: Optional[str]
	is_teacher : Optional[bool]
	is_student : Optional[bool]


class UserInDBBase(UserBase, PKModel):
	class Config:
		orm_mode = True


# Additional properties  to return via API
class User(UserInDBBase, table=True):
	username : str = Field(sa_column=Column(String, unique=True, nullable=False))
	email: EmailStr = Field(sa_column=Column(String, unique=True, nullable=False))
	hashed_password: str = Field(nullable=False)

	# for teacher
	teacher_quizzes : List["Quiz"] = Relationship(back_populates='teacher')

	# for student
	attempts : List["QuizAttempt"] = Relationship(back_populates='student')
	answers : List["QuizAnswer"] = Relationship(back_populates='student')
	
	student_quizzes: List[QuizStudentLink] = Relationship(back_populates='student')

	def __repr__(self):
		"""Represent instance as a unique string."""
		return f"<User({self.email!r})>"

class ShowUser(UserBase):
	full_name: Optional[str] = Field(index=True)
	first_name : str
	last_name : str
	is_superuser: bool = False
	is_teacher : bool = False
	is_student : bool = False
	hashed_password : str