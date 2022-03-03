from typing import Optional

from sqlmodel import Field, SQLModel

class Base(SQLModel):
	id: Optional[int] = Field(primary_key=True, index=True)
