from typing import Optional

from pydantic import BaseModel, EmailStr

# Shared Properties
class UserBase(BaseModel):
	full_name: str
	email: EmailStr
	is_superuser: bool = False

# Properties to receive via API on creation
class UserCreate(UserBase):
	email: EmailStr
	password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
	password: Optional[str] = None

